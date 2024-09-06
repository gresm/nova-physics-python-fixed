import sys
import os
import platform
import shutil
import io
import json
import tarfile
import urllib.request
from time import time
from pathlib import Path
from setuptools import setup, Extension


if platform.system() == "Darwin":
    # ???
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context


BUILD_WEB = False
if "BUILD_WEB" in os.environ:
    BUILD_WEB = True

BUILD_NIGHTLY = False
if "BUILD_NIGHTLY" in os.environ:
    BUILD_NIGHTLY = True


BASE_PATH = Path(os.getcwd())
BUILD_PATH = BASE_PATH / "build"
NOVA_PATH = BUILD_PATH / "nova-physics"
VERSION = "1.0.0"


with open("README.md") as _f:
    LONG_DESCRIPTION = _f.read()


def download(nightly: bool):
    """ Download the latest Nova Physics commit. """

    print("Downloading latest commit...")

    response = urllib.request.urlopen(
        f"https://github.com/kadir014/nova-physics/archive/refs/heads/main.tar.gz"
        if nightly else
        f"https://github.com/kadir014/nova-physics/archive/refs/tags/{VERSION}.tar.gz"
    )

    data = response.read()

    with tarfile.open(mode="r:gz", fileobj=io.BytesIO(data)) as tar:
        name = tar.getmembers()[0].name
        tar.extractall(BUILD_PATH)

    os.rename(BUILD_PATH / name, BUILD_PATH / "nova-physics")

    print("Downloaded and extracted commit.")


if __name__ == "__main__":
    start = time()

    # Remove build directory
    if os.path.exists(BUILD_PATH):
        shutil.rmtree(BUILD_PATH)

    if os.path.exists("src"):
        shutil.rmtree("src")
    shutil.copytree("nova-physics-python/src", "src")

    download(BUILD_NIGHTLY)

    setup(
        name = "nova-physics",
        version = VERSION,
        description = "Nova Physics Engine",
        long_description=LONG_DESCRIPTION,
        setup_requires=["cffi>=1.0.0"],
        cffi_modules=["src/cffi_comp.py:ffibuilder"],
        install_requires=["cffi>=1.0.0"],
        py_modules=["nova"],
        package_dir={"": "src"},
    )
