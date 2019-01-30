from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bottle import run
from sqlalchemy import exc
import warnings
from bottle import route, request, HTTPResponse
from model import User, Skill


def search(json, classe):
    query = session.query(classe)
    for key, value in json.items():
        query = query.filter(getattr(classe, key) == value)
    results = query.all()

    return results


@route("/user/create", method="PUT")
def user_create():
    # we get the json from REST
    json = request.json

    # get all attributes
    entry = User()
    attributes = [attr for attr in dir(entry) if not attr.startswith("__")]
    # take away the away the skill_id if exists
    skills = json.get("skills", [])
    if skills:
        del json["skills"]
        # we search if the skill exists for each skill
        for skill in skills:
            results = search({"skill_id": skill}, Skill)
            # we check that skill arent already in the user skills and if not we had it
            for skill in results:
                if skill not in entry.skills:
                    entry.skills += [skill]

    # we set all attr except skill
    for key in json.keys():
        if key != "type" and key in attributes:
            setattr(entry, key, json[key])

    try:
        session.add(entry)
        session.commit()
    except exc.IntegrityError:
        warnings.simplefilter("default", Warning)
        warnings.warn("You tried to add an already existing item.")
        session.rollback()
    return HTTPResponse(status=201)


@route("/user/delete", method="DELETE")
def user_delete():
    json = request.json
    my_class = User
    results = search(json, my_class)

    for ele in results:
        session.delete(ele)
    session.commit()
    return HTTPResponse(status=200)


@route("/user/research")
def user_research():
    json = request.json
    results = search(json, User)

    return HTTPResponse(status=200, body="<br>".join([str(ele) for ele in results]))


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

    # we check the skills
    skills = json.get("skills", None)
    # if it exists
    if skills == []:
        del json["skills"]
        setattr(row, "skills", [])
    elif skills:
        del json["skills"]
        # we search if the skill exists for each skill
        for skill_id in skills:
            results = search({"skill_id": skill_id}, Skill)
            # we check that skill arent already in the user skills and if not we had it
            for skill in results:
                if skill not in row.skills:
                    row.skills += [skill]

    for key, value in json.items():
        setattr(row, key, value)

    session.commit()
    return HTTPResponse(stauts=200)


# TODO add the same function for skill

if __name__ == "__main__":
    # setup the ORM part with sqlalchemy
    engine = create_engine(f"sqlite:///../sqlite3.db")
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    run(host="localhost", port=8080, debug=True)
