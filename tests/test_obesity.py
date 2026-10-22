"""Tests for the obesity pipeline: cleaning, saving, and the chart."""

import unittest

import pandas as pd

from helpers import OBESITY_STEPS, PNG_SIGNATURE, DataTestCase


class ObesityCleanTests(DataTestCase):
    def setUp(self):
        super().setUp()
        self.run_step("clean_obesity_data.py")
        self.df = pd.read_csv(self.workdir / "obesity_clean.csv")

    def test_keeps_only_both_sexes_rows(self):
        self.assertEqual(len(self.df), 6)  # 2 countries x 3 years
        zaf_1980 = self.df[(self.df["country"] == "ZAF") & (self.df["year"] == 1980)]
        self.assertAlmostEqual(zaf_1980["obesity_percent"].iloc[0], 10.0)

    def test_has_expected_columns(self):
        self.assertEqual(list(self.df.columns), ["country", "year", "obesity_percent"])

    def test_is_sorted_with_no_duplicates_or_nulls(self):
        expected = self.df.sort_values(["country", "year"]).reset_index(drop=True)
        pd.testing.assert_frame_equal(self.df, expected)
        self.assertFalse(self.df.duplicated(["country", "year"]).any())
        self.assertFalse(self.df.isna().any().any())


class ObesitySaveTests(DataTestCase):
    def test_save_writes_table(self):
        self.run_step("clean_obesity_data.py")
        self.run_step("save_obesity_data.py")

        rows = self.read_db("obesity", "country, year, obesity_percent")
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0][0], "GBR")


class ObesityChartTests(DataTestCase):
    def test_chart_is_created(self):
        for script in OBESITY_STEPS:
            self.run_step(script)

        png = self.workdir / "obesity_trends_chart.png"
        self.assertTrue(png.exists())
        self.assertEqual(png.read_bytes()[:8], PNG_SIGNATURE)


if __name__ == "__main__":
    unittest.main()