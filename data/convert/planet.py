from typing import Any, Dict, List, Optional

def planet_to_mongo(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data.get("name")
    climate = data.get("climate")
    terrain = data.get("terrain")
    population_str = data.get("population")

    try:
        population = int(population_str) if population_str and population_str.lower() != 'unknown' else 0
        if population < 0:
            population = 0
    except (ValueError, TypeError):
        population = 0

    species_ids: List[Any] = []

    return {
        "name": name,
        "climate": climate,
        "terrain": terrain,
        "population": population,
        "species_ids": species_ids
    }


