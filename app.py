import streamlit as st
from utils import chatbot, text
from streamlit_chat import message

def add_custom_css():
    st.markdown("""
    <style>
    /* Fundo branco da página */
    .main {
        background-color: #ffffff;
        color: #000000;
    }

    /* Estilo do cabeçalho */
    h1, h2, h3, h4, h5, h6 {
        color: #000000;
    }

    /* Estilo do texto */
    p, div, span {
        color: #333333;
    }

    /* Estilo da caixa de input de texto */
    .stTextInput>div>div>input {
        background-color: #f0f0f0;
        color: #000000;
        border: 1px solid #cccccc;
    }

    /* Estilo dos botões */
    .stButton>button {
        background-color: #cccccc;
        color: #000000;
        border-radius: 5px;
    }

    /* Mensagens do usuário */
    .stMessageUser {
        background-color: #e1e1e1 !important;
        color: #000000 !important;
    }

    /* Mensagens do bot com fundo branco */
    .stMessageBot {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }

    /* Sidebar clara */
    section[data-testid="stSidebar"] {
        background-color: #f9f9f9;
    }

    /* Texto na sidebar */
    .stSidebar {
        color: #000000;
    }

    /* Customizar botões e inputs na sidebar */
    .stSidebar > div > div > input {
        background-color: #f0f0f0;
        color: #000000;
        border: 1px solid #cccccc;
    }

    /* Ajustar o layout do formulário de input */
    .stTextInput > div {
        flex-direction: row-reverse;
    }

    /* Estilo das mensagens do usuário e do bot */
    .stMessageUser, .stMessageBot {
        padding: 10px;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(page_title='Pergunte para nós', page_icon=':books:', layout='centered')

    # Adicionar o CSS customizado
    add_custom_css()

    col1, col2, col3 = st.columns([1, 2, 1])  
    with col2:
        st.image('img/logo.png', width=300)

    st.header('Sou o Portuga, Assistente da Oficina Virtual Porto. Em que posso te ajudar?')

    if 'history' not in st.session_state:
        st.session_state.history = []

    # Mostrar o histórico de perguntas e respostas no chat
    for entry in st.session_state.history:
        message(entry['question'], is_user=True, key=str(entry['question']) + '_user', avatar_style="initials", seed="U")
        message(entry['answer'], is_user=False, key=str(entry['answer']) + '_bot', avatar_style="bottts", seed="B")

    # Carregar e processar o PDF fixo ao iniciar o app
    if 'conversation' not in st.session_state:

        pdf_path = r'C:\\Users\\user\Desktop\\ChatPorto\\PDF_AUTODIAG.pdf'
        all_files_text = text.process_fixed_file(pdf_path)
        chunks = text.create_text_chunks(all_files_text)
        vectorstore = chatbot.create_vectorstore(chunks)

        st.session_state.conversation = chatbot.create_conversation_chain(vectorstore)
        st.session_state.history.clear()

    # Input e botão de envio da pergunta
    with st.form(key='input_form', clear_on_submit=True):
        user_question = st.text_input('Faça uma pergunta para mim', key='user_input', label_visibility="collapsed")
        submit_button = st.form_submit_button('Enviar')

        if submit_button and user_question:
            if 'conversation' in st.session_state:
                response = st.session_state.conversation(user_question)
                answer = response['answer']
            else:
                answer = "Por favor, carregue e processe os arquivos primeiro."
            
            # Adicionar ao histórico de conversas
            st.session_state.history.append({'question': user_question, 'answer': answer})
            message(user_question, is_user=True, key=user_question + '_user', avatar_style="initials", seed="U")
            message(answer, is_user=False, key=answer + '_bot', avatar_style="bottts", seed="B")

if __name__ == '__main__':
    main()
