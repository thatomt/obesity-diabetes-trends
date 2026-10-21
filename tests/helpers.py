"""Plain helper functions and constants shared by the test files."""

import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# Scripts the data tests need, in the order they run.
OBESITY_STEPS = ["clean_obesity_data.py", "save_obesity_data.py", "show_obesity_trends.py"]
DIABETES_STEPS = ["clean_diabetes_data.py", "save_diabetes_data.py", "show_diabetes_trends.py"]


def make_record(country, year, value, sex, age_group):
    """Build one record shaped like a WHO GHO API result."""
    return {
        "SpatialDim": country,
        "TimeDim": year,
        "Dim1": sex,
        "Dim2": age_group,
        "NumericValue": value,
    }


def run_script(script, cwd, *args):
    result = subprocess.run(
        [sys.executable, script, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    return result


def read_db_table(workdir, table, columns):
    conn = sqlite3.connect(workdir / "obesity.db")
    try:
        return conn.execute(f"SELECT {columns} FROM {table} ORDER BY 1, 2").fetchall()
    finally:
        conn.close()