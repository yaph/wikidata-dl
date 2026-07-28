import csv
import json
import re
import sys
import time
from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path

import httpx
import wptools  # type: ignore
from dateutil.parser import parse as parsedate  # type: ignore

from wikidata_dl import vocabulary

api_endpoint = 'https://query.wikidata.org/sparql'

formats = {'csv': 'text/csv', 'json': 'application/sparql-results+json'}

user_agent = 'wikidata-dl'


def download(wikibase_id: str, root: Path, lifetime: int, language: str, last_updated: datetime | None = None) -> str:
    """
    Fetch and cache data for Wikibase ID passed to this function. Returns a status message.

    Parameters
    ----------
    wikibase_id : Wikibase item ID.
    root : Path of cache directory.
    lifetime : Cache lifetime in seconds.
    language : Language code used by Wikimedia, see: https://meta.wikimedia.org/wiki/Table_of_Wikimedia_projects
    last_updated : Optional datetime object representing the last updated time of the item. If provided, it will be used to determine if the cached data is still valid.
    """

    file = root.joinpath(wikibase_id + '.json')
    mtime = file.lstat().st_mtime if file.exists() else None

    if mtime and ((time.time() - mtime < lifetime) or (last_updated and last_updated.timestamp() < mtime)):
        return f'Cached file {file} is still valid.'

    # Fetch Wikidata
    page = wptools.page(wikibase=wikibase_id, lang=language, silent=True, verbose=False)
    try:
        page.get_wikidata()
    except (LookupError, ValueError) as err:
        return f'Wikidata for {wikibase_id} could not be fetched.\n{err}'

    if mtime and is_current(mtime, page.data):
        return f'Last Wikidata update older than {file}.'

    # Only consider items that have a label and a title.
    if not (ensure_label(page.data, wikibase_id) and 'title' in page.data):
        return f'{wikibase_id} must have a label and a title. Skipping.'

    # Make a copy to keep original values in case of redirects
    data = page.data.copy()

    # Add sitelinks to data
    response = json.loads(page.cache['wikidata']['response'])
    data['sitelinks'] = response['entities'][wikibase_id].get('sitelinks')

    # Load summary from Wikipedia
    try:
        page.get_restbase('/page/summary/')
    except (LookupError, ValueError):
        return f'Wikipedia summary for {page.data["title"]} could not be fetched.'

    # In case of redirects or disambiguation pages returned from restbase request keep data from wikidata request
    desc = page.data['description']
    if wikibase_id == page.data['wikibase'] and desc and not desc.startswith('Disambiguation page'):
        data.update(page.data)

    file.write_text(json.dumps(data))
    return f'Saved item data in {file}'


def get(query: str, format_: str, timeout: float) -> str:
    """
    Return a set of Wikibase IDs for given query from Wikidata.

    Parameters
    ----------
    query : SPARQL query string for Wikidata.
    format : Return format for Wikidata response.
    """

    params = {'query': wrap_query_with_last_updated(query)}
    headers = {'accept': formats[format_], 'user-agent': user_agent}

    try:
        resp = httpx.get(api_endpoint, params=params, headers=headers, timeout=timeout)
    except httpx.ReadTimeout:
        print('Timeout error: Use the --timeout option to increase the timeout or set it to 0 to turn timeouts off.')
    else:
        if resp.is_success:
            return resp.text

    sys.exit('Data could not be fetched.')


def get_mul_label(wikibase_id: str) -> str:
    """Return the multilingual label for a Wikidata entity.

    Workaround for Wikidata entities that have no English label. Use the "mul" label instead,
    which is a multilingual label.

    Example URL: https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q187560&props=labels&languages=mul&format=json

    Example response:
    {
        "entities": {
            "Q187560": {
                "type": "item",
                "id": "Q187560",
                "labels": {
                    "mul": {
                        "language": "mul",
                        "value": "Scheme"
                    }
                }
            }
        },
        "success": 1
    }
    """

    resp = httpx.get(
        'https://www.wikidata.org/w/api.php',
        params={'action': 'wbgetentities', 'ids': wikibase_id, 'props': 'labels', 'languages': 'mul', 'format': 'json'},
        headers={'user-agent': user_agent},
    )

    resp.raise_for_status()
    labels = resp.json().get('entities', {}).get(wikibase_id, {}).get('labels', {})
    return labels.get('mul', {}).get('value', '')


def ensure_label(data: dict, wikibase_id: str) -> bool:
    """
    Ensure that the given data has a label. If not, try to get a multilingual label.

    Parameters
    ----------
    data : Data as returned from wptools.
    wikibase_id : Wikibase item ID.
    """

    if data['label']:
        return True

    try:
        data['label'] = get_mul_label(wikibase_id)
    except httpx.HTTPStatusError as err:
        print(f'Error fetching multilingual label for {wikibase_id}: {err}')
        return False

    return True


def is_current(mtime: float, data: dict) -> bool:
    """
    Check whether last Wikidata update is newer than cache file.

    Parameters
    ----------
    mtime : Last modification time of file in seconds.
    data : Data as returned from wptools.
    """

    return datetime.fromtimestamp(mtime, tz=timezone.utc) > parsedate(data['modified']['wikidata'])


def records(result: str, format_: str) -> Iterator[list]:
    """
    Yield Wikidata item values from the query result.

    Parameters
    ----------
    result : Data as returned from Wikidata.
    format : Data format.
    """

    if format_ == 'csv':
        # Ignore first line with column headings
        yield from csv.reader(result.splitlines()[1:])
    elif format_ == 'json':
        for obj in json.loads(result)['results']['bindings']:
            yield [x['value'] for x in obj.values()]


def wikibase_ids(values: list) -> list[str]:
    """
    Return Wikibase IDs from the given record.

    Parameters
    ----------
    values : List of values as returned yielded from records function.
    """

    return [
        v.split('/')[-1] for v in values if isinstance(v, str) and v.startswith(vocabulary.PREFIX_WIKIDATA_ENTITY + 'Q')
    ]


def wrap_query_with_last_updated(original_query: str, entity_var: str = "item") -> str:
    # 1. Normalize entity_var so it always starts with '?'
    var_name = '?' + entity_var.lstrip('?')

    # 2. Robust check for existing schema:dateModified pattern
    if re.search(r'schema:dateModified', original_query, re.IGNORECASE):
        return original_query

    # 3. Separate PREFIX statements from the main query body
    prefixes = []
    query_body_lines = []

    for line in original_query.splitlines():
        if line.strip().upper().startswith('PREFIX'):
            prefixes.append(line)
        else:
            query_body_lines.append(line)

    prefix_str = '\n'.join(prefixes)
    body_str = '\n'.join(query_body_lines).strip()

    # 4. Wrap the body in a clean subquery structure
    wrapped_query = f"""{prefix_str}

SELECT DISTINCT * WHERE {{
  {{
    {body_str}
  }}
  OPTIONAL {{ {var_name} schema:dateModified {var_name}LastUpdated . }}
}}"""

    return wrapped_query.strip()
