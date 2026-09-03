import re
from types import SimpleNamespace

from app.models.enums import ContractStatus, InvoiceStatus
from app.services.pdf_docs import (
    INVOICE_STAMP,
    build_pdf,
    contract_pdf,
    invoice_pdf,
)


def _plain(data: bytes) -> str:
    return data.decode("latin-1", "replace")


def _axis_aligned_boxes(data: bytes) -> list[tuple[float, float, float, float, str]]:
    """Boîtes des textes non rotateés (hors filigrane / cachet)."""
    text = _plain(data)
    chunks = re.split(r"\nQ\n", text)
    boxes = []
    for chunk in chunks:
        if "\nq\n" in chunk or chunk.strip().startswith("q"):
            continue
        for match in re.finditer(
            r"/F[12] (\d+) Tf 1 0 0 1 ([\d.]+) ([\d.]+) Tm \((.*?)\) Tj",
            chunk,
        ):
            size = int(match.group(1))
            x = float(match.group(2))
            y = float(match.group(3))
            raw = match.group(4).replace("\\(", "(").replace("\\)", ")")
            width = max(8.0, len(raw) * size * 0.52)
            boxes.append((x, y, x + width, y + size, raw))
    return boxes


def _overlaps(boxes, min_gap=2.5):
    hits = []
    for i, a in enumerate(boxes):
        for b in boxes[i + 1 :]:
            ax0, ay0, ax1, ay1, at = a
            bx0, by0, bx1, by1, bt = b
            if ax1 < bx0 - min_gap or bx1 < ax0 - min_gap:
                continue
            if ay1 < by0 - min_gap or by1 < ay0 - min_gap:
                continue
            if not at.strip() or not bt.strip():
                continue
            hits.append((at, bt, ay0, by0))
    return hits


def _invoice(status=InvoiceStatus.SENT, **extra):
    company = SimpleNamespace(
        name="Métalco",
        legal_name="Métalco inc.",
        address="1200 rue de l'Usine",
        city="Drummondville",
        province="Quebec",
        country="Canada",
        email="j.rivest@metalco.ca",
    )
    defaults = dict(
        company=company,
        number="F-2026-042",
        amount=4200,
        amount_ht=4200,
        tax_amount=629,
        amount_total=4829,
        currency="CAD",
        status=status,
        issued_at="2026-09-03",
        due_date="2026-10-03",
        notes="Honoraires au succes, placement Soudeur-monteur.",
        lines=[],
    )
    defaults.update(extra)
    return SimpleNamespace(**defaults)


def test_invoice_pdf_has_branding_and_no_overlap():
    data = invoice_pdf(_invoice())
    raw = _plain(data)
    assert data.startswith(b"%PDF")
    assert "TALENDUS" in raw
    assert "FACTURE" in raw
    assert "A PAYER" in raw
    assert "Document officiel" in raw
    assert "2282510496" in raw
    assert "Facturee a" in raw
    assert "Métalco".encode("latin-1", "replace").decode("latin-1") in raw or "Metalco" in raw
    hits = _overlaps(_axis_aligned_boxes(data))
    assert hits == [], hits[:6]


def test_paid_invoice_gets_paid_stamp():
    data = invoice_pdf(_invoice(InvoiceStatus.PAID))
    raw = _plain(data)
    assert "PAYEE" in raw
    assert INVOICE_STAMP["PAID"][0] in raw


def test_overdue_invoice_gets_late_stamp():
    data = invoice_pdf(_invoice(InvoiceStatus.OVERDUE))
    assert "EN RETARD" in _plain(data)


def test_contract_pdf_watermark_and_signed_stamp():
    company = SimpleNamespace(name="Métalco")
    row = SimpleNamespace(
        company=company,
        type="Mandat de recrutement au succès",
        start_date="2026-10-01",
        end_date="2026-12-30",
        commission_percent=16,
        status=ContractStatus.ACTIVE,
        terms="ARTICLE 1 — PARTIES\nTalendus et le Client.",
        signatures=[
            SimpleNamespace(party="TALENDUS", signer_name="Lea Morin", signer_email="lea@talendus.ca", signed_at=None, document_hash="abc"),
            SimpleNamespace(party="CLIENT", signer_name="Jean Rivest", signer_email="j@metalco.ca", signed_at=None, document_hash="def"),
        ],
        client_signed_at="2026-09-03",
        talendus_signed_at="2026-09-03",
    )
    data = contract_pdf(row)
    raw = _plain(data)
    assert data.startswith(b"%PDF")
    assert "TALENDUS" in raw
    assert "SIGNE" in raw
    assert "MANDAT" in raw
    assert "Document officiel" in raw
    assert "2282510496" in raw


def test_build_pdf_keeps_accents_and_branding():
    data = build_pdf("Facture été", ["Honoraires : 1 200 CAD", "Échéance : demain"], stamp=("PAYEE", (0.1, 0.4, 0.2)))
    assert data.startswith(b"%PDF")
    assert b"%%EOF" in data
    raw = _plain(data)
    assert "TALENDUS" in raw
    assert "PAYEE" in raw
