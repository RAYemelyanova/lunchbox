import subprocess
import sys

from lunchbox import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "lunchbox", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
