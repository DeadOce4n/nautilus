from collections.abc import Iterable, Callable

def for_each(callback: Callable, iterable: Iterable):
    for element in iterable:
        callback(element)
