import os
from urllib.parse import urlparse

import requests

from storage_helper import StorageHelper


class ImageHelper:
    FILE_WRITE_BYTES_MODE: str = 'wb'

    def __init__(self, storage_helper: StorageHelper):
        self.storage_helper: StorageHelper = storage_helper

    def _extract_basename(self, url: str) -> str:
        a_parsed = urlparse(url)
        return os.path.basename(a_parsed.path)

    def download_img(self, url: str) -> None:
        if url:
            response = requests.get(url)
            basename_img: str = self._extract_basename(url)

            # enregistrer
            storage_path: str = os.path.join(self.storage_helper.img_storage_path, basename_img)
            file = open(storage_path, ImageHelper.FILE_WRITE_BYTES_MODE)
            file.write(response.content)
            file.close()