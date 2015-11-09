# schema-transformer

[![Master Build Status](https://travis-ci.org/fabianvf/schema-transformer.svg?branch=master)](https://travis-ci.org/fabianvf/schema-transformer)

A library for transforming JSON, XML, or CSV files in various schemas, into JSON.

Docs are a WIP at the moment

## Transformers ##
This module provides a declarative way to map data from an arbitrary XML, JSON, or CSV format to a json schema that you specify. The schema transformers have a schema defined within them. This schema takes the form of a python dictionary. The keys of the schema correspond to the desired (or target) schema, and the values correspond to a small language developed internally to handle pulling the corresponding values from the source schema.

### General language ###
Some pieces of the language are dependent on the type of transformer, but in general the language has the following grammar:
```
schema :: map[key -> value]

key :: JSON_key_string

value :: primitive | (primitive, primitive, ... , post_func) | ((args, kwargs), post_func) | schema

args :: (primitive, ... , primitive)

kwargs :: map[name -> primitive]

primitive :: string | pre_func

pre_func :: function[raw_metadata -> Any]

post_func :: function[(Any, ..., Any) -> JSON_value]
```

schema: At its core, the schema is just a mapping from keys to values

key: a key is simply a valid JSON string that can be a key

value: a value can be a primitive value, a tuple of primitive values with a post processing function at the end, a tuple of unnamed and named arguments with a function that will take those arguments, or a nested schema

args: args can be a tuple of primitive values

kwargs: kwargs can be a mapping of named arguments (keys) to primitive values

primitive: a primitive can either be a string (used by individual transformers to find data), or a pre_func.

pre_func: a function that takes a raw metadata document and does some processing on that document. The return type of the function is not tracked, but the return value will eventually be fed to a post_func

post_func: a function that takes the results of processing the preceding primitives (either (args, kwargs) or the tuple of primitives) and maps them to the single value that is the actual intended value for the given key.

#### Strings ####

Something missing from the above grammar is any information about the actual meaning of the ```string``` type. This is because the actual strings are defined in individual transformers. So far we have implemented three transformers, an XML to JSON transformer, a JSON to JSON transformer, and a CSV to JSON transformer. The semantics of these are defined below:

#### XML Transformer ####

```
string :: XPath_command
```

The XML transformer string semantics are fairly simple. Each string is a valid XPath command. When a string is encountered, the transformer essentially does the following:

```
def transform_string(string, doc):
    return doc.xpath(string)
```
The Xpath implementation we use is provided by lxml. To get started, see [XPath with lxml](http://lxml.de/xpathxslt.html#xpath)


The [full XPath reference](http://www.w3.org/TR/xpath/) may also be helpful.

#### JSON Transformer ####

```
string :: JSON_pointer (RFC6901)
```

When the JSON transformer encounters a string, which can be any valid [RFC6901](https://tools.ietf.org/html/rfc6901) JSON pointer, it simply resolves the pointer and returns the value. For example, the string ```"/data/tidbits/title"``` would return the value located at ```metadata['data']['tidbits']['title']```

```python
def transform_string(val, doc):
    return resolve_pointer(doc, val)
```

If the pointer fails to resolve, the value defaults to the empty string.

#### CSV Transformer ####
 TODO

## Usage

### XMLTransformer
_note: This will require you to have `lxml` installed, which is not listed as a requirement of this library due to its size and installation complexity_
```python
from schema_transformer.transformers import XMLTransformer
```
### JSONTransformer
```python
from schema_transformer.transformers import JSONTransformer
```
### CSVTransformer
The CSV transformer is initialized with a list of keys, where the position of each key in the list indicates which element it is in the CSV document. This allows you to write the schemas using the textual keys, rather than the index numbers.
```python
from schema_transformer.transformers import CSVTransformer
```

