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


def main():
    valid = [*PIPELINES, "all"]
    if len(sys.argv) != 2 or sys.argv[1] not in valid:
        print("Usage: python run_pipeline.py obesity | diabetes | all")
        sys.exit(1)

    choice = sys.argv[1]
    names = list(PIPELINES) if choice == "all" else [choice]
    for name in names:
        print(f"\n=== {name} pipeline ===")
        for script in PIPELINES[name]:
            run_step(script)

    print("\nAll done.")


if __name__ == "__main__":
    main()