from typing import Dict, Any

def vehicle_to_mongo(data: Dict[str, Any]) -> Dict[str, Any]:
    name = data.get("name")
    model = data.get("model")
    vehicle_class = data.get("vehicle_class")
    manufacturer = data.get("manufacturer")
    max_atmosphering_speed_str = data.get("max_atmosphering_speed")

    try:
        # Handle 'unknown' and ensure it's an integer
        max_atmospheric_speed = int(max_atmosphering_speed_str) if max_atmosphering_speed_str and max_atmosphering_speed_str.lower() != 'unknown' else 0
        if max_atmospheric_speed < 0:
            max_atmospheric_speed = 0
    except (ValueError, TypeError):
        max_atmospheric_speed = 0

    return {
        "name": name,
        "model": model,
        "class": vehicle_class, # Map 'vehicle_class' to 'class'
        "manufacturer": manufacturer,
        "max_atmospheric_speed": max_atmospheric_speed
    }
