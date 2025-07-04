import json
import csv
from typing import List, Dict, Any
from bson import ObjectId

def save_list_to_json_file(
    data_list: List[Dict[str, Any]],
    file_path: str,
    id_field_name: str = "_id"
) -> List[Dict[str,Any]]:
    data_to_save = []
    for item in data_list:
        item_copy = item.copy()
        item_copy[id_field_name] = {"$oid":str(ObjectId())}
        data_to_save.append(item_copy)
    print("Saved",file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data_to_save, f, indent=4, ensure_ascii=False)
    return data_to_save


def read_json_to_list_of_dicts(file_path: str) -> List[Dict[str, Any]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {e}", e.doc, e.pos)


def read_csv_to_list_of_dicts(
    file_path: str,
    delimiter: str = ',',
    encoding: str = 'utf-8',
) -> List[Dict[str, Any]]:
    try:
        data = []
        with open(file_path, 'r', encoding=encoding, newline='') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            for row in reader:
                # Convert empty strings to None for cleaner data
                cleaned_row = {key: (value if value != '' else None) for key, value in row.items()}
                data.append(cleaned_row)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except csv.Error as e:
        raise csv.Error(f"Error reading CSV file {file_path}: {e}")


