import streamlit as st
import ollama
from typing import Generator
import streamlit as st
import asyncio


#Configuración de la página
st.set_page_config(
    page_title="Bienvenido al comparador de ollama usaremos el asistente de Mysql y Qwen2.5",
    layout="wide",
    initial_sidebar_state="expanded"
    
)

#Generar respuestas
def generate_chat_responses(chat_completation) -> Generator[str, None, None]:
    for chunk in chat_completation:
        if chunk['message']['content']:
            yield chunk['message']['content']

#Limpiamos listas de mensajes
if "message" not in st.session_state:
    st.session_state.messages=[]
    promtsistemas="Bienvenido al asistente IA de mysql, ¿en que puedo ayudarte?"

    st.session_state.messages.append({'role':'system','content':promtsistemas})


#Genera contenedor
with st.container():
    for message in st.session_state.messages:
       with st.chat_message(message['role']):
            st.markdown(message['content'])
modelos = ollama.list()

prompUser=st.chat_input("¿En que puedo ayudarte?")


if prompUser:

    #Mostrar mensajes en el contenedor de mensajes de usuario
    st.chat_message("user").markdown(prompUser)

    #guardar los mensajes de usuario.
    st.session_state.messages.append({'role':'user','content':prompUser})
    
    
async def chat_completation(
        model="deepseek-coder:6.7b", model="gemma2:2b",
        messages=[
            {
                'role':m['role'],
                'content':m['content']
            }
            for m in st.session_state.messages
        ],
        stream=True,
    )

   
    with st.chat_message("assistant"):
        chat_responses_generator = generate_chat_responses(chat_completation)
        full_response = st.write_stream(chat_responses_generator)
        st.session_state.messages.append({'role':'assistant','content':full_response})
