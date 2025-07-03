
from typing import List, Dict, Any, Optional

from common import read_json_to_list_of_dicts, save_list_to_json_file, read_csv_to_list_of_dicts
from convert import (
    specie_to_mongo,
    planet_to_mongo,
    weapon_to_mongo,
    vehicle_to_mongo,
    faction_to_mongo,
    character_to_mongo,
    starship_to_mongo
)

def find_by_field(field_name: str, field_value: Any, data_array: List[Dict]) -> Optional[Dict]:
    for item in data_array:
        if field_name in item:
            item_value = item[field_name]
            if item_value.lower() == field_value.lower():
                return item
            elif item_value == field_value:
                return item
    return None

# save species first since they dont have relations
species = read_json_to_list_of_dicts("./raw/species.json")
clean_species = list(map(lambda s:specie_to_mongo(s),species))
clean_species = save_list_to_json_file(clean_species,"./clean/species.json")

# now weapons
weapons = read_csv_to_list_of_dicts("./raw/weapons.csv")
clean_weapons = list(map(lambda w:weapon_to_mongo(w),weapons))
clean_weapons = save_list_to_json_file(weapons,"./clean/weapons.json")

# now vehicles
vehicles = read_json_to_list_of_dicts("./raw/vehicles.json")
clean_vehicles = list(map(lambda s:vehicle_to_mongo(s),vehicles))
clean_vehicles = save_list_to_json_file(clean_vehicles,"./clean/vehicles.json")

# now factions
factions = read_csv_to_list_of_dicts("./raw/organizations.csv")
clean_factions = list(map(lambda s:faction_to_mongo(s),factions))
clean_factions = save_list_to_json_file(clean_factions,"./clean/factions.json")

def find_specie_by_name(name:str):
    el = list(filter(lambda s:s['name'].lower()==name, clean_species))
    return None if len(el) == 0 else el[0]

# planets is next. need a csv with planets species
planets = read_json_to_list_of_dicts('./raw/planets.json')
planets_clean = list(map(lambda p:planet_to_mongo(p),planets))
species_with_planets = read_csv_to_list_of_dicts("./raw/species_with_planets.csv")

for p in planets_clean:
    for sp in species_with_planets:
        if sp['homeworld'].lower() == p['name'].lower():
            # find actual specie
            cur_sp = find_specie_by_name(sp['name'].lower())
            if cur_sp:
                p['species_ids'].append(cur_sp['_id'])

planets_clean = save_list_to_json_file(planets_clean, "./clean/planets.json")

# now characters (a hard one)
raw_characters = read_json_to_list_of_dicts("./raw/characters.json")

for rchar in raw_characters:
    rplanet = list(filter(lambda rp: rp['url'].lower() == rchar['homeworld'].lower(), planets))

    if len(rplanet) > 0:
        planet = list(filter(lambda p: p['name'].lower() == rplanet[0]['name'].lower(), planets_clean))
        if len(planet) > 0:
            rchar['homeworld'] = planet[0]['_id']

    # if it has a species pointer, search for its name
    if len(rchar['species']) > 0:
        rspecie = list(filter(lambda rs: rs['url'].lower() == rchar['species'][0], species))
        if len(rspecie) > 0:
            specie = list(filter(lambda p: p['name'].lower() == rspecie[0]['name'].lower(), clean_species))
            if len(specie) > 0:
                rchar['species'] = [specie[0]['_id']]

characters_clean = list(map(lambda cc:character_to_mongo(cc), raw_characters))
characters_clean = save_list_to_json_file(characters_clean, "./clean/characters.json")

# now starships. We will filter those whout pilots
raw_spaceships = read_json_to_list_of_dicts("./raw/starships.json")
# only those with pilots
raw_spaceships = list(filter(lambda rs: len(rs['pilots']) > 0, raw_spaceships))

for rship in raw_spaceships:
    first_pilot = rship['pilots'][0]
    pilot_info = find_by_field("url",first_pilot, raw_characters)
    if pilot_info != None:
        clean_pilot = find_by_field('name',pilot_info['name'],characters_clean)
        if clean_pilot != None:
            rship['pilots'] = [clean_pilot['_id']]

spaceship_clean = list(map(lambda sc:starship_to_mongo(sc), raw_spaceships))
spaceship_clean = save_list_to_json_file(spaceship_clean, "./clean/spaceships.json")
