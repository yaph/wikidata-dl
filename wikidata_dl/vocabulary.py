# -*- coding: utf-8 -*-
# Constants that define OWL and RDF vocabularies.
#
# Source: https://github.com/Wikidata/Wikidata-Toolkit/blob/master/wdtk-rdf/src/main/java/org/wikidata/wdtk/rdf/Vocabulary.java
#
# Wikidata Toolkit RDF
# Copyright (C) 2014 Wikidata Toolkit Developers
# Apache-2.0 license

PREFIX_WIKIDATA_ENTITY = 'http://www.wikidata.org/entity/'
PREFIX_WIKIDATA_STATEMENT = 'http://www.wikidata.org/entity/statement/'

PREFIX_PROPERTY = 'http://www.wikidata.org/prop/'
PREFIX_PROPERTY_STATEMENT = 'http://www.wikidata.org/prop/statement/'
PREFIX_PROPERTY_STATEMENT_VALUE = 'http://www.wikidata.org/prop/statement/value/'
PREFIX_PROPERTY_DIRECT = 'http://www.wikidata.org/prop/direct/'
PREFIX_PROPERTY_QUALIFIER = 'http://www.wikidata.org/prop/qualifier/'
PREFIX_PROPERTY_QUALIFIER_VALUE = 'http://www.wikidata.org/prop/qualifier/value/'
PREFIX_PROPERTY_REFERENCE = 'http://www.wikidata.org/prop/reference/'
PREFIX_PROPERTY_REFERENCE_VALUE = 'http://www.wikidata.org/prop/reference/value/'

PREFIX_GEO = 'http://www.opengis.net/ont/geosparql#'

PREFIX_WIKIDATA_REFERENCE = 'http://www.wikidata.org/reference/'
PREFIX_WIKIDATA_NO_VALUE = 'http://www.wikidata.org/prop/novalue/'
PREFIX_WIKIDATA_NO_QUALIFIER_VALUE = PREFIX_WIKIDATA_NO_VALUE
PREFIX_WIKIDATA_VALUE = 'http://www.wikidata.org/value/'

PREFIX_WBONTO = 'http://wikiba.se/ontology#'
PREFIX_RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
PREFIX_RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
PREFIX_OWL = 'http://www.w3.org/2002/07/owl#'
PREFIX_XSD = 'http://www.w3.org/2001/XMLSchema#'
PREFIX_SCHEMA = 'http://schema.org/'
PREFIX_SKOS = 'http://www.w3.org/2004/02/skos/core#'
PREFIX_PROV = 'http://www.w3.org/ns/prov#'

# Vocabulary elements that are part of ontology language standards
RDF_TYPE = PREFIX_RDF + 'type'
RDF_LANG_STRING = PREFIX_RDF + 'langString'
RDFS_LABEL = PREFIX_RDFS + 'label'
RDFS_SEE_ALSO = PREFIX_RDFS + 'seeAlso'
RDFS_LITERAL = PREFIX_RDFS + 'Literal'
RDFS_SUBCLASS_OF = PREFIX_RDFS + 'subClassOf'
RDFS_SUBPROPERTY_OF = PREFIX_RDFS + 'subPropertyOf'
OWL_THING = PREFIX_OWL + 'Thing'
OWL_CLASS = PREFIX_OWL + 'Class'
OWL_OBJECT_PROPERTY = PREFIX_OWL + 'ObjectProperty'
OWL_DATATYPE_PROPERTY = PREFIX_OWL + 'DatatypeProperty'
OWL_RESTRICTION = PREFIX_OWL + 'Restriction'
OWL_SOME_VALUES_FROM = PREFIX_OWL + 'someValuesFrom'
OWL_ON_PROPERTY = PREFIX_OWL + 'onProperty'
OWL_COMPLEMENT_OF = PREFIX_OWL + 'complementOf'
XSD_DOUBLE = PREFIX_XSD + 'double'
XSD_DECIMAL = PREFIX_XSD + 'decimal'
XSD_INT = PREFIX_XSD + 'int'
XSD_DATE = PREFIX_XSD + 'date'
XSD_G_YEAR = PREFIX_XSD + 'gYear'
XSD_G_YEAR_MONTH = PREFIX_XSD + 'gYearMonth'
XSD_DATETIME = PREFIX_XSD + 'dateTime'
XSD_STRING = PREFIX_XSD + 'string'
OGC_LOCATION = PREFIX_GEO + 'wktLiteral'

# IRIs of property datatypes
DT_ITEM = PREFIX_WBONTO + 'WikibaseItem'
DT_PROPERTY = PREFIX_WBONTO + 'WikibaseProperty'
DT_LEXEME = PREFIX_WBONTO + 'WikibaseLexeme'
DT_FORM = PREFIX_WBONTO + 'WikibaseForm'
DT_SENSE = PREFIX_WBONTO + 'WikibaseSense'
DT_MEDIA_INFO = PREFIX_WBONTO + 'WikibaseMediaInfo'
DT_STRING = PREFIX_WBONTO + 'String'
DT_URL = PREFIX_WBONTO + 'Url'
DT_COMMONS_MEDIA = PREFIX_WBONTO + 'CommonsMedia'
DT_TIME = PREFIX_WBONTO + 'Time'
DT_GLOBE_COORDINATES = PREFIX_WBONTO + 'GlobeCoordinate'
DT_QUANTITY = PREFIX_WBONTO + 'Quantity'
DT_MONOLINGUAL_TEXT = PREFIX_WBONTO + 'Monolingualtext'
DT_EXTERNAL_ID = PREFIX_WBONTO + 'ExternalId'
DT_MATH = PREFIX_WBONTO + 'Math'
DT_GEO_SHAPE = PREFIX_WBONTO + 'GeoShape'
DT_TABULAR_DATA = PREFIX_WBONTO + 'TabularData'
DT_EDTF = PREFIX_WBONTO + 'Edtf'
