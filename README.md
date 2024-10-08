<p align="center"><img src="https://raw.githubusercontent.com/kadir014/kadir014.github.io/master/assets/novaphysics.png" width=340></p>
<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img src="https://img.shields.io/badge/version-0.5.0-yellow">
</p>
<p align="center">
Nova Physics is a lightweight and easy to use 2D physics engine.
</p>


This is re-packaged Nova Physics Python bindings, with custom patches.

Install with:
```shell
pip install git+https://github.com/gresm/nova-physics-python-fixed.git
```

The package will be installed under ``nova-physics`` namespace, but to import it in python use ``import nova``. Uninstalling is simple as ``pip uninstall nova-physics``.

As of currently, this will build [Nova Physics](https://github.com/kadir014/nova-physics) library from source - support for pre-building it is not yet available.
By default, this uses a stable release of [Nova Physics](https://github.com/kadir014/nova-physics), if you want a nightly version, run:
```shell
BUILD_NIGHTLY=1 pip install git+https://github.com/gresm/nova-physics-python-fixed.git
```

Example usage:
```python
import nova

# Create the space
space = nova.Space()

# Create a body with box shape
body = nova.RigidBody(
    nova.RigidBodyType.DYNAMIC, # Type of the body
    nova.Vector2(0, 0)          # Initial position of the body
)

# Add rectangle to the body.
body.add_shape(nova.Shape.rect(5, 5))

# Add body to the space
space.add_rigidbody(body)

# Main loop
while True:
    # Advance the simulation with the timestep of 60 times a second.
    space.step(1 / 60)
```