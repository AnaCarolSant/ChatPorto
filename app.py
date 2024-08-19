
import streamlit as st
from utils import chatbot, text
from streamlit_chat import message

def main():
    
    st.set_page_config(page_title='Pergunte para nós', page_icon=':books:')

    col1, col2, col3 = st.columns([1, 2, 1])  
    # As colunas são proporcionais
    with col2:
        # Adicionar a logo da Porto Seguro
        st.image('img/logo.png', width=300)

    # st.image('img/logo.png', width=300)

    st.header('Converse com seus arquivos')
    
    # Inicializar o histórico de conversas se não existir
    if 'history' not in st.session_state:
        st.session_state.history = []

    user_question = st.text_input('Faça uma pergunta para mim')

    # Mostrar o histórico de perguntas e respostas
    for entry in st.session_state.history:
        message(entry['question'], is_user=True)
        message(entry['answer'], is_user=False)

    if user_question:
        # Processar a pergunta e obter a resposta
        if 'conversation' in st.session_state:
            response = st.session_state.conversation(user_question)
            answer = response['answer']
        else:
            answer = "Por favor, carregue e processe os arquivos primeiro."
        
        # Adicionar a pergunta e resposta ao histórico
        st.session_state.history.append({'question': user_question, 'answer': answer})

        # Mostrar a pergunta e resposta atual
        message(user_question, is_user=True)
        message(answer, is_user=False)

    with st.sidebar:
        st.subheader('Seus arquivos')
        pdf_docs = st.file_uploader('Carregue os seus arquivos em formato pdf', accept_multiple_files=True)

        if st.button('Processar'):
            if pdf_docs:
                all_files_text = text.process_files(pdf_docs)
                chunks = text.create_text_chunks(all_files_text)
                vectorstore = chatbot.create_vectorstore(chunks)
                
                st.session_state.conversation = chatbot.create_conversation_chain(vectorstore)
                st.session_state.history.clear()  # Limpar o histórico ao processar novos arquivos
            else:
                st.error("Por favor, carregue pelo menos um arquivo PDF.")

if __name__ == '__main__':
    main()
