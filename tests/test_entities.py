import json
from pathlib import Path

from wikidata_dl import wikidata


def test_scheme():
    # Scheme has a "mul" label, but no English label. This is a special case that should be handled by the get_mul_label function.
    wikibase = 'Q187560'
    basedir = Path('/tmp')
    wikidata.download(wikibase, basedir, 1, 'en')
    file = basedir / f'{wikibase}.json'
    assert file.exists()
    data = json.loads(file.read_text())
    assert data['wikibase'] == wikibase
    assert data['label'] == 'Scheme'
