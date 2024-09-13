# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter

# def process_fixed_file(file_path):
#     text = ""
#     pdf = PdfReader(file_path)
#     for page in pdf.pages:
#         text += page.extract_text()
#     return text

  

# def create_text_chunks(text):
#     text_splitter = CharacterTextSplitter(
#         separator='\n',
#         chunk_size=1500,
#         chunk_overlap=300, 
#         length_function=len
#     )
#     chunks = text_splitter.split_text(text)
#     return chunks


import io
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter

def process_fixed_file(uploaded_file):
    """
    Processa o arquivo PDF carregado e extrai o texto.
    """
    text = ""
    # Lê o arquivo PDF diretamente do objeto de arquivo
    pdf = PdfReader(io.BytesIO(uploaded_file.read()))
    for page in pdf.pages:
        text += page.extract_text() or ""  # Garante que o texto não seja None
    return text

def create_text_chunks(text):
    """
    Divide o texto em blocos menores com base na configuração do splitter.
    """
    text_splitter = CharacterTextSplitter(
        separator='\n',
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def main():
    st.title('Processador de Arquivos PDF')

    # Carregar o arquivo PDF através do Streamlit
    uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

    if uploaded_file:
        # Processa o arquivo PDF carregado
        all_files_text = process_fixed_file(uploaded_file)
        st.write("Texto extraído:")
        st.write(all_files_text[:1000])  # Mostra os primeiros 1000 caracteres

        # Criar os chunks de texto
        chunks = create_text_chunks(all_files_text)
        st.write("Chunks de texto:")
        for i, chunk in enumerate(chunks):
            st.write(f"Chunk {i+1}:")
            st.write(chunk)

if __name__ == "__main__":
    main()
