# -*- coding: utf-8 -*-
import csv
import json

import httpx

import vocabulary

from collections.abc import Iterator


api_endpoint = 'https://query.wikidata.org/sparql'

formats = {
    'csv': 'text/csv',
    'json': 'application/sparql-results+json'
}


def get(query: str, format: str) -> dict:
    """Return a set of Wikibase IDs for given query from Wikidata."""

    params = {'query': query}
    headers = {'Accept': formats[format]}
    resp = httpx.get(api_endpoint, params=params, headers=headers)

    if resp.is_success:
        return resp.text

    raise Exception('Data could not be fetched.')


def records(result: str, format: str) -> Iterator[list]:
    """Yield Wikidata item values from the query result."""

    if 'csv' == format:
        # Ignore first line with column headings
        for record in csv.reader(result.splitlines()[1:]):
            yield record
    elif 'json' == format:
        for obj in json.loads(result)['results']['bindings']:
            yield [x['value'] for x in obj.values()]


def wikibase_ids(values: list) -> str:
    """Return Wikibase IDs from the given record."""

    return [v.split('/')[-1] for v in values
            if isinstance(v, str) and v.startswith(vocabulary.PREFIX_WIKIDATA_ENTITY + 'Q')]
