from neo4j import GraphDatabase, Session
from pymongo import MongoClient
from pymongo.synchronous.database import Database
from typing import Any, Callable, Iterable,  List

Document = dict[str,Any]
MigrateCollection = Callable[[Database, Session], List[Document]]

def get_connections(mongo_uri:str, mongo_db_name:str, neo4j_uri:str, auth:tuple[str,str]):
    try:
        mongo_client = MongoClient(mongo_uri)
        driver = GraphDatabase.driver(neo4j_uri, auth=auth)
        driver.verify_connectivity()

        return mongo_client[mongo_db_name],driver
    except Exception as e:
        print(f"Error during connection: {e}")
        raise # stops the program

def transform_response(res:list[Document]) -> list[Document]:
    return list(map(lambda x: {**x['n'], '_id': x['node_id']}, res))

def create_nodes_from_docs(session:Session, node:str, docs:list[Document]) -> Any:
    cypher_query:Any = f"""
       UNWIND $documents AS doc
       CREATE (n:{node})
       SET n = doc
       RETURN n, elementId(n) as node_id
    """

    return transform_response(session.run(cypher_query, documents=docs).data())

def create_relationships(
    documents: Any,
    session: Session,
    match_field: str,
    source_node: str,
    relation_name: str,
    target_node: str,
):
    for doc in documents:
        source_id = str(doc['_id'])
        if match_field in doc:
            field_value = doc[match_field]
            target_ids = field_value if isinstance(field_value, list) else [field_value]
            for item in target_ids:
                # this conditions check if the id object has more metadata. This metadata will be added to the relationship
                if isinstance(item,Iterable) and '_id' in item:
                    target_id = str(item['_id'])
                    metadata = {k: v for k, v in item.items() if k != '_id'}

                    relationship_query: Any = f"""
                    MATCH (s:{source_node} {{mongo_id: $source_id}})
                    MATCH (t:{target_node} {{mongo_id: $target_id}})
                    CREATE (s)-[r:{relation_name}]->(t)
                    SET r = $metadata
                    """
                    session.run(relationship_query,
                              source_id=source_id,
                              target_id=target_id,
                              metadata=metadata)
                else:
                    target_id = str(item)
                    relationship_query: Any = f"""
                    MATCH (s:{source_node} {{mongo_id: $source_id}})
                    MATCH (t:{target_node} {{mongo_id: $target_id}})
                    CREATE (s)-[:{relation_name}]->(t)
                    """
                    session.run(relationship_query,
                              source_id=source_id,
                              target_id=target_id)
