"""Tests for the diabetes pipeline: cleaning, saving, and the chart."""

import unittest

import pandas as pd

from helpers import DIABETES_STEPS, PNG_SIGNATURE, DataTestCase


class DiabetesCleanTests(DataTestCase):
    def setUp(self):
        super().setUp()
        self.run_step("clean_diabetes_data.py")
        self.df = pd.read_csv(self.workdir / "diabetes_clean.csv")

    def test_keeps_only_adults_18_plus_and_both_sexes(self):
        self.assertEqual(len(self.df), 6)  # 2 countries x 3 years
        zaf_1990 = self.df[(self.df["country"] == "ZAF") & (self.df["year"] == 1990)]
        # 10.0 is the 18+ both-sexes value; 110.0 would mean the 30+ row was kept.
        self.assertAlmostEqual(zaf_1990["diabetes_percent"].iloc[0], 10.0)

    def test_has_expected_columns_and_no_duplicates(self):
        self.assertEqual(list(self.df.columns), ["country", "year", "diabetes_percent"])
        self.assertFalse(self.df.duplicated(["country", "year"]).any())


class DiabetesSaveTests(DataTestCase):
    def test_save_writes_table(self):
        self.run_step("clean_diabetes_data.py")
        self.run_step("save_diabetes_data.py")

        rows = self.read_db("diabetes", "country, year, diabetes_percent")
        self.assertEqual(len(rows), 6)


class DiabetesChartTests(DataTestCase):
    def test_chart_is_created(self):
        for script in DIABETES_STEPS:
            self.run_step(script)

        png = self.workdir / "diabetes_trends_chart.png"
        self.assertTrue(png.exists())
        self.assertEqual(png.read_bytes()[:8], PNG_SIGNATURE)


if __name__ == "__main__":
    unittest.main()