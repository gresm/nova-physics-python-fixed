import os
import platform
from pathlib import Path
from setuptools import setup, Extension

FORCE_BINARIES = "FORCE_NOVA_BINARIES" in os.environ

PACKAGE_DIR = Path(__file__).parent
PREBUILT_DIR = PACKAGE_DIR / "nova-binaries"

PREBUILT_OS_DIR = PREBUILT_DIR / platform.system()
BINARIES_DIR = PREBUILT_OS_DIR / "lib"
LOCAL_BINARIES = BINARIES_DIR / platform.machine()

if FORCE_BINARIES:
    if not PREBUILT_OS_DIR.exists():
        raise RuntimeError(f"No binary distribution found for {platform.system()} operating system.")
    elif not LOCAL_BINARIES.exists():
        raise RuntimeError(f"Not supported {platform.machine()} architecture for binaries.")
