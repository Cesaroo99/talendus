import json
import logging

from sqlalchemy.orm import Session

from app.models import AuditLog, User

logger = logging.getLogger("talendus.audit")

ACTION_LABELS = {
    "account.register": "Inscription d’un compte",
    "auth.login": "Connexion",
    "auth.logout": "Déconnexion",
    "auth.password_reset": "Réinitialisation du mot de passe",
    "auth.password_change": "Changement de mot de passe",
    "auth.session_revoke": "Révocation d’une session",
    "auth.session_revoke_all": "Révocation de toutes les sessions",
    "admin.user_create": "Création d’un accès interne",
    "admin.user_update": "Mise à jour d’un accès interne",
    "admin.role_change": "Changement de rôle",
    "admin.setting": "Réglage plateforme",
    "candidate.staff_create": "Création d’un dossier candidat",
    "candidate.staff_update": "Mise à jour d’un dossier candidat",
    "candidate.staff_resume_upload": "Dépôt de CV (équipe)",
    "candidate.profile_update": "Le candidat a mis à jour son profil",
    "candidate.resume_upload": "Dépôt de CV",
    "candidate.resume_delete": "Suppression de CV",
    "application.create": "Nouvelle candidature",
    "application.status": "Changement d’étape ATS",
    "application.staff_link": "Liaison candidat–offre",
    "application.client_feedback": "Retour employeur sur un dossier",
    "company.create": "Création d’une entreprise",
    "company.update": "Mise à jour d’une entreprise",
    "company.logo": "Logo entreprise",
    "company.member_invite": "Invitation d’un membre entreprise",
    "company.member_role": "Rôle membre entreprise",
    "company.member_remove": "Retrait d’un membre entreprise",
    "hiring_request.create": "Nouveau besoin de recrutement",
    "hiring_request.update": "Mise à jour d’un besoin",
    "hiring_request.feedback": "Retour entreprise sur un besoin",
    "hiring_request.convert_job": "Besoin converti en offre",
    "mission.create": "Création d’une mission",
    "job.create": "Création d’une offre",
    "job.update": "Mise à jour d’une offre",
    "job.duplicate": "Duplication d’une offre",
    "job.delete": "Suppression d’une offre",
    "job.save": "Offre enregistrée par un talent",
    "job.unsave": "Offre retirée des favoris",
    "interview.create": "Entretien planifié",
    "interview.update": "Entretien modifié",
    "interview.status": "Statut d’entretien",
    "contract.create": "Mandat préparé",
    "contract.update": "Mandat modifié",
    "contract.sign_talendus": "Signature Talendus d’un mandat",
    "contract.sign": "Signature client d’un mandat",
    "contract.send": "Mandat envoyé au client",
    "contract.remind": "Relance de mandat",
    "contract.open": "Mandat ouvert par le client",
    "invoice.create": "Facture créée",
    "invoice.update": "Facture mise à jour",
    "invoice.send": "Facture envoyée",
    "invoice.payment": "Paiement enregistré",
    "invoice.checkout": "Paiement en ligne amorcé",
    "invoice.paypal.checkout": "Paiement PayPal amorcé",
    "invoice.paypal.capture": "Paiement PayPal capturé",
    "invoice.refund": "Remboursement",
    "message.send": "Message envoyé",
    "note.create": "Note interne",
    "document.staff_upload": "Document déposé par l’équipe",
    "document.upload": "Document déposé",
    "document.delete": "Document supprimé",
    "user.update": "Profil utilisateur",
    "user.deactivate": "Désactivation d’un compte",
    "user.avatar": "Photo de profil",
    "user.preferences": "Préférences",
    "recruiter.invite": "Invitation recruteur",
    "prospect.create": "Prospect ajouté",
    "prospect.patch": "Fiche prospect mise à jour",
    "prospect.stage": "Statut prospect",
    "prospect.send": "Courriel prospect envoyé",
}


def action_label(action: str) -> str:
    if not action:
        return "Action"
    if action in ACTION_LABELS:
        return ACTION_LABELS[action]
    if action.startswith("hiring_request."):
        return "Besoin — " + action.split(".", 1)[1].replace("_", " ")
    return action.replace(".", " · ").replace("_", " ")


def serialize_audit(row: AuditLog, actor: User | None = None) -> dict:
    metadata = None
    if row.metadata_json:
        try:
            metadata = json.loads(row.metadata_json)
        except json.JSONDecodeError:
            metadata = row.metadata_json
    return {
        "id": row.id,
        "action": row.action,
        "action_label": action_label(row.action),
        "actor_id": row.actor_id,
        "actor_name": actor.full_name if actor else None,
        "actor_email": actor.email if actor else None,
        "actor_role": actor.role.value if actor and actor.role else None,
        "entity_type": row.entity_type,
        "entity_id": row.entity_id,
        "ip_address": row.ip_address,
        "old_value": row.old_value,
        "new_value": row.new_value,
        "metadata": metadata,
        "created_at": row.created_at.isoformat() if row.created_at else None,
    }


def _as_text(value) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, default=str)


def audit(
    db: Session,
    action: str,
    actor: User | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    ip: str | None = None,
    metadata: dict | None = None,
    old_value: str | dict | None = None,
    new_value: str | dict | None = None,
) -> None:
    row = AuditLog(
        actor_id=actor.id if actor else None,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        ip_address=ip,
        old_value=_as_text(old_value),
        new_value=_as_text(new_value),
        metadata_json=json.dumps(metadata, ensure_ascii=False) if metadata else None,
    )
    db.add(row)
    logger.info("audit %s actor=%s entity=%s:%s", action, getattr(actor, "id", None), entity_type, entity_id)
