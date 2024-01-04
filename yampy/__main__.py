import argparse

from yampy import MathParser
import shutil
import os


def main():
    argparser = argparse.ArgumentParser(
        prog="yampy", description="Yet Another Math Parser (Python)"
    )
    argparser.add_argument("-e", "--expression", required=False, type=str)
    argparser.add_argument("-i", "--interactive", required=False, action="store_const")
    args = argparser.parse_args()

    parser = MathParser()
    if args.expression:
        print(parser.parse(args.expression))
    else:
        while True:
            print(parser.parse(input(f"{os.getenv('USER')}@yampy>")))


if __name__ == "__main__":
    main()
