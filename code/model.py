from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    PrimaryKeyConstraint,
    create_engine,
    Table,
)
from sqlalchemy.orm import relationship

Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("skill_id", Integer, ForeignKey("skills.skill_id")),
    PrimaryKeyConstraint("user_id", "skill_id"),
)


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    fullname = Column(String)
    email = Column(String)
    address = Column(String)
    mobile_phone = Column(String)

    skills = relationship("Skill", secondary=association_table, backref="users")

    def __repr__(self):
        return (
            f"User(user_id={self.user_id}, firstname={self.firstname}, lastname={self.lastname}"
            + f", fullname={self.fullname}, email={self.email}, address={self.address},"
            + f" mobile_phone={self.mobile_phone}, skills={[ele.skill_id for ele in self.skills]})"
        )


class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True)
    name = Column(String)
    level = Column(String)

    def __repr__(self):
        return f"Skill(skill_id={self.skill_id}, name={self.name}, level={self.level}"


engine = create_engine("sqlite:///../sqlite3.db")

Base.metadata.create_all(engine)
