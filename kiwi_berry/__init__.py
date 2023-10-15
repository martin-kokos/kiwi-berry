from importlib.metadata import metadata

pkg_metadata = metadata(__name__)

__version__ = pkg_metadata["Version"]
