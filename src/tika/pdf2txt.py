# !pip install tika
from tika import parser

def pdf2txt(filepath):
    """
    Extract text from a PDF file and save it as a text file.
    Args:
        filepath (str): The path to the PDF file.
    """    
    parsed_document = parser.from_file(filepath)
    with open(filepath+".txt", 'w', encoding='utf-8') as file:
        file.write(parsed_document['content'])

