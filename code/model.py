from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.orm import relationship

Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("skill_id", Integer, ForeignKey("skills.skill_id")),
)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    fullname = Column(String)
    email = Column(String)
    address = Column(String)
    mobile_phone = Column(Integer)

    skills = relationship("Skill", secondary=association_table)


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(String)


engine = create_engine("sqlite:///../sqlite3.db")

Base.metadata.create_all(engine)
