import sys
import os
import configargparse
from typing import List
from distutils.util import strtobool
from loguru import logger
from .pbivcs import extract_pbit, textconv_pbit, compress_pbit
from . import version


def find_confs(path) -> List[str]:
    """
    Find all .pbivcs.conf files (if any) furthest down the path, ordered by hierarchy i.e.
    '/path/to/my/.pbivcs.conf' would come before '/path/to/.pbivcs.conf'
    """

    splat = tuple(
        i for i in os.path.split(os.path.abspath(os.path.normpath(path))) if i
    )
    confs = []
    for i in range(1, len(splat)):
        parent = os.path.join(*splat[:i])
        confpath = os.path.join(parent, ".pbivcs.conf")
        if os.path.exists(confpath):
            confs.append(confpath)
    return confs


def get_parser():
    parser = configargparse.ArgumentParser(
        description="A utility for converting *.pbit files to and from a VCS-friendly format",
        # config_file_parser_class=configargparse.YAMLConfigFileParser,
        # formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input",
        type=str,
        help="the input path",
    )
    parser.add_argument(
        "output",
        type=str,
        help="the output path",
    )
    parser.add_argument(
        "-x",
        "--extract",
        action="store_true",
        dest="extract",
        help="extract pbit at INPUT to VCS-friendly format at OUTPUT",
    )
    parser.add_argument(
        "-c",
        "--compress",
        action="store_true",
        dest="compress",
        help="compress VCS-friendly format at INPUT to pbit at OUTPUT",
    )
    parser.add_argument(
        "-s",
        "--textconv",
        action="store_true",
        dest="textconv",
        help="extract pbit at INPUT to textconv format on stdout",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        dest="overwrite",
        help="if present, allow overwriting of OUTPUT. If not, will fail if OUTPUT exists",
    )
    parser.add_argument(
        "--diffable",
        action="store_true",
        dest="diffable",
        help="if present, reformat output in various ways to improve diff-ability",
    )
    parser.add_argument(
        "--use-config-files",
        type=strtobool,
        help=find_confs.__doc__
        + "\n*True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values are 'n', 'no', 'f', 'false', 'off', and '0'",
    )
    parser.add_argument(
        "--version",
        action="version",
        help="print version.",
        version=f"{version.project} {version.version}",
    )
    parser.set_defaults(
        extract=False,
        compress=False,
        textconv=False,
        overwrite=False,
        diffable=False,
        use_config_files=True,
    )
    return parser


def main(args: List[str] = None, env_vars=None):
    if args is None:
        args = sys.argv[1:]

    if env_vars is None:
        env_vars = os.environ

    kwargs = dict(
        args=args,
        env_vars=env_vars,
    )
    parser = get_parser()
    args = parser.parse_args(**kwargs)
    # parse args first to get input path:
    input_path = args.input
    # now set config files for parser:
    parser._default_config_files = find_confs(
        input_path
    )  # if args.config_files else []
    if parser._default_config_files:
        print(f"Using settings from {parser._default_config_files}.")
    # now parse again to get final args:
    args = parser.parse_args(**kwargs)

    if args.textconv:
        textconv_pbit(args.input, sys.stdout)
    else:
        if args.output is None:
            parser.error("The following arguments are required: output.")
        if args.input == args.output:
            parser.error("Input and output paths cannot be same.")
        if all((args.extract, args.compress)):
            parser.error("Choose either extract or compress.")
        if args.extract:
            extract_pbit(args.input, args.output, args.overwrite, args.diffable)
        else:
            compress_pbit(args.input, args.output, args.overwrite, args.diffable)


if __name__ == "__main__":
    logger.add(
        sink=f"./logs/{version.project}.log",
        enqueue=True,
        rotation="4 weeks",
        retention="4 months",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )
    with logger.catch():
        main()
