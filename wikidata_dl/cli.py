#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from .wikidata_dl import get_wikibase_ids, download


def main():
    parser = argparse.ArgumentParser(description='Download data files from Wikidata for the given query.')
    parser.add_argument('query_file', type=open, metavar='QUERY_FILE',
                        help='The file containing the SPARQL query to pass to the Wikidata query service.')
    parser.add_argument('--cache-dir', '-d', default='wikidata',
                        help='The directory where Wikidata files are stored.')
    parser.add_argument('--cache-lifetime', '-l', default=2592000, type=int,
                        help='Cache lifetime in seconds, set to 30 days by default.')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Run the query and print the result count without downloading any data.')
    args = parser.parse_args()

    wikibase_ids = get_wikibase_ids(args.query_file.read())
    print('Number of results returned by query:', len(wikibase_ids))

    if args.dry_run:
        return

    download(wikibase_ids, cache_dir=args.cache_dir, cache_lifetime=args.cache_lifetime)


if __name__ == '__main__':
    main()