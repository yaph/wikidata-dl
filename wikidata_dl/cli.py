#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for wikidata_dl."""
import argparse
import sys


def main():
    """Console script for wikidata_dl."""
    parser = argparse.ArgumentParser()
    parser.add_argument('query_file')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
