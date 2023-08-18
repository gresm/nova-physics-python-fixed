import sys
from typing import Type, Optional

import os
import shutil
import tarfile
import platform
from pathlib import Path
from setuptools import setup, Extension, Command
from setuptools.command import build_ext
from distutils.core import Command as DistCommand
from warnings import warn

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

REAL_PACKAGE = PACKAGE_DIR / "nova"


def create_if_none(path: Path):
    if not path.exists():
        path.mkdir()


class UpdateBinariesCommand(Command):
    build_binaries: bool

    user_options = [("dont-build-binaries=", None, "Whether to build nova-physics from scratch.")]
    description = "Update binaries for distribution"

    def finalize_options(self) -> None:
        if isinstance(self.build_binaries, str):
            if self.build_binaries.lower() == "false":
                self.build_binaries = False
            else:
                self.build_binaries = True

    def run(self) -> None:
        if self.build_binaries:
            build_nova_physics()

        create_if_none(PREBUILT_OS_DIR)

        create_if_none(BINARIES_DIR)

        for path in NOVA_BUILD_DIRECTORY.iterdir():
            if path.is_dir() and path.name.startswith("libnova_"):
                dir_name = BINARIES_DIR / path.name.split("_", 1)[1]
                create_if_none(dir_name)

                for to_copy in path.iterdir():
                    if to_copy.is_dir():
                        shutil.copytree(to_copy, dir_name)
                    else:
                        shutil.copy(to_copy, dir_name)
            elif path.is_file() and path.suffix == ".gz":
                with tarfile.open(name=path, mode="r:gz") as tar:
                    subdir_and_files = [
                        tarinfo for tarinfo in tar.getmembers()
                        if tarinfo.name.startswith("./include")
                    ]
                    tar.extractall(path=PREBUILT_DIR, members=subdir_and_files)

    def initialize_options(self) -> None:
        self.build_binaries = BUILD_BINARIES


def innit_checks():
    if FORCE_BINARIES:
        if not PREBUILT_OS_DIR.exists():
            raise RuntimeError(f"No binary distribution found for {platform.system()} operating system.")
        elif not LOCAL_BINARIES.exists():
            raise RuntimeError(f"Not supported {platform.machine()} architecture for binaries.")

    if len(list(NOVA_PHYSICS.iterdir())) == 0 or len(list(NOVA_PYTHON.iterdir())) == 0:
        warn("Submodules not initialized, performing additional cloning.")
        if platform.system() == "Windows":
            os.system("git.exe submodule init")
            os.system("git.exe submodule update")
        else:
            os.system("git submodule init && git submodule update")


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


NOVA_TO_LINK = Path("dummy/path")
EXTENSION: Optional[Extension] = None

BUILD_BINARIES = "--dont-build-binaries" not in sys.argv
if not BUILD_BINARIES:
    sys.argv.remove("--dont-build-binaries")


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


def pre_build(self):
    global NOVA_TO_LINK
    innit_checks()
    NOVA_TO_LINK = get_nova_to_link().relative_to(PACKAGE_DIR)
    if EXTENSION is not None:
        EXTENSION.extra_objects = [str(NOVA_TO_LINK)]
    self._old_run()


def generate_cmd_class(orig: Type[DistCommand]):
    return type(f"Overriden{orig.__name__.capitalize()}", (orig,), {"run": pre_build, "_old_run": orig.run})


def main():
    global EXTENSION
    innit_checks()

    nova_to_link = str(NOVA_TO_LINK)
    stubs_to_override = {REAL_PACKAGE / "__init__.pyi": NOVA_PYTHON_STUB, REAL_PACKAGE / "_nova.pyi": NOVA_PYTHON_STUB}

    for write_to, read_from in stubs_to_override.items():
        write_to.write_text(read_from.read_text())

    extension = Extension(
        name="nova._nova",
        sources=get_nova_sources(),
        include_dirs=[str(INCLUDE_DIR.relative_to(PACKAGE_DIR)), str(NOVA_PYTHON_SOURCES.relative_to(PACKAGE_DIR))],
        # A dirty trick, for not-so-conventional implementation nova-python bindings.
        extra_compile_args=["-Wno-format-security"],
        extra_objects=[nova_to_link],
        optional=False
    )

    EXTENSION = extension

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
        include_package_data=True,
        package_data={
            "nova": ["*.pyi", "*.typed"]
        },
        packages=["nova"],
        cmdclass={
            "update_binaries": UpdateBinariesCommand,
            "build_ext": generate_cmd_class(build_ext.build_ext)
        }
    )


if __name__ == "__main__":
    main()
