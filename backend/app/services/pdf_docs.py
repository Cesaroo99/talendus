"""Génération PDF interne (factures et mandats) — aucun service externe."""

from __future__ import annotations

from app.config import get_settings
from app.models import Contract, Invoice

GST_RATE = 0.05
QST_RATE = 0.09975
QC_TAX_BP = 14975

DEFAULT_COMMISSION_PERCENT = 16

MANDATE_TEMPLATES = (
    {
        "key": "succes",
        "type": "Mandat de recrutement au succès",
        "commission_percent": DEFAULT_COMMISSION_PERCENT,
        "duration_days": 90,
        "guarantee_days": 90,
        "presented_months": 12,
    },
    {
        "key": "temporaire",
        "type": "Mandat de placement temporaire",
        "commission_percent": DEFAULT_COMMISSION_PERCENT,
        "duration_days": 90,
        "guarantee_days": 10,
        "presented_months": 12,
    },
)

PARTY_TALENDUS = "TALENDUS"
PARTY_CLIENT = "CLIENT"


def mandate_terms(
    *,
    company_name: str = "le client",
    legal_name: str | None = None,
    address: str | None = None,
    city: str | None = None,
    province: str | None = None,
    commission: int | None = None,
    mandate_type: str = "Mandat de recrutement au succès",
    role: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    template: str = "succes",
    duration_days: int | None = None,
    guarantee_days: int | None = None,
    presented_months: int | None = None,
) -> str:
    issuer = billing_identity()
    percent = commission if commission is not None else DEFAULT_COMMISSION_PERCENT
    client = (legal_name or "").strip()
    trade = (company_name or "").strip() or "le client"
    if client and trade and client.lower() != trade.lower():
        party_client = f"{client} (faisant affaire sous {trade})"
    else:
        party_client = client or trade
    loc = ", ".join(part for part in [address, city, province or "Québec"] if part) or "Québec, Canada"
    email = issuer["email"]
    phone = issuer["phone"]
    agency_addr = issuer["address"]
    agency_name = issuer["legal_name"] or "Talendus"
    kind = (template or "succes").strip().lower()
    days = int(duration_days or 90)
    guarantee = int(guarantee_days or (10 if kind == "temporaire" else 90))
    presented = int(presented_months or 12)
    poste = (role or "").strip() or "le poste confié par le Client"
    debut = start_date or "la date de signature du présent mandat"
    fin = end_date or f"{days} jours à compter de la date d'ouverture"
    neq_line = f" NEQ : {issuer['neq']}." if issuer.get("neq") else ""

    if kind == "temporaire":
        objet = (
            f"Le Client confie à Talendus un mandat de placement temporaire pour le poste de {poste}. "
            "Talendus recherche, présélectionne et présente des personnes disponibles pour une mission "
            "à durée déterminée. Un conseiller coordonne les échanges. Le Client conserve le pouvoir "
            "d'accepter ou de refuser une personne présentée et assume la supervision quotidienne sur "
            "le lieu de travail. La recherche active ne commence qu'après signature électronique du "
            "présent mandat par Talendus et par le Client."
        )
        honoraires = (
            f"Les honoraires de placement temporaire sont de {percent} % de la rémunération brute "
            "versée à la personne placée pendant toute la durée de la mission, taxes en sus "
            "(TPS et TVQ). Ils sont facturés selon les périodes convenues, au plus tard à chaque "
            "période de paie. Si le Client embauche la personne en poste permanent pendant la mission "
            f"ou dans les {presented} mois suivant la fin de la mission, les honoraires du mandat au "
            f"succès ({percent} % de la rémunération annuelle brute) deviennent exigibles, déduction "
            "faite des honoraires temporaires déjà payés pour les quatre (4) dernières semaines de mission."
        )
        garantie = (
            f"Si la mission est interrompue dans les {guarantee} premiers jours ouvrables pour un motif "
            "qui n'est pas imputable à Talendus (refus de se présenter, abandon sans motif valable, "
            "incompétence manifeste constatée par écrit), Talendus relance la recherche pour le même "
            "poste sans honoraires supplémentaires. Cette relance ne s'applique pas si le Client met "
            "fin à la mission pour un motif économique, une réorganisation ou un changement de besoin."
        )
        exclusivite = (
            "Le mandat de placement temporaire n'est pas exclusif. Toutefois, toute personne présentée "
            f"par Talendus est protégée pendant {presented} mois : si le Client l'engage, directement "
            "ou par un autre intermédiaire, les honoraires prévus au présent mandat sont dus."
        )
    else:
        objet = (
            f"Le Client confie à Talendus un mandat de recrutement au succès pour le poste de {poste}. "
            "Talendus agit comme cabinet de recrutement et agence de placement : recherche (y compris "
            "approche directe lorsque le profil l'exige), présélection, vérification des éléments "
            "communiqués, présentation d'une shortlist et coordination jusqu'à la première entrevue "
            "avec le Client. Le Client conserve la décision d'embauche, les conditions d'emploi et "
            "l'offre écrite. La recherche active ne commence qu'après signature électronique du "
            "présent mandat par Talendus et par le Client."
        )
        honoraires = (
            f"Les honoraires sont de {percent} % de la rémunération annuelle brute du candidat placé "
            "(salaire de base annualisé ; si la rémunération est horaire, elle est convertie sur la "
            "base de quarante (40) heures par semaine et de cinquante-deux (52) semaines). Les primes "
            "garanties à l'embauche sont incluses. Les taxes applicables (TPS et TVQ) s'ajoutent. "
            "Les honoraires sont exigibles à la date d'entrée en poste, payables dans les trente (30) "
            "jours de la facture, par virement ou chèque à l'ordre de Talendus. Tout solde en souffrance "
            "porte intérêt à un pour cent et demi (1,5 %) par mois (18 % par an)."
        )
        garantie = (
            f"Si le candidat placé quitte ou est congédié pour un motif valable dans les {guarantee} jours "
            "suivant l'entrée en fonction, Talendus relance la recherche pour le même poste, au même "
            "niveau, sans honoraires supplémentaires. La garantie ne s'applique pas en cas de mise à "
            "pied, de congédiement sans motif valable, de changement substantiel des fonctions ou de "
            "la rémunération, de harcèlement, de non-paiement du salaire, ou si le Client n'a pas "
            "réglé les honoraires du premier placement."
        )
        exclusivite = (
            "Le mandat n'est pas exclusif pour le marché en général. En revanche, tout candidat "
            f"présenté par Talendus (dossier, entrevue, mise en relation) est protégé pendant {presented} mois "
            "à compter de la présentation : si le Client l'embauche, directement ou via un autre canal, "
            "les honoraires prévus à l'article 8 sont dus comme s'il s'agissait d'un placement Talendus."
        )

    return f"""MANDAT DE RECRUTEMENT
{mandate_type}

Entre
{agency_name} (« Talendus » ou « l'Agence »), cabinet de recrutement et agence de placement, {agency_addr}.
Courriel : {email} · Téléphone : {phone}.{neq_line}

Et
{party_client} (« le Client »), {loc}.

Date d'ouverture du mandat : {debut}
Date de fin prévue : {fin}
Poste visé : {poste}

ARTICLE 1 — PARTIES
Talendus et le Client sont les seules parties au présent mandat. Aucun prestataire de signature externe (DocuSign, Adobe Sign ou autre) n'est requis. Les notifications se font dans l'espace Talendus et, le cas échéant, par courriel.

ARTICLE 2 — DÉFINITIONS
« Candidat présenté » : toute personne dont le nom, le dossier, le curriculum vitae ou les coordonnées ont été communiqués au Client par Talendus, ou que le Client a rencontrée par l'entremise de Talendus.
« Placement » : l'acceptation, par le Client, d'une personne présentée, que le contrat de travail soit à durée indéterminée, déterminée, à l'essai ou temporaire.
« Shortlist » : la liste de profils présélectionnés que Talendus juge pertinents au regard du brief.

ARTICLE 3 — OBJET
{objet}

ARTICLE 4 — DURÉE
Le mandat est conclu pour {days} jours à compter de la date d'ouverture, renouvelable par accord écrit ou par poursuite manifeste de la recherche. Il prend fin à l'expiration de cette période, à la résiliation prévue à l'article 14, ou lorsqu'un placement a été réalisé et que les obligations de garantie, s'il y a lieu, sont éteintes.

ARTICLE 5 — OBLIGATIONS DE TALENDUS
Talendus s'engage à : (a) confirmer le brief et le profil recherché avec le Client ; (b) rechercher et présélectionner des profils ; (c) présenter une shortlist et coordonner les entrevues ; (d) tenir le Client informé de l'avancement, sans inventer de délais ou de volumes ; (e) conserver confidentiels les renseignements du Client ; (f) ne pas transmettre les coordonnées des talents en libre-service. Talendus n'est pas l'employeur du candidat placé en recrutement au succès, sauf entente écrite contraire pour une mission temporaire.

ARTICLE 6 — OBLIGATIONS DU CLIENT
Le Client s'engage à : (a) fournir un brief exact (fonctions, horaire, quart, présence, rémunération, exigences) ; (b) donner une suite écrite sur chaque dossier présenté dans les cinq (5) jours ouvrables ; (c) ne pas contacter un candidat présenté autrement que par l'intermédiaire de Talendus pendant la durée du mandat ; (d) informer Talendus sans délai de toute embauche d'un candidat présenté, y compris après la fin du mandat si elle survient pendant la période de protection ; (e) payer les honoraires et les taxes aux échéances prévues.

ARTICLE 7 — EXCLUSIVITÉ ET CANDIDATS PRÉSENTÉS
{exclusivite}

ARTICLE 8 — HONORAIRES ET PAIEMENT
{honoraires}

ARTICLE 9 — GARANTIE DE REMPLACEMENT
{garantie}

ARTICLE 10 — CONFIDENTIALITÉ
Chaque partie garde confidentiels les renseignements de l'autre, les dossiers de candidats et les conditions du présent mandat. Les documents remis au Client restent la propriété de Talendus et ne peuvent être transmis à un tiers, une autre agence ou un autre établissement du Client non partie au mandat, sans accord écrit.

ARTICLE 11 — RENSEIGNEMENTS PERSONNELS
Les parties traitent les renseignements personnels des candidats conformément à la Loi sur la protection des renseignements personnels dans le secteur privé (CQLR c. P-39.1). Le Client n'utilise un dossier présenté que pour évaluer le poste visé et le conserve le temps nécessaire à cette évaluation.

ARTICLE 12 — NON-SOLLICITATION
Pendant la durée du mandat et douze (12) mois après sa fin, le Client ne sollicite pas le personnel de Talendus en vue de l'embaucher. Une embauche contraire à cet article donne lieu à des honoraires égaux à ceux de l'article 8, calculés sur la rémunération offerte.

ARTICLE 13 — RESPONSABILITÉ
Talendus exécute le mandat avec diligence. Elle ne garantit pas qu'un poste sera pourvu dans un délai donné. Sa responsabilité, tous motifs confondus, est limitée aux honoraires effectivement payés au titre du mandat. Talendus n'est pas responsable des actes, omissions, compétences ou conduite du candidat une fois l'embauche décidée par le Client.

ARTICLE 14 — RÉSILIATION
Chaque partie peut résilier le mandat moyennant un avis écrit de quinze (15) jours. La résiliation n'éteint pas les honoraires dus pour un candidat déjà présenté si un placement intervient pendant la période de protection. Les articles 7, 8, 10, 11, 12 et 13 survivent à la fin du mandat.

ARTICLE 15 — FORCE MAJEURE
Aucune partie n'est responsable d'un retard ou d'une inexécution causés par un événement échappant à son contrôle raisonnable (interruption de réseau, sinistre, décision d'autorité). L'obligation de payer les honoraires déjà exigibles n'est pas suspendue.

ARTICLE 16 — DISPOSITIONS GÉNÉRALES
Le présent mandat constitue l'entente complète des parties et remplace toute discussion antérieure sur le même objet. Une modification se fait par écrit (y compris par signature électronique dans l'espace Talendus). La nullité d'une clause n'affecte pas les autres. Le fait de ne pas exercer un droit ne vaut pas renonciation. Le Client ne cède pas le mandat sans accord écrit de Talendus.

ARTICLE 17 — DROIT APPLICABLE ET FOR
Le présent mandat est régi par les lois du Québec et les lois du Canada qui y sont applicables. Les tribunaux compétents du district judiciaire de Montréal ont compétence exclusive, sous réserve d'un recours en injonction ou en recouvrement ailleurs si le Client y a un établissement.

ARTICLE 18 — SIGNATURE ÉLECTRONIQUE ET EXEMPLAIRES
Le mandat est signé électroniquement dans l'espace Talendus : Talendus signe en premier, puis le Client. Chaque signature est horodatée, associée à un nom, un courriel, une adresse IP et une empreinte SHA-256 du document. Conformément à la Loi concernant le cadre juridique des technologies de l'information (CQLR c. C-1.1), cette signature a la même valeur qu'une signature manuscrite entre les parties. Chaque partie peut télécharger un exemplaire PDF. Deux exemplaires électroniques font également foi.

ARTICLE 19 — ACCEPTATION
En signant, chaque partie confirme avoir lu l'intégralité du mandat, en avoir compris la portée et l'accepter. La recherche active commence lorsque le Client a signé.
"""


def _latin(text: str) -> str:
    table = str.maketrans(
        {
            "’": "'",
            "‘": "'",
            "“": '"',
            "”": '"',
            "–": "-",
            "—": "-",
            "…": "...",
            "€": "EUR",
            "\xa0": " ",
        }
    )
    return (text or "").translate(table).replace("\r", "").encode("latin-1", "replace").decode("latin-1")


def _escape(text: str) -> str:
    return _latin(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap(text: str, width: int = 92) -> list[str]:
    lines: list[str] = []
    for raw in _latin(text).split("\n"):
        raw = raw.rstrip()
        if not raw:
            lines.append("")
            continue
        while len(raw) > width:
            cut = raw.rfind(" ", 0, width)
            if cut < 20:
                cut = width
            lines.append(raw[:cut])
            raw = raw[cut:].lstrip()
        lines.append(raw)
    return lines


def build_pdf(title: str, body_lines: list[str], *, heading: str | None = None) -> bytes:
    items: list[tuple[str, int, bool]] = [(_latin(title), 16, True)]
    if heading:
        items.append((_latin(heading), 11, False))
        items.append(("", 8, False))
    for line in body_lines:
        items.append((_latin(line), 10, False))

    pages: list[list[tuple[str, int, bool]]] = []
    current: list[tuple[str, int, bool]] = []
    y = 742
    for item in items:
        size = item[1]
        if y < 56:
            pages.append(current)
            current = []
            y = 742
        current.append(item)
        y -= size + 5
    if current:
        pages.append(current)
    if not pages:
        pages = [[(_latin(title), 16, True)]]

    def content_stream(page_items: list[tuple[str, int, bool]]) -> bytes:
        y = 742
        buf = ["BT"]
        for text, size, bold in page_items:
            font = "F2" if bold else "F1"
            buf.append(f"/{font} {size} Tf")
            buf.append(f"1 0 0 1 48 {y} Tm")
            buf.append(f"({_escape(text)}) Tj")
            y -= size + 5
        buf.append("ET")
        return "\n".join(buf).encode("latin-1")

    n_pages = len(pages)
    font1 = 3 + 2 * n_pages
    font2 = font1 + 1
    objects: list[bytes] = []

    def add(data: bytes | str) -> None:
        objects.append(data if isinstance(data, bytes) else data.encode("latin-1"))

    add(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{i} 0 R" for i in range(3, 3 + n_pages))
    add(f"<< /Type /Pages /Kids [{kids}] /Count {n_pages} >>")
    for i in range(n_pages):
        add(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font1} 0 R /F2 {font2} 0 R >> >> "
            f"/Contents {3 + n_pages + i} 0 R >>"
        )
    for page_items in pages:
        raw = content_stream(page_items)
        add(f"<< /Length {len(raw)} >>\nstream\n".encode("latin-1") + raw + b"\nendstream")
    add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{i} 0 obj\n".encode("latin-1"))
        out.extend(obj)
        if not out.endswith(b"\n"):
            out.extend(b"\n")
        out.extend(b"endobj\n")
    xref = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("latin-1"))
    out.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("latin-1")
    )
    return bytes(out)


def _money(amount: int | None, currency: str = "CAD") -> str:
    n = int(amount or 0)
    sign = "-" if n < 0 else ""
    formatted = f"{abs(n):,}".replace(",", " ")
    return f"{sign}{formatted},00 $ {currency}"


def tax_from_bp(ht: int, bp: int | None) -> int:
    rate = int(bp or 0)
    if rate <= 0 or ht <= 0:
        return 0
    if rate > 2000:
        return int(round(ht * rate / 100000))
    return int(round(ht * rate / 10000))


def qc_tax_split(ht: int, tax_amount: int | None) -> tuple[int, int]:
    gst = int(round(int(ht or 0) * GST_RATE))
    tax = int(tax_amount or 0)
    if tax:
        qst = tax - gst
        if qst < 0:
            qst = int(round(int(ht or 0) * QST_RATE))
        return gst, qst
    return gst, int(round(int(ht or 0) * QST_RATE))


def billing_identity() -> dict:
    s = get_settings()
    return {
        "legal_name": s.billing_legal_name or "Talendus",
        "address": s.billing_address_line or "Montreal (Quebec) Canada",
        "neq": (s.billing_neq or "").strip(),
        "gst": (s.billing_gst or "").strip(),
        "qst": (s.billing_qst or "").strip(),
        "phone": s.public_phone_display or "263 558 5225",
        "email": s.public_email or "info@talendus.ca",
    }


def _pdf_objects(page_streams: list[bytes]) -> bytes:
    n_pages = len(page_streams) or 1
    font1 = 3 + 2 * n_pages
    font2 = font1 + 1
    objects: list[bytes] = []

    def add(data: bytes | str) -> None:
        objects.append(data if isinstance(data, bytes) else data.encode("latin-1"))

    add(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{i} 0 R" for i in range(3, 3 + n_pages))
    add(f"<< /Type /Pages /Kids [{kids}] /Count {n_pages} >>")
    for i in range(n_pages):
        add(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font1} 0 R /F2 {font2} 0 R >> >> "
            f"/Contents {3 + n_pages + i} 0 R >>"
        )
    for raw in page_streams:
        add(f"<< /Length {len(raw)} >>\nstream\n".encode("latin-1") + raw + b"\nendstream")
    add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out.extend(f"{i} 0 obj\n".encode("latin-1"))
        out.extend(obj)
        if not out.endswith(b"\n"):
            out.extend(b"\n")
        out.extend(b"endobj\n")
    xref = len(out)
    out.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("latin-1"))
    out.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("latin-1")
    )
    return bytes(out)


def _text(x: int, y: int, size: int, content: str, *, bold: bool = False) -> str:
    font = "F2" if bold else "F1"
    return f"BT /{font} {size} Tf 1 0 0 1 {x} {y} Tm ({_escape(content)}) Tj ET"


def invoice_pdf(row: Invoice) -> bytes:
    issuer = billing_identity()
    company = row.company
    ht = row.amount_ht if row.amount_ht is not None else row.amount
    tax = int(row.tax_amount or 0)
    total = row.amount_total if row.amount_total is not None else row.amount
    gst, qst = qc_tax_split(int(ht or 0), tax)
    client_lines = [
        company.name if company else "",
        (company.legal_name if company and company.legal_name and company.legal_name != company.name else ""),
        " ".join(part for part in [(company.address if company else None), (company.city if company else None)] if part),
        " ".join(part for part in [(company.province if company else None) or "Quebec", (company.country if company else None) or "Canada"] if part),
        company.email if company and company.email else "",
    ]
    client_lines = [line for line in client_lines if line]

    line_rows: list[tuple[str, str]] = []
    if row.lines:
        for line in row.lines:
            desc = f"{line.description}  x{line.quantity}"
            line_rows.append((desc, _money(line.amount, row.currency)))
    else:
        line_rows.append(("Honoraires de recrutement", _money(ht, row.currency)))

    cmds: list[str] = [
        "0.043 0.122 0.227 rg",
        "0 732 612 60 re f",
        "1 0.42 0 rg",
        "0 728 612 4 re f",
        "1 1 1 rg",
        "36 747 28 28 re f",
        "0.043 0.122 0.227 rg",
        _text(42, 756, 16, "T", bold=True),
        "1 1 1 rg",
        _text(74, 756, 18, "TALENDUS", bold=True),
        _text(74, 740, 9, "Agence de placement  ·  talendus.ca"),
        "0.043 0.122 0.227 rg",
        _text(48, 700, 16, "FACTURE", bold=True),
        _text(400, 704, 11, f"N° {row.number}", bold=True),
        _text(400, 688, 10, f"Date : {row.issued_at or '-'}"),
        _text(400, 674, 10, f"Echeance : {row.due_date or '-'}"),
        _text(400, 660, 10, f"Statut : {row.status.value if row.status else ''}"),
        _text(48, 672, 9, issuer["legal_name"], bold=True),
        _text(48, 658, 9, issuer["address"]),
        _text(48, 644, 9, f"{issuer['email']}  ·  {issuer['phone']}"),
    ]
    y = 630
    if issuer["neq"]:
        cmds.append(_text(48, y, 8, f"NEQ : {issuer['neq']}"))
        y -= 12
    else:
        cmds.append(_text(48, y, 8, "NEQ : a renseigner (Paramètres > Plateforme)"))
        y -= 12
    gst_no = issuer["gst"] or "a renseigner"
    qst_no = issuer["qst"] or "a renseigner"
    cmds.append(_text(48, y, 8, f"N° TPS : {gst_no}    N° TVQ : {qst_no}"))
    cmds += [
        "0.894 0.918 0.941 rg",
        "48 560 516 1 re f",
        "0.043 0.122 0.227 rg",
        _text(48, 600, 10, "Facturee a", bold=True),
    ]
    cy = 584
    for line in client_lines[:5]:
        cmds.append(_text(48, cy, 10, line))
        cy -= 13

    cmds += [
        "0.043 0.122 0.227 rg",
        "48 528 516 22 re f",
        "1 1 1 rg",
        _text(56, 535, 9, "Description", bold=True),
        _text(430, 535, 9, "Montant (CAD)", bold=True),
    ]
    y = 508
    cmds.append("0 0 0 rg")
    for desc, amount in line_rows[:12]:
        wrapped = _wrap(desc, 62)
        cmds.append(_text(56, y, 10, wrapped[0] if wrapped else desc))
        cmds.append(_text(430, y, 10, amount))
        y -= 16
        for extra in wrapped[1:2]:
            cmds.append(_text(56, y, 10, extra))
            y -= 14
    y -= 8
    cmds += [
        "0.894 0.918 0.941 rg",
        f"320 {y - 70} 244 78 re f",
        "0.043 0.122 0.227 rg",
        _text(332, y, 10, "Sous-total (avant taxes)"),
        _text(470, y, 10, _money(ht, row.currency), bold=True),
        _text(332, y - 16, 10, "TPS 5 %"),
        _text(470, y - 16, 10, _money(gst, row.currency)),
        _text(332, y - 32, 10, "TVQ 9,975 %"),
        _text(470, y - 32, 10, _money(qst, row.currency)),
        _text(332, y - 52, 11, "Total a payer", bold=True),
        _text(470, y - 52, 11, _money(total, row.currency), bold=True),
        _text(48, y, 10, "Paiement", bold=True),
        _text(48, y - 16, 9, "Virement ou cheque a l'ordre de Talendus."),
        _text(48, y - 30, 9, "Devise : dollar canadien (CAD). Taxes du Quebec (TPS + TVQ)."),
        _text(48, y - 44, 9, "L'encaissement est enregistre par Talendus. Pas de intermediaire requis."),
    ]
    fy = y - 72
    if row.notes:
        cmds.append(_text(48, fy, 10, "Notes", bold=True))
        fy -= 14
        for line in _wrap(row.notes, 86)[:6]:
            cmds.append(_text(48, fy, 9, line))
            fy -= 12
    cmds += [
        "0.043 0.122 0.227 rg",
        "0 0 612 36 re f",
        "1 1 1 rg",
        _text(48, 14, 8, "Talendus  ·  Agence de placement  ·  talendus.ca  ·  " + issuer["phone"]),
    ]
    stream = "\n".join(cmds).encode("latin-1")
    return _pdf_objects([stream])


def _signature_block(title: str, signatures: list, party: str) -> list[str]:
    match = None
    for item in signatures or []:
        if (getattr(item, "party", None) or PARTY_CLIENT).upper() == party:
            match = item
    lines = ["", title, "-" * len(title)]
    if match:
        signed = match.signed_at.isoformat() if match.signed_at else "-"
        lines += [
            f"Signe par : {match.signer_name}",
            f"Courriel : {match.signer_email or '-'}",
            f"Le : {signed}",
            f"Empreinte SHA-256 : {match.document_hash}",
            "Signature electronique interne Talendus (sans DocuSign ni Adobe Sign).",
        ]
    else:
        waiting = (
            "En attente de la signature de Talendus."
            if party == PARTY_TALENDUS
            else "En attente de la signature du client dans l'espace employeur."
        )
        lines.append(waiting)
    return lines


def contract_pdf(row: Contract) -> bytes:
    company = row.company
    lines = [
        f"Entreprise : {company.name if company else ''}",
        f"Type : {row.type or 'Mandat de recrutement'}",
        f"Debut : {row.start_date or '-'}",
        f"Fin : {row.end_date or '-'}",
        f"Commission : {row.commission_percent or '-'} %",
        f"Statut : {row.status.value if row.status else ''}",
        "",
        "Conditions",
        "----------",
    ]
    lines.extend(_wrap(row.terms or ""))
    lines += _signature_block("Signature Talendus", row.signatures, PARTY_TALENDUS)
    lines += _signature_block("Signature du client", row.signatures, PARTY_CLIENT)
    lines += ["", "Talendus · info@talendus.ca · 263 558 5225"]
    body: list[str] = []
    for line in lines:
        body.extend(_wrap(line) if len(line) > 92 else [line])
    return build_pdf("MANDAT DE RECRUTEMENT", body, heading="Talendus — agence de placement")
