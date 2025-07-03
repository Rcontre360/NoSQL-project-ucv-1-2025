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
        crew_parts = re.split(r'[-–]', crew_str.replace(',', '').strip())
        min_crew = int(crew_parts[0])

    pilot_id = pilots[0]
    faction_id = ""

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
