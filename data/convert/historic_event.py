from bson import ObjectId

def battle_to_mongo(input_data: dict) -> dict:
    name = input_data.get('name', 'Unknown Event')
    stardate = input_data.get('date', '0 BBY')
    description = input_data.get('description', '')
    participants_str = input_data.get('participants', '')
    movie_id = ""

    locations_array = []
    characters_array = []
    factions_array = []
    if participants_str:
        for participant_name in [p.strip() for p in participants_str.split(',') if p.strip()]:
            factions_array.append({
                "faction_id": str(ObjectId()),
                "name": participant_name,
                "role": "minor"
            })

    transformed_document = {
        "name": name,
        "stardate": stardate,
        "description": description,
        "movie_id": movie_id,
        "factions": factions_array,
        "locations": locations_array,
        "characters": characters_array
    }

    return transformed_document
