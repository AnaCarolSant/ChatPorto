from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

def process_fixed_file(file_path):
    text = ""
    pdf = PdfReader(file_path)
    for page in pdf.pages:
        text += page.extract_text()
    return text

def create_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1500,
        chunk_overlap=300, 
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
