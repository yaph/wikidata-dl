# -*- coding: utf-8 -*-
import json
import logging
import os
import time

import requests
import wptools  # type: ignore

from datetime import datetime, timezone
from typing import Set

from dateutil.parser import parse as parsedate


logging.basicConfig(filename='wikidata.log', level=logging.WARNING)


def get_wikibase_ids(query: str) -> Set[str]:
    """Return a set of Wikibase IDs for given query from Wikidata."""

    params = {
        'query': query,
        'format': 'json'
    }
    resp = requests.get('https://query.wikidata.org/sparql', params=params)
    if resp.ok:
        results = resp.json()
        return {r['item']['value'].split('/')[-1] for r in results['results']['bindings']}
    else:
        raise Exception('Data could not be fetched.')


def is_cached(file_name: str, cache_lifetime: int) -> bool:
    """Check whether cache file exists is still valid."""

    if os.path.exists(file_name):
        file_modified = os.path.getmtime(file_name)
        if (time.time() - file_modified < cache_lifetime):
            logging.info(f'Cached file {file_name} is still valid.')
            return True
    return False


def is_wikidata_newer(file_name: str, data: dict) -> bool:
    """Check whether last Wikidata update is newer than cache file."""

    if os.path.exists(file_name):
        file_modified = os.path.getmtime(file_name)
        if datetime.fromtimestamp(file_modified, tz=timezone.utc) > parsedate(data['modified']['wikidata']):
            logging.info(f'Last wikidata update older than {file_name}.')
            return False
    return True


def download(wikibase_ids: Set[str], cache_dir: str, cache_lifetime: int) -> None:
    """Fetch and cache data for all Wikibase IDs passed to this function."""

    os.makedirs(cache_dir, exist_ok=True)

    for count, wikibase in enumerate(wikibase_ids):
        file_name = os.path.join(cache_dir, wikibase + '.json')
        if is_cached(file_name, cache_lifetime):
            continue

        # Fetch Wikidata
        wikidata_url = 'https://www.wikidata.org/wiki/' + wikibase
        print(f'{count + 1:>5}\tGet data for: {wikidata_url}')
        page = wptools.page(wikibase=wikibase, silent=True, verbose=False)

        try:
            page.get_wikidata()
        except LookupError:
            logging.error(f'Wikidata for {wikibase} could not be fetched.')
            continue

        if not is_wikidata_newer(file_name, page.data):
            continue

        # Make a copy to keep original values in case of redirects
        wikidata = page.data.copy()

        # Only consider items that have an English label
        if not wikidata['label']:
            logging.warning(wikidata_url + ' has no English label.')
            continue

        # Add sitelinks to data
        response = json.loads(page.cache['wikidata']['response'])
        wikidata['sitelinks'] = response['entities'][wikibase].get('sitelinks')

        # Load summary from Wikipedia
        try:
            page.get_restbase('/page/summary/')
        except LookupError:
            logging.error(f'Wikipedia summary for {page.data["title"]} could not be fetched.')

        # In case of redirects or disambiguation pages returned from restbase request keep data from wikidata request
        desc = page.data['description']
        if wikibase == page.data['wikibase'] and desc and not desc.startswith('Disambiguation page'):
            wikidata.update(page.data)

        logging.info(f'Write data to {file_name}.')
        with open(file_name, 'w') as f:
            json.dump(wikidata, f)

        time.sleep(1)
