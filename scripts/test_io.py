"""
scripts/test_io.py

Test script for utils/io.py functions:
1. Create a sample JSON file.
2. Read and verify JSON.
3. Modify JSON and write back.
4. Simulate malformed JSON.
5. Define and use a custom DataError exception.
6. Demonstrate exception handling.
7. Run all steps in __main__.
"""

# import os
# import json
from utils.io import read_json, write_json_safely


class DataError(Exception):
    """Custom exception for invalid data shape."""
    pass


def create_sample_json(path: str) -> None:
    """Step 1: Create a sample JSON file."""
    sample_data = {"users": [{"id": 1, "name": "Alice"}]}
    success, msg = write_json_safely(path, sample_data)
    print(f"Create sample JSON: {msg}")


def read_and_verify(path: str) -> dict | list | None:
    """Step 2: Read and verify JSON."""
    data, error = read_json(path)
    if error:
        print(f"Read error: {error}")
        return None
    print(f"Read data: {data}")
    return data


def modify_and_write(path: str, data: dict | list) -> None:
    """Step 3: Modify JSON and write back."""
    if isinstance(data, dict) and "users" in data:
        data["users"].append({"id": 2, "name": "Bob"})
    success, msg = write_json_safely(path, data)
    print(f"Modify and write: {msg}")


def simulate_malformed_json(path: str) -> None:
    """Step 4: Simulate malformed JSON and confirm error handling."""
    malformed_content = '{"users": [{"id": 1, "name": "Alice"}'  # Missing closing bracket
    with open(path, "w", encoding="utf-8") as f:
        f.write(malformed_content)

    data, error = read_json(path)
    if error:
        print(f"Malformed JSON error caught: {error}")
    else:
        print(f"Unexpectedly read data: {data}")


def validate_data_shape(data: dict | list) -> None:
    """Step 5: Validate data shape and raise DataError if invalid."""
    if not isinstance(data, dict) or "users" not in data:
        raise DataError("DataError: Expected a dict with a 'users' key.")
    print("Data shape validated successfully.")


if __name__ == "__main__":
    # Paths for test files
    sample_path = "test_sample.json"
    malformed_path = "test_malformed.json"

    # Step 1: Create sample JSON
    create_sample_json(sample_path)

    # Step 2: Read and verify
    data = read_and_verify(sample_path)

    # Step 3: Modify and write back
    if data:
        modify_and_write(sample_path, data)
        read_and_verify(sample_path)

    # Step 4: Simulate malformed JSON
    simulate_malformed_json(malformed_path)

    # Step 5–6: Custom exception handling
    try:
        bad_data = {"not_users": []}
        validate_data_shape(bad_data)
    except DataError as e:
        print(f"Caught custom exception: {e}")
