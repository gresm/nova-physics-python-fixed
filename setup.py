import os
import platform
from pathlib import Path
from setuptools import setup, Extension

FORCE_BINARIES = "FORCE_NOVA_BINARIES" in os.environ

PACKAGE_DIR = Path(__file__).parent

README = PACKAGE_DIR / "README.md"

PREBUILT_DIR = PACKAGE_DIR / "nova-binaries"
PREBUILT_OS_DIR = PREBUILT_DIR / platform.system()
BINARIES_DIR = PREBUILT_OS_DIR / "lib"
LOCAL_BINARIES = BINARIES_DIR / platform.machine()

NOVA_PHYSICS = PACKAGE_DIR / "nova-physics"
NOVA_PHYSICS_BUILD_SCRIPT = NOVA_PHYSICS / "nova_builder.py"

if FORCE_BINARIES:
    if not PREBUILT_OS_DIR.exists():
        raise RuntimeError(f"No binary distribution found for {platform.system()} operating system.")
    elif not LOCAL_BINARIES.exists():
        raise RuntimeError(f"Not supported {platform.machine()} architecture for binaries.")


def use_binaries():
    if FORCE_BINARIES:
        return True
    return PREBUILT_OS_DIR.exists() and LOCAL_BINARIES.exists()


def get_nova_to_link():
    if use_binaries():
        for path in LOCAL_BINARIES.iterdir():
            if path.stem == "libnova":
                return path
    # TODO: what if libraries are built manually?


def run_nova_builder(*args: str):
    path = Path.cwd()
    os.chdir(NOVA_PHYSICS)
    ret = os.system(f"python {NOVA_PHYSICS_BUILD_SCRIPT} {' '.join(args)}")
    os.chdir(path)
    return ret


def build_nova_physics():
    if not use_binaries():
        code = run_nova_builder("-q", "build")
        if code != 0:
            raise RuntimeError(
                f"Builder script returned non-zero ({code}) error code. For troubleshooting guide, go to "
                f"https://github.com/gresm/nova-physics-python-fixed/blob/master/troubleshooting-guide.md"
            )


def main():
    extension = Extension(
        name="nova",
    )
    setup(
        name="nova-physics",
        version="0.4.0",
        description="Nova Physics Python bindings",
        long_description=README.read_text(),
        ext_modules=[extension]
    )


if __name__ == "__main__":
    main()
