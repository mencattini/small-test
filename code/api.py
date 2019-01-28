from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from model import User, Skill, Credentials
import warnings
from bottle import route, response, run, request
from json import dumps


def serialize_object(obj):
    dic = obj.__dict__.copy()
    for key, value in obj.__dict__.items():
        if "_" in key or "_" in key:
            del (dic[key])
    return dic


def init_operation(d):
    class_type = {}
    class_type["user"] = User
    class_type["skill"] = Skill
    class_type["credentials"] = Credentials

    entry = class_type.get(d["type"].lower(), "error")
    if entry == "error":
        warnings.simplefilter("error", Warning)
        warnings.warn("Unknown type")
    return entry


@route("/crud/create", method="PUT")
def create():

    json = request.json
    entry = init_operation(json)()
    attributes = [attr for attr in dir(entry) if not attr.startswith("__")]

    for key in json.keys():
        if key != "type" and key in attributes:
            setattr(entry, key, json[key])

    session.add(entry)
    session.commit()


@route("/crud/delete", method="DELETE")
def delete():
    results = research()
    for ele in results:
        session.delete(ele)
    session.commit()


@route("/crud/research")
def research():
    json = request.json
    my_class = init_operation(json)
    del json["type"]

    query = session.query(my_class)
    for key, value in json.items():
        query = query.filter(getattr(my_class, key) == value)
    results = query.all()
    response.content_type = "application/json"

    return dumps([serialize_object(ele) for ele in results])


@route("/crud/update", method="PUT")
def update():
    my_class = init_operation(d)

    new_value = d["new_value"]
    del d["type"]
    del d["new_value"]
    query = session.query(my_class)
    for key, value in d.items():
        query = query.filter(getattr(my_class, key) == value)
    row = query.first()

    for key, value in new_value.items():
        setattr(row, key, value)

    session.commit()


if __name__ == "__main__":
    # setup the ORM part with sqlalchemy
    engine = create_engine(f"sqlite:///../sqlite3.db")
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    run(host="localhost", port=8080, debug=True)
