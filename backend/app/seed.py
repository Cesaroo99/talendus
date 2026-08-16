"""Données de démonstration alignées sur le site public et le back-office."""

from __future__ import annotations

import logging
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import SessionLocal, init_db
from app.models import (
    Application,
    ApplicationStatusHistory,
    Candidate,
    CandidateCertification,
    CandidateEducation,
    CandidateExperience,
    Company,
    CompanyMembership,
    Contract,
    Conversation,
    ConversationParticipant,
    InternalNote,
    Interview,
    Invoice,
    InvoiceLine,
    JobOffer,
    Message,
    Notification,
    Payment,
    Permission,
    Recruiter,
    RecruitmentMission,
    Resume,
    Role,
    SystemSetting,
    User,
    UserPreference,
    BlogPost,
)
from app.models.enums import (
    ApplicationStatus,
    BlogStatus,
    CompanyMemberRole,
    CompanyStatus,
    ContractStatus,
    InterviewStatus,
    InterviewType,
    InvoiceStatus,
    JobSearchStatus,
    JobStatus,
    MissionStatus,
    NotificationType,
    PaymentMethod,
    UserRole,
    utcnow,
)
from app.rbac import ADMINS, PERMISSIONS
from app.security import hash_password

logger = logging.getLogger("talendus.seed")
settings = get_settings()

STAFF = [
    ("lea.super@talendus.ca", "Léa", "Morin", UserRole.SUPER_ADMIN, "Super administratrice", "LM", None),
    ("sophie.admin@talendus.ca", "Sophie", "Tremblay", UserRole.ADMIN, "Directrice générale", "ST", None),
    ("marc.recruiter@talendus.ca", "Marc", "Gagnon", UserRole.RECRUITER, "Recruteur senior", "MG", "Métiers d'usine"),
    ("camille.recruiter@talendus.ca", "Camille", "Bouchard", UserRole.RECRUITER, "Recruteuse industrielle", "CB", "CNC / plasturgie"),
    ("nathalie.finance@talendus.ca", "Nathalie", "Roy", UserRole.FINANCE, "Contrôleure financière", "NR", None),
    ("alex.editeur@talendus.ca", "Alexandre", "Fortin", UserRole.EDITOR, "Éditeur de contenu", "AF", None),
]

COMPANIES = [
    ("Métalco", "Métallurgie", "Drummondville", "Jean Rivest", "j.rivest@metalco.ca", "819 555-2001", 180, "metalco.example", CompanyStatus.ACTIVE),
    ("LogiCentre Laval", "Entrepôt", "Laval", "Amélie Fortin", "a.fortin@logicentre.ca", "450 555-2002", 95, "logicentre.example", CompanyStatus.ACTIVE),
    ("Alimor", "Transformation alimentaire", "Longueuil", "Maude Lavoie", "m.lavoie@alimor.ca", "450 555-2003", 240, "alimor.example", CompanyStatus.ACTIVE),
    ("Plastika", "Plasturgie", "Saint-Jérôme", "Benoit Gauthier", "b.gauthier@plastika.ca", "450 555-2004", 70, "plastika.example", CompanyStatus.ACTIVE),
    ("TransQuébec", "Transport", "Anjou", "David Chen", "d.chen@transquebec.ca", "514 555-2005", 130, "transquebec.example", CompanyStatus.ACTIVE),
    ("Usine Nordique", "Manufacturier", "Québec", "Sylvie Paquet", "s.paquet@nordique.ca", "418 555-2006", 310, "nordique.example", CompanyStatus.ACTIVE),
    ("Forge Mauricie", "Métallurgie", "Trois-Rivières", "Luc Tremblay", "l.tremblay@forgemauricie.ca", "819 555-2007", 55, "forge.example", CompanyStatus.PROSPECT),
    ("Distro Plus", "Distribution", "Boucherville", "Cathy Nguyen", "c.nguyen@distroplus.ca", "450 555-2008", 88, "distroplus.example", CompanyStatus.ACTIVE),
]

JOBS = [
    ("cariste", "Cariste", "LogiCentre Laval", "Laval", "Entrepôt", "Permanent", 22, 26, "22 à 26 $/h", "Permis chariot, WMS", "1 an", "Quart de jour", JobStatus.PUBLISHED),
    ("operateur-production", "Opérateur de production", "Alimor", "Longueuil", "Production", "Permanent", 20, 24, "20 à 24 $/h", "Procédures, équipe", "Expérience d'usine", "Quarts rotatifs", JobStatus.PUBLISHED),
    ("soudeur", "Soudeur-monteur", "Métalco", "Drummondville", "Métallurgie", "Permanent", 28, 34, "28 à 34 $/h", "MIG/TIG, plans", "3 ans", "Quart de jour", JobStatus.PUBLISHED),
    ("machiniste-cnc", "Machiniste CNC", "Plastika", "Saint-Jérôme", "Manufacturier", "Permanent", 30, 38, "30 à 38 $/h", "Set-up, dessins", "3 ans", "Quart de jour", JobStatus.PUBLISHED),
    ("electromecanicien", "Électromécanicien", "Usine Nordique", "Montréal", "Maintenance", "Permanent", 32, 40, "32 à 40 $/h", "Hydraulique, électricité", "5 ans", "Quarts rotatifs", JobStatus.PUBLISHED),
    ("mecanicien-industriel", "Mécanicien industriel", "Forge Mauricie", "Sherbrooke", "Maintenance", "Permanent", 30, 36, "30 à 36 $/h", "Préventif, convoyeurs", "3 ans", "Quart de jour", JobStatus.DRAFT),
    ("journalier-usine", "Journalier d'usine", "Distro Plus", "Boucherville", "Production", "Permanent", 18, 21, "18 à 21 $/h", "Manutention", "Aucune", "Quart de soir", JobStatus.PUBLISHED),
    ("superviseur-production", "Superviseur de production", "Alimor", "Trois-Rivières", "Supervision", "Permanent", 70000, 85000, "70 000 à 85 000 $", "Lean, KPI", "5 ans", "Quart de jour", JobStatus.ARCHIVED),
    ("coordonnateur-logistique", "Coordonnateur logistique", "TransQuébec", "Anjou", "Logistique", "Permanent", 55000, 68000, "55 000 à 68 000 $", "WMS, anglais", "3 ans", "Quart de jour", JobStatus.PUBLISHED),
    ("directeur-usine", "Directeur d'usine", "Usine Nordique", "Québec", "Cadres", "Permanent", 120000, 150000, "120 000 à 150 000 $", "P&L, Lean", "10 ans", "Quart de jour", JobStatus.PAUSED),
]

CANDIDATES = [
    ("karine.lavoie@email.ca", "Karine", "Lavoie", "Cariste", "Laval", "Entrepôt", 6, "Chariot élévateur classe I-IV, WMS, SST"),
    ("hugo.belanger@email.ca", "Hugo", "Bélanger", "Opérateur de production", "Longueuil", "Production", 4, "Ligne d'assemblage, Contrôle qualité, 5S"),
    ("nadia.cote@email.ca", "Nadia", "Côté", "Soudeuse-monteuse", "Drummondville", "Métallurgie", 8, "MIG, TIG, Lecture de plans"),
]


def seed_rbac(db: Session) -> None:
    if db.scalar(select(Role).limit(1)):
        return
    perms: dict[str, Permission] = {}
    for code in PERMISSIONS:
        perm = Permission(code=code, name=code.replace(":", " ").title())
        db.add(perm)
        perms[code] = perm
    db.flush()
    labels = {
        UserRole.CANDIDATE: "Candidat",
        UserRole.EMPLOYER: "Employeur",
        UserRole.RECRUITER: "Recruteur",
        UserRole.ADMIN: "Administrateur",
        UserRole.SUPER_ADMIN: "Super administrateur",
        UserRole.FINANCE: "Finance",
        UserRole.EDITOR: "Éditeur",
    }
    for role_enum, label in labels.items():
        role = Role(code=role_enum.value, name=label)
        for perm_code, allowed in PERMISSIONS.items():
            if role_enum in ADMINS or role_enum in allowed:
                role.permissions.append(perms[perm_code])
        db.add(role)


def seed_blog_defaults(db: Session) -> None:
    if db.scalar(select(BlogPost).limit(1)):
        return
    editor = db.scalar(select(User).where(User.email == "alex.editeur@talendus.ca"))
    now = utcnow()
    author_id = editor.id if editor else None
    posts = [
        (
            "penurie-main-oeuvre-industrielle",
            "Pénurie de main-d'œuvre industrielle : ce que les usines peuvent encore faire",
            "La rareté des métiers n'est pas une fatalité. Quart, salaire réel et accueil 30/60/90 restent les leviers qui tiennent.",
            "Les usines québécoises ne manquent pas d'offres d'emploi : elles manquent de profils qui tiennent un quart. "
            "Un portail généraliste attire du volume ; il n'évalue pas la SST, le rythme de ligne ni le fit d'horaire.\n\n"
            "Les employeurs qui s'en sortent clarifient le salaire réel, le quart et l'accueil dès le brief. "
            "Talendus approche aussi des candidats passifs — déjà en poste — plutôt que de recycler les mêmes CV.",
            "Marché de l'emploi",
            "pénurie de main-d'œuvre, recrutement industriel, métiers spécialisés",
            "/assets/img/all-images/industry/usine-equipe.jpg",
            "Pénurie de main-d'œuvre industrielle au Québec | Talendus",
            "Comment les usines québécoises attirent encore des métiers spécialisés malgré la pénurie : quart, salaire réel et recrutement ciblé.",
        ),
        (
            "conseils-cv-usine",
            "CV d'usine : ce que les contremaîtres regardent vraiment",
            "Cartes de compétences, quarts tenus et machines utilisées pèsent plus qu'un paragraphe d'objectifs.",
            "Un CV industriel utile indique les machines, les quarts, les cartes SST et la durée en poste. "
            "Les objectifs génériques n'aident pas un superviseur pressé.\n\n"
            "Si vous cherchez un poste en production, maintenance ou entrepôt au Québec, déposez un dossier clair : "
            "Talendus le présente seulement aux employeurs dont l'horaire et le salaire correspondent.",
            "Conseils candidats",
            "CV, recherche d'emploi, entretiens d'embauche",
            "/assets/img/all-images/industry/cnc-machiniste.jpg",
            "CV et recherche d'emploi en usine au Québec | Talendus",
            "Conseils concrets pour un CV industriel : compétences, quarts, cartes SST. Destiné aux candidats d'usine au Québec.",
        ),
        (
            "salaires-industrie-quebec",
            "Salaires dans l'industrie au Québec : ce qu'il faut afficher pour recruter",
            "Un taux horaire flou ou trop bas par rapport au quart fait fuir les métiers avant même l'entrevue.",
            "En production, maintenance et entrepôt, les candidats comparent le salaire réel — primes de quart comprises — pas seulement l'affichage d'une offre.\n\n"
            "Avant d'ouvrir un mandat, Talendus recadre la fourchette avec ce que le marché industriel tient vraiment dans la région. "
            "Mieux vaut un brief honnête qu'une cascade d'entrevues perdues.",
            "Conseils employeurs",
            "salaires, industrie, recrutement manufacturier",
            "/assets/img/all-images/industry/soudeur-atelier.jpg",
            "Salaires dans l'industrie au Québec | Talendus",
            "Comment afficher une rémunération industrielle crédible au Québec pour attirer opérateurs, métiers et superviseurs.",
        ),
        (
            "retention-employes-usine",
            "Rétention des employés en usine : le 30/60/90 jours qui change la donne",
            "Le roulement se joue souvent après l'embauche, pas à l'offre. L'accueil de quart fait plus que le panneau RH.",
            "Un opérateur qui part à 45 jours a rarement « mal choisi le métier ». Il a souvent mal vécu le premier mois : horaire réel, SST, contremaître, formation.\n\n"
            "Les usines qui retiennent formalisent un suivi 30/60/90 jours. Sur les mandats permanents, Talendus l'inclut : ce n'est pas une option cosmétique.",
            "Gestion des talents",
            "rétention des employés, gestion des talents, roulement",
            "/assets/img/all-images/industry/usine-equipe.jpg",
            "Rétention des employés en usine au Québec | Talendus",
            "Accueil 30/60/90 jours, quart et SST : leviers concrets pour réduire le roulement en recrutement manufacturier.",
        ),
        (
            "entretiens-embauche-industriel",
            "Entretiens d'embauche en usine : évaluer le savoir-faire, pas le discours",
            "Une entrevue de bureau ne dit pas si quelqu'un tient un quart. Mises en situation et cartes de compétences pèsent davantage.",
            "Demander « parlez-moi de vous » à un soudeur ou un électromécanicien perd 20 minutes. Mieux : lecture de plan, exemple de dépannage, quarts déjà tenus.\n\n"
            "Talendus prépare ces entrevues avec l'employeur pour que le contremaître ne découvre pas l'écart en fin de processus.",
            "Conseils employeurs",
            "entretiens d'embauche, recrutement de travailleurs spécialisés",
            "/assets/img/all-images/industry/maintenance-tech.jpg",
            "Entretiens d'embauche industriels au Québec | Talendus",
            "Comment structurer une entrevue d'usine : savoir-faire, SST et fit de quart, sans questions RH génériques.",
        ),
    ]
    for slug, title, excerpt, body, category, tags, cover, seo_title, seo_description in posts:
        db.add(
            BlogPost(
                slug=slug,
                lang="fr",
                title=title,
                excerpt=excerpt,
                body=body,
                category=category,
                tags=tags,
                author_name="Alexandre Fortin",
                cover_image=cover,
                seo_title=seo_title,
                seo_description=seo_description,
                status=BlogStatus.PUBLISHED,
                published_at=now,
                created_by=author_id,
            )
        )


def seed_if_empty() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.scalar(select(User).limit(1)):
            seed_rbac(db)
            seed_blog_defaults(db)
            db.commit()
            return
        _seed(db)
        db.commit()
        logger.info("Base Talendus initialisée (seed).")
    except Exception:
        db.rollback()
        logger.exception("Échec du seed")
        raise
    finally:
        db.close()


def _seed(db: Session) -> None:
    seed_rbac(db)
    password = hash_password(settings.seed_password)
    users: dict[str, User] = {}
    for email, first, last, role, title, initials, specialty in STAFF:
        user = User(
            email=email,
            password_hash=password,
            first_name=first,
            last_name=last,
            role=role,
            title=title,
            is_active=True,
            is_email_verified=True,
            email_verified_at=utcnow(),
        )
        db.add(user)
        db.flush()
        db.add(UserPreference(user_id=user.id, locale="fr-CA"))
        if role == UserRole.RECRUITER:
            db.add(Recruiter(user_id=user.id, initials=initials, specialty=specialty))
        users[email] = user

    marc = users["marc.recruiter@talendus.ca"]
    companies: dict[str, Company] = {}
    for name, sector, city, contact, email, phone, employees, website, status in COMPANIES:
        company = Company(
            name=name,
            legal_name=f"{name} inc.",
            trade_name=name,
            description=f"Entreprise {sector.lower()} basée à {city}.",
            sector=sector,
            city=city,
            address="100, rue Industrielle",
            province="Québec",
            country="Canada",
            contact_name=contact,
            email=email,
            phone=phone,
            employees=employees,
            size_label="PME" if employees < 200 else "Grande entreprise",
            website=website,
            status=status,
            assigned_recruiter_id=marc.id,
        )
        db.add(company)
        db.flush()
        companies[name] = company
        employer = User(
            email=email,
            password_hash=password,
            first_name=contact.split(" ", 1)[0],
            last_name=contact.split(" ", 1)[-1],
            role=UserRole.EMPLOYER,
            title="Directrice / directeur des opérations" if name != "Métalco" else "Directeur d'usine",
            is_active=True,
            is_email_verified=True,
        )
        db.add(employer)
        db.flush()
        db.add(UserPreference(user_id=employer.id, locale="fr-CA"))
        company.owner_user_id = employer.id
        db.add(CompanyMembership(company_id=company.id, user_id=employer.id, member_role=CompanyMemberRole.OWNER))
        users[email] = employer

    db.add(
        Contract(
            company_id=companies["Métalco"].id,
            type="Retainer + succès",
            start_date="2026-01-01",
            end_date="2026-12-31",
            commission_percent=18,
            terms="18 % du salaire annuel, garantie 90 jours.",
            status=ContractStatus.ACTIVE,
            document_name="contrat-metalco-2026.pdf",
        )
    )

    jobs: dict[str, JobOffer] = {}
    now = utcnow()
    for slug, title, company_name, city, sector, contract, smin, smax, display, skills, exp, shift, status in JOBS:
        job = JobOffer(
            company_id=companies[company_name].id,
            recruiter_id=marc.id,
            slug=slug,
            title=title,
            description=f"Poste de {title} à {city}. Recrutement industriel Talendus.",
            location=city,
            sector=sector,
            contract_type=contract,
            salary_min=smin,
            salary_max=smax,
            salary_display=display,
            skills=skills,
            experience_level=exp,
            shift=shift,
            status=status,
            published_at=now - timedelta(days=10) if status != JobStatus.DRAFT else None,
        )
        db.add(job)
        db.flush()
        jobs[slug] = job

    mission = RecruitmentMission(
        company_id=companies["LogiCentre Laval"].id,
        job_id=jobs["cariste"].id,
        recruiter_id=marc.id,
        title="Caristes — pic saisonnier",
        seats=8,
        status=MissionStatus.IN_PROGRESS,
        value=72000,
        commission=11520,
        progress=62,
        start_date="2026-07-15",
        due_date="2026-09-01",
    )
    db.add(mission)
    db.flush()
    mission.linked_jobs.append(jobs["cariste"])

    candidates: dict[str, Candidate] = {}
    applications: dict[str, Application] = {}
    for email, first, last, title, city, sector, years, skills in CANDIDATES:
        user = User(
            email=email,
            password_hash=password,
            first_name=first,
            last_name=last,
            role=UserRole.CANDIDATE,
            is_active=True,
            is_email_verified=True,
        )
        db.add(user)
        db.flush()
        db.add(UserPreference(user_id=user.id, locale="fr-CA", notify_match=True))
        cand = Candidate(
            user_id=user.id,
            title=title,
            city=city,
            sector=sector,
            years_experience=years,
            skills=skills,
            education_level="DEP",
            job_search_status=JobSearchStatus.ACTIVE,
            work_preferences="Quart de jour, équipe d'usine",
            availability="Immédiate",
            assigned_recruiter_id=marc.id,
        )
        db.add(cand)
        db.flush()
        candidates[email] = cand
        db.add(CandidateExperience(candidate_id=cand.id, company="Usine partenaire", role=title, years="2021 — 2026"))
        db.add(CandidateEducation(candidate_id=cand.id, school="Formation professionnelle", diploma="DEP", year="2018"))
        db.add(CandidateCertification(candidate_id=cand.id, name="SST", issuer="CNESST", year="2024"))
        resume = Resume(
            candidate_id=cand.id,
            original_name=f"CV_{first}_{last}.pdf",
            stored_name="seed-placeholder.pdf",
            storage_url="resumes/seed-placeholder.pdf",
            mime_type="application/pdf",
            size_bytes=1024,
            is_primary=True,
        )
        db.add(resume)
        db.flush()
        slug = {
            "Cariste": "cariste",
            "Opérateur de production": "operateur-production",
            "Soudeuse-monteuse": "soudeur",
        }[title]
        application = Application(
            candidate_id=cand.id,
            job_id=jobs[slug].id,
            resume_id=resume.id,
            status=ApplicationStatus.UNDER_REVIEW,
            cover_note="Profil issu de la banque Talendus.",
            source="seed",
            staff_notes="Note interne seed — ne jamais exposer au candidat.",
            match_score=72,
        )
        db.add(application)
        db.flush()
        applications[email] = application
        db.add(
            ApplicationStatusHistory(
                application_id=application.id,
                old_status=None,
                new_status=ApplicationStatus.SUBMITTED.value,
                actor_id=user.id,
            )
        )
        db.add(
            ApplicationStatusHistory(
                application_id=application.id,
                old_status=ApplicationStatus.SUBMITTED.value,
                new_status=ApplicationStatus.UNDER_REVIEW.value,
                actor_id=marc.id,
                comment="Qualification initiale.",
            )
        )
        db.add(
            InternalNote(
                entity_type="candidate",
                entity_id=cand.id,
                author_id=marc.id,
                text="Dossier seed — à qualifier selon le quart demandé.",
            )
        )

    karine = candidates["karine.lavoie@email.ca"]
    hugo = candidates["hugo.belanger@email.ca"]
    db.add(
        Interview(
            candidate_id=hugo.id,
            application_id=applications["hugo.belanger@email.ca"].id,
            job_id=jobs["operateur-production"].id,
            company_id=companies["Alimor"].id,
            recruiter_id=marc.id,
            scheduled_at=utcnow() + timedelta(days=2),
            duration_minutes=30,
            location="Visio",
            type=InterviewType.TALENDUS,
            status=InterviewStatus.SCHEDULED,
        )
    )
    invoice = Invoice(
        number="F-2026-014",
        company_id=companies["Alimor"].id,
        mission_id=mission.id,
        amount=13260,
        amount_ht=11540,
        tax_amount=1720,
        amount_total=13260,
        tax_rate_bp=14975,
        currency="CAD",
        status=InvoiceStatus.PAID,
        issued_at="2026-07-02",
        due_date="2026-08-01",
        paid_at="2026-07-28",
    )
    db.add(invoice)
    db.flush()
    db.add(
        InvoiceLine(
            invoice_id=invoice.id,
            description="Honoraires de recrutement — opérateur de production",
            quantity=1,
            unit_price=11540,
            amount=11540,
            reference="MISS-ALIMOR",
            mission_id=mission.id,
        )
    )
    db.add(
        Payment(
            invoice_id=invoice.id,
            amount=13260,
            method=PaymentMethod.TRANSFER,
            paid_at="2026-07-28",
            reference="VIR-ALIMOR",
            recorded_by=users["nathalie.finance@talendus.ca"].id,
        )
    )
    pending = Invoice(
        number="F-2026-018",
        company_id=companies["LogiCentre Laval"].id,
        mission_id=mission.id,
        amount=8640,
        amount_ht=7520,
        tax_amount=1120,
        amount_total=8640,
        tax_rate_bp=14975,
        currency="CAD",
        status=InvoiceStatus.PENDING,
        issued_at="2026-07-28",
        due_date="2026-08-27",
    )
    db.add(pending)
    db.flush()
    db.add(
        InvoiceLine(
            invoice_id=pending.id,
            description="Acompte mission caristes — pic saisonnier",
            quantity=1,
            unit_price=7520,
            amount=7520,
            reference="MISS-LOGI",
            mission_id=mission.id,
            job_id=jobs["cariste"].id,
        )
    )
    conversation = Conversation(
        application_id=applications["karine.lavoie@email.ca"].id,
        subject="Suivi candidature cariste",
    )
    db.add(conversation)
    db.flush()
    db.add(ConversationParticipant(conversation_id=conversation.id, user_id=marc.id))
    db.add(ConversationParticipant(conversation_id=conversation.id, user_id=karine.user_id))
    db.add(
        Message(
            conversation_id=conversation.id,
            sender_id=marc.id,
            recipient_id=karine.user_id,
            application_id=applications["karine.lavoie@email.ca"].id,
            body="Bonjour Karine, merci pour votre dossier cariste. On se parle sous peu pour le quart de jour à Laval.",
        )
    )
    db.add(
        Notification(
            user_id=karine.user_id,
            type=NotificationType.MESSAGE,
            title="Nouveau message",
            message="Marc Gagnon vous a écrit au sujet du poste de cariste.",
            href="/espace.html#/messages",
        )
    )
    db.add(
        Notification(
            user_id=marc.id,
            type=NotificationType.APPLICATION_NEW,
            title="Nouvelle candidature",
            message="Karine Lavoie a postulé pour Cariste.",
            href="/admin/#/jobs",
        )
    )
    settings_rows = [
        ("platform.locale", "fr-CA", "Langue par défaut"),
        ("billing.currency", "CAD", "Devise de facturation"),
        ("billing.tax_rate_bp", "14975", "Taux de taxes (points de base)"),
        ("jobs.auto_expire_days", "60", "Expiration automatique des offres (jours)"),
        ("storage.backend", "local", "Backend de stockage des fichiers"),
    ]
    for key, value, label in settings_rows:
        db.add(SystemSetting(key=key, value=value, label=label, updated_by=users["sophie.admin@talendus.ca"].id))
    seed_blog_defaults(db)


if __name__ == "__main__":
    seed_if_empty()
    print("Seed Talendus terminé.")
