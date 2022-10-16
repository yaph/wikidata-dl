# -*- coding: utf-8 -*-
import csv
import json
import time

import wptools  # type: ignore
import httpx

import vocabulary

from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path

from dateutil.parser import parse as parsedate  # type: ignore


api_endpoint = 'https://query.wikidata.org/sparql'

formats = {
    'csv': 'text/csv',
    'json': 'application/sparql-results+json'
}


def download(wikibase_id: str, root: Path, lifetime: int, sleep: int = 1) -> None:
    """
    Fetch and cache data for Wikibase ID passed to this function.

    Parameters
    ----------
    wikibase_id : Wikibase item ID.
    root : Path of cache directory.
    lifetime : Cache lifetime in seconds.
    sleep : Sleep time after request in seconds.
    """

    root.mkdir(exist_ok=True, parents=True)
    file = root.joinpath(wikibase_id + '.json')
    mtime = file.lstat().st_mtime if file.exists() else None

    if mtime and (time.time() - mtime < lifetime):
        print(f'Cached file {file} is still valid.')
        return

    # Fetch Wikidata
    page = wptools.page(wikibase=wikibase_id, silent=True, verbose=False)
    try:
        page.get_wikidata()
    except (LookupError, ValueError) as err:
        print(f'Wikidata for {wikibase_id} could not be fetched.\n{err}')
        return

    if mtime and is_current(mtime, page.data):
        print(f'Last wikidata update older than {file}.')
        return

    # Make a copy to keep original values in case of redirects
    data = page.data.copy()

    # Only consider items that have an English label
    if not data['label']:
        print(f'{wikibase_id} has no English label.')
        return

    # Add sitelinks to data
    response = json.loads(page.cache['wikidata']['response'])
    data['sitelinks'] = response['entities'][wikibase_id].get('sitelinks')

    # Load summary from Wikipedia
    try:
        page.get_restbase('/page/summary/')
    except LookupError:
        print(f'Wikipedia summary for {page.data["title"]} could not be fetched.')

    # In case of redirects or disambiguation pages returned from restbase request keep data from wikidata request
    desc = page.data['description']
    if wikibase_id == page.data['wikibase'] and desc and not desc.startswith('Disambiguation page'):
        data.update(page.data)

    file.write_text(json.dumps(data))
    time.sleep(sleep)


def get(query: str, format: str) -> str:
    """
    Return a set of Wikibase IDs for given query from Wikidata.

    Parameters
    ----------
    query : SPARQL query string for Wikidata.
    format : Return format for Wikidata response.
    """

    params = {'query': query}
    headers = {'Accept': formats[format]}
    resp = httpx.get(api_endpoint, params=params, headers=headers)

    if resp.is_success:
        return resp.text

    raise Exception('Data could not be fetched.')


def is_current(mtime: float, data: dict) -> bool:
    """
    Check whether last Wikidata update is newer than cache file.

    Parameters
    ----------
    mtime : Last modification time of file in seconds.
    data : Data as returned from wptools.
    """

    return datetime.fromtimestamp(mtime, tz=timezone.utc) > parsedate(data['modified']['wikidata'])


def records(result: str, format: str) -> Iterator[list]:
    """
    Yield Wikidata item values from the query result.

    Parameters
    ----------
    result : Data as returned from Wikidata.
    format : Data format.
    """

    if 'csv' == format:
        # Ignore first line with column headings
        for record in csv.reader(result.splitlines()[1:]):
            yield record
    elif 'json' == format:
        for obj in json.loads(result)['results']['bindings']:
            yield [x['value'] for x in obj.values()]


def wikibase_ids(values: list) -> list[str]:
    """
    Return Wikibase IDs from the given record.

    Parameters
    ----------
    values : List of values as returned yielded from records function.
    """

    return [v.split('/')[-1] for v in values
            if isinstance(v, str) and v.startswith(vocabulary.PREFIX_WIKIDATA_ENTITY + 'Q')]
