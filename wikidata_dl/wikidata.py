# -*- coding: utf-8 -*-
from email import header
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


def records(result: str) -> Iterator[dict]:
    """Yield Wikidata item records from the query result."""

    for rec in result['results']['bindings']:
        for prop in result['head']['vars']:
            obj = rec.get(prop, {})
            val = obj.get('value')

            match obj.get('datatype'):
                case vocabulary.XSD_DECIMAL | vocabulary.XSD_DOUBLE | vocabulary.XSD_INT:
                    val = int(val)

            yield {prop: val}


def wikibase_id(record: dict) -> str:
    """Return the Wikibase ID from the given record."""

    for val in record.values():
        if isinstance(val, str) and val.startswith(vocabulary.PREFIX_WIKIDATA_ENTITY + 'Q'):
            return val.split('/')[-1]
