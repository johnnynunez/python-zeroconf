"""Verification-only helper: assert the installed wheel is compiled, then run the test suite."""

import pathlib
import platform
import sys
import sysconfig

import pytest

import zeroconf
from zeroconf import _dns

project = pathlib.Path(sys.argv[1])
tag = f"cp{sys.version_info[0]}{sys.version_info[1]}{'t' if sysconfig.get_config_var('Py_GIL_DISABLED') else ''}"
print("python", sys.version, platform.machine(), tag)
print("zeroconf", zeroconf.__version__, zeroconf.__file__)
print("zeroconf._dns", _dns.__file__)
pkg = pathlib.Path(zeroconf.__file__).parent
pyds = sorted(p.relative_to(pkg).as_posix() for p in pkg.rglob("*.pyd"))
print("compiled modules:", len(pyds), pyds)
assert _dns.__file__.endswith(".pyd"), "installed zeroconf is not the compiled wheel"
assert "src" not in pathlib.Path(zeroconf.__file__).parts, "tests would import the source tree"
junit = project / "junit" / f"junit-{tag}-{platform.machine()}.xml"
junit.parent.mkdir(exist_ok=True)
sys.exit(
    pytest.main(
        [
            "--durations=20",
            "--timeout=60",
            "-v",
            "-p",
            "no:cacheprovider",
            f"--junitxml={junit}",
            "tests",
        ]
    )
)
