import functools
from copy import deepcopy


def compose(*functions):
    ''' evaluates functions from right to left.

        >>> add = lambda x, y: x + y
        >>> add3 = lambda x: x + 3
        >>> divide2 = lambda x: x/2
        >>> subtract4 = lambda x: x - 4
        >>> subtract1 = compose(add3, subtract4)
        >>> subtract1(1)
        0
        >>> compose(subtract1, add3)(4)
        6
        >>> compose(int, add3, add3, divide2)(4)
        8
        >>> compose(int, divide2, add3, add3)(4)
        5
        >>> compose(int, divide2, compose(add3, add3), add)(7, 3)
        8
    '''
    def inner(func1, func2):
        return lambda *x, **y: func1(func2(*x, **y))
    return functools.reduce(inner, functions)


def updated_schema(old, new):
    ''' Creates a dictionary resulting from adding all keys/values of the second to the first
        The second dictionary will overwrite the first.

        >>> old, new = {'name': 'ric', 'job': None}, {'name': 'Rick'}
        >>> updated = updated_schema(old, new)
        >>> len(updated.keys())
        2
        >>> print(updated['name'])
        Rick
        >>> updated['job'] is None
        True

    '''
    d = deepcopy(old)
    for key, value in new.items():
        if isinstance(value, dict) and old.get(key) and isinstance(old[key], dict):
            d[key] = updated_schema(old[key], new[key])
        else:
            d[key] = value
    return d


def single_result(l, default=''):
    ''' A function that will return the first element of a list if it exists

        >>> print(single_result(['hello', None]))
        hello
        >>> print(single_result([], default='hello'))
        hello
        >>> print(single_result([]))
        <BLANKLINE>

    '''
    return l[0] if l else default
