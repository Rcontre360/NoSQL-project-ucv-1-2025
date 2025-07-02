import re
from typing import Dict, Any, List

def character_to_mongo(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data.get("name")
    gender = data.get("gender")
    height_str = data.get("height")
    mass_str = data.get("mass")
    homeworld_url = data.get("homeworld")
    species_urls = data.get("species", [])

    try:
        height = int(height_str) if height_str and height_str.lower() != 'unknown' else 0
        if height < 0:
            height = 0
    except (ValueError, TypeError):
        height = 0

    try:
        mass = int(mass_str) if mass_str and mass_str.lower() != 'unknown' and mass_str.replace(',', '').isdigit() else 0
        if mass < 0:
            mass = 0
    except (ValueError, TypeError):
        mass = 0

    homeworld_id = None
    if homeworld_url:
        match = re.search(r'/(\d+)/?$', homeworld_url)
        if match:
            # In a real scenario, this would involve looking up/generating a true ObjectId
            # For now, we use a placeholder or convert to int if ObjectIds are not generated externally.
            # As per instruction "dont worry about the external ids", we assume this is handled later.
            homeworld_id = f"placeholder_objectId_{match.group(1)}"
        else:
            homeworld_id = "invalid_homeworld_id"

    species_id = None
    if species_urls and isinstance(species_urls, list) and len(species_urls) > 0:
        # Assuming a character belongs to a single species for 'species_id'
        # If multiple species are possible and you need to link all, schema would need 'species_ids' (array)
        # For simplicity, taking the first one if multiple are present, or a placeholder if none.
        first_species_url = species_urls[0]
        match = re.search(r'/(\d+)/?$', first_species_url)
        if match:
            species_id = f"placeholder_objectId_{match.group(1)}"
        else:
            species_id = "invalid_species_id"
    elif not species_urls:
         # If species is an empty list as per the example, provide a default placeholder or None
         species_id = "placeholder_objectId_unknown_species" # Or None if schema allows for null ObjectIds

    faction_ids: List[Any] = [] # Faction info is not in source data, so empty list.

    return {
        "name": name,
        "gender": gender,
        "height": height,
        "mass": mass,
        "homeworld_id": homeworld_id,
        "species_id": species_id,
        "faction_ids": faction_ids
    }
