#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import base64
from typing import List, Dict, Optional

from embyapi import utils
from embyapi.base import EmbyPartialObject
from embyapi.media import Image


class Video(EmbyPartialObject):
    def _load(self, data):
        self._data = data
        self.id: str = data['Id']
        self.name: str = data['Name']
        self.type: str = data['Type']

        self.path: Optional[str] = data.get("Path")
        self.year: Optional[int] = data.get("ProductionYear")
        self.parent_id: Optional[str] = data.get("ParentId")
        self.sort_name: Optional[str] = data.get("SortName")
        self.media_type: Optional[str] = data.get("MediaType")
        self.run_time_ticks: Optional[int] = data.get("RunTimeTicks")
        self.is_folder: Optional[bool] = utils.cast(bool, data.get("IsFolder"))
        self.image_tags: Optional[Dict[str, str]] = data.get("ImageTags")
        self.backdrop_image_tags: Optional[List[str]] = data.get("BackdropImageTags")

    def images(self):
        return self.fetch_items(f"Items/{self.id}/Images", **{'cls': Image})

    def upload_image(self, image_type: str, filepath: str):
        path = f"Items/{self.id}/Images/{image_type}"
        with open(filepath, 'rb') as image:
            b64_image = base64.b64encode(image.read())
        return self._server.query(method="POST", api_path=path, data=b64_image)


@utils.register_emby_object
class Movie(Video):
    TYPE = "Movie"

    def _load(self, data):
        Video._load(self, data)


@utils.register_emby_object
class Show(Video):
    TYPE = "Show"

    def _load(self, data):
        Video._load(self, data)


@utils.register_emby_object
class Season(Video):
    TYPE = "Season"

    def _load(self, data):
        Video._load(self, data)


@utils.register_emby_object
class Episode(Video):
    TYPE = "Episode"

    def _load(self, data):
        Video._load(self, data)
