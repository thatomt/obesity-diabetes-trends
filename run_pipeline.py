import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

PIPELINES = {
    "obesity": [
        "get_obesity_data.py",
        "clean_obesity_data.py",
        "save_obesity_data.py",
        "show_obesity_trends.py",
    ],
    "diabetes": [
        "get_diabetes_data.py",
        "clean_diabetes_data.py",
        "save_diabetes_data.py",
        "show_diabetes_trends.py",
    ],
}


def run_step(script):
    print(f"\n--- Running {script} ---")
    result = subprocess.run([sys.executable, script], cwd=PROJECT_DIR)
    if result.returncode != 0:
        print(f"\nStopped: {script} failed.")
        sys.exit(result.returncode)

