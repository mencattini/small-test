from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    fullname = Column(String)
    address = Column(String)
    email = Column(String)
    mobile_phone = Column(Integer)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    level = Column(String)


class Credentials(Base):
    # very very very very bad practices
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    id_identification = Column(String, ForeignKey("users.email"))
    password = Column(String)


engine = create_engine("sqlite:///../sqlite3.db")

Base.metadata.create_all(engine)
