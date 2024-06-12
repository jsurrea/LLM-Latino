from src.files.files import get_bitstream_info, download_file

# UUID de los items a descargar
uuid = "8fa3afff-90d0-49d1-b13a-ea4c358f01c6"

# Obtener la URL del bitstream y el nombre del archivo
bitstream_url, file_name = get_bitstream_info(uuid)

# Descargar el archivo
download_file(bitstream_url, file_name)