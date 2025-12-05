import json
import os
import tempfile
from typing import Tuple, Union
import unicodedata

def normalize_json(data):
    """Recursively normalize all strings in JSON-like data to NFC form."""
    if isinstance(data, dict):
        return {unicodedata.normalize("NFC", k): normalize_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [normalize_json(item) for item in data]
    elif isinstance(data, str):
        return unicodedata.normalize("NFC", data)
    else:
        return data


def read_json(path: str) -> Tuple[Union[dict, list, None], Union[str, None]]:
    """Read a .json file safely.

    Args:
        path (str): Absolute or relative path of the input file.

    Returns:
        tuple: (data, error_message)
            - data (dict | list | None): Parsed JSON if successful, else None
            - error_message (str | None): Error description if failed, else None
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return normalize_json(data), None
    except FileNotFoundError:
        return None, f"Error: The file '{path}' was not found."
    except json.JSONDecodeError:
        return None, f"Error: Could not decode JSON from the file '{path}'."
    except Exception as e:
        return None, f"An unexpected error occurred: {e}"


def write_json_safely(path: str, data) -> tuple[bool, str]:
    """
    Safely writes data to a JSON file using a temporary file and atomic replacement.

    Args:
        path (str): The absolute or relative path of the target file.
        data: The specific data to be written to the file.

    Returns:
        tuple[bool, str]: A tuple indicating success (True/False) and a status message.
    """
    # Ensure the directory exists before proceeding
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            return False, f"Error creating directory '{directory}': {e}"

    # Determine the directory for the temporary file
    # Using the same directory as the destination ensures atomicity on replace
    temp_dir = os.path.dirname(os.path.abspath(path)) or None
    
    # Initialize tmp_file_name outside the try block for finally block access
    tmp_file_name = None

    # Use tempfile.NamedTemporaryFile for a unique, safely handled temporary file
    try:
        # mode='w' for text, delete=False because we need to manually manage the file path
        with tempfile.NamedTemporaryFile(mode='w', delete=False, dir=temp_dir, suffix='.tmp', encoding='utf-8')\
            as tmp_file:
            tmp_file_name = tmp_file.name
            
            # --- Data Format Validation Point ---
            # json.dump raises a TypeError if the data is not JSON serializable.
            try:
                normalized_data = normalize_json(data)
                json.dump(normalized_data, tmp_file, indent=4)
            except TypeError as e:
                # Catch the specific error related to unformatable data
                return False, f"Error: Data is not JSON serializable. Details: {e}"
        
        # After successful writing and closing, replace the original file
        # This operation is atomic (or close to it) on POSIX and Windows systems
        os.replace(tmp_file_name, path)
        
        return True, "Data successfully written to file."

    except PermissionError:
        # Handle permission issues during file creation, writing, or replacement
        return False, f"Error: Permission denied when trying to write to '{path}' or directory '{temp_dir}'."
    except IOError as e:
        # Catches general I/O errors (disk full, invalid path characters, etc.)
        return False, f"Error writing file '{path}': {e}"
    except Exception as e:
        # Catches any unexpected errors not covered above
        return False, f"An unexpected error occurred: {e}"
    finally:
        # Crucial cleanup: ensure the temporary file is removed if an error occurred
        if tmp_file_name and os.path.exists(tmp_file_name):
            os.unlink(tmp_file_name)


