from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función para obtener una mención del producto de manera probabilística
def get_random_product_mention():
    mentions = ["Directa", "Indirecta", "Metafórica"]
    probabilities = [0.34, 0.33, 0.33]  
    return random.choices(mentions, probabilities)[0]

# Crear la instrucción de mención basada en la opción seleccionada
def get_mention_instruction(product_mention, product):
    if product_mention == "Directa":
        return f"Introduce directamente el producto '{product}' como la solución clara al problema que enfrenta el lector."
    elif product_mention == "Indirecta":
        return f"Referencia sutilmente el producto '{product}' como una posible solución al problema del lector sin nombrarlo explícitamente."
    elif product_mention == "Metafórica":
        return f"Introduce el producto '{product}' usando una metáfora, conectándolo simbólicamente a la solución que necesita el lector."
    return ""

# Función para generar titulares
def generate_headlines(number_of_headlines, target_audience, product, temperature):
    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)

    # Crear la configuración del modelo
    generation_config = {
        "temperature": temperature,  # Usar el valor del slider aquí
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Eres un copywriter de clase mundial, con experiencia en la creación de ganchos, titulares y líneas de asunto que capturan la atención de inmediato. Tu habilidad radica en comprender profundamente las emociones, deseos y desafíos de una audiencia específica."
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Tu tarea es crear {number_of_headlines} ganchos o encabezados titulares llamativos diseñados para {target_audience} con el fin de generar interés en {product}. "
                    f"Usa la siguiente mención: {mention_instruction}. "
                    "Los ganchos deben ser de este tipo: "
                    "1. Secretos: 'El secreto detrás de...'; "
                    "2. Consejos: 'Consejos para que...'; "
                    "3. Historias: 'La historia del...', 'Los misterios de...', 'La leyenda de...'; "
                    "4. Deseos: 'Cómo...'; "
                    "5. Listas: '10 razones por las que...'; "
                    "6. Haciendo una pregunta: '¿Sabías que...'; "
                    "7. Curiosidad: '¿Por qué...'."
                ],
            },
        ]
    )

    response = chat_session.send_message("Genera los titulares")  # Enviar mensaje para obtener la respuesta
    return response.text  # Regresar la respuesta directamente

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="Generador de Titulares", layout="wide")

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Generador de Titulares</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Usa el poder de Gemini AI para crear titulares atractivos.</h4>", unsafe_allow_html=True)

# Añadir CSS personalizado para el botón
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #FFCC00;
        color: black;
        width: 90%;
        height: 60px;
        font-weight: bold;
        font-size: 22px;
        text-transform: uppercase;
        border: 1px solid #000000;
        border-radius: 8px;
        display: block;
        margin: 0 auto;
    }
    div.stButton > button:hover {
        background-color: #FFD700;
        color: black;
    }
    </style>
""", unsafe_allow_html=True)

# Crear columnas
col1, col2 = st.columns([1, 2])  # 1: tamaño de la columna izquierda, 2: tamaño de la columna derecha

# Columnas de entrada
with col1:
    target_audience = st.text_input("¿Quién es tu público objetivo?", placeholder="Ejemplo: Estudiantes Universitarios")
    product = st.text_input("¿Qué producto tienes en mente?", placeholder="Ejemplo: Curso de Inglés")
    number_of_headlines = st.selectbox("Número de Titulares", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=4)
    temperature = st.slider("Creatividad", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    
    # Botón de enviar
    if st.button("Generar Titulares"):
        if target_audience and product:
            # Obtener la respuesta del modelo
            generated_headlines = generate_headlines(number_of_headlines, target_audience, product, temperature)
            # Mostrar los bullets generados
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Aquí están tus titulares:</h4>
                    <p>{generated_headlines}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            col2.error("Por favor, proporciona el público objetivo y el producto.")

