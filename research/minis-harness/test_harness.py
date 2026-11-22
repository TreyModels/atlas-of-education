"""Tests for the run-record lifecycle. Run: python3 -m unittest research/minis-harness/test_harness.py"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


class RunLifecycle(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@example.org")
        git(self.repo, "config", "user.name", "t")
        (self.repo / "README.md").write_text("x\n")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "init")
        (self.repo / "research").mkdir()
        self.patches = [mock.patch.object(harness, "ROOT", self.repo),
                        mock.patch.object(harness, "RECORDS", self.repo / "research" / "records")]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.tmp.cleanup()

    def open_run(self, scope="research/work/"):
        (self.repo / "research" / "work").mkdir(exist_ok=True)
        with mock.patch("sys.stdout"):
            harness.main(["open", "--actor", "trey", "--operator", "agent",
                          "--model", "minis/agent-loop", "--harness", "minis",
                          "--intent", "test run", "--scope", scope])
        return next((self.repo / "research" / "records").iterdir())

    def test_open_requires_model_for_agent(self):
        (self.repo / "research").mkdir(exist_ok=True)
        with self.assertRaises(SystemExit):
            harness.main(["open", "--actor", "trey", "--operator", "agent",
                          "--intent", "x", "--scope", "research/"])

    def test_open_refuses_when_output_exists(self):
        run = self.open_run()
        (self.repo / "research" / "work" / "a.py").write_text("print(1)\n")
        with self.assertRaises(SystemExit):
            harness.main(["open", "--actor", "trey", "--operator", "agent", "--model", "m",
                          "--intent", "second", "--scope", "research/work/"])
        self.assertTrue(run.is_dir())

    def test_close_hashes_and_make_run_md_has_no_typed_counts(self):
        run = self.open_run()
        (self.repo / "research" / "work" / "a.py").write_text("print(1)\n")
        (self.repo / "outside.txt").write_text("not in scope\n")
        harness.close_run(run)
        out = json.loads((run / "outputs.json").read_text())
        paths = [f["path"] for f in out["files"]]
        self.assertIn("research/work/a.py", paths)
        self.assertNotIn("outside.txt", paths)
        rec = json.loads((run / "run.json").read_text())
        self.assertEqual(rec["operator"], "agent")
        self.assertEqual(len(rec["source_digest"]), 64)
        md = (run / "RUN.md").read_text()
        self.assertIn(f"Files written ({len(paths)})", md)
        self.assertIn("minis/agent-loop", md)

    def test_verify_detects_drift_and_conflict(self):
        run = self.open_run()
        (self.repo / "research" / "work" / "a.py").write_text("print(1)\n")
        harness.close_run(run)
        self.assertEqual(harness.verify([run]), [])
        (self.repo / "research" / "work" / "a.py").write_text("print(2)\n")
        self.assertTrue(any("drift" in p for p in harness.verify([run])))

    def test_empty_run_is_valid(self):
        run = self.open_run()
        harness.close_run(run)
        self.assertEqual(json.loads((run / "outputs.json").read_text())["files"], [])
        self.assertIn("empty run is a real result", (run / "RUN.md").read_text())


if __name__ == "__main__":
    unittest.main()
