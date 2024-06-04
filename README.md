<p align="center"><img src="https://raw.githubusercontent.com/kadir014/kadir014.github.io/master/assets/novaphysics.png" width=340></p>
<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img src="https://img.shields.io/badge/version-0.5.0-yellow">
</p>
<p align="center">
Nova Physics is a lightweight and easy to use 2D physics engine.
</p>


This is re-packaged Nova Physics Python bindings, as currently official bindings fail to build with ``pip install git+https://github.com/kadir014/nova-physics-python.git`` command.

Install with ``pip install git+https://github.com/gresm/nova-physics-python-fixed.git``

The command will try to use the [Nova Physics](https://github.com/kadir014/nova-physics) binaries and fall-backs if none found, if you want to force usage pre-build Nova binaries run:
``NOVA_FORCE="binaries" pip install git+https://github.com/gresm/nova-physics-python-fixed.git``
Binaries can be found [here](nova-binaries) but currently only for Linux x86/x86_64. To force building from source run ``NOVA_FORCE="source" pip install git+https://github.com/gresm/nova-physics-python-fixed.git`` 

The package will be installed under ``nova-physics`` namespace, but to import it in python use ``import nova``. Uninstalling is simple as ``pip uninstall nova-physics``.


# Excerpts from the original [README.md](nova-physics-python/README.md):

> # Python binding for [Nova Physics Engine](https://github.com/kadir014/nova-physics)
>
> This binding aims to provide a Pythonic API while keeping everything as similar as to the original.
>
> ## Usage
> ```py
> import nova
> 
> # Create the space
> space = nova.Space()
> 
> # Create a body with box shape
> body = nova.Rect(
>     nova.DYNAMIC,      # Type of the body
>     nova.Vector2(0, 0), # Initial position of the body
>     0,                 # Initial rotation of the body
>     5, 5               # Width & height of the rect shape
> )
> 
> # Add body to the space
> space.add(body)
> 
> # Main loop
> while True:
>     # Advance the simulation with the timestep of 60 times a second.
>     space.step(1 / 60)
> ```
> 
> ## Requirements
> - [Python](https://www.python.org/downloads/) (3.8+)
> - [Nova Physics](https://github.com/kadir014/nova-physics) (Prebuilt in the PyPI release)
> - [Setuptools](https://pypi.org/project/setuptools/) (Should be included by default)
> 
> ## License
> [MIT](LICENSE) © Kadir Aksoy
