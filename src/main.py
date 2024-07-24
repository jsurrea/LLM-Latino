import pandas as pd
from tqdm import tqdm

from src.utils.utils import get_json
from src.metadata.metadata import extract_metadata
from src.files.files import get_bitstream_info, download_file

def fetch_data(uuids, max_pages=-1):
    base_url = "https://repositorio.uniandes.edu.co/server/api/discover/search/objects?scope={uuid}&configuration=default&page={page}&size=10"
    all_data = []
    
    for uuid in uuids:
        page = 0
        total_pages = 1
        
        with tqdm(total=total_pages, desc=f"UUID {uuid} pages") as pbar:
            while True:
                try:
                    url = base_url.format(uuid=uuid, page=page)
                    json_data = get_json(url)

                    search_result = json_data['_embedded']['searchResult']
                    objects = search_result['_embedded']['objects']
                    
                    with tqdm(total=len(objects), desc=f"Page {page+1} items") as item_pbar:
                        data = extract_metadata(objects)
                        for item in data:
                            try:
                                bitstream_url, file_name = get_bitstream_info(item['uuid'])
                                if bitstream_url is not None and file_name is not None:
                                    download_file(bitstream_url, file_name)
                                item["file_name"] = file_name
                            except Exception as e:
                                item["file_name"] = None
                                print(f"Error downloading file for object {item['uuid']}: {e}")
                            item_pbar.update(1)

                    all_data.extend(data)

                    page_info = search_result.get('page', {})
                    total_pages = page_info.get('totalPages', total_pages)
                
                except Exception as e:
                    print(f"Error fetching data for UUID {uuid} and page {page}: {e}")

                finally:
                    if page >= total_pages - 1 or (max_pages != -1 and page >= max_pages - 1):
                        break
                    if max_pages == -1:
                        pbar.total = total_pages
                    else:
                        pbar.total = max_pages
                    page += 1
                    pbar.update(1)


    df = pd.DataFrame(all_data)
    df.to_csv('downloads/repositorio_uniandes_data.csv', index=False)

uuids = [
    '9d6d8fb8-dfc8-4f12-9689-90922ec6f946', # Administración
    '0253089e-b02f-4c0b-91f6-26d29f64febb', # Arquitectura y Diseño
    'ba3138b7-1e4c-42f9-b462-163936574e64', # Artes y Humanidades
    'f756e30f-8cb4-4090-8d9a-9ffb0f6bab10', # Centro Interdisciplinario de Estudios sobre Desarrollo - CIDER
    'd3c988ec-ea05-484d-a128-da0dbaa52aee', # Ciencias
    'f21012c9-3539-4efd-98ad-f9cabeb446a5', # Ciencias Sociales
    '95b30f28-97de-4a4e-b1f3-3dc71fce1ef0', # Derecho
    '2664c78e-aadd-4c67-815d-aa201c3215b1', # Economía
    '196f68f5-feba-4108-9143-2501834d732d', # Educación
    '811559f7-8706-40a0-82ba-f37cf856bf19', # Escuela de Gobierno Alberto Lleras Camargo
    '4b005e8d-5527-46a9-bbf0-61ce879432b0', # Ingeniería
    '9a8975c9-fcae-4049-a6d5-0bb3f5e5db23', # Medicina
    'bee8fbe6-846f-41e9-8202-e73ea7754aab', # Nodo de Innovación
    'fedfccbb-9f0a-4848-bb7b-20c4f3146fb8', # Secretaría General
    '4272016d-2779-4f32-96fb-e89fed4256e5', # Sistema de Bibliotecas
    'e1e56670-a1c4-4431-b130-031ec2fd7dd2', # Observatorio Regional ODS
]

fetch_data(uuids)  # Descarga las primeras 5 páginas
