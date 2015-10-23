from __future__ import unicode_literals

import pytest
from six.moves import xrange
from lxml.etree import XPathEvalError
from jsonschema.exceptions import ValidationError

from schema_transformer.transformer import XMLTransformer
from schema_transformer.helpers import updated_schema, CONSTANT

from .utils import TEST_SCHEMA, TEST_NAMESPACES, TEST_XML_DOC


class TestTransformer(object):

    def setup_method(self, method):
        self.transformer = XMLTransformer(TEST_SCHEMA, namespaces=TEST_NAMESPACES)

    def test_arg_kwargs(self):
        def process_title(title, title1="test"):
            return title[0] + (title1[0] if isinstance(title1, list) else title1)

        def process_title2(title1="test"):
            return title1[0] if isinstance(title1, list) else title1

        args = ("//dc:title/node()", )
        kwargs = {"title1": "//dc:title/node()"}

        self.transformer.schema = updated_schema(
            TEST_SCHEMA,
            {
                'title': ((args, kwargs), process_title),
            }
        )

        result = self.transformer.transform(TEST_XML_DOC)

        assert result['title'] == "TestTest"

    def test_transform(self):
        result = self.transformer.transform(TEST_XML_DOC)

        assert result['title'] == "Title overwritten"

    def test_constants(self):
        self.transformer.schema = updated_schema(
            TEST_SCHEMA, {
                'tags': (CONSTANT(['X']), lambda x: x),
            }
        )
        result = self.transformer.transform(TEST_XML_DOC)

        assert result['tags'] == ['X']

    def test_failing_transformation_with_raises(self):

        self.transformer.schema = updated_schema(TEST_SCHEMA, {'title': 'A completely 1n\/@lid expre55ion'})

        with pytest.raises(XPathEvalError) as e:
            x = self.transformer.transform(TEST_XML_DOC, fail=True)

    def test_failing_transformation_wont_raise(self):
        self.transformer.schema = updated_schema(TEST_SCHEMA, {'title': 'A completely 1n\/@lid expre55ion'})

        x = self.transformer.transform(TEST_XML_DOC, fail=False)
        assert x
