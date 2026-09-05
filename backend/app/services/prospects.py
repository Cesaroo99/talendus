"""CRM prospects : deux pipelines, propositions personnalisées, anti-doublon, PJ."""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from urllib.parse import quote

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Application, AuditLog, Candidate, Company, Contract, EmailLog, InternalNote, Interview, Invoice, RecruitmentMission, User
from app.models.enums import EmailType, UserRole, utcnow
from app.models.prospect import Prospect, ProspectSend
from app.services.email import (
    EmailAttachment,
    delivery_error,
    email_actually_sent,
    mark_fake_sent_logs,
    send_composed_email,
    start_worker,
)

logger = logging.getLogger("talendus.prospects")
BULK_SEND_MAX = 400
BULK_SEND_DAILY_MAX = 400

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
        "intent": "Premier contact talent — se présenter, expliquer pourquoi on écrit, proposer un échange. Ni argent, ni promesse de placement.",
        "subject": "Votre profil {{title_or_metier}}",
        "body": "{{hello}}\n\nJe vous écris de Talendus, cabinet de recrutement au Québec. Nous travaillons avec des employeurs de tous les secteurs qui cherchent un profil{{title_bit}}{{city_bit}}.\n\nSi un changement de poste vous intéresse, même à explorer, répondez-moi. Je reviendrai ensuite avec des mandats précis — pas une liste envoyée à l’aveugle.\n\nVous pouvez aussi me déposer votre CV ici :\n{{candidate_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_followup",
        "side": "candidate",
        "stage": "contacte",
        "label": "2. Relance",
        "intent": "Relance talent — une question, sans formulaire et sans pression.",
        "subject": "Je me permets de revenir vers vous",
        "body": "{{hello}}\n\nJe vous avais écrit au sujet de postes{{sector_bit}}{{city_bit}}. Je ne veux pas alourdir votre boîte.\n\nDites-moi seulement si le moment est bon pour en parler, ou si je dois refermer le dossier. Les deux réponses me conviennent.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_qualify",
        "side": "candidate",
        "stage": "qualifie",
        "label": "3. Qualification",
        "intent": "Qualification — trois précisions pour cibler, formulées comme un service, pas un interrogatoire.",
        "subject": "Quelques précisions pour cibler juste",
        "body": "{{hello}}\n\nPour vous proposer quelque chose de juste{{title_bit}}, j’ai besoin de trois précisions :\n\n- votre disponibilité\n- l’horaire que vous acceptez\n- la fourchette que vous visez\n\nRépondez directement à ce courriel. Dès que j’ai ça, je reviens vers vous avec des postes concrets{{city_bit}}.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_documents",
        "side": "candidate",
        "stage": "qualifie",
        "label": "4. CV / documents",
        "intent": "Demander un CV à jour sans formuler un manque ni une urgence artificielle.",
        "subject": "Votre CV pour présenter le dossier",
        "body": "{{hello}}\n\nPour présenter votre dossier à un employeur, j’ai besoin d’un CV à jour, de préférence en PDF.\n\nVous pouvez le déposer ici :\n{{candidate_link}}\n\nSi un permis ou une carte est nécessaire ensuite, je vous le préciserai.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_interview",
        "side": "candidate",
        "stage": "entretien",
        "label": "5. Entretien Talendus",
        "intent": "Proposer un appel court, avec deux créneaux, sans formules vendeuses.",
        "subject": "Un échange de vingt minutes",
        "body": "{{hello}}\n\nJe vous propose un appel de vingt minutes pour parler de votre parcours{{title_bit}} et des postes ouverts{{city_bit}}.\n\nIndiquez-moi deux créneaux qui vous conviennent, ou confirmez ici :\n{{candidate_link}}\n\nVous pouvez aussi me joindre au {{phone}}.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_job_ready",
        "side": "candidate",
        "stage": "presente",
        "label": "6. Poste à présenter",
        "intent": "Annoncer un poste concret et demander l’accord avant d’envoyer le détail. Sans parler d’honoraires.",
        "subject": "Un poste {{title_or_metier}} à vous soumettre",
        "body": "{{hello}}\n\nNous avons un poste {{title_or_metier}}{{city_bit}} qui me semble correspondre à votre profil.\n\nSi vous souhaitez en voir le détail — horaire, rémunération, lieu — répondez-moi. On verra ensuite ensemble s’il vaut la peine de vous présenter.\n\nVotre espace :\n{{candidate_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_offer",
        "side": "candidate",
        "stage": "offre",
        "label": "7. Offre / décision",
        "intent": "Rester l’interlocuteur unique, sans précipiter la décision.",
        "subject": "Je reste disponible pour votre décision",
        "body": "{{hello}}\n\nVotre dossier avance. Je reste votre interlocuteur pour les conditions, l’horaire et tout ce qui reste à clarifier.\n\nSi une question vous retient, même courte, répondez à ce courriel. Vous pouvez aussi suivre le dossier ici :\n{{candidate_link}}\n\nPrenez le temps qu’il faut.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_placed",
        "side": "candidate",
        "stage": "place",
        "label": "8. Placement confirmé",
        "intent": "Confirmer l’embauche avec calme, et rester disponible les premiers jours.",
        "subject": "Bonne rentrée dans votre nouveau poste",
        "body": "{{hello}}\n\nVotre embauche est confirmée. Je vous souhaite un bon départ.\n\nLes premiers jours, je reste disponible si un horaire, un document ou une question pratique bloque. Répondez à ce courriel, ou écrivez-nous à {{info}}.\n\n{{recruiter_name}}",
    },
    {
        "key": "cand_reactivate",
        "side": "candidate",
        "stage": "inactif",
        "label": "9. Réactivation",
        "intent": "Rouvrir le contact sans culpabiliser et sans demander un mot-clé.",
        "subject": "Toujours ouvert à un échange ?",
        "body": "{{hello}}\n\nCela fait un moment que nous n’avons pas échangé. Des postes{{sector_bit}}{{city_bit}} sont ouverts.\n\nSi vous êtes de nouveau en recherche, répondez-moi. Sinon, vous pouvez ignorer ce message : je n’insisterai pas.\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_first_contact",
        "side": "employer",
        "stage": "nouveau",
        "label": "1. Premier contact",
        "intent": "Premier contact employeur — se présenter, une question sur le besoin. Ni slogan, ni honoraires, ni paiement.",
        "subject": "{{company_lead}}Recrutement",
        "body": "{{hello}}\n\nJe vous contacte{{about_company}}. Je travaille chez Talendus : nous aidons les entreprises du Québec, tous secteurs, à pourvoir tous les types de postes.\n\nSi un poste{{title_bit}} reste ouvert, j’aimerais en comprendre le contexte. Un mot sur le métier et le besoin suffit pour commencer.\n\nVous pouvez aussi m’écrire le besoin ici :\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_followup",
        "side": "employer",
        "stage": "contacte",
        "label": "2. Relance",
        "intent": "Relance employeur — une question, sans argumentaire commercial.",
        "subject": "{{company_lead}}Le besoin est-il toujours d’actualité ?",
        "body": "{{hello}}\n\nJe me permets de revenir{{about_company}}. Avez-vous encore un poste{{sector_bit}} à pourvoir ?\n\nS’il est toujours d’actualité, un retour avec le métier et le contexte me suffit pour reprendre le fil.\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_discovery",
        "side": "employer",
        "stage": "qualifie",
        "label": "3. Appel de cadrage",
        "intent": "Demander un appel de cadrage. On décide ensuite ensemble, sans parler d’argent.",
        "subject": "{{company_lead}}Un appel pour cadrer le poste",
        "body": "{{hello}}\n\nPour bien cerner le besoin {{chez_company}}, je vous propose un appel de vingt minutes : le poste, l’équipe, et ce qui a déjà été tenté.\n\nIndiquez-moi deux créneaux. Ensuite, on verra ensemble s’il est pertinent d’ouvrir une recherche.\n\nVous pouvez aussi me joindre au {{phone}}.\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_mandate",
        "side": "employer",
        "stage": "proposition",
        "label": "4. Mandat à signer",
        "intent": "Transmettre le mandat à lire. Les conditions restent dans le document, pas dans le courriel.",
        "subject": "{{company_lead}}Mandat de recrutement à votre lecture",
        "body": "{{hello}}\n\nÀ la suite de nos échanges{{about_company}}, je vous transmets le mandat de recrutement.\n\nPrenez le temps de le lire. Les conditions y sont écrites. Quand vous serez à l’aise, signez-le dans votre espace : la recherche commencera à ce moment.\n\nSi un point du document appelle une précision, répondez-moi directement.\n\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_search_start",
        "side": "employer",
        "stage": "proposition",
        "label": "5. Recherche lancée",
        "intent": "Confirmer que la recherche est en cours et ce que le client peut attendre.",
        "subject": "{{company_lead}}La recherche est en cours",
        "body": "{{hello}}\n\nLe mandat est signé {{chez_company}}. La recherche est en cours.\n\nJe reviens vers vous dès qu’un dossier mérite d’être présenté. En attendant, vous n’avez rien à préparer de votre côté.\n\nLe suivi reste disponible ici :\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_talent_ready",
        "side": "employer",
        "stage": "client",
        "label": "6. Profils à présenter",
        "intent": "Annoncer des candidatures et demander un créneau, sans enfler le propos.",
        "subject": "{{company_lead}}Des candidatures{{title_bit}} à vous présenter",
        "body": "{{hello}}\n\nNous avons des candidatures{{title_bit}} à vous présenter {{chez_company}}.\n\nDites-moi deux disponibilités, en visio ou sur place, et je m’organise.\n\nVous pouvez aussi confirmer ici :\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_invoice",
        "side": "employer",
        "stage": "client",
        "label": "7. Facture",
        "intent": "Transmettre la facture après embauche, selon le mandat. Sans rappeler un pourcentage.",
        "subject": "{{company_lead}}Facture selon le mandat signé",
        "body": "{{hello}}\n\nL’embauche est confirmée {{chez_company}}. La facture est établie selon le mandat signé.\n\nLe règlement se fait par virement ou par chèque, aux conditions prévues. Pour une question sur le montant ou l’échéance, répondez à ce courriel.\n\nVous pouvez aussi la consulter ici :\n{{employer_link}}\n\n{{recruiter_name}}",
    },
    {
        "key": "emp_reactivate",
        "side": "employer",
        "stage": "inactif",
        "label": "8. Réactivation",
        "intent": "Reprendre contact sans urgence artificielle.",
        "subject": "{{company_lead}}Un besoin de recrutement de nouveau ?",
        "body": "{{hello}}\n\nNous n’avons pas échangé depuis un moment. Si un poste {{title_or_poste}} est de nouveau à pourvoir {{chez_company}}, je peux reprendre une recherche.\n\nUn mot sur le métier et le besoin suffit. Si le besoin n’est plus là, ignorez simplement ce message.\n\n{{recruiter_name}}",
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


_GENERIC_PERSON_TOKENS = {
    "accueil",
    "administration",
    "bonjour",
    "contact",
    "direction",
    "equipe",
    "équipe",
    "humaine",
    "humaines",
    "info",
    "recrutement",
    "ressource",
    "ressources",
    "rh",
    "service",
}

_GENERIC_TITLES = {
    "recrutement",
    "ressource humaine",
    "ressources humaines",
    "rh",
    "service des ressources humaines",
}


def is_generic_person_name(first: str = "", last: str = "") -> bool:
    tokens = [part.casefold() for part in re.split(r"[\s/,.-]+", f"{first} {last}") if part]
    if not tokens:
        return True
    return all(part in _GENERIC_PERSON_TOKENS for part in tokens)


def is_generic_job_title(title: str | None) -> bool:
    return (title or "").strip().casefold() in _GENERIC_TITLES


def person_name_parts(raw: str | None) -> tuple[str, str]:
    first, last = _split_name(raw)
    if is_generic_person_name(first, last):
        return "", ""
    return first, last


def sanitize_generic_person(row: Prospect) -> None:
    if is_generic_person_name(row.first_name or "", row.last_name or ""):
        row.first_name = ""
        row.last_name = ""


def display_name(row: Prospect) -> str:
    if not is_generic_person_name(row.first_name or "", row.last_name or ""):
        name = f"{row.first_name} {row.last_name}".strip()
        if name:
            return name
    return (row.company_name or "").strip() or row.email


def account_links_for(email: str | None, side: str | None, company_name: str | None = None) -> dict[str, str]:
    encoded = quote((email or "").strip().lower(), safe="")
    portal = EMPLOYEUR if (side or "") == "employer" else ESPACE
    role = "EMPLOYER" if (side or "") == "employer" else "CANDIDATE"
    register = f"{portal}#/register?email={encoded}&role={role}"
    company = (company_name or "").strip()
    if role == "EMPLOYER" and company:
        register += f"&company={quote(company, safe='')}"
    return {
        "portal_link": portal,
        "login_link": f"{portal}#/login?email={encoded}",
        "register_link": register,
        "candidate_link": ESPACE,
        "employer_link": EMPLOYEUR,
    }


def context_for(row: Prospect, actor: User | None = None) -> dict[str, str]:
    raw_first = (row.first_name or "").strip()
    raw_last = (row.last_name or "").strip()
    generic = is_generic_person_name(raw_first, raw_last)
    first = "" if generic else raw_first
    last = "" if generic else raw_last
    company = (row.company_name or "").strip()
    title = (row.title or "").strip()
    if (row.side or "") == "employer" and is_generic_job_title(title):
        title = ""
    city = (row.city or "").strip()
    sector = (row.sector or "").strip()
    recruiter = ""
    if actor:
        recruiter = f"{actor.first_name} {actor.last_name}".strip()
    hello = f"Bonjour {first}," if first else "Bonjour,"
    ctx = {
        "first_name": first,
        "last_name": last,
        "name": display_name(row),
        "hello": hello,
        "who_lead": f"{first}, " if first else "",
        "company": company or "votre entreprise",
        "company_lead": f"{company} — " if company else "",
        "about_company": f" au sujet de {company}" if company else "",
        "chez_company": f"chez {company}" if company else "chez vous",
        "title": title,
        "title_or_metier": title or "ouvert",
        "title_or_poste": title or "à pourvoir",
        "title_bit": f" ({title})" if title else "",
        "city": city,
        "city_bit": f" à {city}" if city else "",
        "sector": sector,
        "sector_or_industrie": sector or "ouverts",
        "sector_bit": f" en {sector.lower()}" if sector else "",
        "phone": PHONE,
        "info": INFO,
        "recruiter_name": recruiter or "L’équipe Talendus",
    }
    ctx.update(account_links_for(row.email, row.side, row.company_name))
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
    generic = is_generic_person_name(row.first_name or "", row.last_name or "")
    return {
        "id": row.id,
        "side": row.side,
        "stage": row.stage,
        "email": row.email,
        "first_name": "" if generic else row.first_name,
        "last_name": "" if generic else row.last_name,
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
        **account_links_for(row.email, row.side, row.company_name),
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
        row = upsert_prospect(
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
        if company:
            from app.services.employer_claim import attach_user_to_company_prospects

            attach_user_to_company_prospects(db, user, company)
        return row
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
            stage=None,
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


def _delivered_send_logs(db: Session, sends: list[ProspectSend]) -> dict[str, EmailLog]:
    ids = [row.email_log_id for row in sends if row.email_log_id]
    if not ids:
        return {}
    logs = list(db.scalars(select(EmailLog).where(EmailLog.id.in_(ids))).all())
    return {log.id: log for log in logs if email_actually_sent(log)}


def sent_keys_map(db: Session, prospect_ids: list[str]) -> dict[str, list[str]]:
    if not prospect_ids:
        return {}
    rows = list(db.scalars(select(ProspectSend).where(ProspectSend.prospect_id.in_(prospect_ids))).all())
    delivered = _delivered_send_logs(db, rows)
    out: dict[str, list[str]] = {pid: [] for pid in prospect_ids}
    for row in rows:
        if row.email_log_id and row.email_log_id in delivered:
            out.setdefault(row.prospect_id, []).append(row.template_key)
    return out


def _send_was_delivered(db: Session, row: ProspectSend | None) -> bool:
    if row is None or not row.email_log_id:
        return False
    return email_actually_sent(db.get(EmailLog, row.email_log_id))


CONTACT_STAGES = frozenset({"contacte"})


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
    sends = list(db.scalars(select(ProspectSend).where(ProspectSend.prospect_id == row.id)).all())
    delivered = _delivered_send_logs(db, sends)
    sent = {s.template_key for s in sends if s.email_log_id and s.email_log_id in delivered}
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


def _attachments_for(
    db: Session,
    row: Prospect,
    invoice_ids: list[str] | None,
    contract_ids: list[str] | None,
    actor: User | None = None,
) -> list[EmailAttachment]:
    from sqlalchemy.orm import joinedload, selectinload

    from app.services.contracts import ensure_talendus_signed
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
        contract = db.scalar(
            select(Contract)
            .options(selectinload(Contract.signatures), joinedload(Contract.company))
            .where(Contract.id == contract_id)
        )
        if not contract:
            raise AppError(404, "Contrat introuvable.", "NOT_FOUND")
        if row.company_id and contract.company_id and contract.company_id != row.company_id:
            raise AppError(403, "Ce contrat n’appartient pas à ce prospect.", "FORBIDDEN")
        if actor:
            ensure_talendus_signed(db, contract, actor)
            db.flush()
            db.refresh(contract)
        elif not contract.talendus_signed_at and not any(
            (getattr(sig, "party", "") or "").upper() == "TALENDUS" for sig in (contract.signatures or [])
        ):
            raise AppError(409, "Ce mandat n’est pas encore signé par Talendus.", "TALENDUS_NOT_SIGNED")
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
        "- Vous avez déjà un compte : connectez-vous ici :\n"
        f"{login}\n"
        "- Vous n’avez pas encore de compte : ce lien ouvre l’inscription, avec votre courriel déjà indiqué :\n"
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
                "- régler par virement ou par chèque, selon les conditions du mandat signé\n"
                f"- m’écrire, ou écrire à {ctx.get('info') or INFO}, si une ligne demande une précision\n\n"
                f"{howto}"
            )
        elif kind == "contract" or "mandat" in name.lower() or "contrat" in name.lower():
            blocks.append(
                f"{hook}\n\n"
                "À faire :\n"
                "- ouvrir le PDF et le lire en entier\n"
                "- le signer dans votre espace, sans l’imprimer\n"
                "- me le confirmer ensuite par retour de courriel\n\n"
                f"{howto}"
            )
        else:
            blocks.append(
                f"{hook}\n\n"
                "À faire : ouvrez le fichier, puis répondez-moi si une suite est demandée.\n\n"
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


def send_to_prospect(db: Session, actor: User, row: Prospect, req: SendRequest, *, sync: bool = True) -> dict:
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
    if existing and _send_was_delivered(db, existing) and not req.force:
        raise AppError(
            409,
            f"{display_name(row)} a déjà reçu ce message ({existing.subject}). Choisissez un autre modèle, ou forcez l’envoi.",
            "ALREADY_SENT",
        )
    if existing and not _send_was_delivered(db, existing):
        db.delete(existing)
        db.flush()
        existing = None
    attachments = _attachments_for(db, row, req.invoice_ids, req.contract_ids, actor)
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
    delivered = email_actually_sent(log)
    names = "|".join(att.filename for att in attachments)
    from app.services.audit import audit

    audit(
        db,
        "prospect.send",
        actor,
        "prospect",
        row.id,
        metadata={
            "template": key,
            "to": row.email,
            "subject": subject[:180],
            "email_status": log.status.value if log.status else "QUEUED",
            "delivered": delivered,
            "error": log.error or "",
        },
    )
    if not delivered:
        db.flush()
        return {
            "prospect_id": row.id,
            "to_email": row.email,
            "template_key": key,
            "subject": subject,
            "email_status": log.status.value if log.status else "QUEUED",
            "delivered": False,
            "email_error": delivery_error(log),
            "attachments": [att.filename for att in attachments],
        }
    if existing and req.force:
        existing.subject = subject[:180]
        existing.body = body
        existing.to_email = row.email
        existing.email_log_id = log.id
        existing.attachment_names = names
        existing.sent_by_id = actor.id
    else:
        db.add(
            ProspectSend(
                prospect_id=row.id,
                template_key=key,
                subject=subject[:180],
                body=body,
                to_email=row.email,
                email_log_id=log.id,
                attachment_names=names,
                sent_by_id=actor.id,
            )
        )
    row.last_contacted_at = utcnow()
    if row.stage in {"nouveau", "a-contacter"}:
        row.stage = "contacte"
    db.flush()
    return {
        "prospect_id": row.id,
        "to_email": row.email,
        "template_key": key,
        "subject": subject,
        "email_status": log.status.value if log.status else "QUEUED",
        "delivered": True,
        "attachments": [att.filename for att in attachments],
    }


def _prospect_sends_today(db: Session) -> int:
    start = utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    return int(db.scalar(select(func.count()).select_from(ProspectSend).where(ProspectSend.created_at >= start)) or 0)


def send_bulk(db: Session, actor: User, ids: list[str], req: SendRequest) -> dict:
    ids = list(dict.fromkeys((prospect_id or "").strip() for prospect_id in ids if (prospect_id or "").strip()))
    if not ids:
        raise AppError(400, "Choisissez au moins un prospect.", "VALIDATION_ERROR")
    if len(ids) > BULK_SEND_MAX:
        raise AppError(400, f"Maximum {BULK_SEND_MAX} destinataires à la fois.", "VALIDATION_ERROR")
    already = _prospect_sends_today(db)
    if already + len(ids) > BULK_SEND_DAILY_MAX:
        raise AppError(
            400,
            f"Plafond quotidien atteint ({BULK_SEND_DAILY_MAX} courriels prospects / jour). Réessayez demain ou envoyez un lot plus petit.",
            "BULK_DAILY_LIMIT",
        )
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
            result = send_to_prospect(db, actor, row, req, sync=True)
            if result.get("delivered"):
                sent.append(result)
            else:
                failed.append(
                    {
                        "id": row.id,
                        "email": row.email,
                        "reason": result.get("email_error") or "Le courriel n’a pas quitté le serveur.",
                    }
                )
        except AppError as exc:
            if exc.code == "ALREADY_SENT":
                skipped.append({"id": row.id, "email": row.email, "reason": exc.message})
            else:
                failed.append({"id": row.id, "email": row.email, "reason": exc.message})
    start_worker()
    return {"sent": sent, "skipped": skipped, "failed": failed}


def reconcile_undelivered_prospect_mails(db: Session) -> dict[str, int]:
    """Remet à « à contacter » les fiches dont le courriel n’est jamais vraiment parti."""
    fake_logs = mark_fake_sent_logs(db)
    sends = list(db.scalars(select(ProspectSend)).all())
    delivered_logs = _delivered_send_logs(db, sends)
    removed = 0
    for send in sends:
        if send.email_log_id and send.email_log_id in delivered_logs:
            continue
        db.delete(send)
        removed += 1
    db.flush()
    remaining = list(db.scalars(select(ProspectSend)).all())
    still_delivered = _delivered_send_logs(db, remaining)
    delivered_ids = {send.prospect_id for send in remaining if send.email_log_id and send.email_log_id in still_delivered}
    latest_by_prospect: dict[str, ProspectSend] = {}
    for send in remaining:
        if not send.email_log_id or send.email_log_id not in still_delivered:
            continue
        current = latest_by_prospect.get(send.prospect_id)
        if current is None or (send.created_at and (current.created_at is None or send.created_at > current.created_at)):
            latest_by_prospect[send.prospect_id] = send
    reset = 0
    cleared = 0
    for row in db.scalars(select(Prospect)).all():
        if row.id in delivered_ids:
            latest = latest_by_prospect.get(row.id)
            if latest and latest.created_at:
                row.last_contacted_at = latest.created_at
            continue
        changed = False
        if row.stage in CONTACT_STAGES:
            row.stage = "a-contacter"
            reset += 1
            changed = True
        if row.last_contacted_at is not None:
            row.last_contacted_at = None
            cleared += 1
            changed = True
        if changed:
            logger.info("prospect undelivered reset id=%s email=%s", row.id, row.email)
    return {"fake_logs": fake_logs, "removed_sends": removed, "reset_stages": reset, "cleared_contact": cleared}
