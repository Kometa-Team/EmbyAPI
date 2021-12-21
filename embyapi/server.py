#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from typing import List

from embyapi.base import EmbyObject
from embyapi.library import Library, MovieLibrary, ShowLibrary

# Need these imports to populate utils.EMBY_OBJECTS
from embyapi import media as _media  # noqa: F401
from embyapi import video as _video  # noqa: F401


class EmbyServer(EmbyObject):
    url = ""
    api_key = ""

    _session = requests.Session()
    _timeout = 60

    def __init__(self, url: str, api_key: str, session=None, timeout=60):
        self.url = url
        self.api_key = api_key
        self._timeout = timeout

        if isinstance(session, requests.Session):
            self._session = session

        path = "emby/system/info/public"
        data = self._server.query(method="GET", api_path=path)
        super().__init__(self, data)

    def _load(self, data):
        self._data = data
        self.id = data['Id']
        self.name = data['ServerName']
        self.version = data['Version']
        self.wan_address = data['WanAddress']

    def query(self, method, api_path="", headers=None, params=None, data=None, json=None):
        if params is None:
            params = {}
        if headers is None:
            headers = {}

        api_url = f"{self.url}/{api_path}"

        headers.update({
            'X-Emby-Token': self.api_key
        })

        if data is not None and json is None:
            headers.update({
                'Content-type': "application/octet-stream"
            })

        response = self._session.request(method, api_url, timeout=self._timeout,
                                         headers=headers, params=params, data=data,
                                         json=json)
        response.raise_for_status()

        return response

    def libraries(self) -> List[Library]:
        media_folders_path = "emby/Library/SelectableMediaFolders"
        media_folders_response = self.query(method="GET", api_path=media_folders_path)

        virtual_folders_path = "emby/Library/VirtualFolders"
        virtual_folders_response = self.query(method="GET", api_path=virtual_folders_path)

        _libraries = []
        for virtual_folder in virtual_folders_response.json():
            sub_folders = []

            for media_folder in media_folders_response.json():
                if media_folder['Id'] == virtual_folder['ItemId']:
                    sub_folders = media_folder.get("SubFolders", [])
                    break

            virtual_folder['SubFolders'] = sub_folders

            if virtual_folder[Library.TAG] == MovieLibrary.TYPE:
                _libraries.append(MovieLibrary(self, virtual_folder))
            elif virtual_folder[Library.TAG] == ShowLibrary.TYPE:
                _libraries.append(ShowLibrary(self, virtual_folder))
            else:
                _libraries.append(Library(self, virtual_folder))

        return _libraries
