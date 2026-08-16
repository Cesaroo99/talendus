from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.errors import AppError
from app.models import Application, Candidate, Company, Conversation, ConversationParticipant, JobOffer, Message, User
from app.models.enums import NotificationType, UserRole, utcnow
from app.rbac import ADMINS
from app.services.access import company_ids_for_employer
from app.services.audit import audit
from app.services.notifications import notify, portal_href


def _is_staff(user: User) -> bool:
    return user.role in {UserRole.RECRUITER, UserRole.FINANCE} | ADMINS


def _can_converse(db: Session, sender: User, recipient: User) -> bool:
    if sender.id == recipient.id:
        return False
    if not recipient.is_active:
        return False
    if _is_staff(sender) and recipient.role in {UserRole.CANDIDATE, UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN, UserRole.FINANCE}:
        return True
    if sender.role == UserRole.CANDIDATE and _is_staff(recipient):
        return True
    if sender.role == UserRole.EMPLOYER and _is_staff(recipient):
        return True
    if sender.role == UserRole.EMPLOYER and recipient.role == UserRole.CANDIDATE:
        ids = company_ids_for_employer(db, sender)
        if not ids:
            return False
        return (
            db.scalar(
                select(Application.id)
                .join(JobOffer, Application.job_id == JobOffer.id)
                .join(Candidate, Application.candidate_id == Candidate.id)
                .where(JobOffer.company_id.in_(ids), Candidate.user_id == recipient.id)
            )
            is not None
        )
    if sender.role == UserRole.CANDIDATE and recipient.role == UserRole.EMPLOYER:
        return _can_converse(db, recipient, sender)
    return False


def _get_or_create_conversation(db: Session, user_a: str, user_b: str, application_id: str | None) -> Conversation:
    sub_a = select(ConversationParticipant.conversation_id).where(ConversationParticipant.user_id == user_a)
    shared_id = db.scalar(
        select(ConversationParticipant.conversation_id).where(
            ConversationParticipant.user_id == user_b,
            ConversationParticipant.conversation_id.in_(sub_a),
        )
    )
    if shared_id:
        conv = db.get(Conversation, shared_id)
        if application_id and conv and not conv.application_id:
            conv.application_id = application_id
        return conv
    conv = Conversation(application_id=application_id)
    db.add(conv)
    db.flush()
    db.add(ConversationParticipant(conversation_id=conv.id, user_id=user_a))
    db.add(ConversationParticipant(conversation_id=conv.id, user_id=user_b))
    return conv


def send_message(db: Session, sender: User, recipient_id: str, body: str, application_id: str | None, ip: str | None) -> Message:
    text = (body or "").strip()
    if not text or len(text) > 4000:
        raise AppError(400, "Le message doit contenir entre 1 et 4000 caractères.", "VALIDATION_ERROR")
    recipient = db.get(User, recipient_id)
    if not recipient:
        raise AppError(404, "Destinataire introuvable.", "USER_NOT_FOUND")
    if not _can_converse(db, sender, recipient):
        raise AppError(403, "Vous ne pouvez pas écrire à cette personne.", "FORBIDDEN")
    if application_id:
        application = db.get(Application, application_id)
        if not application:
            raise AppError(404, "Candidature introuvable.", "APPLICATION_NOT_FOUND")
    conversation = _get_or_create_conversation(db, sender.id, recipient.id, application_id)
    row = Message(
        conversation_id=conversation.id,
        sender_id=sender.id,
        recipient_id=recipient.id,
        application_id=application_id,
        body=text,
    )
    db.add(row)
    notify(
        db,
        recipient,
        NotificationType.MESSAGE,
        "Nouveau message",
        f"{sender.full_name} vous a écrit.",
        href=portal_href(recipient, "messages"),
    )
    audit(db, "message.send", sender, "message", None, ip, {"to": recipient.id})
    db.commit()
    db.refresh(row)
    return row


def list_threads(db: Session, user: User) -> list[dict]:
    rows = list(
        db.scalars(
            select(Message)
            .options(joinedload(Message.sender), joinedload(Message.recipient))
            .where(or_(Message.sender_id == user.id, Message.recipient_id == user.id))
            .order_by(Message.created_at.desc())
        ).unique().all()
    )
    threads: dict[str, dict] = {}
    for row in rows:
        other_id = row.recipient_id if row.sender_id == user.id else row.sender_id
        if other_id in threads:
            if row.recipient_id == user.id and not row.is_read:
                threads[other_id]["unread"] += 1
            continue
        other = row.recipient if row.sender_id == user.id else row.sender
        threads[other_id] = {
            "user_id": other_id,
            "first_name": other.first_name if other else "",
            "last_name": other.last_name if other else "",
            "email": other.email if other else "",
            "role": other.role.value if other else "",
            "last_message": row.body,
            "last_at": row.created_at.isoformat() if row.created_at else None,
            "unread": 1 if (row.recipient_id == user.id and not row.is_read) else 0,
        }
    return list(threads.values())


def list_conversation(db: Session, user: User, other_id: str) -> list[Message]:
    other = db.get(User, other_id)
    if not other:
        raise AppError(404, "Destinataire introuvable.", "USER_NOT_FOUND")
    if not _can_converse(db, user, other) and not _has_history(db, user.id, other_id):
        raise AppError(403, "Vous n'avez pas accès à cette conversation.", "FORBIDDEN")
    rows = list(
        db.scalars(
            select(Message)
            .options(joinedload(Message.sender), joinedload(Message.recipient))
            .where(
                or_(
                    (Message.sender_id == user.id) & (Message.recipient_id == other_id),
                    (Message.sender_id == other_id) & (Message.recipient_id == user.id),
                )
            )
            .order_by(Message.created_at.asc())
        ).unique().all()
    )
    changed = False
    for row in rows:
        if row.recipient_id == user.id and not row.is_read:
            row.is_read = True
            row.read_at = utcnow()
            changed = True
    if changed:
        db.commit()
    return rows


def _has_history(db: Session, a: str, b: str) -> bool:
    return (
        db.scalar(
            select(Message.id).where(
                or_(
                    (Message.sender_id == a) & (Message.recipient_id == b),
                    (Message.sender_id == b) & (Message.recipient_id == a),
                )
            )
        )
        is not None
    )


def serialize_message(row: Message) -> dict:
    return {
        "id": row.id,
        "sender_id": row.sender_id,
        "recipient_id": row.recipient_id,
        "application_id": row.application_id,
        "body": row.body,
        "is_read": row.is_read,
        "read_at": row.read_at.isoformat() if row.read_at else None,
        "conversation_id": row.conversation_id,
        "created_at": row.created_at.isoformat() if row.created_at else None,
        "sender_name": row.sender.full_name if row.sender else None,
    }


def directory(db: Session, user: User) -> list[dict]:
    """Personnes auxquelles l'utilisateur peut écrire."""
    people: list[User] = []
    if user.role == UserRole.CANDIDATE:
        people = list(db.scalars(select(User).where(User.role.in_([UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN]), User.is_active.is_(True))).all())
        applied_owners = list(
            db.scalars(
                select(User)
                .join(Company, Company.owner_user_id == User.id)
                .join(JobOffer, JobOffer.company_id == Company.id)
                .join(Application, Application.job_id == JobOffer.id)
                .join(Candidate, Application.candidate_id == Candidate.id)
                .where(Candidate.user_id == user.id, User.is_active.is_(True))
            ).unique().all()
        )
        people = people + [p for p in applied_owners if p.id not in {x.id for x in people}]
    elif user.role == UserRole.EMPLOYER:
        people = list(db.scalars(select(User).where(User.role.in_([UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN]), User.is_active.is_(True))).all())
        ids = company_ids_for_employer(db, user)
        if ids:
            applicants = list(
                db.scalars(
                    select(User)
                    .join(Candidate, Candidate.user_id == User.id)
                    .join(Application, Application.candidate_id == Candidate.id)
                    .join(JobOffer, Application.job_id == JobOffer.id)
                    .where(JobOffer.company_id.in_(ids), User.is_active.is_(True))
                ).unique().all()
            )
            people = people + [p for p in applicants if p.id not in {x.id for x in people}]
    elif _is_staff(user):
        people = list(
            db.scalars(
                select(User).where(
                    User.is_active.is_(True),
                    User.role.in_([UserRole.CANDIDATE, UserRole.EMPLOYER, UserRole.RECRUITER, UserRole.ADMIN, UserRole.SUPER_ADMIN]),
                    User.id != user.id,
                )
            ).all()
        )
    return [
        {
            "id": p.id,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "email": p.email if _is_staff(user) else None,
            "role": p.role.value,
        }
        for p in people
    ]
