from typing import Dict, Any, List

def character_to_mongo(
    data: Dict[str, Any],
) -> Dict[str, Any]:

    name = data.get("name")
    gender = data.get("gender")
    height_str = data.get("height")
    mass_str = data.get("mass")
    homeworld_url = data.get("homeworld")
    species_urls = data.get("species", [])
    faction_ids = data.get("faction_ids", [])
    weapon = data.get("weapon", {})

    height = int(height_str) if height_str and height_str.lower() != 'unknown' else 0
    if height < 0:
        height = 0

    mass = int(mass_str.replace(',','')) if mass_str.replace(',', '').isdigit() else 0
    if mass < 0:
        mass = 0

    homeworld_id = homeworld_url
    species_id = None if len(species_urls) == 0 else species_urls[0]
    
    weapon_data = {
        "name": weapon.get("name", "None"),
        "type": weapon.get("type", "None"),
        "manufacturer": weapon.get("manufacturer", "None"),
    }
    if "crystal_color" in weapon and weapon["crystal_color"]:
        weapon_data["crystal_color"] = weapon["crystal_color"]

    return {
        "name": name,
        "gender": gender,
        "height": height,
        "mass": mass,
        "homeworld_id": homeworld_id,
        "species_id": species_id,
        "faction_ids": faction_ids,
        "weapon": weapon_data
    }
