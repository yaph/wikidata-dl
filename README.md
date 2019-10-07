# wikidata-dl

## Description

**wikidata-dl** is a command line program for downloading data from [Wikidata](https://www.wikidata.org/) based on [SPARQL](https://en.wikipedia.org/wiki/SPARQL) queries.

## Installation

    pip install wikidata_dl

## Usage

    wikidata-dl /path/to/my-query.sparql

## Sample Query

The following query returns IDs for all Wikidata entities that are an instance of ([P31](https://www.wikidata.org/wiki/Property:P31)) a continent ([Q5107](https://www.wikidata.org/wiki/Q5107)).

    SELECT ?item WHERE {
        ?item wdt:P31 wd:Q5107.
    }

## Conventions

* The SPARQL query you pass to the program must return [Wikibase](https://www.mediawiki.org/wiki/Wikibase/DataModel/Primer) IDs.
* The query variable where the entity ID is stored must be called ``item``.