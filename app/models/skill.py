from sqlalchemy import String, Column, Boolean

from app.db.base_class import Base
from app.helpers import generate_uuid


class Skill(Base):
    __tablename__ = "skills"
    id = Column(
        String,
        default=generate_uuid,
        primary_key=True,
        index=True
    )
    name = Column(String(256), nullable=True)
    status = Column(Boolean, default=True)
