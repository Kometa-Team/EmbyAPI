#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class EmbyApiException(Exception):
    """ Base class for all PlexAPI exceptions. """
    pass


class BadRequest(EmbyApiException):
    """ An invalid request, generally a user error. """
    pass


class NotFound(EmbyApiException):
    """ Request media item or device is not found. """
    pass


class UnknownType(EmbyApiException):
    """ Unknown library type. """
    pass


class Unsupported(EmbyApiException):
    """ Unsupported client request. """
    pass


class Unauthorized(BadRequest):
    """ Invalid username/password or token. """
    pass
