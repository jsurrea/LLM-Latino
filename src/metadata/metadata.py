# Función para extraer los metadatos de los objetos
def extract_metadata(objects):
    data = []
    for obj in objects:
        try:
            indexableObject = obj['_embedded']['indexableObject']
            metadata = indexableObject.get('metadata', {})
            item = {
                'id': indexableObject.get('id', ''),
                'uuid': indexableObject.get('uuid', ''),
                'name': indexableObject.get('name', ''),
                'handle': indexableObject.get('handle', ''),
                'lastModified': indexableObject.get('lastModified', ''),
                'entityType': indexableObject.get('entityType', ''),
                'authorProfile.id.code': [entry.get('value', None) for entry in metadata.get('authorProfile.id.code', [])],
                'dc.contributor.advisor': [entry.get('value', None) for entry in metadata.get('dc.contributor.advisor', [])],
                'dc.contributor.author': [entry.get('value', None) for entry in metadata.get('dc.contributor.author', [])],
                'dc.contributor.other': [entry.get('value', None) for entry in metadata.get('dc.contributor.other', [])],
                'dc.contributor.researchgroup': [entry.get('value', None) for entry in metadata.get('dc.contributor.researchgroup', [])],
                'dc.date.accessioned': [entry.get('value', None) for entry in metadata.get('dc.date.accessioned', [])],
                'dc.date.available': [entry.get('value', None) for entry in metadata.get('dc.date.available', [])],
                'dc.date.issued': [entry.get('value', None) for entry in metadata.get('dc.date.issued', [])],
                'dc.description': [entry.get('value', None) for entry in metadata.get('dc.description', [])],
                'dc.description.abstract': [entry.get('value', None) for entry in metadata.get('dc.description.abstract', [])],
                'dc.description.degreelevel': [entry.get('value', None) for entry in metadata.get('dc.description.degreelevel', [])],
                'dc.description.degreename': [entry.get('value', None) for entry in metadata.get('dc.description.degreename', [])],
                'dc.description.researcharea': [entry.get('value', None) for entry in metadata.get('dc.description.researcharea', [])],
                'dc.format.extent': [entry.get('value', None) for entry in metadata.get('dc.format.extent', [])],
                'dc.format.mimetype': [entry.get('value', None) for entry in metadata.get('dc.format.mimetype', [])],
                'dc.identifier.instname': [entry.get('value', None) for entry in metadata.get('dc.identifier.instname', [])],
                'dc.identifier.reponame': [entry.get('value', None) for entry in metadata.get('dc.identifier.reponame', [])],
                'dc.identifier.repourl': [entry.get('value', None) for entry in metadata.get('dc.identifier.repourl', [])],
                'dc.identifier.uri': [entry.get('value', None) for entry in metadata.get('dc.identifier.uri', [])],
                'dc.language.iso': [entry.get('value', None) for entry in metadata.get('dc.language.iso', [])],
                'dc.publisher': [entry.get('value', None) for entry in metadata.get('dc.publisher', [])],
                'dc.publisher.department': [entry.get('value', None) for entry in metadata.get('dc.publisher.department', [])],
                'dc.publisher.faculty': [entry.get('value', None) for entry in metadata.get('dc.publisher.faculty', [])],
                'dc.publisher.program': [entry.get('value', None) for entry in metadata.get('dc.publisher.program', [])],
                'dc.rights.accessrights': [entry.get('value', None) for entry in metadata.get('dc.rights.accessrights', [])],
                'dc.rights.coar': [entry.get('value', None) for entry in metadata.get('dc.rights.coar', [])],
                'dc.rights.license': [entry.get('value', None) for entry in metadata.get('dc.rights.license', [])],
                'dc.rights.uri': [entry.get('value', None) for entry in metadata.get('dc.rights.uri', [])],
                'dc.subject.keyword': [entry.get('value', None) for entry in metadata.get('dc.subject.keyword', [])],
                'dc.subject.themes': [entry.get('value', None) for entry in metadata.get('dc.subject.themes', [])],
                'dc.title': [entry.get('value', None) for entry in metadata.get('dc.title', [])],
                'dc.type': [entry.get('value', None) for entry in metadata.get('dc.type', [])],
                'dc.type.coar': [entry.get('value', None) for entry in metadata.get('dc.type.coar', [])],
                'dc.type.coarversion': [entry.get('value', None) for entry in metadata.get('dc.type.coarversion', [])],
                'dc.type.content': [entry.get('value', None) for entry in metadata.get('dc.type.content', [])],
                'dc.type.driver': [entry.get('value', None) for entry in metadata.get('dc.type.driver', [])],
                'dc.type.redcol': [entry.get('value', None) for entry in metadata.get('dc.type.redcol', [])],
                'dc.type.version': [entry.get('value', None) for entry in metadata.get('dc.type.version', [])],
                'dspace.entity.type': [entry.get('value', None) for entry in metadata.get('dspace.entity.type', [])],
            }
            data.append(item)
        except Exception as e:
            print(f"Error extracting metadata for object {obj}: {e}")
    return data