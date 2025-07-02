import json
from typing import List, Dict, Any, Optional

def save_list_to_json_file(data_list: List[Dict[str, Any]], file_path: str, indent: Optional[int] = 4) -> None:
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=indent, ensure_ascii=False)
        print(f"Data successfully saved to {file_path}")
    except IOError as e:
        print(f"Error saving data to file {file_path}: {e}")
    except TypeError as e:
        print(f"Error: Data is not JSON serializable. Details: {e}")
