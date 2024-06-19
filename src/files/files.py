import os
import requests

from src.utils.utils import get_json

# Función para obtener la URL del bitstream y el nombre del archivo
def get_bitstream_info(uuid):
    base_url = f"https://repositorio.uniandes.edu.co/server/api/core/items/{uuid}/bundles"
    bundles = get_json(base_url)["_embedded"]["bundles"]
    bitstream_url, file_name = None, None
    for bundle in bundles:
        if bundle['name'] == 'TEXT':
            bitstreams_url = bundle['_links']['bitstreams']['href']
            bitstream = get_json(bitstreams_url)["_embedded"]["bitstreams"][0]
            bitstream_url = bitstream['_links']['content']['href']
            file_name = uuid + '.pdf.txt'
    return bitstream_url, file_name

# Función para descargar el archivo desde la URL del bitstream
def download_file(bitstream_url, file_name, download_dir='./downloads'):
    response = requests.get(bitstream_url, stream=True)
    if response.status_code == 200:
        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, file_name)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        response.raise_for_status()