"""CRM prospects : deux pipelines, propositions personnalisées, anti-doublon, PJ."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Candidate, Company, Contract, Invoice, User
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
EMPLOYEUR = "https://talendus.ca/employeur.html"
INFO = "info@talendus.ca"
PHONE = "263 558 5225"

TEMPLATES: tuple[dict, ...] = (
    {
        "key": "cand_first_contact",
        "side": "candidate",
        "label": "Premier contact",
        "intent": "Présenter Talendus et l’inviter à nous confier sa recherche.",
        "subject": "{{first_name}}, Talendus peut vous placer — sans frais pour vous",
        "body": "{{first_name}},\n\nJe vous écris de la part de Talendus, cabinet de recrutement au Québec.\n\nNous travaillons avec des usines, entrepôts et ateliers qui cherchent des profils {{title_or_metier}}. Vous n’avez rien à payer : nos honoraires sont versés par l’employeur (16 %).\n\nSi une opportunité vous intéresse, répondez à ce courriel ou ouvrez votre espace :\n{{candidate_link}}\n\n{{recruiter_name}}\nTalendus · {{phone}}",
    },
    {
        "key": "cand_followup",
        "side": "candidate",
        "label": "Relance",
        "intent": "Relancer un profil qui n’a pas répondu.",
        "subject": "{{first_name}}, un mot rapide de Talendus",
        "body": "{{first_name}},\n\nJe reviens vers vous : nous avons toujours des mandats {{sector_or_industrie}} au Québec{{city_bit}}.\n\nDeux minutes suffisent pour me dire si vous êtes ouvert à échanger, ou pour déposer votre CV ici :\n{{candidate_link}}\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "cand_qualify",
        "side": "candidate",
        "label": "Qualification",
        "intent": "Obtenir disponibilité, quart et prétentions.",
        "subject": "{{first_name}}, quelques précisions pour vous proposer le bon poste",
        "body": "{{first_name}},\n\nPour vous proposer un poste qui tient la route, j’ai besoin de trois infos :\n- votre disponibilité\n- le quart accepté (jour, soir, rotatif)\n- votre fourchette salariale\n\nRépondez directement à ce courriel. Je reviens ensuite avec des mandats concrets.\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "cand_interview",
        "side": "candidate",
        "label": "Proposition d’entretien",
        "intent": "Proposer un appel de qualification.",
        "subject": "{{first_name}}, 20 minutes avec Talendus ?",
        "body": "{{first_name}},\n\nJe vous propose un court appel pour parler de votre parcours{{title_bit}} et des postes ouverts.\n\nRépondez avec deux créneaux qui vous conviennent, ou ouvrez votre espace pour confirmer :\n{{candidate_link}}\n\n{{recruiter_name}}\nTalendus · {{phone}}",
    },
    {
        "key": "cand_job_ready",
        "side": "candidate",
        "label": "Poste à pourvoir",
        "intent": "Annoncer qu’un mandat correspond au profil.",
        "subject": "{{first_name}}, un mandat {{title_or_metier}} peut vous correspondre",
        "body": "{{first_name}},\n\nNous avons un mandat {{title_or_metier}}{{city_bit}} qui correspond à votre profil. L’employeur passe par Talendus : vous n’avez pas à négocier les honoraires.\n\nSi vous êtes intéressé, répondez « oui » et je vous envoie le détail, ou ouvrez :\n{{candidate_link}}\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "cand_documents",
        "side": "candidate",
        "label": "Documents manquants",
        "intent": "Demander CV ou pièces pour avancer.",
        "subject": "{{first_name}}, il nous manque un document pour avancer",
        "body": "{{first_name}},\n\nPour présenter votre dossier aux employeurs, déposez votre CV à jour dans votre espace :\n{{candidate_link}}\n\nDès réception, on avance.\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "cand_offer",
        "side": "candidate",
        "label": "Offre / suite",
        "intent": "Encadrer une offre ou une décision.",
        "subject": "{{first_name}}, suite de votre dossier Talendus",
        "body": "{{first_name}},\n\nVotre dossier avance. Je reste votre interlocuteur pour les conditions, les horaires et la décision.\n\nRépondez à ce courriel si une question bloque, ou suivez l’étape dans votre espace :\n{{candidate_link}}\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "cand_reactivate",
        "side": "candidate",
        "label": "Réactivation",
        "intent": "Relancer un profil inactif.",
        "subject": "{{first_name}}, on a de nouveaux mandats",
        "body": "{{first_name}},\n\nCela fait un moment. Nous avons de nouveaux mandats {{sector_or_industrie}}. Si vous cherchez encore, répondez simplement « je suis ouvert ».\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "emp_first_contact",
        "side": "employer",
        "label": "Premier contact",
        "intent": "Présenter le cabinet et proposer un mandat.",
        "subject": "{{company}}, Talendus recrute vos profils d’usine — 16 %",
        "body": "{{hello}},\n\nJe vous contacte pour {{company}}. Talendus est un cabinet de recrutement au Québec : on préqualifie les talents d’usine, d’entrepôt et de maintenance, puis on vous présente seulement les profils qui tiennent.\n\nHonoraires : 16 % du salaire annuel, payés à l’embauche. Pas de logiciel à acheter, pas de mise de fonds.\n\nSi un poste vous manque{{title_bit}}, répondez à ce courriel ou déposez le besoin ici :\n{{employer_link}}\n\n{{recruiter_name}}\nTalendus · {{phone}} · {{info}}",
    },
    {
        "key": "emp_followup",
        "side": "employer",
        "label": "Relance",
        "intent": "Relancer un employeur silencieux.",
        "subject": "{{company}} — un mot de Talendus",
        "body": "{{hello}},\n\nJe reviens vers {{company}}. Nous recrutons encore des profils {{sector_or_industrie}} pour des usines d’ici.\n\nSi le besoin est toujours là, dites-moi le poste et le quart : je reviens avec un plan concret.\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "emp_discovery",
        "side": "employer",
        "label": "Appel découverte",
        "intent": "Obtenir un appel pour cadrer le besoin.",
        "subject": "{{company}}, 20 minutes pour cadrer votre besoin ?",
        "body": "{{hello}},\n\nPour {{company}}, je vous propose un court appel : poste, quart, salaire, et ce qui a déjà échoué en recrutement.\n\nRépondez avec deux créneaux. Ensuite on décide ensemble s’il vaut la peine d’ouvrir un mandat.\n\n{{recruiter_name}}\nTalendus · {{phone}}",
    },
    {
        "key": "emp_mandate",
        "side": "employer",
        "label": "Proposition de mandat",
        "intent": "Envoyer ou rappeler le mandat à signer.",
        "subject": "{{company}} — mandat Talendus à lire et signer",
        "body": "{{hello}},\n\nVoici la suite pour {{company}} : le mandat de recrutement Talendus (honoraires 16 %). Lisez-le, signez-le dans votre espace, et on lance la recherche.\n\n{{employer_link}}\n\nLe PDF peut être joint à ce courriel.\n\n{{recruiter_name}}\nTalendus · {{info}}",
    },
    {
        "key": "emp_talent_ready",
        "side": "employer",
        "label": "Talents à présenter",
        "intent": "Annoncer des profils préqualifiés.",
        "subject": "{{company}}, des profils {{title_or_poste}} sont prêts",
        "body": "{{hello}},\n\nNous avons préqualifié des profils {{title_or_poste}} pour {{company}}. Je peux vous les présenter dès que vous confirmez un créneau.\n\nRépondez à ce courriel, ou ouvrez votre espace :\n{{employer_link}}\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "emp_invoice",
        "side": "employer",
        "label": "Facture",
        "intent": "Transmettre une facture en pièce jointe.",
        "subject": "{{company}} — facture Talendus",
        "body": "{{hello}},\n\nVeuillez trouver la facture Talendus pour {{company}}. Paiement par virement ou chèque, selon les modalités du mandat.\n\nLe PDF est joint. Vous pouvez aussi la télécharger ici :\n{{employer_link}}\n\n{{recruiter_name}}\nTalendus · {{info}} · {{phone}}",
    },
    {
        "key": "emp_contract",
        "side": "employer",
        "label": "Contrat / mandat PDF",
        "intent": "Joindre le contrat ou le mandat.",
        "subject": "{{company}} — document Talendus",
        "body": "{{hello}},\n\nLe document Talendus pour {{company}} est joint à ce courriel (mandat ou contrat).\n\nPour signer électroniquement :\n{{employer_link}}\n\n{{recruiter_name}}\nTalendus",
    },
    {
        "key": "emp_reactivate",
        "side": "employer",
        "label": "Réactivation",
        "intent": "Relancer un ancien prospect employeur.",
        "subject": "{{company}}, Talendus recrute encore vos métiers",
        "body": "{{hello}},\n\nNous n’avons pas échangé depuis un moment. Si {{company}} a un poste {{title_or_poste}} à pourvoir, je peux relancer une recherche cette semaine.\n\n{{recruiter_name}}\nTalendus · {{phone}}",
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


def context_for(row: Prospect, actor: User | None = None) -> dict[str, str]:
    first = (row.first_name or "").strip() or (row.company_name or "bonjour")
    last = (row.last_name or "").strip()
    company = (row.company_name or "").strip() or "votre entreprise"
    title = (row.title or "").strip()
    city = (row.city or "").strip()
    sector = (row.sector or "").strip()
    recruiter = ""
    if actor:
        recruiter = f"{actor.first_name} {actor.last_name}".strip() or "L’équipe Talendus"
    return {
        "first_name": first,
        "last_name": last,
        "name": display_name(row),
        "hello": f"Bonjour {first}" if row.first_name else f"Bonjour {company}",
        "company": company,
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
        "candidate_link": ESPACE,
        "employer_link": EMPLOYEUR,
        "recruiter_name": recruiter or "L’équipe Talendus",
    }


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
        rows.append({k: item[k] for k in ("key", "side", "label", "intent")})
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
    return row


def patch_prospect(db: Session, prospect_id: str, data: dict) -> Prospect:
    row = get_prospect(db, prospect_id)
    if "stage" in data and data["stage"]:
        row.stage = _valid_stage(row.side, data["stage"])
    for key in ("first_name", "last_name", "phone", "company_name", "title", "city", "sector", "source_detail", "message"):
        if key in data and data[key] is not None:
            setattr(row, key, str(data[key])[:500] if key != "message" else str(data[key])[:5000])
    if "assigned_recruiter_id" in data:
        row.assigned_recruiter_id = data["assigned_recruiter_id"] or None
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
            )
        )
    return files


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
