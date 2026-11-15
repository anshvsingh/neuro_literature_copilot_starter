"""Launcher for the Neuro Literature Research Copilot Web Application."""

import sys
import webbrowser
from pathlib import Path
import uvicorn

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HOST = "127.0.0.1"
PORT = 8000
URL = f"http://{HOST}:{PORT}"


def main():
    print("=" * 70)
    print("🧠 NEURO LITERATURE RESEARCH COPILOT — WEB APPLICATION")
    print("=" * 70)
    print(f"Starting server at: {URL}")
    print("Corpus: 25 Real Research Papers across 4 Conditions (1,363 chunks)")
    print("Benchmark: 16 Verified Questions (100% Coverage)")
    print("Press CTRL+C to terminate.")
    print("=" * 70)

    # Open browser automatically after a short delay
    try:
        webbrowser.open(URL)
    except Exception:
        pass

    uvicorn.run("src.app:app", host=HOST, port=PORT, reload=False)


if __name__ == "__main__":
    main()
