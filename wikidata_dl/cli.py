#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import wikidata

from pathlib import Path
from sys import exit

from download import download


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
    parser.add_argument('--format', '-f', choices=('csv', 'json'), default='csv',
                        help='Download format, defaults to csv.')
    parser.add_argument('--items', '-i', action='store_true',
                        help='Download Wikidata items as individual JSON files.')
    cli_args = parser.parse_args()

    # Get and save result
    result = wikidata.get(cli_args.query_file.read(), cli_args.format)
    file_name = f'{Path(cli_args.query_file.name).stem}.{cli_args.format}'
    Path(cli_args.cache_dir).joinpath(file_name).write_text(result)

    if not cli_args.items:
        exit()

    # Download individual items as JSON files.
    for record in wikidata.records(result, cli_args.format):
        wikibase_ids = wikidata.wikibase_ids(record)
        download(wikibase_ids, cache_dir=cli_args.cache_dir, cache_lifetime=cli_args.cache_lifetime)


if __name__ == '__main__':
    main()
