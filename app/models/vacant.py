from sqlalchemy import Integer, String, Column, Enum

from app.helpers import generate_uuid, CurrencyEnum
from app.db.base_class import Base


class Vacant(Base):
    __tablename__ = "vacants"
    id = Column(
        String,
        default=generate_uuid,
        primary_key=True,
        index=True
    )
    vacancy_link = Column(String(256), nullable=False)
    position_name = Column(String(256), nullable=False)
    company_name = Column(String(256), nullable=False)
    salary = Column(Integer, default=False)
    currency = Column(
        Enum(CurrencyEnum),
        default=CurrencyEnum.USD,
        nullable=False
    )
