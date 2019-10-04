#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from .wikidata_dl import get_wikibase_ids, download


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query_file')
    args = parser.parse_args()

    with open(args.query_file) as f:
        query = f.read()

    wikibase_ids = get_wikibase_ids(query)
    download(wikibase_ids)


if __name__ == '__main__':
    main()