#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time

from pathlib import Path
from sys import exit

from wikidata_dl import wikidata


def main():
    parser = argparse.ArgumentParser(description='Download data files from Wikidata for the given query.')
    parser.add_argument('query_file', type=Path, metavar='QUERY_FILE',
                        help='The file containing the SPARQL query to pass to the Wikidata query service.')
    parser.add_argument('--cache-dir', '-d', type=Path, default='wikidata',
                        help='The directory where Wikidata files are stored.')
    parser.add_argument('--cache-time', '-t', default=2592000, type=int,
                        help='Cache time for items in seconds, set to 30 days by default.')
    parser.add_argument('--format', '-f', choices=('csv', 'json'), default='csv',
                        help='Download format of query result, defaults to csv.')
    parser.add_argument('--items', '-i', action='store_true',
                        help='Download Wikidata items as individual JSON files.')
    parser.add_argument('--language', '-l', type=str, default='en',
                        help='Get item results in this language. Enter a language code used by Wikimedia.')
    parser.add_argument('--sleep', '-s', type=int, default=1,
                        help='Sleep time between file downloads in seconds.')
    parser.add_argument('--timeout', type=float, default=5.0,
                        help='Set the timeout for fetching content (in seconds). Use 0 for no timeout.')

    argv = parser.parse_args()

    argv.cache_dir.mkdir(exist_ok=True, parents=True)

    # Timeout must be a float larger than 0. Users can pass 0 as a CLI option to turn off the timeout.
    timeout = argv.timeout if argv.timeout > 0 else None

    # Get and save result.
    result = wikidata.get(argv.query_file.read_text(), argv.format, timeout)
    file = argv.cache_dir.joinpath(f'{argv.query_file.stem}.{argv.format}')
    file.write_text(result)
    print(f'Saved query result in {file}\n')

    if not argv.items:
        exit()

    # Save items in language sub directory.
    cache_items = argv.cache_dir.joinpath(argv.language)
    cache_items.mkdir(exist_ok=True)

    # Download individual items as JSON files.
    count = 0
    for record in wikidata.records(result, argv.format):
        for wid in wikidata.wikibase_ids(record):
            count += 1
            print(f'{count:>5}\tProcess Wikidata item: {wid}')
            msg = wikidata.download(wid, root=cache_items, lifetime=argv.cache_time, language=argv.language)
            msg and print(f'\t{msg}')
            time.sleep(argv.sleep)


if __name__ == '__main__':
    main()
