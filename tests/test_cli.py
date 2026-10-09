"""Exercise CLI startup against real temporary filesystem and SQLite files."""

import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize("custom_path", [None, "custom/nested/stats.db"])
def test_cli_database_location(tmp_path, custom_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    args = [sys.executable, "-m", "softball_statistics.cli", "--list-leagues"]
    if custom_path:
        args.extend(["--db", custom_path])
    result = subprocess.run(args, cwd=tmp_path, env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "No leagues found." in result.stdout
    assert (tmp_path / (custom_path or "data/output/stats.db")).is_file()
    assert not (tmp_path / "stats.db").exists()
    if custom_path:
        assert not (tmp_path / "data/output/stats.db").exists()
