#!/usr/bin/env python3

import argparse
import sys

from rbhmap import functions

def main():
    args = parse_args()
    function = functions[args.function]
    try:
        function(*args.args)
    except TypeError as e:
        print(e)
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("function", choices=functions)
    parser.add_argument("args", type=str, nargs="*")
    args = parser.parse_args()
    return args

functions = {
    "blast": functions.blast,
    "map2split": functions.map2split,
    "map2colin": functions.map2colin
}

if __name__ == "__main__":
    main()