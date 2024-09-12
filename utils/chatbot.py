import streamlit as st
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Carregar a chave da API dos secrets do sistema ou da variável de ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")

# Verifica se a chave da API foi carregada corretamente
if not openai_api_key:
    st.error("A chave da API da OpenAI não foi encontrada. Verifique a variável de ambiente OPENAI_API_KEY.")

def create_vectorstore(chunks):
    # Verifica se a chave da API foi carregada corretamente
    if not openai_api_key:
        raise ValueError("A chave da API da OpenAI não foi encontrada. Verifique a variável de ambiente.")
    
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vectorstore

def create_conversation_chain(vectorstore):
    llm = ChatOpenAI(api_key=openai_api_key)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain
