import streamlit as st
import textwrap
import google.generativeai as genai
import json

# Configuración de la API usando secretos
genai.configure(api_key=st.secrets["general"]["api_key"])  # Lee la clave API desde los secretos

def to_markdown(text):
    text = text.replace('•', '  *')  # Reemplaza los puntos con asteriscos
    return textwrap.indent(text, '> ')  # Indenta el texto

def save_to_json(data, filename='generated_responses.json'):
    # Guardar la respuesta generada en un archivo JSON
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# Título de la aplicación
st.title("Generador de Texto con Google Generative AI")

# Mensaje de bienvenida
welcome_message = (
    "Hola, soy Presupuesto Inteligente AI, tu asistente personal de finanzas. "
    "Estoy aquí para ayudarte a gestionar tu dinero de manera eficiente. "
    "Para comenzar, cuéntame sobre tus ingresos, gastos mensuales y cualquier meta financiera que tengas. "
    "Juntos, podemos crear un plan para alcanzar tus objetivos."
)

# Mostrar el mensaje de bienvenida
st.markdown(to_markdown(welcome_message))

# Ingreso del prompt
prompt = st.text_input("Escribe tu información financiera:")

# Botón para enviar el prompt
if st.button("Enviar"):
    if prompt:
        try:
            # Crear la instancia del modelo usando el nombre correcto
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')  # Asegúrate de usar el nombre correcto del modelo
            
            # Generar texto a partir del prompt
            response = model.generate_content(prompt)  # Generar texto
            
            # Mostrar el texto generado en formato Markdown
            st.markdown(to_markdown(response.text))
            
            # Guardar el texto generado en un archivo JSON
            save_to_json({"prompt": prompt, "response": response.text})
            st.success("Respuesta guardada en 'generated_responses.json'.")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Por favor, ingresa tu información financiera.")