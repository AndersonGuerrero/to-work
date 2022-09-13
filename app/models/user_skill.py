from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref

from app.db.base_class import Base


class UserSkill(Base):
    __tablename__ = "users_skills"
    user_id = Column(String, ForeignKey('users.id'), primary_key=True)
    skill_id = Column(String, ForeignKey('skills.id'), primary_key=True)

    value = Column(Integer)

    user = relationship('User', backref=backref('skills'))
    skill = relationship('Skill', backref=backref('users'))
