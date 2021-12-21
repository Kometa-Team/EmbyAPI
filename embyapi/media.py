#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from typing import List, Dict, Optional

from embyapi import utils
from embyapi.base import EmbyObject, EmbyPartialObject


@utils.register_emby_object
class Folder(EmbyPartialObject):
    TYPE = "Folder"

    def _load(self, data):
        self._data = data
        self.id: str = data['Id']
        self.name: str = data['Name']
        self.type: str = data['Type']

        self.path: Optional[str] = data.get("Path")
        self.parent_id: Optional[str] = data.get("ParentId")
        self.sort_name: Optional[str] = data.get("SortName")
        self.is_folder: Optional[bool] = utils.cast(bool, data.get("IsFolder"))
        self.image_tags: Optional[Dict[str, str]] = data.get("ImageTags")
        self.backdrop_image_tags: Optional[List[str]] = data.get("BackdropImageTags")


class Image(EmbyObject):
    def _load(self, data):
        self._data = data
        self.filename: str = data['Filename']
        self.image_type: str = data['ImageType']
        self.image_index: str = data['ImageIndex']

        self.path: Optional[str] = data.get("Path")
        self.size: Optional[int] = data.get("Size")
        self.height: Optional[int] = data.get("Height")
        self.width: Optional[int] = data.get("Width")
