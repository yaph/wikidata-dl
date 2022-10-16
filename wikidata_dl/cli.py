#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import wikidata

from pathlib import Path
from sys import exit


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
    argv = parser.parse_args()

    # Get and save result
    result = wikidata.get(argv.query_file.read(), argv.format)
    name = f'{Path(argv.query_file.name).stem}.{argv.format}'
    p_cache = Path(argv.cache_dir)
    p_cache.joinpath(name).write_text(result)

    if not argv.items:
        exit()

    # Download individual items as JSON files.
    count = 0
    for record in wikidata.records(result, argv.format):
        for wid in wikidata.wikibase_ids(record):
            count += 1
            print(f'{count:>5}\tProcess Wikidata item: {wid}')
            wikidata.download(wid, root=p_cache, lifetime=argv.cache_lifetime)


if __name__ == '__main__':
    main()
