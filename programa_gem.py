import streamlit as st
import ollama
from typing import Generator

#Configuración de la página
st.set_page_config(
    page_title="Bienvenido al comparador de ollama usaremos el asistente de Mysql y Qwen2.5",
    layout="wide",
    initial_sidebar_state="expanded"
    
)

#obtenemos los modelosS
#modelos = ollama.list()['models']


#funcion para mostrar modelos

#@st.dialog("información de modelos", width="large")
#def mostrarinfomodelos(modelo):
    #listamodelos = [x['name'] for x in modelos if x['name']==modelo]
    #st.write(modelos)

#Recorrer modelos
#def generarlistasmodelos():
    #listamodelos = [x['name'] for x in modelos]
    #return listamodelos

def generate_chat_responses(chat_completation) -> Generator[str, None, None]:
    for chunk in chat_completation:
        if chunk['message']['content']:
            yield chunk['message']['content']

#Limpiamos listas de mensajes
if "message" not in st.session_state:
    st.session_state.messages=[]

    #Definimos como se comporta el sistema o podemos usar un mensaje de bienvenida hay que descomentar st.session_state.messages.append
    promtsistemas="Eres un asistente experto en programación power BI, solo hablarás Español"
    st.session_state.messages.append({'role':'system','content':promtsistemas})
    
    

#mostrar caja de información 
#with st.sidebar:
    #param_Modelo=st.selectbox("Modelos Disponible: ",options = generarlistasmodelos())
    #verinfomodelos = st.button("Ver información")
    #if verinfomodelos:
        #mostrarinfomodelos(param_Modelo)


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
    
    
    chat_completation = ollama.chat(
        model="gemma2:2b",
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
