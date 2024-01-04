"""Commandline interface to parsematic
"""

import argparse
import os

from parsematic import MathParser


def main():
    """e"""
    argparser = argparse.ArgumentParser(
        prog="parsematic", description="Parsematic: just another math parser"
    )
    argparser.add_argument("-e", "--expression", required=False, type=str)
    argparser.add_argument(
        "-i", "--interactive", required=False, action="store_const"
    )
    args = argparser.parse_args()

    parser = MathParser()
    if args.expression:
        print(parser.parse(args.expression))
    else:
        while True:
            print(parser.parse(input(f"{os.getenv('USER')}@parsematic>")))


if __name__ == "__main__":
    main()
