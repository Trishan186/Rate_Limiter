from sqlalchemy import Column, String, Float
from backend.database import Base


class ClientRateLimit(Base):

    __tablename__ = "client_rate_limits"

    client_id = Column(String, primary_key=True, index=True)

    tokens = Column(Float, nullable=False)

    last_refill = Column(Float, nullable=False)