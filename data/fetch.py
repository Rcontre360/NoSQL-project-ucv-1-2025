
import requests
import os

from typing import Any, Dict
from convert import planet_to_mongo, character_to_mongo, specie_to_mongo, vehicle_to_mongo, starship_to_mongo
from common import save_list_to_json_file

def make_fetch(url:str) -> list[Dict[str, Any]]:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url} data: {e}")
        return []

def fetch_planets():
    url = f"https://swapi.info/api/planets"
    res = make_fetch(url)
    return list(map(lambda p: planet_to_mongo(p),res))

def fetch_characters():
    url = f"https://swapi.info/api/people"
    res = make_fetch(url)
    return list(map(lambda p: character_to_mongo(p),res))

def fetch_species():
    url = f"https://swapi.info/api/species"
    res = make_fetch(url)
    return list(map(lambda p: specie_to_mongo(p),res))

def fetch_vehicles():
    url = f"https://swapi.info/api/vehicles"
    res = make_fetch(url)
    return list(map(lambda p: vehicle_to_mongo(p),res))

def fetch_starships():
    url = f"https://swapi.info/api/starships"
    res = make_fetch(url)
    return list(map(lambda p: starship_to_mongo(p),res))

folder_name = "raw"

try:
    os.mkdir(folder_name)
except FileExistsError:
    pass
except Exception as e:
    print(f"An error occurred: {e}")

planets = fetch_planets()
characters = fetch_characters()
species = fetch_species()
vehicles = fetch_vehicles()
starships = fetch_starships()

save_list_to_json_file(planets, "./raw/planets.json")
save_list_to_json_file(characters, "./raw/characters.json")
save_list_to_json_file(vehicles, "./raw/vehicles.json")
save_list_to_json_file(species, "./raw/species.json")
save_list_to_json_file(starships, "./raw/starships.json")

