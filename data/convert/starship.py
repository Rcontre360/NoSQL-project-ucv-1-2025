import re
from typing import Dict, Any

def starship_to_mongo(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data.get("name")
    model = data.get("model")
    starship_class = data.get("starship_class")
    manufacturer = data.get("manufacturer")
    length_str = data.get("length")
    crew_str = data.get("crew")
    pilots = data.get("pilots", []) # Source has a list of pilot URLs

    try:
        # Length can have spaces, remove them and convert to float
        length = float(length_str.replace(" ", "")) if length_str and length_str.lower() not in ('unknown', 'n/a') else 0.0
        if length < 0:
            length = 0.0
    except (ValueError, TypeError):
        length = 0.0

    min_crew = 0
    if crew_str and crew_str.lower() != 'unknown':
        try:
            # Extract the first number if it's a range (e.g., "30-165" -> 30)
            crew_parts = re.split(r'[-–]', crew_str.replace(',', '').strip())
            min_crew = int(crew_parts[0])
            if min_crew < 0:
                min_crew = 0
        except (ValueError, TypeError):
            min_crew = 0

    # As per instruction "dont worry about the external ids", provide placeholders or None
    pilot_id = None
    if pilots and isinstance(pilots, list) and len(pilots) > 0:
        # Taking the first pilot's ID as a placeholder
        match = re.search(r'/(\d+)/?$', pilots[0])
        if match:
            pilot_id = f"placeholder_objectId_{match.group(1)}"
        else:
            pilot_id = "invalid_pilot_id_format"
    # If no pilots, and pilot_id is required, we still need a placeholder
    if pilot_id is None:
         pilot_id = "placeholder_objectId_no_pilot"

    # Faction information is not present in the source data, so provide a placeholder
    faction_id = "placeholder_objectId_no_faction"

    return {
        "name": name,
        "model": model,
        "class": starship_class,
        "manufacturer": manufacturer,
        "length": length,
        "min_crew": min_crew,
        "pilot_id": pilot_id,
        "faction_id": faction_id
    }
