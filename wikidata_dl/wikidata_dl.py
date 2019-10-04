# -*- coding: utf-8 -*-
import json
import logging
import os
import time

import requests
import wptools

from datetime import datetime, timezone
from dateutil.parser import parse as parsedate


CACHE_LIFETIME = 3600 * 24 * 30

logging.basicConfig(filename='wikidata.log', level=logging.WARNING)


def get_wikibase_ids(query):
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


def download(wikibase_ids, cache_dir='wikidata'):
    """Fetch and cache data for all Wikibase IDs passed to this function."""

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

    for count, wikibase in enumerate(wikibase_ids):
        file_name = os.path.join(cache_dir, wikibase + '.json')
        file_modified = None
        if os.path.exists(file_name):
            file_modified = os.path.getmtime(file_name)
            if (time.time() - file_modified < CACHE_LIFETIME):
                logging.info(f'Cached file {file_name} is still valid.')
                continue

        wikidata_url = 'https://www.wikidata.org/wiki/' + wikibase

        print(f'{count + 1:>5}\tGet data for: {wikidata_url}')
        page = wptools.page(wikibase=wikibase, silent=True, verbose=False)
        page.get_wikidata()

        # Continue if last Wikidata update is older than last modification of JSON file
        if file_modified and datetime.fromtimestamp(file_modified, tz=timezone.utc) > parsedate(page.data['modified']['wikidata']):
            logging.info(f'Last wikidata update older than {file_name}.')
            continue

        # Make a copy to keep original values in case of redirects
        wikidata = page.data.copy()

        # Only consider items that have an English label
        if not wikidata['label']:
            logging.warning(wikidata_url + ' has no English label.')
            continue

        # Add sitelinks to data
        response = json.loads(page.cache['wikidata']['response'])
        item = response['entities'][wikibase]
        sitelinks = item.get('sitelinks')
        if sitelinks:
            wikidata['sitelinks'] = sitelinks

        try:
            page.get_restbase('/page/summary/')
        except LookupError:
            logging.error(f'Wikipedia summary for {page.data["title"]} could not be fetched.')

        # In case of redirects or disambiguation pages returned from restbase request keep data from wikidata request
        if wikibase == page.data['wikibase'] and page.data['description'] and not page.data['description'].startswith('Disambiguation page'):
            wikidata.update(page.data)

        logging.info(f'Write data to {file_name}.')
        with open(file_name, 'w') as f:
            json.dump(wikidata, f)

        time.sleep(1)