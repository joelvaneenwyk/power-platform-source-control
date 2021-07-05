try:
    # importlib.metadata is present in Python 3.8 and later
    import importlib.metadata as importlib_metadata
except ImportError:
    # use the shim package importlib-metadata pre-3.8
    import importlib_metadata as importlib_metadata  # type: ignore
import pathlib


for distribution_name in [__package__, __name__, pathlib.Path(__file__).parent.name]:
    try:
        _DISTRIBUTION_METADATA = importlib_metadata.metadata(
            distribution_name=distribution_name,
        )
        break
    except importlib_metadata.PackageNotFoundError:
        continue
else:
    pass

author = _DISTRIBUTION_METADATA["Author"]
project = _DISTRIBUTION_METADATA["Name"]
version = _DISTRIBUTION_METADATA["Version"]
version_info = tuple([int(d) for d in version.split("-")[0].split(".")])
