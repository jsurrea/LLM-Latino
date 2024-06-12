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
                url = base_url.format(uuid=uuid, page=page)
                json_data = get_json(url)

                search_result = json_data['_embedded']['searchResult']
                objects = search_result['_embedded']['objects']
                
                with tqdm(total=len(objects), desc=f"Page {page+1} items") as item_pbar:
                    data = extract_metadata(objects)
                    for item in data:
                        bitstream_url, file_name = get_bitstream_info(item['uuid'])
                        try:
                            download_file(bitstream_url, file_name)
                            item["file_name"] = file_name
                        except Exception:
                            item["file_name"] = None
                        item_pbar.update(1)

                all_data.extend(data)

                page_info = search_result['page']
                total_pages = page_info['totalPages']
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
    '4b005e8d-5527-46a9-bbf0-61ce879432b0'
]

fetch_data(uuids, max_pages=5)  # Descarga las primeras 5 páginas
