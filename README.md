# wikidata-dl

## Description

**wikidata-dl** is a command line programm for downloading data from [Wikidata](https://www.wikidata.org/) based on [SPARQL](https://en.wikipedia.org/wiki/SPARQL) queries passed to the program.

## Installation

    pip install wikidata_dl

## Usage

    wikidata-dl /path/to/my-query.sparql

## Conventions

* The SPARQL query you pass to the program must return Wikidata entity IDs.
* The query variable where the entity ID is stored must be called ``item``.