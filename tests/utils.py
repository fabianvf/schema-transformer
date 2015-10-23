from schema_transformer.helpers import compose, single_result


TEST_XML_DOC = b'''
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcq="http://purl.org/dc/terms/">
        <records count="97" morepages="true" start="1" end="10">
            <record rownumber="1">
                <dc:title>Test</dc:title>
                <dc:creator>
                Raveh-Sadka, Tali; Thomas, Brian C; Singh, Andrea; Firek, Brian; Brooks,
                Brandon; Castelle, Cindy J; Sharon, Itai; Baker, Robyn; Good, Misty; Morowitz,
                Michael J; Banfield, Jillian F
                </dc:creator>
                <dc:subject/>
                <dc:subjectRelated/>
                <dc:description/>
                <dcq:publisher>
                    eLife Sciences Publications, Ltd.
                </dcq:publisher>
                <dcq:publisherAvailability/>
                <dcq:publisherResearch>
                    None
                </dcq:publisherResearch>
                <dcq:publisherSponsor>
                    USDOE
                </dcq:publisherSponsor>
                <dcq:publisherCountry>
                    Country unknown/Code not available
                </dcq:publisherCountry>
                <dc:date>
                    2015-03-03
                </dc:date>
                <dc:language>
                    English
                </dc:language>
                <dc:type>
                    Journal Article
                </dc:type>
                <dcq:typeQualifier/>
                <dc:relation>
                    Journal Name: eLife; Journal Volume: 4
                </dc:relation>
                <dc:coverage/>
                <dc:format>
                    Medium: X
                </dc:format>
                <dc:identifier>
                    OSTI ID: 1171761, Legacy ID: OSTI ID: 1171761
                </dc:identifier>
                <dc:identifierReport>
                    None
                </dc:identifierReport>
                <dcq:identifierDOEcontract>
                    5R01AI092531; Long term fellowship; SC0004918; ER65561; APSF-2012-10-05
                </dcq:identifierDOEcontract>
                <dc:identifierOther>Journal ID: ISSN 2050-084X</dc:identifierOther>
                <dc:doi>10.7554/eLife.05477</dc:doi><dc:rights/>
                <dc:dateEntry>2015-03-05</dc:dateEntry>
                <dc:dateAdded>2015-03-05</dc:dateAdded>
                <dc:ostiId>1171761</dc:ostiId>
                <dcq:identifier-purl type=""/>
                <dcq:identifier-citation>
                    http://www.osti.gov/pages/biblio/1171761
                </dcq:identifier-citation>
            </record>
        </records>
    </rdf:RDF>
'''
TEST_SCHEMA = {
    "description": ('//dc:description/node()', compose(lambda x: x.strip(), single_result)),
    "contributors": ('//dc:creator/node()', compose(lambda x: x.split(';'), single_result)),
    "title": ("//dc:title/node()", lambda x: "Title overwritten"),
    "providerUpdatedDateTime": ('//dc:dateEntry/node()', single_result),
    "uris": {
        "canonicalUri": ('//dcq:identifier-citation/node()', compose(lambda x: x.strip(), single_result)),
        "objectUris": [('//dc:doi/node()', compose(lambda x: 'http://dx.doi.org/' + x, single_result))]
    },
    "languages": ("//dc:language/text()", single_result),
    "publisher": {
        "name": ("//dcq:publisher/node()", single_result)
    },
    "sponsorships": [{
        "sponsor": {
            "sponsorName": ("//dcq:publisherSponsor/node()", single_result)
        }
    }]
}

TEST_NAMESPACES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcq': 'http://purl.org/dc/terms/'
}
