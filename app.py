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
st.title("Presupuesto Inteligente AI")

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
user_income = st.number_input("Ingresa tus ingresos mensuales:", min_value=0.0, step=0.01)
user_expenses = st.number_input("Ingresa tus gastos mensuales:", min_value=0.0, step=0.01)
financial_goals = st.text_input("Describe tus metas financieras:")

# Botón para enviar el prompt
if st.button("Enviar"):
    if user_income and user_expenses and financial_goals:
        try:
            # Crear la instancia del modelo usando el nombre correcto
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')  # Asegúrate de usar el nombre correcto del modelo

            # Crear un contexto detallado para el prompt
            full_prompt = (
                f"Tengo un ingreso mensual de {user_income} y mis gastos mensuales son {user_expenses}. "
                f"Mis metas financieras incluyen: {financial_goals}. "
                "¿Puedes proporcionarme consejos específicos para gestionar mis finanzas y alcanzar mis metas?"
                "Por favor, proporciona consejos específicos y detallados para gestionar mis finanzas, mejorar mis estrategias de ahorro e inversión, y superar mis desafíos financieros. Evita información inventada y enfócate en soluciones prácticas y realistas."
            )

            # Generar texto a partir del prompt
            response = model.generate_content(full_prompt)  # Generar texto

            # Mostrar el texto generado en formato Markdown
            st.markdown(to_markdown(response.text))

            # Guardar el texto generado en un archivo JSON
            # save_to_json({"context": context, "response": response.text})
            # st.success("Respuesta guardada en 'generated_responses.json'.")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("Por favor, ingresa toda tu información financiera.")
