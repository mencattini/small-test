from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from model import User, Skill, Credentials
import argparse
import warnings
import json


def init_cli():
    parser = argparse.ArgumentParser(description="CRUD system")

    parser.add_argument("--db", type=str, help="Path of the database.", default=".")
    parser.add_argument(
        "--operation",
        type=str,
        help="Type of operation we want to do. Possible operations are [create, research, update, delete",
    )

    # put the json.loads as type doesn't work. Don't know why. So need a small trick to return a json
    parser.add_argument(
        "--json",
        type=json.loads,
        help='A json structure with the mandatory field from wished operation such as\
        "{"type": "user","firstname":"rené","lastname":"Marshall"}"',
    )
    return parser.parse_args()


def create(d, session):
    class_type = {}
    class_type["user"] = User()
    class_type["skill"] = Skill()
    class_type["credentials"] = Credentials()

    entry = class_type.get(d["type"].lower(), "error")
    if entry == "error":
        warnings.simplefilter("error", Warning)
        warnings.warn("Unknown type")

    attributes = [attr for attr in dir(entry) if not attr.startswith("__")]
    for key in d.keys():
        if key != "type" and key in attributes:
            entry.__dict__[key] = d[key]

    # TODO add a research to check the unique constraint
    session.add(entry)
    session.commit()


def delete(d, session):
    pass


def research(d, session):
    pass


def update(d, session):
    pass


if __name__ == "__main__":
    # init the cli arguments
    args = init_cli()
    # setup the ORM part with sqlalchemy
    engine = create_engine(f"sqlite:///{args.db}/sqlite3.db")
    Base = declarative_base()
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    operations = {}
    operations["create"] = create
    operations["research"] = research
    operations["update"] = update
    operations["delete"] = delete
    create(args.json, session)
