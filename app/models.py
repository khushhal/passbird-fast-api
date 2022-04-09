from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer

from app.database import Base


class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    chain = Column(String(255))
    user_id = Column(String(255))
    application_id = Column(String(16))
    application_secret = Column(String(32))

    created_at = Column(DateTime, default=datetime.utcnow)
