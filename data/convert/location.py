from typing import Dict, Any

def city_to_mongo(city: Dict[str, Any]) -> Dict[str, Any]:
    location = {
        "name": city['name'],
        "planet_id": city['planet'],
        "location_type": "city",
    }

    return location

