import requests
import os
from tqdm import tqdm

# Función para obtener el JSON desde un endpoint
def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Función para obtener la URL del bitstream y el nombre del archivo
def get_bitstream_info(uuid):
    base_url = f"https://repositorio.uniandes.edu.co/server/api/core/items/{uuid}/bundles"
    bundles_json = get_json(base_url)

    for bundle in bundles_json:
        if bundle['name'] == 'ORIGINAL':
            bitstreams_url = bundle['_links']['bitstreams']['href']
            bitstreams_json = get_json(bitstreams_url)

            # TODO ESTA PARTE HAY QUE REVISARLA, NO ES CLARO DONDE (URL) DESCARGAR EL ARCHIVO FINAL CON EL NOMBRE ENCONTRADO EN EL BUNDLE
            if bitstreams_json:
                bitstream_url = bitstreams_json[0]['_links']['content']['href']
                file_name = bitstreams_json[0]['name']
                return bitstream_url, file_name

    return None, None

# Función para descargar el archivo desde la URL del bitstream
def download_file(bitstream_url, file_name, download_dir='downloads'):
    response = requests.get(bitstream_url, stream=True)
    if response.status_code == 200:
        os.makedirs(download_dir, exist_ok=True)
        file_path = os.path.join(download_dir, file_name)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Archivo descargado: {file_path}")
    else:
        response.raise_for_status()

# Lista de UUIDs para los items a descargar
uuids = [
    'uuid1',
    'uuid2',
    'uuid3',
    # Agregar más UUIDs según sea necesario
]

# Proceso ETL
for uuid in tqdm(uuids):
    print(f"Procesando UUID: {uuid}")
    bitstream_url, file_name = get_bitstream_info(uuid)
    if bitstream_url and file_name:
        download_file(bitstream_url, file_name)
    else:
        print(f"No se encontró el bitstream para el UUID: {uuid}")
