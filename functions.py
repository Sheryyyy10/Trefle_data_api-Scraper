import os
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from urllib.parse import urlparse


def download_image(url, folder_name):
    if url:
        image_name = os.path.basename(urlparse(url).path)
        image_path = os.path.join(folder_name, image_name)
        if not default_storage.exists(image_path):
            response = requests.get(url)
            if response.status_code == 200:
                default_storage.save(image_path, ContentFile(response.content))
        return image_path
    return None