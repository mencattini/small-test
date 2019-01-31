def delete(json, classe, session):
    results = search(json, classe, session)

    for ele in results:
        session.delete(ele)
    session.commit()


def search(json, classe, session):
    query = session.query(classe)
    for key, value in json.items():
        query = query.filter(getattr(classe, key) == value)
    results = query.all()

    return results


def create(json, classe, secondary_classe, session, ext, ext_id):
    # get all attributes
    entry = classe()
    attributes = [attr for attr in dir(entry) if not attr.startswith("__")]
    # set the ext attr
    entry = set_ext(entry, json, secondary_classe, session, ext, ext_id)

    # we set all attr except skill
    for key in json.keys():
        if key in attributes:
            setattr(entry, key, json[key])

    return entry


def set_ext(entry, json, secondary_classe, session, ext, ext_id):

    ext_attr = json.get(ext, None)
    if ext_attr == []:
        del json[ext]
        setattr(entry, ext, [])
    elif ext_attr:
        del json[ext]
        # we search if the ext_attr exists as object in database for each external attributes
        for ele in ext_attr:
            # so we search into the seconadry classe database
            results = search({ext_id: ele}, secondary_classe, session)
            # we check that attr arent already in the object attribute and if not we had it
            for res in results:
                if res not in getattr(entry, ext):
                    setattr(entry, ext, getattr(entry, ext) + [res])
    return entry
