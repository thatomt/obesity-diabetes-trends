"""Shared constants, functions, and a base test class for the pipeline tests."""

import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# Scripts the data tests need, in the order they run.
OBESITY_STEPS = ["clean_obesity_data.py", "save_obesity_data.py", "show_obesity_trends.py"]
DIABETES_STEPS = ["clean_diabetes_data.py", "save_diabetes_data.py", "show_diabetes_trends.py"]

ADULTS = "AGEGROUP_YEARS18-PLUS"


def make_record(country, year, value, sex, age_group):
    """Build one record shaped like a WHO GHO API result."""
    return {
        "SpatialDim": country,
        "TimeDim": year,
        "Dim1": sex,
        "Dim2": age_group,
        "NumericValue": value,
    }


def build_obesity_raw():
    """Two countries, three years, three sex groups, all adults 18+, shuffled.

    For each country the both-sexes value is `base + offset`. The male value
    is one higher and the female value one lower.
    """
    records = []
    for country, base in [("ZAF", 10.0), ("GBR", 7.0)]:
        for offset, year in enumerate((1980, 1981, 1982)):
            records.append(make_record(country, year, base + offset, "SEX_BTSX", ADULTS))
            records.append(make_record(country, year, base + offset + 1, "SEX_MLE", ADULTS))
            records.append(make_record(country, year, base + offset - 1, "SEX_FMLE", ADULTS))
    return list(reversed(records))


def build_diabetes_raw():
    """Same shape as the obesity data, plus a 30+ age group.

    The 30+ values are 100 higher, so a test can tell if they were kept by
    mistake.
    """
    records = []
    for country, base in [("ZAF", 10.0), ("GBR", 7.0)]:
        for offset, year in enumerate((1990, 1991, 1992)):
            records.append(make_record(country, year, base + offset, "SEX_BTSX", ADULTS))
            records.append(make_record(country, year, base + offset + 1, "SEX_MLE", ADULTS))
            records.append(make_record(country, year, base + offset + 100, "SEX_BTSX", "AGEGROUP_YEARS30-PLUS"))
    return list(reversed(records))


class DataTestCase(unittest.TestCase):
    """Runs the real data scripts in a temporary copy of the project folder."""

    def setUp(self):
        self.workdir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.workdir, ignore_errors=True)

        for name in OBESITY_STEPS + DIABETES_STEPS:
            shutil.copy(ROOT / name, self.workdir / name)
        (self.workdir / "obesity_raw.json").write_text(
            json.dumps(build_obesity_raw()), encoding="utf-8"
        )
        (self.workdir / "diabetes_raw.json").write_text(
            json.dumps(build_diabetes_raw()), encoding="utf-8"
        )

    def run_step(self, script):
        result = subprocess.run(
            [sys.executable, script],
            cwd=self.workdir,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def read_db(self, table, columns):
        conn = sqlite3.connect(self.workdir / "obesity.db")
        try:
            return conn.execute(f"SELECT {columns} FROM {table} ORDER BY 1, 2").fetchall()
        finally:
            conn.close()