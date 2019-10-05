#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from .wikidata_dl import get_wikibase_ids, download


def main():
    parser = argparse.ArgumentParser(description='Download data files from Wikidata for the given query.')
    parser.add_argument('query_file', metavar='QUERY_FILE', help='The file containing the SPARQL query to pass to the Wikidata query service.')

    parser.add_argument('--cache-dir', '-d', default='wikidata')
    args = parser.parse_args()

    with open(args.query_file) as f:
        query = f.read()

    wikibase_ids = get_wikibase_ids(query)
    download(wikibase_ids, cache_dir=args.cache_dir)


if __name__ == '__main__':
    main()