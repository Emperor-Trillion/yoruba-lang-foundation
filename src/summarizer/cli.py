"""Simple summarizer entrypoint (placeholder)

Run:
    python -m src.summarizer.cli "Some text to summarize..."
"""
from __future__ import annotations
import argparse

def main() -> None:
    parser = argparse.ArgumentParser(prog="summarizer-cli")
    parser.add_argument("text", help="Text to summarize", nargs="?")
    args = parser.parse_args()
    if args.text:
        print("SUMMARY (placeholder):", args.text[:120] + ("..." if len(args.text) > 120 else ""))
    else:
        print("No text provided. Use: python -m src.summarizer.cli 'long text'")

if __name__ == "__main__":
    main()
