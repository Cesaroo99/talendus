"""Génération PDF interne (factures et mandats) — aucun service externe."""

from __future__ import annotations

from app.models import Contract, Invoice

DEFAULT_MANDATE_TERMS = """Objet
Talendus agit comme agence de placement. L'entreprise confie un besoin de recrutement. Talendus recherche, présélectionne et présente les profils. Un conseiller coordonne les échanges. L'entreprise conserve la décision d'embauche.

Honoraires
Commission calculée sur la rémunération annuelle brute du candidat placé, payable à l'embauche selon le pourcentage indiqué au présent mandat.

Garantie
En cas de départ du candidat dans les 90 jours suivant l'entrée en fonction, Talendus relance la recherche sans honoraires supplémentaires, sauf congédiement sans motif valable.

Confidentialité
Les dossiers présentés restent confidentiels. Les coordonnées des talents ne sont pas transmises en libre-service.

Signature
La signature électronique interne Talendus (empreinte SHA-256, horodatage, adresse IP) a la même valeur qu'une signature manuscrite entre les parties. Aucun prestataire d'e-signature externe n'est requis.
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


def _money(cents: int | None, currency: str = "CAD") -> str:
    return f"{int(cents or 0)} {currency}"


def invoice_pdf(row: Invoice) -> bytes:
    company = row.company
    total = row.amount_total if row.amount_total is not None else row.amount
    lines = [
        f"Numero : {row.number}",
        f"Statut : {row.status.value if row.status else ''}",
        f"Client : {company.name if company else ''}",
        f"Date : {row.issued_at or '-'}",
        f"Echeance : {row.due_date or '-'}",
        "",
        "Lignes",
        "------",
    ]
    if row.lines:
        for line in row.lines:
            lines.append(f"- {line.description}  x{line.quantity}  {_money(line.amount, row.currency)}")
    else:
        lines.append(f"- Honoraires de recrutement  {_money(row.amount, row.currency)}")
    lines += [
        "",
        f"Sous-total : {_money(row.amount_ht if row.amount_ht is not None else row.amount, row.currency)}",
        f"Taxes : {_money(row.tax_amount, row.currency)}",
        f"Total : {_money(total, row.currency)}",
        "",
        "Paiement",
        "--------",
        "Virement bancaire ou cheque a l'ordre de Talendus.",
        "Aucun intermediaire de paiement n'est requis. Talendus enregistre l'encaissement.",
        "Questions : info@talendus.ca",
    ]
    if row.notes:
        lines += ["", "Notes", "-----"] + _wrap(row.notes)
    body: list[str] = []
    for line in lines:
        body.extend(_wrap(line) if len(line) > 92 else [line])
    return build_pdf("FACTURE TALENDUS", body, heading="Agence de placement · talendus.ca")


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
    lines += ["", "Talendus · info@talendus.ca"]
    body: list[str] = []
    for line in lines:
        body.extend(_wrap(line) if len(line) > 92 else [line])
    return build_pdf("MANDAT DE RECRUTEMENT", body, heading="Talendus — agence de placement")
