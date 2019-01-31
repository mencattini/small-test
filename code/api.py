from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bottle import run
from sqlalchemy import exc
import warnings
from bottle import route, request, HTTPResponse
from model import User, Skill
from utilitiy import search, delete, create, set_ext


# create methods
@route("/user/create", method="PUT")
def user_create():
    # we get the json from REST
    json = request.json

    entry = create(json, User, Skill, session, "skills", "skill_id")

    try:
        session.add(entry)
        session.commit()
    except exc.IntegrityError:
        warnings.simplefilter("default", Warning)
        warnings.warn("You tried to add an already existing item.")
        session.rollback()
    return HTTPResponse(status=201)


@route("/skill/create", method="PUT")
def skill_create():
    # we get the json from REST
    json = request.json

    entry = create(json, Skill, User, session, "users", "user_id")

    try:
        session.add(entry)
        session.commit()
    except exc.IntegrityError:
        warnings.simplefilter("default", Warning)
        warnings.warn("You tried to add an already existing item.")
        session.rollback()
    return HTTPResponse(status=201)


# delete methods
@route("/user/delete", method="DELETE")
def user_delete():
    json = request.json
    delete(json, User, session)
    return HTTPResponse(status=200)


@route("/skill/delete", method="DELETE")
def skill_delete():
    json = request.json
    delete(json, Skill, session)
    return HTTPResponse(status=200)


# research methods
@route("/user/research")
def user_research():
    json = request.json
    results = search(json, User, session)

    return HTTPResponse(status=200, body="<br>".join([str(ele) for ele in results]))


@route("/skill/research")
def skill_research():
    json = request.json
    results = search(json, Skill, session)

    return HTTPResponse(status=200, body="<br>".join([str(ele) for ele in results]))


# update methods
@route("/user/update", method="POST")
def user_update():
    json = request.json
    my_class = User

    user_id = json.get("user_id", None)
    if not user_id:
        warnings.simplefilter("error", Warning)
        warnings.warn("You need to specify user_id")

    # we use the id to search user
    query = session.query(my_class).filter(
        getattr(my_class, "user_id") == json["user_id"]
    )
    row = query.first()

    row = set_ext(row, json, Skill, session, "skills", "skill_id")

    for key, value in json.items():
        setattr(row, key, value)

    session.commit()
    return HTTPResponse(stauts=200)


@route("/skill/update", method="POST")
def skill_update():
    json = request.json
    my_class = Skill

    skill_id = json.get("skill_id", None)
    if not skill_id:
        warnings.simplefilter("error", Warning)
        warnings.warn("You need to specify skill_id")

    # we use the id to search skill
    query = session.query(my_class).filter(
        getattr(my_class, "skill_id") == json["skill_id"]
    )
    row = query.first()

    row = set_ext(row, json, User, session, "users", "user_id")

    for key, value in json.items():
        setattr(row, key, value)

    session.commit()
    return HTTPResponse(stauts=200)


if __name__ == "__main__":
    # setup the ORM part with sqlalchemy
    engine = create_engine(f"sqlite:///../sqlite3.db")
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    run(host="localhost", port=8080, debug=True)
