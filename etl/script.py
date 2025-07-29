from typing import List
from pymongo import MongoClient
from pymongo.synchronous.database import Database
from neo4j import GraphDatabase, Session

from etl_types import CollectionContext, Document, MigrateCollection

# Configuración de Neo4j
neo4j_uri = "neo4j://127.0.0.1:7687"
neo4j_user = "neo4j"
neo4j_password = "12345678"

# Configuración de MongoDB
mongo_uri = "mongodb://localhost:27017"
mongo_db_name = "nosql"

def get_connections():
    try:
        mongo_client = MongoClient(mongo_uri)
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))
        driver.verify_connectivity()

        return mongo_client[mongo_db_name],driver
    except Exception as e:
        print(f"Error during connection: {e}")
        raise # stops the program

def clean_node_res(res:list[Document]) -> list[Document]:
    return list(map(lambda x: {**x['n'], '_id': x['node_id']}, res))

def migrate_species(db: Database, session: Session, context: CollectionContext) -> List[Document]:
    collection_name = "specie"
    collection = db[collection_name]
    documents = list(collection.find())

    for doc in documents:
        if '_id' in doc:
           doc.pop('_id')

    # we insert all in a single operation
    cypher_query = """
       UNWIND $documents AS doc
       CREATE (n:Specie)
       SET n = doc
       RETURN n, elementId(n) as node_id
    """

    res = clean_node_res(session.run(cypher_query, documents=documents).data())
    context.species = res
    return res

def migrate_weapons(db:Database, session:Session, context: CollectionContext) -> List[Document]:
    collection_name = "character"
    collection = db[collection_name]
    documents = list(collection.find())
    weapons = []

    for doc in documents:
        weapons.append(doc['weapon'])

    cypher_query = """
       UNWIND $documents AS doc
       CREATE (n:Weapon)
       SET n = doc
       RETURN n, elementId(n) as node_id
    """

    result = clean_node_res(session.run(cypher_query, documents=weapons).data())
    context.weapons = result
    return result

def migrate_vehicles(db: Database, session: Session, context: CollectionContext) -> List[Document]:
    collection_name = "vehicle"
    collection = db[collection_name]
    documents = list(collection.find())

    for doc in documents:
        if '_id' in doc:
           doc.pop('_id')

    # we insert all in a single operation
    cypher_query = """
       UNWIND $documents AS doc
       CREATE (n:Vehicle)
       SET n = doc
       RETURN n, elementId(n) as node_id
    """

    res = clean_node_res(session.run(cypher_query, documents=documents).data())
    context.vehicles = res
    return res

def migrate_faction(db: Database, session: Session, context: CollectionContext) -> List[Document]:
    collection_name = "faction"
    collection = db[collection_name]
    documents = list(collection.find())

    for doc in documents:
        if '_id' in doc:
           doc.pop('_id')

    # we insert all in a single operation
    cypher_query = """
       UNWIND $documents AS doc
       CREATE (n:Faction)
       SET n = doc
       RETURN n, elementId(n) as node_id
    """

    res = clean_node_res(session.run(cypher_query, documents=documents).data())
    context.factions = res
    return res

def migrate_planets(db: Database, session: Session, context: CollectionContext) -> List[Document]:
    collection_name = "planet"
    collection = db[collection_name]
    documents = list(collection.find())

    for doc in documents:
        if '_id' in doc:
           doc.pop('_id')
        for specie in doc['species_ids']:
            pass

    cypher_query = """
       UNWIND $documents AS doc
       CREATE (n:Planet)
       SET n = doc
       RETURN n, elementId(n) as node_id
    """

    res = clean_node_res(session.run(cypher_query, documents=documents).data())
    context.planets = res
    return res

def migrate_characters(db:Database):
    pass

def migrate_spaceships(db:Database):
    pass

def migrate_locations(db:Database):
    pass

def migrate_movies(db:Database):
    pass

def migrate_historic_events(db:Database):
    pass

migrators:List[MigrateCollection] = [migrate_species, migrate_weapons, migrate_vehicles, migrate_faction]

def migrate_data():
    db,target = get_connections()
    context = CollectionContext()

    with target.session() as session:
        # only during development
        clear_neo4j(session)

        for migrator in migrators:
            migrator(db,session,context)

def clear_neo4j(session: Session) -> None:
   cypher_query = """
   MATCH (n)
   DETACH DELETE n
   """
   session.run(cypher_query)
   print("Neo4j cleared successfully")

if __name__ == "__main__":
    migrate_data()
