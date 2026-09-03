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
    },
    {
        "key": "temporaire",
        "type": "Mandat de placement temporaire",
        "commission_percent": DEFAULT_COMMISSION_PERCENT,
    },
)


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
    template: str = "succes",
) -> str:
    settings = get_settings()
    percent = commission if commission is not None else DEFAULT_COMMISSION_PERCENT
    client = (legal_name or "").strip()
    trade = (company_name or "").strip() or "le client"
    if client and trade and client.lower() != trade.lower():
        party_client = f"{client} (faisant affaire sous {trade})"
    else:
        party_client = client or trade
    loc = ", ".join(part for part in [address, city, province or "Québec"] if part)
    email = settings.public_email
    phone = settings.public_phone_display
    if (template or "succes").lower() == "temporaire":
        fees = (
            f"Honoraires de placement temporaire : {percent} % de la rémunération brute "
            "versée pendant la période de mission, facturés selon les périodes convenues."
        )
        guarantee = (
            "Si la mission est interrompue dans les 10 premiers jours ouvrables pour un motif "
            "qui n'est pas imputable à Talendus, une relance de recherche est offerte sans "
            "honoraires supplémentaires pour le même poste."
        )
    else:
        fees = (
            f"Commission de {percent} % calculée sur la rémunération annuelle brute du candidat "
            "placé, payable à l'entrée en poste."
        )
        guarantee = (
            "En cas de départ du candidat dans les 90 jours suivant l'entrée en fonction, "
            "Talendus relance la recherche sans honoraires supplémentaires, sauf congédiement "
            "sans motif valable."
        )
    role_line = f"Poste visé : {role.strip()}.\n\n" if role and role.strip() else ""
    date_line = f"Date d'ouverture : {start_date}.\n\n" if start_date else ""
    return f"""Parties
Talendus (« l'agence »), {email}, {phone}.
Le client : {party_client}, {loc or 'Québec'}.

{date_line}{role_line}Type de mandat
{mandate_type}

Objet
Talendus agit comme agence de placement. Le client confie un besoin de recrutement. Talendus recherche, présélectionne et présente les profils. Un conseiller coordonne les échanges. Le client conserve la décision d'embauche. La recherche active ne commence qu'après signature électronique du présent mandat.

Honoraires
{fees}

Garantie
{guarantee}

Confidentialité
Les dossiers présentés restent confidentiels. Les coordonnées des talents ne sont pas transmises en libre-service.

Signature
Le client signe électroniquement dans son espace Talendus (empreinte SHA-256, horodatage, adresse IP). Cette signature a la même valeur qu'une signature manuscrite entre les parties.
"""


DEFAULT_MANDATE_TERMS = mandate_terms()


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


def contract_pdf(row: Contract) -> bytes:
    company = row.company
    latest = row.signatures[-1] if row.signatures else None
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
    lines += ["", "Signature", "---------"]
    if latest:
        signed = latest.signed_at.isoformat() if latest.signed_at else "-"
        lines += [
            f"Signe par : {latest.signer_name}",
            f"Courriel : {latest.signer_email or '-'}",
            f"Le : {signed}",
            f"Empreinte SHA-256 : {latest.document_hash}",
            "Signature electronique interne Talendus (sans DocuSign ni Adobe Sign).",
        ]
    else:
        lines.append("En attente de signature dans l'espace employeur Talendus.")
    lines += ["", "Talendus · info@talendus.ca · 263 558 5225"]
    body: list[str] = []
    for line in lines:
        body.extend(_wrap(line) if len(line) > 92 else [line])
    return build_pdf("MANDAT DE RECRUTEMENT", body, heading="Talendus — agence de placement")
