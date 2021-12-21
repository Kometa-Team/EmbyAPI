#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import List

from embyapi.base import EmbyObject, EmbyPartialObject
from embyapi.folder import LibraryFolder, MovieFolder, ShowFolder


class Library(EmbyObject):
    TAG = "CollectionType"

    def _load(self, library):
        self.id: str = library['ItemId']
        self.name: str = library['Name']
        self.type: str = library[self.TAG]
        self._folders: List[LibraryFolder] = []

        for folder in library.get("SubFolders", []):
            folder['CollectionType'] = self.type
            if self.type == MovieFolder.TYPE:
                self._folders.append(MovieFolder(self._server, folder))
            elif self.type == ShowFolder.TYPE:
                self._folders.append(ShowFolder(self._server, folder))
            else:
                self._folders.append(LibraryFolder(self._server, folder))

    def folders(self) -> List[LibraryFolder]:
        return self._folders

    def items(self) -> List[EmbyPartialObject]:
        return self.fetch_items("emby/Items", **{'ParentId': self.id})

    def total_items(self) -> int:
        params = {
            'ParentId': self.id,
        }
        path = "emby/Items"
        response = self._server.query(method="GET", api_path=path, params=params)

        return len(response.json()['Items'])


class MovieLibrary(Library):
    TYPE = "movies"


class ShowLibrary(Library):
    TYPE = "tvshows"
