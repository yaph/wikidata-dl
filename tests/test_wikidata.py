# -*- coding: utf-8 -*-
from wikidata_dl import wikidata

from pathlib import Path


data_dir = Path('tests/data').absolute()
result_csv = data_dir.joinpath('continents-on-earth.csv').read_text()
result_json = data_dir.joinpath('continents-on-earth.json').read_text()
sample_record = ['http://www.wikidata.org/entity/Q51', 'Antarctica', 14200000.0, '🇦🇶']


def is_record(rec):
    return len(rec) and list == type(rec)


def test_records_csv():
    for rec in wikidata.records(result_csv, format='csv'):
        assert is_record(rec)


def test_records_json():
    for rec in wikidata.records(result_json, format='json'):
        assert is_record(rec)


def test_wikibase_ids():
    assert ['Q51'] == wikidata.wikibase_ids(sample_record)
