from pymongo import MongoClient
from neo4j import GraphDatabase

# Configuración de Neo4j
neo4j_uri = "neo4j://127.0.0.1:7687"
neo4j_user = "neo4j"
neo4j_password = "bdyari123"

# Configuración de MongoDB
mongo_uri = "mongodb://localhost:27017"
mongo_db_name = "NoSQLProy"
mongo_collection_name = "vehicle"

def migrate_data():

    try:
        # Conexión a MongoDB
        mongo_client = MongoClient(mongo_uri)
        print("mongo_client: ", mongo_client)
        db = mongo_client[mongo_db_name]
        print("db: ", db)
        collection = db[mongo_collection_name]
        print("collection: ", collection)

        # Conexión a Neo4j
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

        # Obtención de colecciones MongoDB
        collection_names = db.list_collection_names()
        print(f"Colecciones encontradas en '{mongo_db_name}': {collection_names}")

        with driver.session() as session:
            for collection_name in collection_names:
                print(f"\n--- Migrando colección: '{collection_name}' ---")
                collection = db[collection_name]

                for document in collection.find():
                    print(document)
                    session.execute_write(create_node_from_document, document, collection_name)
                print(f"Colección '{collection_name}' migrada exitosamente.")

    except Exception as e:
        print(f"Error durante la migración: {e}")
    finally:
        if 'mongo_client' in locals():
            mongo_client.close()
        if 'driver' in locals():
            driver.close()


def create_node_from_document(tx, document, collection_label):
    if '_id' in document:
        document.pop('_id')

    properties_parts = []
    for key, value in document.items():
        if isinstance(value, str):
            escaped_value = value.replace("'", "\\'")
            properties_parts.append(f"{key}: '{escaped_value}'")
        else:
            properties_parts.append(f"{key}: {value}")

    properties_string = ", ".join(properties_parts)
    
    query = f"CREATE (n:{collection_label} {{{properties_string}}})"
    tx.run(query)


if __name__ == "__main__":
    migrate_data()