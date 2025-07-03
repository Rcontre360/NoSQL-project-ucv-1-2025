from typing import List, Dict, Any

def weapon_to_mongo(item: Dict[str, Any]) -> Dict[str, Any]:
    transformed_item = {
        "name": item.get("name", ""),
        "type": item.get("type", ""),
        "manufacturer": item.get("manufacturer", ""),
        "crystal_color": "Unknown"  # Default value since not in source data
    }
    # Keep original _id if it exists
    if "_id" in item:
        transformed_item["_id"] = item["_id"]
    elif "id" in item:
        transformed_item["_id"] = item["id"]

    return transformed_item
