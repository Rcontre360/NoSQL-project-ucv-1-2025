
from typing import List, Dict, Any, Optional

from common import read_json_to_list_of_dicts, save_list_to_json_file, read_csv_to_list_of_dicts
from convert import (
    specie_to_mongo,
    planet_to_mongo,
    weapon_to_mongo,
    vehicle_to_mongo,
    faction_to_mongo,
    character_to_mongo,
    starship_to_mongo,
    city_to_mongo,
    battle_to_mongo,
    movie_to_mongo
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
raw_characters_weapons = read_json_to_list_of_dicts("./manual/characters-weapons.json")
print("raw_characters_weapons: ", raw_characters_weapons)

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

    # if it has weapons
    char_weapon_info = next((cw for cw in raw_characters_weapons if cw['character_name'].lower() == rchar['name'].lower()), None)
    print("char_weapon_info: ", char_weapon_info)

    if char_weapon_info and 'weapon_name' in char_weapon_info:
        weapon_data = next((w for w in clean_weapons if w['name'].lower() == char_weapon_info['weapon_name'].lower()), None)
        if weapon_data:
            rchar['weapon'] = {
                'name': weapon_data['name'],
                'type': weapon_data['type'],
                'manufacturer': weapon_data['manufacturer']
            }
            if 'color' in char_weapon_info:
                rchar['weapon']['crystal_color'] = char_weapon_info['color']

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

# now with locations! for now we only have cities
raw_cities = read_csv_to_list_of_dicts("./raw/cities.csv")
cities_clean = list(map(lambda c: city_to_mongo(c),raw_cities))

for city in cities_clean:
    planet = find_by_field('name', city['planet_id'], planets_clean)
    if planet:
        city['planet_id'] = planet['_id']

cities_clean = save_list_to_json_file(cities_clean, "./clean/locations.json")

# now with historic events. for now we only have battles
raw_battles = read_csv_to_list_of_dicts('./raw/battles.csv')
battles_clean = list(map(lambda c: battle_to_mongo(c),raw_battles))

def character_to_historic(clean_char: dict) -> dict:
    return {
        "character_id":str(clean_char['_id']),
        "name":clean_char['name'],
        "role": ""
    }

for battle in battles_clean:
    for fact in battle['factions']:
        clean_fact = find_by_field('name',fact['name'],clean_factions)
        if clean_fact != None:
            fact['faction_id'] = str(clean_fact['_id'])
            fact['name'] = clean_fact['name']
            # lets get all characters of this faction
            battle_characters = list(filter(lambda char: clean_fact['_id'] in char['faction_ids'], characters_clean))
            battle_characters = list(map(character_to_historic,battle_characters))

            battle['characters']+=battle_characters

battles_clean = save_list_to_json_file(battles_clean, "./clean/historic_events.json")

# finally, movies
movies_raw = read_json_to_list_of_dicts("./raw/movies.json")
movies_clean = list(map(lambda c: movie_to_mongo(c),movies_raw))

for movie in movies_clean:
    new_chars = []
    new_spaceships = []
    for char_url in movie['characters']:
        raw_char = find_by_field('url',char_url,raw_characters)
        clean_char = find_by_field('name', raw_char['name'], characters_clean)
        new_chars.append({
            'character_id':clean_char['_id'],
            'name':clean_char['name'],
            'role':'',
        })

    for ship_url in movie['starships']:
        raw_ship = find_by_field('url',ship_url,raw_spaceships)
        if raw_ship != None:
            clean_ship = find_by_field('name', raw_ship['name'], spaceship_clean)
            new_spaceships.append({
                'starship_id':clean_ship['_id'],
                'name':clean_ship['name'],
            })

    movie['characters'] = new_chars
    movie['starships'] = new_spaceships

movies_clean = save_list_to_json_file(movies_clean, "./clean/movies.json")
