from neo4j import Session
from pymongo.synchronous.database import Database
from typing import Any, Callable,  List

Document = dict[str,Any]

class CollectionContext:
    species: List[Document]
    weapons: List[Document]
    vehicles: List[Document]
    characters: List[Document]
    factions: List[Document]
    historic_events: List[Document]
    planets: List[Document]
    spaceships: List[Document]

    def __init__(self):
       self.species = []
       self.weapons = []
       self.vehicles = []
       self.characters = []
       self.factions = []
       self.historic_events = []
       self.planets = []
       self.spaceships = []

MigrateCollection = Callable[[Database, Session, CollectionContext], List[Document]]

