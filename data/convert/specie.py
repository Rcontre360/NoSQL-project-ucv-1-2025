from typing import Dict, Any

def specie_to_mongo(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data.get("name")
    classification = data.get("classification")
    average_lifespan_str = data.get("average_lifespan")
    language = data.get("language")

    try:
        average_lifespan = int(average_lifespan_str) if average_lifespan_str and average_lifespan_str.lower() != 'unknown' else 0
        if average_lifespan < 0:
            average_lifespan = 0
    except (ValueError, TypeError):
        average_lifespan = 0

    return {
        "name": name,
        "classification": classification,
        "average_lifespan": average_lifespan,
        "language": language
    }
