from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función para obtener una mención del producto de manera probabilística
def get_random_product_mention():
    mentions = ["Directa", "Indirecta", "Metafórica"]
    probabilities = [0.34, 0.33, 0.33]  
    return random.choices(mentions, probabilities)[0]

# Función para obtener una cantidad de bullets
def get_gemini_response_bullets(target_audience, product, num_bullets, creativity):
    product_mention = get_random_product_mention()
    model_choice = "gemini-1.5-flash"  

    model = genai.GenerativeModel(model_choice)

    # Crear el prompt para generar bullets
    full_prompt = f"""
    You are a marketing expert specializing in writing persuasive and impactful benefit bullets for {target_audience}. Write {num_bullets} creative and engaging bullets that highlight the key benefits of {product}. Each bullet should emotionally resonate with the audience, creating a strong connection between the product's features and the problems it solves. The tone should be {creativity}, ensuring each benefit clearly addresses their needs and desires. Use {product_mention} mention.
    """

    response = model.generate_content([full_prompt])

    if response and response.parts:
        return response.parts[0].text
    else:
        raise ValueError("Lo sentimos, intenta con una combinación diferente de entradas.")

# Inicializar la aplicación Streamlit
st.set_page_config(page_title="Generador de Bullets", layout="wide")

# Inicializar el estado de la expansión del acordeón
if "accordion_expanded" not in st.session_state:
    st.session_state["accordion_expanded"] = False

def toggle_accordion():
    st.session_state["accordion_expanded"] = not st.session_state["accordion_expanded"]

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Generador de Bullets</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Crea bullets efectivos que conecten emocionalmente con tu audiencia.</h4>", unsafe_allow_html=True)

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

# Crear dos columnas para el layout (40% y 60%)
col1, col2 = st.columns([2, 3])

with col1:
    # Campos de entrada
    target_audience = st.text_input("¿Quién es tu público objetivo?")
    product = st.text_input("¿Qué producto tienes en mente?")

    # Acordeón para personalizar los bullets
    with st.expander("Personaliza tus bullets", expanded=st.session_state["accordion_expanded"]):
        num_bullets = st.slider("Número de Bullets", min_value=1, max_value=15, value=5)
        creativity = st.selectbox("Creatividad", ["Alta", "Media", "Baja"])

    # Botón de enviar
    submit = st.button("Generar Bullets", on_click=toggle_accordion)

# Mostrar los bullets generados
if submit:
    if target_audience and product:
        try:
            # Obtener la respuesta del modelo
            generated_bullets = get_gemini_response_bullets(target_audience, product, num_bullets, creativity)
            col2.markdown("""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Aquí están tus bullets:</h4>
                    <p>{}</p>
                </div>
            """.format(generated_bullets), unsafe_allow_html=True)
        except ValueError as e:
            col2.error(f"Error: {str(e)}")
    else:
        col2.error("Por favor, proporciona el público objetivo y el producto.")
