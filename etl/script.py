from typing import List
from pymongo.synchronous.database import Database
from neo4j import Session

from common import Document, MigrateCollection, create_nodes_from_docs, create_relationships, get_connections, transform_response

# Configuración de Neo4j
neo4j_uri = "neo4j://127.0.0.1:7687"
neo4j_user = "neo4j"
neo4j_password = "12345678"

# Configuración de MongoDB
mongo_uri = "mongodb://localhost:27017"
mongo_db_name = "nosql"


def migrate_species(db: Database, session: Session) -> List[Document]:
    collection_name = "specie"
    collection = db[collection_name]
    documents = list(collection.find())

    for doc in documents:
        if '_id' in doc:
           doc['mongo_id'] = str(doc.pop('_id'))

    res = create_nodes_from_docs(session, "Specie", documents)
    return res

def migrate_vehicles(db: Database, session: Session) -> List[Document]:
    collection_name = "vehicle"
    collection = db[collection_name]
    documents = list(collection.find())

    for doc in documents:
        if '_id' in doc:
           doc['mongo_id'] = str(doc.pop('_id'))

    res = create_nodes_from_docs(session, "Vehicle", documents)
    return res

def migrate_faction(db: Database, session: Session) -> List[Document]:
    collection_name = "faction"
    collection = db[collection_name]
    documents = list(collection.find())

    for doc in documents:
        if '_id' in doc:
           doc['mongo_id'] = str(doc.pop('_id'))

    res = create_nodes_from_docs(session, "Faction", documents)
    return res

def migrate_planets(db: Database, session: Session) -> List[Document]:
   collection_name = "planet"
   collection = db[collection_name]
   documents = list(collection.find())
   for doc in documents:
       if '_id' in doc:
          doc['mongo_id'] = str(doc.pop('_id'))
       if 'species_ids' in doc:
           doc.pop('species_ids')

   res = create_nodes_from_docs(session,"Planet",documents)
   create_relationships(collection.find(), session, "species_ids", "Planet", "HOSTS", "Specie")

   return res

def migrate_characters(db: Database, session: Session) -> List[Document]:
    collection_name = "character"
    collection = db[collection_name]
    documents = list(collection.find())
    weapons = []

    weapon_id=0
    for doc in documents:
        doc['mongo_id'] = str(doc.pop('_id'))
        doc.pop('homeworld_id')
        doc.pop('species_id')
        doc.pop('faction_ids')
        weapons.append({**doc.pop('weapon'), 'character_id': doc['mongo_id'], '_id':weapon_id})
        weapon_id+=1

    res = create_nodes_from_docs(session,"Character",documents)
    res = create_nodes_from_docs(session,"Weapon",weapons)

    create_relationships(collection.find(),session,"homeworld_id","Character","HABITS","Planet")
    create_relationships(collection.find(),session,"species_id","Character","IS","Specie")
    create_relationships(collection.find(),session,"faction_ids","Character","BELONGS","Faction")
    create_relationships(weapons,session,"character_id","Weapon","IS_OWNED_BY","Character")

    return res

def migrate_spaceships(db: Database, session: Session) -> List[Document]:
   collection_name = "spaceship"
   collection = db[collection_name]
   documents = list(collection.find())

   for doc in documents:
        doc['mongo_id'] = str(doc.pop('_id'))
        doc.pop('pilot_id')
        doc.pop('faction_id')

   res = create_nodes_from_docs(session,"Spaceship",documents)

   create_relationships(collection.find(), session, "pilot_id", "Spaceship", "PILOTED_BY", "Character")
   create_relationships(collection.find(), session, "faction_id", "Spaceship", "BELONGS", "Faction")

   return res

def migrate_location(db: Database, session: Session) -> List[Document]:
    collection_name = "location"
    collection = db[collection_name]
    documents = list(collection.find())

    for doc in documents:
        if 'coordinates' in doc:
            coord = doc.pop('coordinates')
            doc['latitude'] = coord['latitude']
            doc['longitude'] = coord['longitude']

        doc['mongo_id'] = str(doc.pop('_id'))
        doc.pop('planet_id')

    res = create_nodes_from_docs(session,"Location",documents)

    create_relationships(collection.find(), session, "planet_id", "Location", "LOCATED_AT", "Planet")

    return res

def migrate_movies(db: Database, session: Session) -> List[Document]:
   collection_name = "movie"
   collection = db[collection_name]
   documents = list(collection.find())
   docs_copy = []
   # WE ARE CREATING A NEW OBJECT CALLED ACTOR
   actors = []

   actor_id = 0
   for doc in documents:
        doc['mongo_id'] = str(doc['_id'])
        doc['_id'] = str(doc['_id'])
        without_arrs = dict(doc)

        doc['character_ids'] = []
        doc['actor_ids'] = []
        doc['starship_ids'] = []

        # movie points to actor and actor and characters. Actor also points to character
        for char in doc['characters']:
            char['character_id'] = str(char['character_id'])
            actors.append({**char,'_id':str(actor_id)})

            doc['character_ids'].append(char['character_id'])
            doc['actor_ids'].append(actor_id)

        for star in doc['starships']:
            doc['starship_ids'].append(str(star['starship_id']))

        # now we have character_ids and actor_ids to point to them
        doc.pop('characters')
        doc.pop('starships')
        without_arrs.pop('characters')
        without_arrs.pop('starships')

        docs_copy.append(without_arrs)

   res = create_nodes_from_docs(session,"Movie",docs_copy)
   res = create_nodes_from_docs(session,"Actor",actors)

   # movie => relations
   create_relationships(documents, session, "starship_ids", "Movie", "SHOWS", "Spaceship")
   create_relationships(documents, session, "actor_ids", "Movie", "FEATURES", "Actor")
   create_relationships(documents, session, "character_ids", "Movie", "INCLUDES", "Character")

   # actor => character
   create_relationships(actors, session, "character_id", "Actor", "PLAYS", "Character")

   return res

def migrate_historic_events(db: Database, session: Session) -> List[Document]:
    collection_name = "historic_event"
    collection = db[collection_name]
    documents = list(collection.find())
    docs_copy = []

    for doc in documents:
        cpy = dict(doc)
        cpy['mongo_id'] = str(cpy.pop('_id'))
        doc['movie_id'] = str(doc.pop('movie_id'))

        # factions relations will only have role as metadata
        for fact in doc['factions']:
            # we already have the name on the faction node
            fact.pop('name')
            # for compatibility with the create relation function
            fact['_id'] = str(fact.pop('faction_id'))

        # factions relations will only have role as metadata
        for char in doc['characters']:
            # we already have the name on the faction node
            char.pop('name')
            # for compatibility with the create relation function
            char['_id'] = str(char.pop('character_id'))

        doc['locations'] = list(map(lambda loc:str(loc.pop('location_id')), doc['locations']))

        cpy.pop('factions')
        cpy.pop('characters')
        cpy.pop('movie_id')
        cpy.pop('locations')
        docs_copy.append(cpy)

    res = create_nodes_from_docs(session,"HistoricEvent",docs_copy)

    create_relationships(documents, session, "movie_id", "HistoricEvent", "APPEARS_AT", "Movie")
    create_relationships(documents, session, "factions", "HistoricEvent", "HAS_PARTICIPATION", "Faction")
    create_relationships(documents, session, "characters", "HistoricEvent", "HAS_CHARACTER", "Character")

    return res


migrators:List[MigrateCollection] = [migrate_species, migrate_vehicles, migrate_faction, migrate_planets, migrate_characters, migrate_spaceships, migrate_location, migrate_movies, migrate_historic_events]

def migrate_data():
    db,target = get_connections(mongo_uri,mongo_db_name, neo4j_uri, (neo4j_user, neo4j_password))

    with target.session() as session:
        # only during development
        clear_neo4j(session)

        for migrator in migrators:
            migrator(db,session)

def clear_neo4j(session: Session) -> None:
   cypher_query = """
   MATCH (n)
   DETACH DELETE n
   """
   session.run(cypher_query)
   print("Neo4j cleared successfully")

if __name__ == "__main__":
    migrate_data()
