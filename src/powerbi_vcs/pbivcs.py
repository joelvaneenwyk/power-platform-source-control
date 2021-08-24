# 1: have scripts which extract from .pbit to .pbit.extract - gitignore .pbit (and .pbix), AND creates .pbix.chksum (which is only useful for versioning purposes - one can confirm the state of their pbix)
# - script basically extracts .pbit to new folder .pbit.extract, but a) also extracts double-zipped content, and b) formats stuff nicely so it's readable/diffable/mergeable.
# 2: have git hooks which check, before a commit:
# - checks that the .pbit.extract folder is up to date with the latest .pbit (i.e. they match exactly - and the .pbit hasn't been exported but user forgot to run the extract script)
# - adds a warning (with y/n continue feedback) if the .pbix has been updated *after* the latest .pbit.extract is updated. (I.e. they maybe forgot to export the latest .pbit and extract, or exported .pbit but forgot to extract.) Note that this will be obvious in the case of only a single change (as it were) - since .pbix aren't tracked, they'll see no changes to git tracked files.

import zipfile
import os
import shutil
import fnmatch
from loguru import logger
from . import converters


CONVERTERS = [
    ("DataModelSchema", converters.JSONConverter("utf-16-le")),
    ("DiagramState", converters.JSONConverter("utf-16-le")),
    ("DiagramLayout", converters.JSONConverter("utf-16-le")),
    ("Report/Layout", converters.JSONConverter("utf-16-le")),
    ("Report/LinguisticSchema", converters.XMLConverter("utf-16-le", False)),
    ("[[]Content_Types[]].xml", converters.XMLConverter("utf-8-sig", True)),
    ("SecurityBindings", converters.NoopConverter()),
    ("Settings", converters.NoopConverter()),
    ("Version", converters.NoopConverter()),
    ("Report/StaticResources/", converters.NoopConverter()),
    ("DataMashup", converters.DataMashupConverter()),
    ("Metadata", converters.JSONConverter("utf-16-le")),
    ("*.json", converters.JSONConverter("utf-8")),
]


def find_converter(path):
    result = converters.NoopConverter()
    for pattern, converter in CONVERTERS:
        if fnmatch.fnmatch(path, pattern):
            result = converter
            break
    else:
        logger.warning(f"{path!r} has no converter matching. Using {result}")
    return result


def extract_pbit(pbit_path, outdir, overwrite, diffable):
    """
    Convert a pbit to vcs format
    """
    # TODO: check ends in pbit
    # TODO: check all expected files are present (in the right order)

    # wipe output directory and create:
    if os.path.exists(outdir):
        if overwrite:
            shutil.rmtree(outdir)
        else:
            raise Exception('Output path "{0}" already exists'.format(outdir))

    os.mkdir(outdir)

    order = []

    with zipfile.ZipFile(pbit_path, compression=zipfile.ZIP_DEFLATED) as zd:

        # read items (in the order they appear in the archive)
        for name in zd.namelist():
            order.append(name)
            outpath = os.path.join(outdir, name)
            # get converter:
            conv = find_converter(name)
            # convert
            conv.diffable = diffable
            conv.write_raw_to_vcs(zd.read(name), outpath)

        # write order files:
        open(os.path.join(outdir, ".zo"), "w").write("\n".join(order))


def compress_pbit(extracted_path, compressed_path, overwrite, diffable):
    """Convert a vcs store to valid pbit."""
    # TODO: check all paths exists

    if os.path.exists(compressed_path):
        if overwrite:
            os.remove(compressed_path)
        else:
            raise Exception('Output path "{0}" already exists'.format(compressed_path))

    # get order
    with open(os.path.join(extracted_path, ".zo")) as f:
        order = f.read().split("\n")

    with zipfile.ZipFile(
        compressed_path, mode="w", compression=zipfile.ZIP_DEFLATED
    ) as zd:
        for name in order:
            if name == "":
                continue
            # get converter:
            conv = find_converter(name)
            # convert
            conv.diffable = diffable
            print(">" + name)
            with zd.open(name, "w") as z:
                conv.write_vcs_to_raw(os.path.join(extracted_path, name), z)


def textconv_pbit(pbit_path, outio):
    """
    Convert a pbit to a text format suitable for diffing
    """
    # TODO: check ends in pbit

    order = []

    with zipfile.ZipFile(pbit_path, compression=zipfile.ZIP_DEFLATED, mode="r") as zd:

        # read items (in the order they appear in the archive)
        for name in zd.namelist():
            order.append(name)
            print("Filename: " + name, file=outio)
            # get converter:
            conv = find_converter(name)
            # convert
            conv.write_raw_to_textconv(zd.read(name), outio)
