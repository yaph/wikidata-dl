# wikidata-dl

## Description

**wikidata-dl** is a command line program for downloading data from [Wikidata](https://www.wikidata.org/) based on [SPARQL](https://en.wikipedia.org/wiki/SPARQL) queries.

## Installation

    pip install wikidata_dl

## Usage

Download all results returned by the query and store them in the `wikidata` directory in the current working directory:

    wikidata-dl /path/to/my-query.sparql

Show only the result count returned by the query without downloading anything:

    wikidata-dl --dry-run /path/to/my-query.sparql

For a complete reference of the command line options run:

    wikidata-dl --help

## Sample Query

The following query returns IDs for all Wikidata entities that are an instance of ([P31](https://www.wikidata.org/wiki/Property:P31)) a continent ([Q5107](https://www.wikidata.org/wiki/Q5107)).

    SELECT ?item WHERE {
        ?item wdt:P31 wd:Q5107.
    }

## Conventions

* The SPARQL query you pass to the program must return [Wikibase](https://www.mediawiki.org/wiki/Wikibase/DataModel/Primer) IDs.
* The query variable where the entity ID is stored must be called ``item``.