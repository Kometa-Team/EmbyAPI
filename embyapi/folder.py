#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import List

from embyapi.base import EmbyObject, EmbyPartialObject


class LibraryFolder(EmbyObject):
    TAG = "CollectionType"

    def _load(self, folder):
        self.id: str = folder['Id']
        self.name: str = folder['Name']
        self.path: str = folder['Path']
        self.type: str = folder[self.TAG]

    def items(self) -> List[EmbyPartialObject]:
        return self.fetch_items("Items", **{'ParentId': self.id})

    def total_items(self) -> int:
        params = {
            'ParentId': self.id,
        }
        path = "Items"
        response = self._server.query(method="GET", api_path=path, params=params)

        return len(response.json()['Items'])


class MovieFolder(LibraryFolder):
    TYPE = "movies"


class ShowFolder(LibraryFolder):
    TYPE = "tvshows"
