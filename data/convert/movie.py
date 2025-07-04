import re
from typing import Dict, Any, List

def movie_to_mongo(
    data: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "title" : data.get("title"),
        "episode" : data.get("episode_id"),
        "director" : data.get("director"),
        "release_date" : data.get("release_date"),
        "characters" : data.get("characters", []),
        "starships" : data.get("starships", []),
    }

