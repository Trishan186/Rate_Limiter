import time
from sqlalchemy.orm import Session

from backend.models import ClientRateLimit


# Rate limiter configuration
BUCKET_CAPACITY = 5
REFILL_RATE = 1 / 12


def check_rate_limit(db: Session, client_id: str):

    current_time = time.time()

    client = db.query(ClientRateLimit).filter(
        ClientRateLimit.client_id == client_id
    ).first()

    if client is None:
        client = ClientRateLimit(
            client_id=client_id,
            tokens=BUCKET_CAPACITY,
            last_refill=current_time
        )
        db.add(client)
        db.flush()

    time_passed = max(0, current_time - client.last_refill)

    new_tokens = time_passed * REFILL_RATE

    client.tokens = min(
        BUCKET_CAPACITY,
        client.tokens + new_tokens
    )

    client.last_refill = current_time

    if client.tokens >= 1:

        client.tokens -= 1
        db.commit()

        return {
            "allowed": True,
            "client_id": client_id,
            "remaining_tokens": round(client.tokens, 2),
            "message": "Request allowed"
        }

    else:

        retry_after = (1 - client.tokens) / REFILL_RATE

        db.commit()

        return {
            "allowed": False,
            "client_id": client_id,
            "remaining_tokens": round(client.tokens, 2),
            "retry_after_seconds": round(retry_after, 2),
            "message": "Rate limit exceeded"
        }


# Separate function to check client status
def get_rate_limit_status(db: Session, client_id: str):

    current_time = time.time()

    client = db.query(ClientRateLimit).filter(
        ClientRateLimit.client_id == client_id
    ).first()

    if client is None:
        return {
            "client_id": client_id,
            "remaining_tokens": BUCKET_CAPACITY,
            "bucket_capacity": BUCKET_CAPACITY,
            "message": "New client. Bucket is full."
        }

    time_passed = max(0, current_time - client.last_refill)

    new_tokens = time_passed * REFILL_RATE

    client.tokens = min(
        BUCKET_CAPACITY,
        client.tokens + new_tokens
    )

    client.last_refill = current_time

    db.commit()

    return {
        "client_id": client_id,
        "remaining_tokens": round(client.tokens, 2),
        "bucket_capacity": BUCKET_CAPACITY,
        "message": "Rate limit status retrieved successfully"
    }