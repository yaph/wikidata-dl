# wikidata-dl

## Description

**wikidata-dl** is a command line program for downloading data from [Wikidata](https://www.wikidata.org/) based on [SPARQL](https://en.wikipedia.org/wiki/SPARQL) queries.

## Installation

    pip install wikidata-dl

## Usage

Download result returned from the query and save it in the directory `./wikidata`:

    wikidata-dl /path/to/my-query.sparql

For a complete reference of the command line options run:

    wikidata-dl --help

## Sample Query

The following query returns IDs for all Wikidata entities that are an instance of ([P31](https://www.wikidata.org/wiki/Property:P31)) a continent ([Q5107](https://www.wikidata.org/wiki/Q5107)).

    SELECT ?item WHERE {
        ?item wdt:P31 wd:Q5107.
    }

[Try the query](https://query.wikidata.org/#SELECT%20%3Fitem%20WHERE%20%7B%20%3Fitem%20wdt%3AP31%20wd%3AQ5107.%20%7D)