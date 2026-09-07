"""Courriels publics trouvés pour des fiches déjà au catalogue.

Ne crée aucune entreprise. Ne remplace jamais un courriel déjà présent.
Aucune adresse inventée : uniquement des courriels vus sur une source publique.
"""

from __future__ import annotations

from typing import Any

# name (clé d’idempotence du catalogue) -> champs d’enrichissement.
PUBLIC_EMAILS: dict[str, dict[str, Any]] = {
    "Bell Textron Canada": {
        "email": "mediarelations@bellflight.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.bellflight.com",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Soucy": {
        "email": "info@soucy-group.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.soucy-group.com/contact",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "ADF Group": {
        "email": "eric.ducharme@adfgroup.com",
        "email_source": "site officiel — vice-président ventes publié",
        "email_source_url": "https://adfgroup.com/contact/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
        "contact_name": "Éric Ducharme",
        "contact_title": "Vice-président, ventes",
    },
    "Exceldor": {
        "email": "info@exceldor.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.exceldor.ca/contact",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Canards du Lac Brome": {
        "email": "servicerh@cdlb.ca",
        "email_source": "site officiel",
        "email_source_url": "https://canardsdulacbrome.com/en/about-us/contact/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Transport L.F.L.": {
        "email": "lindsay.longchamps@transportlfl.com",
        "email_source": "site officiel — directrice RH publiée",
        "email_source_url": "https://transportlfl.com/qui-nous-sommes/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
        "contact_name": "Lindsay Longchamps",
        "contact_title": "Directrice RH et conformité",
    },
    "La Milanaise": {
        "email": "info@lamilanaise.com",
        "email_source": "site officiel",
        "email_source_url": "https://lamilanaise.com/a-propos-lamilanaise/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "FDC Composites": {
        "email": "info@fdccomposites.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.fdccomposites.com/contact",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "CMC Electronics": {
        "email": "customer.support@cmcelectronics.ca",
        "email_source": "site officiel",
        "email_source_url": "https://cmcelectronics.ca/contact/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Ciment Québec": {
        "email": "info@cqi.ca",
        "email_source": "site officiel",
        "email_source_url": "https://www.cimentquebec.com/nous-joindre/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "QSL": {
        "email": "info@qsl.com",
        "email_source": "site officiel",
        "email_source_url": "https://qsl.com/fr/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Familiprix": {
        "email": "experienceclient@familiprix.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.familiprix.com/fr/nous-joindre",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Uniboard": {
        "email": "pr@uniboard.com",
        "email_source": "communiqué officiel",
        "email_source_url": "https://www.uniboard.com/en/news/uniboard-invests-250-million-to-modernize-and-expand-its-val-d-or-plant",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Groupe Meloche": {
        "email": "rh@melocheinc.com",
        "email_source": "offre / communication employeur",
        "email_source_url": "https://www.infosuroit.com/plusieurs-postes-a-pourvoir-chez-groupe-meloche/",
        "email_confidence": "VERIFIED_MEDIUM",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Laboratoire Riva": {
        "email": "info@labriva.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.labriva.com/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Kinova": {
        "email": "info@kinova.ca",
        "email_source": "site officiel",
        "email_source_url": "https://www.kinovarobotics.com/fr/contact",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Broccolini": {
        "email": "bonjour@broccolini.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.broccolini.com/fr/contact",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Aecon": {
        "email": "aecon@aecon.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.aecon.com/contact-us",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Lightspeed": {
        "email": "info@lightspeedhq.com",
        "email_source": "site officiel",
        "email_source_url": "https://www.lightspeedhq.com/contact/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Metro": {
        "email": "consommateurs@metro.ca",
        "email_source": "site officiel",
        "email_source_url": "https://www.corpo.metro.ca/fr/contact-quebec.html",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Lallemand": {
        "email": "info@lallemand.com",
        "email_source": "chambre de commerce",
        "email_source_url": "https://ccemontreal.ca/membre/lallemand-inc/",
        "email_confidence": "VERIFIED_MEDIUM",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Nétur": {
        "email": "emploi@netur.ca",
        "email_source": "site officiel",
        "email_source_url": "https://netur.ca/contact/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Attitude": {
        "email": "sales@attitudeliving.com",
        "email_source": "site officiel",
        "email_source_url": "https://attitudeliving.com/contact-us",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Videotron": {
        "email": "videotron.communications@videotron.com",
        "email_source": "site officiel",
        "email_source_url": "https://corpo.videotron.com/nous-joindre",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Intelcom": {
        "email": "info@intelcomexpress.com",
        "email_source": "site officiel",
        "email_source_url": "https://intelcom.ca/fr/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Warner Bros. Games Montréal": {
        "email": "infomtl@wbgames.com",
        "email_source": "site officiel",
        "email_source_url": "https://wbgamesmontreal.com/contact/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Magellan Aerospace": {
        "email": "magellan.corporate@magellan.aero",
        "email_source": "site officiel",
        "email_source_url": "https://magellan.aero/contact/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Nemaska Lithium": {
        "email": "info@nemaskalithium.com",
        "email_source": "site officiel",
        "email_source_url": "https://nemaskalithium.com/fr/nous-joindre/",
        "email_confidence": "VERIFIED_HIGH",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
    "Nutrinor": {
        "email": "ressources.humaines@nutrinor.com",
        "email_source": "offre d’emploi employeur",
        "email_source_url": "https://emplois.ca.indeed.com/q-nutrinor-l-alma,-qc-emplois.html",
        "email_confidence": "VERIFIED_MEDIUM",
        "email_verified": True,
        "email_verified_at": "2026-09-07",
        "researched_at": "2026-09-07",
    },
}


def apply_public_emails(leads: tuple[dict, ...]) -> tuple[dict, ...]:
    """Complète uniquement les fiches existantes sans courriel."""
    out: list[dict] = []
    for lead in leads:
        name = (lead.get("name") or "").strip()
        patch = PUBLIC_EMAILS.get(name)
        if not patch or (lead.get("email") or "").strip():
            out.append(lead)
            continue
        updated = dict(lead)
        updated.update(patch)
        extra = (
            f" Courriel public relevé le {patch.get('researched_at')}: "
            f"{patch['email']} (source {patch.get('email_source')}, "
            f"{patch.get('email_source_url')})."
        )
        hiring = (updated.get("hiring") or "").rstrip()
        if patch["email"] not in hiring:
            updated["hiring"] = (hiring + extra)[:4000]
        out.append(updated)
    return tuple(out)
