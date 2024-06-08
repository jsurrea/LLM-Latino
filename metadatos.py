import requests
import pandas as pd
from tqdm import tqdm

# Función para obtener el JSON desde un endpoint
def get_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

# Función para extraer los metadatos de los objetos
def extract_metadata(objects):
    data = []
    for obj in objects:
        indexableObject = obj['_embedded']['indexableObject']
        metadata = indexableObject.get('metadata', {})
        item = {
            'id': indexableObject.get('id', ''),
            'uuid': indexableObject.get('uuid', ''),
            'name': indexableObject.get('name', ''),
            'handle': indexableObject.get('handle', ''),
            'lastModified': indexableObject.get('lastModified', ''),
            'entityType': indexableObject.get('entityType', ''),
            'authorProfile.id.code': [entry['value'] for entry in metadata.get('authorProfile.id.code', [])],
            'dc.contributor.advisor': [entry['value'] for entry in metadata.get('dc.contributor.advisor', [])],
            'dc.contributor.author': [entry['value'] for entry in metadata.get('dc.contributor.author', [])],
            'dc.contributor.other': [entry['value'] for entry in metadata.get('dc.contributor.other', [])],
            'dc.contributor.researchgroup': [entry['value'] for entry in metadata.get('dc.contributor.researchgroup', [])],
            'dc.date.accessioned': [entry['value'] for entry in metadata.get('dc.date.accessioned', [])],
            'dc.date.available': [entry['value'] for entry in metadata.get('dc.date.available', [])],
            'dc.date.issued': [entry['value'] for entry in metadata.get('dc.date.issued', [])],
            'dc.description': [entry['value'] for entry in metadata.get('dc.description', [])],
            'dc.description.abstract': [entry['value'] for entry in metadata.get('dc.description.abstract', [])],
            'dc.description.degreelevel': [entry['value'] for entry in metadata.get('dc.description.degreelevel', [])],
            'dc.description.degreename': [entry['value'] for entry in metadata.get('dc.description.degreename', [])],
            'dc.description.researcharea': [entry['value'] for entry in metadata.get('dc.description.researcharea', [])],
            'dc.format.extent': [entry['value'] for entry in metadata.get('dc.format.extent', [])],
            'dc.format.mimetype': [entry['value'] for entry in metadata.get('dc.format.mimetype', [])],
            'dc.identifier.instname': [entry['value'] for entry in metadata.get('dc.identifier.instname', [])],
            'dc.identifier.reponame': [entry['value'] for entry in metadata.get('dc.identifier.reponame', [])],
            'dc.identifier.repourl': [entry['value'] for entry in metadata.get('dc.identifier.repourl', [])],
            'dc.identifier.uri': [entry['value'] for entry in metadata.get('dc.identifier.uri', [])],
            'dc.language.iso': [entry['value'] for entry in metadata.get('dc.language.iso', [])],
            'dc.publisher': [entry['value'] for entry in metadata.get('dc.publisher', [])],
            'dc.publisher.department': [entry['value'] for entry in metadata.get('dc.publisher.department', [])],
            'dc.publisher.faculty': [entry['value'] for entry in metadata.get('dc.publisher.faculty', [])],
            'dc.publisher.program': [entry['value'] for entry in metadata.get('dc.publisher.program', [])],
            'dc.rights.accessrights': [entry['value'] for entry in metadata.get('dc.rights.accessrights', [])],
            'dc.rights.coar': [entry['value'] for entry in metadata.get('dc.rights.coar', [])],
            'dc.rights.license': [entry['value'] for entry in metadata.get('dc.rights.license', [])],
            'dc.rights.uri': [entry['value'] for entry in metadata.get('dc.rights.uri', [])],
            'dc.subject.keyword': [entry['value'] for entry in metadata.get('dc.subject.keyword', [])],
            'dc.subject.themes': [entry['value'] for entry in metadata.get('dc.subject.themes', [])],
            'dc.title': [entry['value'] for entry in metadata.get('dc.title', [])],
            'dc.type': [entry['value'] for entry in metadata.get('dc.type', [])],
            'dc.type.coar': [entry['value'] for entry in metadata.get('dc.type.coar', [])],
            'dc.type.coarversion': [entry['value'] for entry in metadata.get('dc.type.coarversion', [])],
            'dc.type.content': [entry['value'] for entry in metadata.get('dc.type.content', [])],
            'dc.type.driver': [entry['value'] for entry in metadata.get('dc.type.driver', [])],
            'dc.type.redcol': [entry['value'] for entry in metadata.get('dc.type.redcol', [])],
            'dc.type.version': [entry['value'] for entry in metadata.get('dc.type.version', [])],
            'dspace.entity.type': [entry['value'] for entry in metadata.get('dspace.entity.type', [])],
        }
        data.append(item)
    return data

# Lista de UUIDs para los items a descargar
uuids = [
    '4b005e8d-5527-46a9-bbf0-61ce879432b0',
    'a11f8b49-0ec6-4769-98df-ab072cd528c2',
]

# Base URL para la API
base_url = "https://repositorio.uniandes.edu.co/server/api/discover/search/objects?scope={uuid}&configuration=default&page={page}&size=10"

# DataFrame para almacenar todos los datos
all_data = []

# Proceso de extracción de datos
for uuid in uuids:
    page = 0
    while True:
        url = base_url.format(uuid=uuid, page=page)
        print(f"Fetching data from: {url}")
        json_data = get_json(url)
        
        search_result = json_data['_embedded']['searchResult']
        objects = search_result['_embedded']['objects']
        
        # Extraer los metadatos
        data = extract_metadata(objects)
        all_data.extend(data)
        
        # Verificar si hay más páginas
        page_info = search_result['page']
        if page >= page_info['totalPages'] - 1:
            break
        page += 1

# Crear un DataFrame y exportarlo a CSV
df = pd.DataFrame(all_data)
df.to_csv('repositorio_uniandes_data.csv', index=False)
print("Datos exportados a repositorio_uniandes_data.csv")
