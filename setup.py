import os
import platform
from pathlib import Path
from setuptools import setup, Extension

FORCE_BINARIES = "NOVA_FORCE" in os.environ and os.environ["NOVA_FORCE"].lower() == "binaries"
FORCE_BUILD_SOURCE = "NOVA_FORCE" in os.environ and os.environ["NOVA_FORCE"].lower() == "source"

PACKAGE_DIR = Path(__file__).parent

README = PACKAGE_DIR / "README.md"

PREBUILT_DIR = PACKAGE_DIR / "nova-binaries"
PREBUILT_OS_DIR = PREBUILT_DIR / platform.system()
BINARIES_DIR = PREBUILT_OS_DIR / "lib"
LOCAL_BINARIES = BINARIES_DIR / platform.machine()
INCLUDE_DIR = PREBUILT_DIR / "include"

NOVA_PHYSICS = PACKAGE_DIR / "nova-physics"
NOVA_PHYSICS_BUILD_SCRIPT = NOVA_PHYSICS / "nova_builder.py"
NOVA_BUILD_DIRECTORY = NOVA_PHYSICS / "build"

NOVA_PYTHON = PACKAGE_DIR / "nova-physics-python"
NOVA_PYTHON_STUB = NOVA_PYTHON / "nova.pyi"
NOVA_PYTHON_SOURCES = NOVA_PYTHON / "src"

if FORCE_BINARIES:
    if not PREBUILT_OS_DIR.exists():
        raise RuntimeError(f"No binary distribution found for {platform.system()} operating system.")
    elif not LOCAL_BINARIES.exists():
        raise RuntimeError(f"Not supported {platform.machine()} architecture for binaries.")


def use_binaries():
    if FORCE_BINARIES:
        return True
    if FORCE_BUILD_SOURCE:
        return False
    return PREBUILT_OS_DIR.exists() and LOCAL_BINARIES.exists()


def run_nova_builder(*args: str):
    path = Path.cwd()
    os.chdir(NOVA_PHYSICS)
    ret = os.system(f"python {NOVA_PHYSICS_BUILD_SCRIPT} {' '.join(args)} -fPIC")
    os.chdir(path)
    return ret


def build_nova_physics():
    code = run_nova_builder("-q", "build")
    if code != 0:
        raise RuntimeError(
            f"Builder script returned non-zero ({code}) error code. For troubleshooting guide, go to "
            f"https://github.com/gresm/nova-physics-python-fixed/blob/master/troubleshooting-guide.md"
        )


def get_nova_to_link():
    if use_binaries():
        for path in LOCAL_BINARIES.iterdir():
            if path.stem == "libnova":
                return path

    build_nova_physics()

    if not NOVA_BUILD_DIRECTORY.exists():
        raise RuntimeError(
            "Building nova-physics from source failed. For troubleshooting guide, go to "
            f"https://github.com/gresm/nova-physics-python-fixed/blob/master/troubleshooting-guide.md"
        )

    to_link = NOVA_BUILD_DIRECTORY / f"libnova_{platform.machine()}"

    if not to_link.exists():
        raise RuntimeError(
            f"No built binaries found for architecture {platform.machine()}. For troubleshooting guide, go to "
            f"https://github.com/gresm/nova-physics-python-fixed/blob/master/troubleshooting-guide.md"
        )

    for path in to_link.iterdir():
        if path.stem == "libnova":
            return path

    raise RuntimeError(
        f"This should not happen: no proper binary was found in {to_link} and yet the directory was created. "
        f"For troubleshooting guide, go to "
        f"https://github.com/gresm/nova-physics-python-fixed/blob/master/troubleshooting-guide.md"
    )


def get_nova_sources():
    sources = []

    for file in NOVA_PYTHON_SOURCES.iterdir():
        if file.suffix == ".c":
            sources.append(str(file.relative_to(PACKAGE_DIR)))

    return sources


def main():
    nova_to_link = str(get_nova_to_link().relative_to(PACKAGE_DIR))
    python_stub = str(NOVA_PYTHON_STUB.relative_to(PACKAGE_DIR))

    extension = Extension(
        name="nova",
        sources=get_nova_sources(),
        include_dirs=[str(INCLUDE_DIR.relative_to(PACKAGE_DIR)), str(NOVA_PYTHON_SOURCES.relative_to(PACKAGE_DIR))],
        # A dirty trick, for not-so-conventional implementation nova-python bindings.
        extra_compile_args=["-Wno-format-security"],
        extra_objects=[nova_to_link],
        optional=False
    )

    print(
        "See https://github.com/gresm/nova-physics-python-fixed/blob/master/troubleshooting-guide.md if error occurred "
        "to see whether there is solution for your problem."
    )

    setup(
        name="nova-physics",
        version="0.4.0",
        description="Nova Physics Python bindings",
        long_description=README.read_text(),
        long_description_content_type="text/markdown",
        ext_modules=[extension],
        package_data={
            "": [python_stub]
        }
    )


if __name__ == "__main__":
    main()
