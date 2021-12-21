#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional

from embyapi.utils import EMBY_OBJECTS
from embyapi.exceptions import UnknownType

if TYPE_CHECKING:
    from embyapi.server import EmbyServer


class EmbyObject(object):
    def __init__(self, server: EmbyServer, *args, **kwargs):
        self._server = server
        self._load(*args, **kwargs)

    def _load(self, data):
        raise NotImplementedError("Abstract method not implemented.")

    def _build_item(self, item, cls=None):
        emby_class: Optional[type] = cls

        if emby_class is None:
            emby_type: Optional[str] = item.get("Type")
            emby_hash = f"{emby_type}"
            emby_class: Optional[type] = EMBY_OBJECTS.get(emby_hash)
            if emby_class is None:
                raise UnknownType(f"Unknown item type: '{emby_type}': {item}")

        return emby_class(self._server, item)

    def fetch_items(self, path, **kwargs):
        params = {}

        fields = "Name,DateCreated,ServerId,Id,ParentId,Path,ProductionYear,ProviderIds,SortName"
        additional_fields: Optional[str] = kwargs.pop("Fields")
        if additional_fields is not None:
            fields += f",{additional_fields}"
        params['Fields'] = fields

        parent_id: Optional[str] = kwargs.pop("ParentId")
        if parent_id is not None:
            params['ParentId'] = parent_id

        response = self._server.query(method="GET", api_path=path, params=params)

        _items: List[EmbyPartialObject] = []
        for item in response.json()['Items']:
            _items.append(self._build_item(item, kwargs.get("cls")))

        return _items


class EmbyPartialObject(EmbyObject):
    def _load(self, data):
        raise NotImplementedError("Abstract method not implemented.")
