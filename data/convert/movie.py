from typing import Dict, Any
from datetime import datetime

def movie_to_mongo(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    dt_object = datetime.strptime(data.get("release_date"), "%Y-%m-%d")
    return {
        "title" : data.get("title"),
        "episode" : data.get("episode_id"),
        "director" : data.get("director"),
        "release_date" : {
            "$date":dt_object.strftime("%Y-%m-%dT%H:%M:%S")
        },
        "characters" : data.get("characters", []),
        "starships" : data.get("starships", []),
    }

