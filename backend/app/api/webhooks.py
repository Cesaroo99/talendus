from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.errors import ok
from app.services import stripe_billing

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")
    event = stripe_billing.construct_event(payload, signature)
    stripe_billing.apply_event(db, event)
    return ok({"received": True, "type": event.get("type")})
