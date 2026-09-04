"""CRM prospects : deux pipelines, propositions personnalisées, anti-doublon, PJ."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from urllib.parse import quote

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Application, AuditLog, Candidate, Company, Contract, InternalNote, Interview, Invoice, RecruitmentMission, User
from app.models.enums import EmailType, UserRole, utcnow
from app.models.prospect import Prospect, ProspectSend
from app.services.email import EmailAttachment, send_composed_email

SIDES = ("candidate", "employer")

CANDIDATE_STAGES = (
    ("nouveau", "Nouveau"),
    ("a-contacter", "À contacter"),
    ("contacte", "Contacté"),
    ("qualifie", "Qualifié"),
    ("entretien", "Entretien"),
    ("presente", "Présenté"),
    ("offre", "Offre"),
    ("place", "Placé"),
    ("refuse", "Refusé"),
    ("inactif", "Inactif"),
)

EMPLOYER_STAGES = (
    ("nouveau", "Nouveau"),
    ("a-contacter", "À contacter"),
    ("contacte", "Contacté"),
    ("qualifie", "Qualifié"),
    ("discussion", "En discussion"),
    ("proposition", "Proposition / mandat"),
    ("client", "Client"),
    ("perdu", "Perdu"),
    ("inactif", "Inactif"),
)

SOURCES = ("inscription", "site", "talent", "contact", "prospection", "referral")
SOURCE_LABELS = (
    ("inscription", "Inscription"),
    ("site", "Site"),
    ("talent", "Profil talent"),
    ("contact", "Formulaire"),
    ("prospection", "Prospection"),
    ("referral", "Référence"),
)

ESPACE = "https://talendus.ca/espace.html"
EMPLOYEUR = "https://talendus.ca/espace-employeur.html"
INFO = "info@talendus.ca"
PHONE = "263 558 5225"
ATTACHMENT_HOOK = "Vous trouverez ceci en pièce jointe"

TEMPLATES: tuple[dict, ...] = (
    {
        "key": "cand_first_contact",
        "side": "candidate",
        "stage": "nouveau",
        "label": "1. Premier contact",
        "intent": "Étape Nouveau / à contacter — présenter le cabinet et obtenir un oui, sans frais pour le talent.",
        "subject": "{{who_lead}}Talendus peut vous placer — sans frais pour vous",
        "body": "{{hello}}\n\nJe vous écris de Talendus, cabinet de recrutement au Québec. Nous travaillons avec des usines, entrepôts et ateliers qui cherchent des profils {{title_or_metier}}{{city_bit}}.\n\nVous n’avez rien à débourser : c’est l’employeur qui nous mandate, pas vous.\n\nSi vous êtes ouvert à voir des mandats concrets, répondez simplement « oui » à ce courriel. Je ne vous enverrai que des postes qui tiennent la route.\n\nVous pouvez aussi déposer votre CV ici :\n{{candidate_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_followup",
        "side": "candidate",
        "stage": "contacte",
        "label": "2. Relance",
        "intent": "Étape Contacté — relancer sans pression, obtenir une réponse claire.",
        "subject": "{{who_lead}}est-ce que je vous reviens plus tard ?",
        "body": "{{hello}}\n\nJe vous avais écrit au sujet de mandats {{sector_or_industrie}} au Québec{{city_bit}}. Je ne veux pas insister : dites-moi simplement où vous en êtes.\n\n- « oui » si vous êtes ouvert à échanger\n- « plus tard » si ce n’est pas le bon moment\n- « non » si vous n’êtes plus en recherche\n\nDeux lignes suffisent. Si oui, déposez votre CV ici pour qu’on avance :\n{{candidate_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_qualify",
        "side": "candidate",
        "stage": "qualifie",
        "label": "3. Qualification",
        "intent": "Étape Qualifié — obtenir disponibilité, quart et fourchette avant de proposer un poste.",
        "subject": "{{who_lead}}trois infos pour vous proposer le bon poste",
        "body": "{{hello}}\n\nAvant de vous envoyer un mandat{{title_bit}}, j’ai besoin de trois précisions pour ne pas vous faire perdre de temps :\n\n- votre disponibilité (immédiat, 2 semaines, 1 mois…)\n- le quart accepté (jour, soir, rotatif)\n- votre fourchette salariale\n\nRépondez directement à ce courriel. Dès que j’ai ça, je reviens avec des postes concrets{{city_bit}}.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_documents",
        "side": "candidate",
        "stage": "qualifie",
        "label": "4. CV / documents",
        "intent": "Avant présentation — obtenir un CV à jour pour ouvrir le dossier aux employeurs.",
        "subject": "{{who_lead}}il nous manque votre CV pour vous présenter",
        "body": "{{hello}}\n\nVotre dossier est bien engagé. Pour vous présenter à un employeur, il nous faut un CV à jour (PDF de préférence).\n\nDéposez-le ici, ça prend deux minutes :\n{{candidate_link}}\n\nDès réception, on avance. Si un autre document est demandé (cartes, permis), je vous le précise.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_interview",
        "side": "candidate",
        "stage": "entretien",
        "label": "5. Entretien Talendus",
        "intent": "Étape Entretien — proposer un appel de 20 minutes, avec deux créneaux en réponse.",
        "subject": "{{who_lead}}20 minutes pour parler d’un vrai poste ?",
        "body": "{{hello}}\n\nJe vous propose un court appel (20 minutes) pour parler de votre parcours{{title_bit}} et des mandats ouverts{{city_bit}}.\n\nRépondez avec deux créneaux qui vous conviennent, ou confirmez ici :\n{{candidate_link}}\n\nVous pouvez aussi m’appeler au {{phone}}.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_job_ready",
        "side": "candidate",
        "stage": "presente",
        "label": "6. Poste à présenter",
        "intent": "Étape Présenté — annoncer un mandat concret et demander un oui pour envoyer le détail.",
        "subject": "{{who_lead}}un mandat {{title_or_metier}} peut vous correspondre",
        "body": "{{hello}}\n\nNous avons un mandat {{title_or_metier}}{{city_bit}} qui correspond à votre profil. L’employeur passe par Talendus : vous n’avez pas à négocier les honoraires.\n\nSi ça vous parle, répondez « oui » : je vous envoie le détail (quart, salaire, lieu) et on voit ensemble si on vous présente.\n\nVotre espace :\n{{candidate_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_offer",
        "side": "candidate",
        "stage": "offre",
        "label": "7. Offre / décision",
        "intent": "Étape Offre — rester l’interlocuteur pour les conditions et débloquer la décision.",
        "subject": "{{who_lead}}votre dossier avance — je reste votre contact",
        "body": "{{hello}}\n\nUne offre ou une suite concrète est sur la table. Je reste votre interlocuteur pour les conditions, les horaires et ce qui bloque encore.\n\nRépondez à ce courriel si une question vous retient, même courte. Vous pouvez aussi suivre l’étape ici :\n{{candidate_link}}\n\nOn règle ça ensemble, sans précipiter une décision qui ne vous convient pas.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_placed",
        "side": "candidate",
        "stage": "place",
        "label": "8. Placement confirmé",
        "intent": "Étape Placé — confirmer l’embauche et rester disponible pour les premiers jours.",
        "subject": "{{who_lead}}bienvenue dans votre nouveau poste",
        "body": "{{hello}}\n\nVotre placement est confirmé. Bravo. Les premiers jours, je reste disponible si un horaire, un document ou une question pratique bloque.\n\nRépondez à ce courriel, ou écrivez-nous à {{info}}. Votre espace reste ouvert :\n{{candidate_link}}\n\nBon départ, et merci de votre confiance.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_reactivate",
        "side": "candidate",
        "stage": "inactif",
        "label": "9. Réactivation",
        "intent": "Étape Inactif — rouvrir le dossier sans insister.",
        "subject": "{{who_lead}}de nouveaux mandats {{sector_or_industrie}} sont ouverts",
        "body": "{{hello}}\n\nCela fait un moment. Nous avons de nouveaux mandats {{sector_or_industrie}}{{city_bit}}.\n\nSi vous cherchez encore, répondez simplement « je suis ouvert ». Sinon, ignorez ce message, aucun suivi ne sera envoyé.\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_first_contact",
        "side": "employer",
        "stage": "nouveau",
        "label": "1. Premier contact",
        "intent": "Étape Nouveau / à contacter — présenter le cabinet et demander le poste ouvert, sans honoraires ni paiement.",
        "subject": "{{company_lead}}recruter sans perdre de semaines",
        "body": "{{hello}}\n\nJe vous contacte{{about_company}}. Talendus préqualifie des talents d’usine, d’entrepôt et de maintenance, puis ne vous présente que les profils qui tiennent.\n\nS’il vous manque un poste{{title_bit}}, répondez avec le métier et le quart : je vous dis ensuite si on peut le pourvoir.\n\nVous pouvez aussi déposer le besoin ici :\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_followup",
        "side": "employer",
        "stage": "contacte",
        "label": "2. Relance",
        "intent": "Étape Contacté — relancer avec une question unique (poste + quart).",
        "subject": "{{company_lead}}le poste est-il toujours ouvert ?",
        "body": "{{hello}}\n\nJe reviens{{about_company}}. Nous recrutons encore des profils {{sector_or_industrie}} pour des usines d’ici.\n\nSi le besoin est toujours là, répondez avec le poste et le quart. Je reviens avec un plan concret, sans engagement de votre côté à ce stade.\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_discovery",
        "side": "employer",
        "stage": "qualifie",
        "label": "3. Appel de cadrage",
        "intent": "Étape Qualifié — obtenir 20 minutes pour cadrer poste, quart, salaire et ce qui a échoué.",
        "subject": "{{company_lead}}20 minutes pour cadrer le besoin ?",
        "body": "{{hello}}\n\nAvant d’ouvrir un mandat{{about_company}}, je vous propose un court appel : poste, quart, salaire, et ce qui a déjà échoué en recrutement.\n\nRépondez avec deux créneaux. Ensuite on décide ensemble s’il vaut la peine de lancer une recherche.\n\nVous pouvez aussi m’appeler au {{phone}}.\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_mandate",
        "side": "employer",
        "stage": "proposition",
        "label": "4. Mandat à signer",
        "intent": "Étape Proposition — envoyer le mandat à lire et signer. Le pourcentage reste dans le contrat, pas dans le courriel.",
        "subject": "{{company_lead}}mandat Talendus à lire et signer",
        "body": "{{hello}}\n\nVoici la suite{{about_company}} : le mandat de recrutement Talendus.\n\nLisez-le, signez-le dans votre espace, et on lance la recherche.\n\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_search_start",
        "side": "employer",
        "stage": "proposition",
        "label": "5. Recherche lancée",
        "intent": "Après signature — confirmer que la chasse est ouverte et ce qui se passe ensuite.",
        "subject": "{{company_lead}}la recherche Talendus est lancée",
        "body": "{{hello}}\n\nLe mandat est en place{{about_company}}. La recherche est ouverte : on préqualifie, on ne vous présente que les profils qui tiennent.\n\nDe votre côté, rien à faire pour le moment. Dès qu’un dossier est prêt, je vous propose un créneau de présentation.\n\nSuivi dans votre espace :\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_talent_ready",
        "side": "employer",
        "stage": "client",
        "label": "6. Profils à présenter",
        "intent": "Pendant le mandat — annoncer des talents préqualifiés et fixer un créneau.",
        "subject": "{{company_lead}}des profils {{title_or_poste}} sont prêts",
        "body": "{{hello}}\n\nNous avons préqualifié des profils {{title_or_poste}}{{about_company}}. Je peux vous les présenter dès que vous confirmez un créneau (visio ou sur place).\n\nRépondez à ce courriel avec deux disponibilités, ou ouvrez votre espace :\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_invoice",
        "side": "employer",
        "stage": "client",
        "label": "7. Facture",
        "intent": "Après embauche — transmettre la facture et dire comment payer, sans rappeler un pourcentage.",
        "subject": "{{company_lead}}facture Talendus",
        "body": "{{hello}}\n\nLa facture Talendus{{about_company}} est prête, selon le mandat signé.\n\nPaiement par virement ou chèque, aux conditions prévues. Une question sur le montant ou l’échéance : répondez à ce courriel.\n\nVous pouvez aussi la télécharger ici :\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_reactivate",
        "side": "employer",
        "stage": "inactif",
        "label": "8. Réactivation",
        "intent": "Étape Inactif / perdu — rouvrir un besoin sans relance lourde.",
        "subject": "{{company_lead}}un poste à pourvoir cette semaine ?",
        "body": "{{hello}}\n\nNous n’avons pas échangé depuis un moment. Si un poste {{title_or_poste}} est à pourvoir{{about_company}}, je peux relancer une recherche cette semaine.\n\nRépondez avec le métier et le quart, ou ignorez ce message si le besoin n’est plus là.\n\n{{recruiter_name}}",
    },
)


def normalize_side(raw: str | None) -> str:
    value = (raw or "").strip().lower()
    if value in {"employer", "employeur", "recruteur", "recruiter", "client", "company"}:
        return "employer"
    if value in {"candidate", "candidat", "talent"}:
        return "candidate"
    raise AppError(400, "Côté requis : candidat ou employeur.", "VALIDATION_ERROR")


def stages_for(side: str) -> tuple[tuple[str, str], ...]:
    return EMPLOYER_STAGES if side == "employer" else CANDIDATE_STAGES


def _valid_stage(side: str, stage: str) -> str:
    allowed = {key for key, _ in stages_for(side)}
    if stage not in allowed:
        raise AppError(400, "Étape inconnue pour ce pipeline.", "VALIDATION_ERROR")
    return stage


def _clean_email(raw: str | None) -> str:
    return (raw or "").strip().lower()


def _split_name(raw: str | None) -> tuple[str, str]:
    parts = [p for p in re.split(r"\s+", (raw or "").strip()) if p]
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def display_name(row: Prospect) -> str:
    name = f"{row.first_name} {row.last_name}".strip()
    return name or row.company_name or row.email


def account_links_for(email: str | None, side: str | None) -> dict[str, str]:
    encoded = quote((email or "").strip().lower(), safe="")
    portal = EMPLOYEUR if (side or "") == "employer" else ESPACE
    role = "EMPLOYER" if (side or "") == "employer" else "CANDIDATE"
    return {
        "portal_link": portal,
        "login_link": f"{portal}#/login?email={encoded}",
        "register_link": f"{portal}#/register?email={encoded}&role={role}",
        "candidate_link": ESPACE,
        "employer_link": EMPLOYEUR,
    }


def context_for(row: Prospect, actor: User | None = None) -> dict[str, str]:
    first = (row.first_name or "").strip()
    last = (row.last_name or "").strip()
    company = (row.company_name or "").strip()
    title = (row.title or "").strip()
    city = (row.city or "").strip()
    sector = (row.sector or "").strip()
    recruiter = ""
    if actor:
        recruiter = f"{actor.first_name} {actor.last_name}".strip()
    hello = f"Bonjour {first}," if first else "Bonjour,"
    ctx = {
        "first_name": first or company or "bonjour",
        "last_name": last,
        "name": display_name(row),
        "hello": hello,
        "who_lead": f"{first}, " if first else "",
        "company": company or "votre entreprise",
        "company_lead": f"{company} — " if company else "",
        "about_company": f" au sujet de {company}" if company else "",
        "chez_company": f"chez {company}" if company else "chez vous",
        "title": title,
        "title_or_metier": title or "industriels",
        "title_or_poste": title or "recherchés",
        "title_bit": f" ({title})" if title else "",
        "city": city,
        "city_bit": f" à {city}" if city else "",
        "sector": sector,
        "sector_or_industrie": sector or "industriels",
        "phone": PHONE,
        "info": INFO,
        "recruiter_name": recruiter or "L’équipe Talendus",
    }
    ctx.update(account_links_for(row.email, row.side))
    return ctx


def fill_tokens(text: str, ctx: dict[str, str]) -> str:
    out = text or ""
    for key, value in ctx.items():
        out = out.replace("{{" + key + "}}", str(value))
    return out


def catalog(side: str | None = None) -> list[dict]:
    wanted = normalize_side(side) if side else None
    rows = []
    for item in TEMPLATES:
        if wanted and item["side"] != wanted:
            continue
        rows.append({k: item[k] for k in ("key", "side", "label", "intent", "stage") if k in item})
    return rows


def get_template(key: str) -> dict:
    for item in TEMPLATES:
        if item["key"] == key:
            return item
    raise AppError(400, "Modèle de courriel inconnu.", "UNKNOWN_TEMPLATE")


def custom_template_key(subject: str) -> str:
    digest = hashlib.sha256((subject or "").strip().lower().encode("utf-8")).hexdigest()[:16]
    return f"custom:{digest}"


def serialize_prospect(row: Prospect, sent_keys: list[str] | None = None) -> dict:
    return {
        "id": row.id,
        "side": row.side,
        "stage": row.stage,
        "email": row.email,
        "first_name": row.first_name,
        "last_name": row.last_name,
        "phone": row.phone,
        "company_name": row.company_name,
        "title": row.title,
        "city": row.city,
        "sector": row.sector,
        "source": row.source,
        "source_detail": row.source_detail,
        "message": row.message,
        "assigned_recruiter_id": row.assigned_recruiter_id,
        "user_id": row.user_id,
        "candidate_id": row.candidate_id,
        "company_id": row.company_id,
        "last_contacted_at": row.last_contacted_at.isoformat() if row.last_contacted_at else None,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "display_name": display_name(row),
        "sent_templates": sent_keys or [],
        **account_links_for(row.email, row.side),
    }


def serialize_send(row: ProspectSend) -> dict:
    return {
        "id": row.id,
        "prospect_id": row.prospect_id,
        "template_key": row.template_key,
        "subject": row.subject,
        "to_email": row.to_email,
        "attachment_names": [n for n in (row.attachment_names or "").split("|") if n],
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def _iso(value) -> str | None:
    return value.isoformat() if value else None


def _account(user: User | None) -> dict | None:
    if not user:
        return None
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "role": user.role.value if user.role else None,
        "is_active": bool(user.is_active),
        "is_email_verified": bool(user.is_email_verified),
        "account_status": user.account_status.value if user.account_status else None,
        "last_login_at": _iso(user.last_login_at),
        "created_at": _iso(user.created_at),
    }


def _note_row(note: InternalNote, authors: dict[str, User]) -> dict:
    author = authors.get(note.author_id)
    return {
        "id": note.id,
        "entity_type": note.entity_type,
        "entity_id": note.entity_id,
        "text": note.text,
        "author_id": note.author_id,
        "author_name": author.full_name if author else None,
        "created_at": _iso(note.created_at),
    }


def dossier_for(db: Session, row: Prospect) -> dict:
    from app.services.audit import serialize_audit
    from app.services.candidates import serialize_candidate
    from app.services.companies import serialize_company
    from app.services.hiring_requests import serialize_request

    user = db.get(User, row.user_id) if row.user_id else None
    if user is None:
        user = db.scalar(select(User).where(User.email == row.email))
    profile = db.get(Candidate, row.candidate_id) if row.candidate_id else None
    if profile is None and user:
        profile = db.scalar(select(Candidate).where(Candidate.user_id == user.id))
    company = db.get(Company, row.company_id) if row.company_id else None
    if company is None and user:
        company = db.scalar(select(Company).where(Company.owner_user_id == user.id))

    applications = []
    interviews = []
    if profile:
        applications = list(
            db.scalars(select(Application).where(Application.candidate_id == profile.id).order_by(Application.created_at.desc())).all()
        )
        interviews = list(
            db.scalars(select(Interview).where(Interview.candidate_id == profile.id).order_by(Interview.scheduled_at.desc())).all()
        )
    hiring = []
    contracts = []
    invoices = []
    if company:
        hiring = list(
            db.scalars(
                select(RecruitmentMission).where(RecruitmentMission.company_id == company.id).order_by(RecruitmentMission.created_at.desc())
            ).all()
        )
        contracts = list(db.scalars(select(Contract).where(Contract.company_id == company.id).order_by(Contract.created_at.desc())).all())
        invoices = list(db.scalars(select(Invoice).where(Invoice.company_id == company.id).order_by(Invoice.created_at.desc())).all())

    related_ids = {row.id}
    if profile:
        related_ids.add(profile.id)
    if company:
        related_ids.add(company.id)
    if user:
        related_ids.add(user.id)
    related_ids.update(item.id for item in applications)
    related_ids.update(item.id for item in hiring)

    notes = list(
        db.scalars(
            select(InternalNote)
            .where(InternalNote.entity_id.in_(related_ids))
            .order_by(InternalNote.created_at.desc())
            .limit(40)
        ).all()
    )
    authors = {
        person.id: person
        for person in (
            db.scalars(select(User).where(User.id.in_({n.author_id for n in notes if n.author_id}))).all() if notes else []
        )
    }
    audits = list(
        db.scalars(
            select(AuditLog)
            .where(
                or_(
                    (AuditLog.entity_type == "prospect") & (AuditLog.entity_id == row.id),
                    AuditLog.entity_id.in_(related_ids),
                )
            )
            .order_by(AuditLog.created_at.desc())
            .limit(40)
        ).all()
    )
    audit_actors = {
        person.id: person
        for person in (
            db.scalars(select(User).where(User.id.in_({a.actor_id for a in audits if a.actor_id}))).all() if audits else []
        )
    }

    expectations = {}
    if profile:
        expectations = {
            "availability": profile.availability,
            "shift": profile.shift_preference,
            "salary_min": profile.desired_salary_min,
            "salary_max": profile.desired_salary_max,
            "mobility": profile.mobility,
            "contract_type": profile.contract_type,
            "work_status": profile.work_status,
            "job_search_status": profile.job_search_status.value if profile.job_search_status else None,
            "work_preferences": profile.work_preferences,
            "languages": profile.languages,
            "city": profile.city,
            "title": profile.title,
        }
    elif hiring:
        first = hiring[0]
        expectations = {
            "title": first.title,
            "location": first.location,
            "shift": first.shift,
            "salary": first.salary_display,
            "contract_type": first.contract_type,
            "skills": first.skills,
            "seats": first.seats,
            "work_authorization": first.work_authorization,
            "notes": first.notes,
        }

    return {
        "account": _account(user),
        "linked": {
            "candidate_id": profile.id if profile else row.candidate_id,
            "company_id": company.id if company else row.company_id,
            "user_id": user.id if user else row.user_id,
        },
        "profile": serialize_candidate(profile, include_private=True) if profile else None,
        "company": serialize_company(company) if company else None,
        "expectations": expectations,
        "applications": [
            {
                "id": item.id,
                "status": item.status.value if item.status else None,
                "job_id": item.job_id,
                "job_title": item.job.title if item.job else None,
                "company_name": item.job.company.name if item.job and item.job.company else None,
                "cover_note": item.cover_note,
                "created_at": _iso(item.created_at),
            }
            for item in applications
        ],
        "hiring_requests": [serialize_request(item) for item in hiring],
        "interviews": [
            {
                "id": item.id,
                "type": item.type.value if item.type else None,
                "status": item.status.value if item.status else None,
                "scheduled_at": _iso(item.scheduled_at),
                "location": item.location,
                "job_id": item.job_id,
            }
            for item in interviews
        ],
        "contracts": [
            {
                "id": item.id,
                "type": item.type,
                "status": item.status.value if item.status else None,
                "commission_percent": item.commission_percent,
                "start_date": item.start_date,
                "end_date": item.end_date,
            }
            for item in contracts
        ],
        "invoices": [
            {
                "id": item.id,
                "number": item.number,
                "status": item.status.value if item.status else None,
                "amount_total": item.amount_total or item.amount,
                "due_date": item.due_date,
            }
            for item in invoices
        ],
        "notes": [_note_row(note, authors) for note in notes],
        "recent_actions": [serialize_audit(item, audit_actors.get(item.actor_id)) for item in audits],
    }


def add_prospect_note(db: Session, actor: User, prospect_id: str, text: str) -> InternalNote:
    from app.services.audit import audit

    row = get_prospect(db, prospect_id)
    note = InternalNote(entity_type="prospect", entity_id=row.id, author_id=actor.id, text=(text or "").strip())
    if not note.text:
        raise AppError(400, "La note ne peut pas être vide.", "VALIDATION_ERROR")
    db.add(note)
    audit(db, "note.create", actor, "prospect", row.id)
    db.flush()
    return note


def upsert_prospect(
    db: Session,
    *,
    side: str,
    email: str,
    source: str = "prospection",
    first_name: str = "",
    last_name: str = "",
    phone: str = "",
    company_name: str = "",
    title: str = "",
    city: str = "",
    sector: str = "",
    source_detail: str = "",
    message: str = "",
    user_id: str | None = None,
    candidate_id: str | None = None,
    company_id: str | None = None,
    assigned_recruiter_id: str | None = None,
    stage: str | None = None,
) -> Prospect | None:
    email = _clean_email(email)
    if not email or "@" not in email:
        return None
    side = normalize_side(side)
    row = db.scalar(select(Prospect).where(Prospect.side == side, Prospect.email == email))
    created = row is None
    if created:
        row = Prospect(side=side, email=email, source=source[:40], stage="nouveau")
        db.add(row)
        db.flush()
    updates = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "company_name": company_name,
        "title": title,
        "city": city,
        "sector": sector,
        "source_detail": source_detail,
        "message": message,
        "user_id": user_id,
        "candidate_id": candidate_id,
        "company_id": company_id,
        "assigned_recruiter_id": assigned_recruiter_id,
    }
    for key, value in updates.items():
        if value in (None, ""):
            continue
        current = getattr(row, key)
        if not current:
            setattr(row, key, value[:500] if isinstance(value, str) else value)
    if created and source:
        row.source = source[:40]
    if stage:
        row.stage = _valid_stage(side, stage)
    return row


def touch_from_user(db: Session, user: User, *, source: str = "inscription", company_name: str = "") -> Prospect | None:
    if user.role == UserRole.CANDIDATE:
        profile = db.scalar(select(Candidate).where(Candidate.user_id == user.id))
        return upsert_prospect(
            db,
            side="candidate",
            email=user.email,
            source=source,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            phone=user.phone or "",
            title=(profile.title if profile else "") or user.title or "",
            city=profile.city if profile else "",
            sector=profile.sector if profile else "",
            user_id=user.id,
            candidate_id=profile.id if profile else None,
        )
    if user.role == UserRole.EMPLOYER:
        company = db.scalar(select(Company).where(Company.owner_user_id == user.id))
        return upsert_prospect(
            db,
            side="employer",
            email=user.email,
            source=source,
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            phone=user.phone or (company.phone if company else "") or "",
            company_name=company_name or (company.name if company else ""),
            city=company.city if company else "",
            sector=company.sector if company else "",
            user_id=user.id,
            company_id=company.id if company else None,
        )
    return None


def sync_known_people(db: Session) -> int:
    added = 0
    candidates = db.scalars(select(Candidate)).all()
    for profile in candidates:
        user = db.get(User, profile.user_id)
        if not user or not user.email:
            continue
        before = db.scalar(select(Prospect.id).where(Prospect.side == "candidate", Prospect.email == user.email.lower()))
        touch_from_user(db, user, source="inscription")
        if before is None:
            added += 1
    companies = db.scalars(select(Company)).all()
    for company in companies:
        email = (company.email or "").lower()
        owner = None
        if company.owner_user_id:
            owner = db.get(User, company.owner_user_id)
        if owner and owner.email:
            email = owner.email.lower()
        if not email:
            continue
        before = db.scalar(select(Prospect.id).where(Prospect.side == "employer", Prospect.email == email))
        first, last = _split_name(company.contact_name)
        upsert_prospect(
            db,
            side="employer",
            email=email,
            source="inscription" if owner else "prospection",
            first_name=(owner.first_name if owner else first) or first,
            last_name=(owner.last_name if owner else last) or last,
            phone=company.phone or (owner.phone if owner else "") or "",
            company_name=company.name or "",
            city=company.city or "",
            sector=company.sector or "",
            user_id=owner.id if owner else None,
            company_id=company.id,
            stage="client" if before is None and getattr(company.status, "value", str(company.status)) == "ACTIVE" else None,
        )
        if before is None:
            added += 1
    return added


def list_prospects(
    db: Session,
    *,
    side: str,
    stage: str | None = None,
    q: str | None = None,
    source: str | None = None,
    city: str | None = None,
    sector: str | None = None,
) -> list[Prospect]:
    sync_known_people(db)
    wanted = normalize_side(side)
    stmt = select(Prospect).where(Prospect.side == wanted).order_by(Prospect.updated_at.desc())
    if stage:
        stmt = stmt.where(Prospect.stage == stage)
    if source:
        stmt = stmt.where(Prospect.source == source)
    if city:
        stmt = stmt.where(Prospect.city.ilike(city.strip()))
    if sector:
        stmt = stmt.where(Prospect.sector.ilike(sector.strip()))
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where(
            or_(
                Prospect.email.ilike(like),
                Prospect.first_name.ilike(like),
                Prospect.last_name.ilike(like),
                Prospect.company_name.ilike(like),
                Prospect.title.ilike(like),
                Prospect.phone.ilike(like),
            )
        )
    return list(db.scalars(stmt).all())


def filter_options(db: Session, side: str) -> dict[str, list[str]]:
    wanted = normalize_side(side)
    cities = [
        value
        for value in db.scalars(select(Prospect.city).where(Prospect.side == wanted, Prospect.city != "").distinct()).all()
        if value
    ]
    sectors = [
        value
        for value in db.scalars(select(Prospect.sector).where(Prospect.side == wanted, Prospect.sector != "").distinct()).all()
        if value
    ]
    return {
        "cities": sorted(cities, key=str.casefold),
        "sectors": sorted(sectors, key=str.casefold),
    }


def sent_keys_map(db: Session, prospect_ids: list[str]) -> dict[str, list[str]]:
    if not prospect_ids:
        return {}
    rows = db.scalars(select(ProspectSend).where(ProspectSend.prospect_id.in_(prospect_ids))).all()
    out: dict[str, list[str]] = {pid: [] for pid in prospect_ids}
    for row in rows:
        out.setdefault(row.prospect_id, []).append(row.template_key)
    return out


RESERVED_PATHS = frozenset({"catalog", "templates", "broadcast", "send-bulk", "sync", "p"})


def get_prospect(db: Session, prospect_id: str) -> Prospect:
    key = (prospect_id or "").strip()
    if not key or key.lower() in RESERVED_PATHS:
        raise AppError(404, "Prospect introuvable.", "NOT_FOUND")
    row = db.get(Prospect, key)
    if row:
        return row
    raise AppError(404, "Prospect introuvable.", "NOT_FOUND")


def create_prospect(db: Session, actor: User, data: dict) -> Prospect:
    side = normalize_side(data.get("side"))
    email = _clean_email(data.get("email"))
    if not email:
        raise AppError(400, "Le courriel du prospect est requis.", "VALIDATION_ERROR")
    existing = db.scalar(select(Prospect).where(Prospect.side == side, Prospect.email == email))
    if existing:
        raise AppError(409, "Ce prospect existe déjà de ce côté.", "PROSPECT_EXISTS")
    row = upsert_prospect(
        db,
        side=side,
        email=email,
        source=data.get("source") or "prospection",
        first_name=data.get("first_name") or "",
        last_name=data.get("last_name") or "",
        phone=data.get("phone") or "",
        company_name=data.get("company_name") or "",
        title=data.get("title") or "",
        city=data.get("city") or "",
        sector=data.get("sector") or "",
        source_detail=data.get("source_detail") or "Ajout admin",
        message=data.get("message") or "",
        assigned_recruiter_id=data.get("assigned_recruiter_id") or actor.id,
        stage=data.get("stage") or "nouveau",
    )
    if row is None:
        raise AppError(400, "Impossible de créer ce prospect.", "VALIDATION_ERROR")
    from app.services.audit import audit

    audit(db, "prospect.create", actor, "prospect", row.id, metadata={"side": row.side, "email": row.email})
    return row


def patch_prospect(db: Session, prospect_id: str, data: dict, actor: User | None = None) -> Prospect:
    row = get_prospect(db, prospect_id)
    tracked = ("stage", "first_name", "last_name", "phone", "company_name", "title", "city", "sector", "source_detail", "message", "assigned_recruiter_id")
    old = {key: getattr(row, key) for key in tracked}
    if "stage" in data and data["stage"]:
        row.stage = _valid_stage(row.side, data["stage"])
    for key in ("first_name", "last_name", "phone", "company_name", "title", "city", "sector", "source_detail", "message"):
        if key in data and data[key] is not None:
            setattr(row, key, str(data[key])[:500] if key != "message" else str(data[key])[:5000])
    if "assigned_recruiter_id" in data:
        row.assigned_recruiter_id = data["assigned_recruiter_id"] or None
    changed = {key: getattr(row, key) for key in tracked if old.get(key) != getattr(row, key)}
    if actor and changed:
        from app.services.audit import audit

        action = "prospect.stage" if list(changed.keys()) == ["stage"] else "prospect.patch"
        audit(db, action, actor, "prospect", row.id, old_value={k: old[k] for k in changed}, new_value=changed)
    return row


def proposals_for(db: Session, row: Prospect, actor: User | None) -> list[dict]:
    sent = {s.template_key for s in db.scalars(select(ProspectSend).where(ProspectSend.prospect_id == row.id)).all()}
    ctx = context_for(row, actor)
    out = []
    for item in TEMPLATES:
        if item["side"] != row.side:
            continue
        out.append(
            {
                "key": item["key"],
                "label": item["label"],
                "intent": item["intent"],
                "stage": item.get("stage") or "",
                "subject": fill_tokens(item["subject"], ctx),
                "body": fill_tokens(item["body"], ctx),
                "already_sent": item["key"] in sent,
            }
        )
    return out


@dataclass
class SendRequest:
    template_key: str | None = None
    subject: str | None = None
    body: str | None = None
    invoice_ids: list[str] | None = None
    contract_ids: list[str] | None = None
    force: bool = False


def _attachments_for(db: Session, row: Prospect, invoice_ids: list[str] | None, contract_ids: list[str] | None) -> list[EmailAttachment]:
    from app.services.pdf_docs import contract_pdf, invoice_pdf

    files: list[EmailAttachment] = []
    for invoice_id in invoice_ids or []:
        invoice = db.get(Invoice, invoice_id)
        if not invoice:
            raise AppError(404, "Facture introuvable.", "NOT_FOUND")
        if row.company_id and invoice.company_id and invoice.company_id != row.company_id:
            raise AppError(403, "Cette facture n’appartient pas à ce prospect.", "FORBIDDEN")
        files.append(
            EmailAttachment(
                filename=f"{invoice.number or 'facture'}.pdf",
                data=invoice_pdf(invoice),
                mime="application/pdf",
                kind="invoice",
                label=invoice.number or "facture",
            )
        )
    for contract_id in contract_ids or []:
        contract = db.get(Contract, contract_id)
        if not contract:
            raise AppError(404, "Contrat introuvable.", "NOT_FOUND")
        if row.company_id and contract.company_id and contract.company_id != row.company_id:
            raise AppError(403, "Ce contrat n’appartient pas à ce prospect.", "FORBIDDEN")
        files.append(
            EmailAttachment(
                filename=f"mandat-{(contract.company.name if contract.company else 'talendus')}.pdf",
                data=contract_pdf(contract),
                mime="application/pdf",
                kind="contract",
                label=contract.type or "Mandat",
            )
        )
    return files


def _account_howto(ctx: dict[str, str]) -> str:
    login = ctx.get("login_link") or f"{EMPLOYEUR}#/login"
    register = ctx.get("register_link") or f"{EMPLOYEUR}#/register?role=EMPLOYER"
    return (
        "Comment faire :\n"
        "- Si vous avez déjà un compte Talendus, connectez-vous ici :\n"
        f"{login}\n"
        "- Si vous n’avez pas encore créé de compte, ouvrez ce lien : il préremplit votre courriel et crée votre accès :\n"
        f"{register}"
    )


def attachment_note(attachments: list[EmailAttachment], ctx: dict[str, str]) -> str:
    blocks = []
    for att in attachments:
        name = att.filename or "document.pdf"
        kind = (att.kind or "").lower()
        hook = f"{ATTACHMENT_HOOK} : {name}"
        howto = _account_howto(ctx)
        if kind == "invoice" or name.lower().startswith("f-") or "facture" in name.lower():
            blocks.append(
                f"{hook}\n\n"
                "À faire :\n"
                "- ouvrir le PDF et vérifier le montant\n"
                "- régler par virement ou chèque, selon les conditions du mandat signé\n"
                f"- écrire à {ctx.get('info') or INFO} si une ligne vous interroge\n\n"
                f"{howto}"
            )
        elif kind == "contract" or "mandat" in name.lower() or "contrat" in name.lower():
            blocks.append(
                f"{hook}\n\n"
                "À faire :\n"
                "- ouvrir le PDF et le lire en entier\n"
                "- le signer dans votre espace (plus simple que d’imprimer)\n"
                "- nous répondre « signé » une fois c’est fait\n\n"
                f"{howto}"
            )
        else:
            blocks.append(
                f"{hook}\n\n"
                "À faire : ouvrez le fichier, puis répondez si une suite est demandée.\n\n"
                f"{howto}"
            )
    return "\n\n".join(blocks)


def _body_has_attachment_note(body: str) -> bool:
    low = (body or "").lower()
    return "trouverez ceci en pièce jointe" in low or "pièce jointe —" in low or "pièce jointe\n" in low


def append_attachment_note(body: str, attachments: list[EmailAttachment], ctx: dict[str, str]) -> str:
    if not attachments:
        return body
    if _body_has_attachment_note(body):
        return body
    return f"{(body or '').rstrip()}\n\n{attachment_note(attachments, ctx)}"


def available_attachments(db: Session, row: Prospect) -> dict:
    invoices = []
    contracts = []
    if row.company_id:
        invoices = [
            {"id": inv.id, "label": inv.number or inv.id, "amount": str(inv.amount or "")}
            for inv in db.scalars(select(Invoice).where(Invoice.company_id == row.company_id)).all()
        ]
        contracts = [
            {"id": c.id, "label": c.type or "Mandat", "status": getattr(c.status, "value", str(c.status or ""))}
            for c in db.scalars(select(Contract).where(Contract.company_id == row.company_id)).all()
        ]
    return {"invoices": invoices, "contracts": contracts}


def send_to_prospect(db: Session, actor: User, row: Prospect, req: SendRequest) -> dict:
    key = (req.template_key or "").strip()
    subject = (req.subject or "").strip()
    body = (req.body or "").strip()
    ctx = context_for(row, actor)
    if key and not key.startswith("custom"):
        tpl = get_template(key)
        if tpl["side"] != row.side:
            raise AppError(400, "Ce modèle ne correspond pas à ce côté.", "VALIDATION_ERROR")
        subject = fill_tokens(subject or tpl["subject"], ctx)
        body = fill_tokens(body or tpl["body"], ctx)
    else:
        if not subject or not body:
            raise AppError(400, "Sujet et message sont requis pour un courriel libre.", "VALIDATION_ERROR")
        key = custom_template_key(subject)
        subject = fill_tokens(subject, ctx)
        body = fill_tokens(body, ctx)
    existing = db.scalar(select(ProspectSend).where(ProspectSend.prospect_id == row.id, ProspectSend.template_key == key))
    if existing and not req.force:
        raise AppError(
            409,
            f"{display_name(row)} a déjà reçu ce message ({existing.subject}). Choisissez un autre modèle, ou forcez l’envoi.",
            "ALREADY_SENT",
        )
    attachments = _attachments_for(db, row, req.invoice_ids, req.contract_ids)
    body = append_attachment_note(body, attachments, ctx)
    log = send_composed_email(
        db,
        row.email,
        subject,
        body,
        email_type=EmailType.ADMIN,
        sync=True,
        attachments=attachments,
    )
    names = "|".join(att.filename for att in attachments)
    if existing and req.force:
        existing.subject = subject[:180]
        existing.body = body
        existing.to_email = row.email
        existing.email_log_id = log.id
        existing.attachment_names = names
        existing.sent_by_id = actor.id
        send_row = existing
    else:
        send_row = ProspectSend(
            prospect_id=row.id,
            template_key=key,
            subject=subject[:180],
            body=body,
            to_email=row.email,
            email_log_id=log.id,
            attachment_names=names,
            sent_by_id=actor.id,
        )
        db.add(send_row)
    row.last_contacted_at = utcnow()
    if row.stage in {"nouveau", "a-contacter"}:
        row.stage = "contacte"
    from app.services.audit import audit

    audit(db, "prospect.send", actor, "prospect", row.id, metadata={"template": key, "to": row.email, "subject": subject[:180]})
    db.flush()
    return {
        "prospect_id": row.id,
        "to_email": row.email,
        "template_key": key,
        "subject": subject,
        "email_status": log.status.value if log.status else "QUEUED",
        "attachments": [att.filename for att in attachments],
    }


def send_bulk(db: Session, actor: User, ids: list[str], req: SendRequest) -> dict:
    if not ids:
        raise AppError(400, "Choisissez au moins un prospect.", "VALIDATION_ERROR")
    if len(ids) > 80:
        raise AppError(400, "Maximum 80 destinataires à la fois.", "VALIDATION_ERROR")
    sent, skipped, failed = [], [], []
    found = [db.get(Prospect, prospect_id) for prospect_id in ids]
    sides = {row.side for row in found if row}
    if len(sides) > 1:
        raise AppError(400, "Impossible d’envoyer aux deux bases en même temps.", "SIDE_MIXED")
    for prospect_id, row in zip(ids, found):
        if not row:
            failed.append({"id": prospect_id, "reason": "introuvable"})
            continue
        try:
            sent.append(send_to_prospect(db, actor, row, req))
        except AppError as exc:
            if exc.code == "ALREADY_SENT":
                skipped.append({"id": row.id, "email": row.email, "reason": exc.message})
            else:
                failed.append({"id": row.id, "email": row.email, "reason": exc.message})
    return {"sent": sent, "skipped": skipped, "failed": failed}
