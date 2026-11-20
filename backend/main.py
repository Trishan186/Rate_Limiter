from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import math

from backend.database import Base, engine, get_db
from backend.rate_limiter import check_rate_limit, get_rate_limit_status

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Rate Limiter API",
    description="A Token Bucket based Rate Limiter",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Rate Limiter API is running successfully"
    }


@app.post("/request/{client_id}")
def process_request(
    client_id: str,
    db: Session = Depends(get_db)
):
    result = check_rate_limit(db, client_id)

    if not result["allowed"]:
        raise HTTPException(
            status_code=429,
            detail=result,
            headers={
                "Retry-After": str(
                    max(1, math.ceil(result["retry_after_seconds"]))
                )
            }
        )

    return result


@app.get("/rate-limit/{client_id}")
def get_client_status(
    client_id: str,
    db: Session = Depends(get_db)
):
    return get_rate_limit_status(db, client_id)