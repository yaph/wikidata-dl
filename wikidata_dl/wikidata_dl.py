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


def query_wikibase_ids(query):
    """Return a set of Wikibase IDs for given queried from Wikidata."""

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
