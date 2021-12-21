#!/usr/bin/env python3
# -*- coding: utf-8 -*-


EMBY_OBJECTS = {}


def register_emby_object(cls):
    """ Registry of library types we may come across when parsing JSON. This allows us to
        define a few helper functions to dynamically convert the JSON into objects.
    """
    emby_type = getattr(cls, "TYPE", cls.TYPE)
    emby_hash = f"{emby_type}"
    if emby_hash in EMBY_OBJECTS:
        raise Exception(f"Ambiguous EmbyObject definition {cls.__name__}(type={emby_type}) with "
                        f"{EMBY_OBJECTS[emby_hash].__name__}")
    EMBY_OBJECTS[emby_hash] = cls
    return cls


def cast(func, value):
    """ Cast the specified value to the specified type (returned by func). Currently this
        only support str, int, float, bool. Should be extended if needed.

        Parameters:
            func (func): Calback function to used cast to type (int, bool, float).
            value (any): value to be cast and returned.
    """
    if value is not None:
        if func == bool:
            if value in (1, True, "1", "true"):
                return True
            elif value in (0, False, "0", "false"):
                return False
            else:
                raise ValueError(value)

        elif func in (int, float):
            try:
                return func(value)
            except ValueError:
                return float('nan')
        return func(value)
    return value
