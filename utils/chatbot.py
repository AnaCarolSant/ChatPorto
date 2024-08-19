from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain  # Atualizado
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

def create_vectorstore(chunks):
    if not openai_api_key:
        raise ValueError("A chave da API da OpenAI não foi encontrada. Verifique o arquivo .env.")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

def create_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain
