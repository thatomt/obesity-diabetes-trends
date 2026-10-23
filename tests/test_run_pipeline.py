import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from helpers import DIABETES_STEPS, OBESITY_STEPS, ROOT

ALL_STEPS = ["get_obesity_data.py"] + OBESITY_STEPS + ["get_diabetes_data.py"] + DIABETES_STEPS


class RunPipelineTests(unittest.TestCase):
    def setUp(self):
        self.folder = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.folder, ignore_errors=True)
        shutil.copy(ROOT / "run_pipeline.py", self.folder / "run_pipeline.py")

    def make_stubs(self, failing=None):
        """Create stand-in scripts that only record that they ran.

        `failing` names one script that exits with an error, to test stopping.
        """
        for name in ALL_STEPS:
            exit_code = 1 if name == failing else 0
            (self.folder / name).write_text(
                "import sys\n"
                "from pathlib import Path\n"
                f"Path('{name}.ran').touch()\n"
                f"sys.exit({exit_code})\n",
                encoding="utf-8",
            )

    def run_runner(self, *args):
        return subprocess.run(
            [sys.executable, "run_pipeline.py", *args],
            cwd=self.folder,
            capture_output=True,
            text=True,
        )

    def ran(self):
        return {p.name.removesuffix(".ran") for p in self.folder.glob("*.ran")}

    def test_without_argument_shows_usage(self):
        self.make_stubs()
        result = self.run_runner()

        self.assertEqual(result.returncode, 1)
        self.assertIn("Usage", result.stdout)
        self.assertEqual(self.ran(), set())

    def test_unknown_topic_is_rejected(self):
        self.make_stubs()
        result = self.run_runner("bogus")

        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.ran(), set())

    def test_obesity_runs_only_obesity_steps(self):
        self.make_stubs()
        result = self.run_runner("obesity")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.ran(), {"get_obesity_data.py", *OBESITY_STEPS})

    def test_all_runs_both_pipelines(self):
        self.make_stubs()
        result = self.run_runner("all")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.ran(), set(ALL_STEPS))

    def test_stops_when_a_step_fails(self):
        self.make_stubs(failing="clean_obesity_data.py")
        result = self.run_runner("all")

        self.assertEqual(result.returncode, 1)
        self.assertIn("Stopped: clean_obesity_data.py failed", result.stdout)
        self.assertIn("get_obesity_data.py", self.ran())
        self.assertNotIn("save_obesity_data.py", self.ran())
        self.assertNotIn("get_diabetes_data.py", self.ran())


if __name__ == "__main__":
    unittest.main()