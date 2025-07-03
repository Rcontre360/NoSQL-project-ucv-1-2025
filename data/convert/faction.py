from typing import Any, Dict

def faction_to_mongo(item: Dict[str, Any]) -> Dict[str, Any]:
   transformed_item = {
       "name": item.get("name", ""),
       "type": "",  # Leave empty as requested
       "leader_name": item.get("leader", "")
   }
   # Keep original _id if it exists
   if "_id" in item:
       transformed_item["_id"] = item["_id"]
   elif "id" in item:
       transformed_item["_id"] = item["id"]
   return transformed_item
