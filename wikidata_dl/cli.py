#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time

import wikidata

from pathlib import Path
from sys import exit


def main():
    parser = argparse.ArgumentParser(description='Download data files from Wikidata for the given query.')
    parser.add_argument('query_file', type=Path, metavar='QUERY_FILE',
                        help='The file containing the SPARQL query to pass to the Wikidata query service.')
    parser.add_argument('--cache-dir', '-d', type=Path, default='wikidata',
                        help='The directory where Wikidata files are stored.')
    parser.add_argument('--cache-lifetime', '-l', default=2592000, type=int,
                        help='Cache lifetime in seconds, set to 30 days by default.')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Run the query and print the result count without downloading any data.')
    parser.add_argument('--format', '-f', choices=('csv', 'json'), default='csv',
                        help='Download format, defaults to csv.')
    parser.add_argument('--items', '-i', action='store_true',
                        help='Download Wikidata items as individual JSON files.')
    parser.add_argument('--sleep', '-s', type=int, default=1,
                        help='Sleep time between file downloads in seconds.')
    argv = parser.parse_args()

    argv.cache_dir.mkdir(exist_ok=True, parents=True)

    # Get and save result
    result = wikidata.get(argv.query_file.read_text(), argv.format)
    file = argv.cache_dir.joinpath(f'{argv.query_file.stem}.{argv.format}')
    file.write_text(result)
    print(f'Saved query result in {file}\n')

    if not argv.items:
        exit()

    # Download individual items as JSON files.
    count = 0
    for record in wikidata.records(result, argv.format):
        for wid in wikidata.wikibase_ids(record):
            count += 1
            print(f'{count:>5}\tProcess Wikidata item: {wid}')
            msg = wikidata.download(wid, root=argv.cache_dir, lifetime=argv.cache_lifetime)
            msg and print(f'\t{msg}')
            time.sleep(argv.sleep)


if __name__ == '__main__':
    main()
