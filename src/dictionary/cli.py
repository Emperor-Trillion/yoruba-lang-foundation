"""Simple dictionary CLI used during Stage 0.

Run:
    python -m src.dictionary.cli lookup ile
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Dict

DEFAULT_DATA = Path(__file__).resolve().parents[1] / "data" / "dictionary_sample.json"

def load_data(path: Path | str = DEFAULT_DATA) -> Dict[str, dict]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Corrupt JSON at {path}: {e}") from e

def lookup(word: str, data_path: Path | str = DEFAULT_DATA) -> None:
    data = load_data(data_path)
    entry = data.get(word)
    if not entry:
        print(f"No entry for: {word!r}")
        return
    print(f"Word: {word}")
    print(f"POS: {entry.get('pos')}")
    print(f"English: {entry.get('eng')}")
    examples = entry.get("examples") or []
    if examples:
        print("Examples:")
        for ex in examples:
            print(" -", ex)

def main() -> None:
    parser = argparse.ArgumentParser(prog="dictionary-cli")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_lookup = sub.add_parser("lookup", help="Lookup a word")
    p_lookup.add_argument("word", help="Yoruba word to lookup")
    p_lookup.add_argument("--data-file", help="path to JSON data file", default=str(DEFAULT_DATA))

    args = parser.parse_args()
    if args.cmd == "lookup":
        lookup(args.word, args.data_file)

if __name__ == "__main__":
    main()
