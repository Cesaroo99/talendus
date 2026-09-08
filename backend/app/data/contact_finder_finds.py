"""Trouvailles Deep Contact — entreprises déjà au catalogue uniquement.

Chaque adresse a été vue sur une page publique indexée.
Aucune adresse générée à partir d’un prénom. Aucune nouvelle entreprise.
"""

from __future__ import annotations

from app.services.contact_finder import RESEARCHED_AT

# name -> list of public contact finds
DEEP_CONTACT_FINDS: dict[str, list[dict]] = {
    "Ville de Montréal": [
        {
            "email": "dotation@montreal.ca",
            "contact_name": "",
            "contact_title": "Dotation / acquisition de talents",
            "source_url": "https://montreal.ca/articles/offres-demploi-2944",
            "source_type": "website",
            "email_source": "page officielle Offres d’emploi",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 96,
            "search_depth": 1,
        }
    ],
    "SPVM": [
        {
            "email": "recrutement@spvm.qc.ca",
            "contact_name": "",
            "contact_title": "Recrutement",
            "source_url": "https://www.recrutementspvm.ca/faq/",
            "source_type": "careers",
            "email_source": "FAQ officielle recrutement SPVM",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 97,
            "search_depth": 1,
            "secondary_emails": ["embauche@spvm.qc.ca"],
        }
    ],
    "Sûreté du Québec": [
        {
            "email": "recrutement.policier@surete.qc.ca",
            "contact_name": "",
            "contact_title": "Recrutement policier",
            "source_url": "https://www.sq.gouv.qc.ca/wp-content/uploads/2016/11/depliant-recrutement.pdf",
            "source_type": "documents",
            "email_source": "dépliant recrutement public (PDF)",
            "discovered_at": "2016-11-01",
            "confidence_score": 72,
            "search_depth": 5,
        }
    ],
    "Urgences-santé": [
        {
            "email": "dotation@urgences-sante.qc.ca",
            "contact_name": "",
            "contact_title": "Dotation",
            "source_url": "https://www.urgences-sante.qc.ca/carrieres/",
            "source_type": "careers",
            "email_source": "page Carrières officielle",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 96,
            "search_depth": 1,
        }
    ],
    "Loto-Québec": [
        {
            "email": "support.rh@loto-quebec.com",
            "contact_name": "",
            "contact_title": "Soutien RH / carrières",
            "source_url": "https://carrieres.lotoquebec.com/fr/foire-aux-questions",
            "source_type": "careers",
            "email_source": "FAQ officielle Carrières Loto-Québec",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 92,
            "search_depth": 1,
        }
    ],
    "Héma-Québec": [
        {
            "email": "info@hema-quebec.qc.ca",
            "contact_name": "",
            "contact_title": "",
            "source_url": "https://www.hemaquebec.ca/nous-joindre/formulaire-contact",
            "source_type": "website",
            "email_source": "formulaire de contact officiel",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 90,
            "search_depth": 1,
        }
    ],
    "Polytechnique Montréal": [
        {
            "email": "brigitte.morneau@polymtl.ca",
            "contact_name": "Brigitte Morneau",
            "contact_title": "Directrice par intérim — Service talents et culture",
            "source_url": "https://www.polymtl.ca/bottin/unites/325",
            "source_type": "website",
            "email_source": "bottin officiel Service talents et culture",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 96,
            "search_depth": 1,
            "secondary_emails": ["stc@polymtl.ca"],
        }
    ],
    "ETS": [
        {
            "email": "rhumaines@etsmtl.ca",
            "contact_name": "",
            "contact_title": "Service des ressources humaines",
            "source_url": "https://www.etsmtl.ca/a-propos/travailler/emplois-gestion-soutien",
            "source_type": "careers",
            "email_source": "page Emplois gestion et soutien",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 94,
            "search_depth": 1,
            "secondary_emails": ["recrutement@etsmtl.ca"],
        }
    ],
    "INRS": [
        {
            "email": "isabelle.genest@inrs.ca",
            "contact_name": "Isabelle Genest",
            "contact_title": "Coordonnatrice à la dotation et au développement organisationnel",
            "source_url": "https://inrs.ca/linrs/directions-et-services/service-des-ressources-humaines/",
            "source_type": "website",
            "email_source": "page officielle Service des ressources humaines",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 97,
            "search_depth": 1,
            "secondary_emails": ["recrutement@inrs.ca"],
        }
    ],
    "CNESST": [
        {
            "email": "recrutement@cnesst.gouv.qc.ca",
            "contact_name": "",
            "contact_title": "Équipe du recrutement",
            "source_url": "https://emplois.carrieres.gouv.qc.ca/plateforme-emploi/poste/21114",
            "source_type": "government",
            "email_source": "affichage Emplois en ligne du Québec",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 90,
            "search_depth": 2,
        }
    ],
    "SAAQ": [
        {
            "email": "emplois@saaq.gouv.qc.ca",
            "contact_name": "",
            "contact_title": "Emplois / recrutement",
            "source_url": "https://emplois.carrieres.gouv.qc.ca/plateforme-emploi/poste/21515",
            "source_type": "government",
            "email_source": "affichage Emplois en ligne — emplois étudiants SAAQ",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 88,
            "search_depth": 2,
        }
    ],
    "Cirque du Soleil": [
        {
            "email": "talents@cirquedusoleil.com",
            "contact_name": "",
            "contact_title": "Talents / emploi",
            "source_url": "https://www.cirquedusoleil.com/faq/careers",
            "source_type": "careers",
            "email_source": "FAQ officielle Circus Careers",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 86,
            "search_depth": 1,
            "secondary_emails": ["contact@cirquedusoleil.com"],
        }
    ],
    "Chiasson & Thomas": [
        {
            "email": "jnormand@chiassonthomas.com",
            "contact_name": "Jacques Normand",
            "contact_title": "Arpenteur-géomètre / associé",
            "source_url": "https://chiassonthomas.com/nous-joindre/",
            "source_type": "website",
            "email_source": "page Nous joindre — personnes ressources",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 96,
            "search_depth": 1,
        }
    ],
    "Kraft Heinz Canada": [
        {
            "email": "",
            "contact_name": "Heidi Turner",
            "contact_title": "Talent Acquisition Leader — Canada Operations",
            "source_url": "https://ca.indeed.com/cmp/Kraft-Heinz-3e502a27",
            "source_type": "linkedin",
            "email_source": "profil / page employeur publics",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 0,
            "search_depth": 3,
            "status": "CONTACT_FOUND_EMAIL_NOT_FOUND",
        }
    ],
    "Beneva": [
        {
            "email": "",
            "contact_name": "Mélanie Rancourt",
            "contact_title": "Directrice Acquisition de talents",
            "source_url": "https://www.linkedin.com/in/melanierancourt",
            "source_type": "linkedin",
            "email_source": "profil LinkedIn public",
            "discovered_at": RESEARCHED_AT,
            "confidence_score": 0,
            "search_depth": 3,
            "status": "CONTACT_FOUND_EMAIL_NOT_FOUND",
        }
    ],
}


# Entreprises A+ / A clairement en portail-only après passes documentées.
PORTAL_ONLY = {
    "Desjardins",
    "Banque Nationale",
    "Air Canada",
    "TELUS",
    "Loblaw",
    "STM",
    "Shopify",
    "RBC",
    "BMO",
    "TD Canada Trust",
    "CDPQ",
    "Investissement Québec",
    "GardaWorld",
    "Capgemini Canada",
    "Accenture Canada",
    "Deloitte Canada",
    "PwC Canada",
    "iA Groupe financier",
    "Intact Assurance",
    "Canada Vie",
    "Manuvie",
    "IKEA Canada",
    "McCain Foods",
    "Université de Montréal",
    "Revenu Québec",
    "CRA",
    "CBC/Radio-Canada",
    "Great-West",
    "Altasciences",
    "Agnico Eagle",
}
