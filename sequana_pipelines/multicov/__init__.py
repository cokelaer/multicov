try:
    from importlib.metadata import version
    __version__ = version("sequana_multicov")
except Exception:
    __version__ = ">=1.1.1"
