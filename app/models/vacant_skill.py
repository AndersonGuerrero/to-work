from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref

from app.db.base_class import Base


class VacantSkill(Base):
    __tablename__ = "vacants_skills"

    vacant_id = Column(String, ForeignKey('vacants.id'), primary_key=True)
    skill_id = Column(String, ForeignKey('skills.id'), primary_key=True)

    value = Column(Integer)

    vacant = relationship('Vacant', backref=backref('required_skills'))
    skill = relationship('Skill', backref=backref('vacants'))
