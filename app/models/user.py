from sqlalchemy import Integer, String, Column

from app.helpers import generate_uuid
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"
    id = Column(
        String,
        default=generate_uuid,
        primary_key=True,
        index=True
    )
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    email = Column(String, index=True, nullable=False)
    years_previous_experience = Column(Integer, default=False)
