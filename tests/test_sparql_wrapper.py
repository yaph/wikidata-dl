from wikidata_dl.wikidata import wrap_query_with_last_updated


def test_basic_query_wrapping():
    """Tests that a standard simple query gets wrapped correctly."""
    query = "SELECT ?item WHERE { ?item wdt:P31 wd:Q146. }"
    result = wrap_query_with_last_updated(query, entity_var="item")

    assert "SELECT DISTINCT * WHERE {" in result
    assert "OPTIONAL { ?item schema:dateModified ?itemLastUpdated . }" in result
    assert query in result


def test_preserves_prefix_declarations():
    """PREFIX statements must remain outside the inner subquery block."""
    query = """PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>
SELECT ?item WHERE { ?item wdt:P31 wd:Q146. }"""

    result = wrap_query_with_last_updated(query, entity_var="item")

    # Prefixes should appear before the main SELECT DISTINCT block
    prefix_pos = result.find("PREFIX wdt:")
    select_pos = result.find("SELECT DISTINCT * WHERE")

    assert prefix_pos != -1
    assert select_pos != -1
    assert prefix_pos < select_pos
    assert "OPTIONAL { ?item schema:dateModified ?itemLastUpdated . }" in result


def test_skips_query_with_existing_date_modified():
    """If the query already selects schema:dateModified, return it unchanged."""
    query = """
    SELECT ?item ?lastUpdated WHERE {
      ?item wdt:P31 wd:Q9143 .
      ?item schema:dateModified ?lastUpdated .
    }
    """
    result = wrap_query_with_last_updated(query, entity_var="item")
    assert result == query


def test_handles_entity_var_formatting():
    """Normalizes entity_var whether passed with or without a leading '?'."""
    query = "SELECT ?concept WHERE { ?concept wdt:P31 wd:Q146. }"

    # Test passing without '?'
    result_no_question = wrap_query_with_last_updated(query, entity_var="concept")
    assert "OPTIONAL { ?concept schema:dateModified ?conceptLastUpdated . }" in result_no_question

    # Test passing with '?'
    result_with_question = wrap_query_with_last_updated(query, entity_var="?concept")
    assert "OPTIONAL { ?concept schema:dateModified ?conceptLastUpdated . }" in result_with_question


def test_case_insensitive_prefix_handling():
    """Ensures lowercase or mixed-case 'prefix' statements are properly handled."""
    query = "prefix wdt: <http://www.wikidata.org/prop/direct/>\nSELECT ?item WHERE { ?item wdt:P31 wd:Q146. }"
    result = wrap_query_with_last_updated(query, entity_var="item")

    assert result.startswith("prefix wdt:")
    assert "OPTIONAL { ?item schema:dateModified ?itemLastUpdated . }" in result


def test_multiline_complex_query():
    """Verifies behavior on a realistic multi-line query with MINUS clauses."""
    query = """# Programming Languages
SELECT DISTINCT ?item ?itemLabel WHERE {
  ?item (wdt:P31/wdt:P279*) wd:Q9143.
  MINUS { ?item wdt:P31 wd:Q184148. }
}"""

    result = wrap_query_with_last_updated(query, entity_var="item")

    assert "SELECT DISTINCT * WHERE {" in result
    assert "MINUS { ?item wdt:P31 wd:Q184148. }" in result
    assert "OPTIONAL { ?item schema:dateModified ?itemLastUpdated . }" in result
