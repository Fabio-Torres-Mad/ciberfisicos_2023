import argparse
import logging
import os

def get_parser(description: str = "") -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-c",
        "--config",
        help="Path to the config file",
        default="",
        type=str,
    )
    parser.add_argument(
        '--log-level',
        dest='log_level',
        default=logging.INFO,
        type=lambda x: getattr(logging, x),
        help='Configure the logging level.',
    )
    parser.add_argument(
        "-s",
        "--stream-output",
        dest="stream_output",
        help="Stream output to stdout",
        action="store_true",
    )
    return parser
