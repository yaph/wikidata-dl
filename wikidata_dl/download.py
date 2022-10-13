# -*- coding: utf-8 -*-
import json
import logging
import time

import wptools  # type: ignore

from pathlib import Path
from datetime import datetime, timezone

from dateutil.parser import parse as parsedate  # type: ignore


logging.basicConfig(filename='wikidata.log', level=logging.WARNING)


def is_current(mtime: float, data: dict) -> bool:
    """Check whether last Wikidata update is newer than cache file."""

    return datetime.fromtimestamp(mtime, tz=timezone.utc) > parsedate(data['modified']['wikidata'])


def download(wikibase_id: str, root: str, lifetime: int) -> None:
    """Fetch and cache data for all Wikibase IDs passed to this function."""

    p_dir = Path(root)
    p_dir.mkdir(exist_ok=True, parents=True)

    p_file = p_dir.joinpath(wikibase_id + '.json')
    mtime = p_file.lstat().st_mtime if p_file.exists() else None

    if mtime and (mtime - p_file.lstat().st_mtime < lifetime):
        logging.info(f'Cached file {p_file} is still valid.')
        return

    # Fetch Wikidata
    wikidata_url = 'https://www.wikidata.org/wiki/' + wikibase_id
    page = wptools.page(wikibase=wikibase_id, silent=True, verbose=False)

    try:
        page.get_wikidata()
    except (LookupError, ValueError) as err:
        logging.error(f'Wikidata for {wikibase_id} could not be fetched.\n{err}')
        return

    if mtime and is_current(mtime, page.data):
        logging.info(f'Last wikidata update older than {p_file}.')
        return

    # Make a copy to keep original values in case of redirects
    wikidata = page.data.copy()

    # Only consider items that have an English label
    if not wikidata['label']:
        logging.warning(wikidata_url + ' has no English label.')
        return

    # Add sitelinks to data
    response = json.loads(page.cache['wikidata']['response'])
    wikidata['sitelinks'] = response['entities'][wikibase_id].get('sitelinks')

    # Load summary from Wikipedia
    try:
        page.get_restbase('/page/summary/')
    except LookupError:
        logging.error(f'Wikipedia summary for {page.data["title"]} could not be fetched.')

    # In case of redirects or disambiguation pages returned from restbase request keep data from wikidata request
    desc = page.data['description']
    if wikibase_id == page.data['wikibase'] and desc and not desc.startswith('Disambiguation page'):
        wikidata.update(page.data)

    logging.info(f'Write data to {p_file}.')
    p_file.write_text(json.dumps(wikidata))

    time.sleep(1)
