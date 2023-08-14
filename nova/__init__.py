try:
    from ._nova import *
except ImportError:
    raise ImportError("Package built improperly: missing nova._nova module.")


__all__ = [
    "STATIC",
    "DYNAMIC",
    "Vector2",
    "Space",
    "Body",
    "create_circle",
    "create_rect"
]
