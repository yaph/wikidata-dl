#!/usr/bin/env python
import json

from pathlib import Path


data = json.loads(Path('./tests/data/en/Q15.json').read_text())

labels = data['labels']
claims = data['claims']

doc = {
    'description': data['description'],
    'abstract': data['exrest'],
    'image': data['image'][0]['url'],
    'label': data['label'],
    'title': data['title'],
    'wikibase': data['wikibase'],
}

for key, values in claims.items():
    doc[labels[key]] = [labels.get(v, v) for v in values if isinstance(v, str)]
