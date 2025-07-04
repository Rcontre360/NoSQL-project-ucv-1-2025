# this file is necesary to import its stuff as a module

from .planet import planet_to_mongo
from .character import character_to_mongo
from .specie import specie_to_mongo
from .starship import starship_to_mongo
from .vehicle import vehicle_to_mongo
from .weapon import weapon_to_mongo
from .faction import faction_to_mongo
from .location import city_to_mongo
from .historic_event import battle_to_mongo

__all__ = [
    "planet_to_mongo"
    "character_to_mongo"
    "specie_to_mongo"
    "starship_to_mongo"
    "vehicle_to_mongo"
    "weapon_to_mongo"
    "faction_to_mongo"
    "city_to_mongo"
    "battle_to_mongo"
]

