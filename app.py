from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Nueva función para generar beneficios basados en enfoques seleccionados por el usuario
def generate_benefits(focus_points, product, target_audience):
    # Prompt basado en las descripciones de los bullets
    prompt = (
        "Qué son los bullets: "
        "Son pequeños anzuelos que capturan la atención sin que parezca que estás esforzándote en ello. "
        "Hacen que hasta los más distraídos digan: \"Oye, esto suena interesante\". "
        "Son como los tráilers de una película, pero en lugar de vender entradas, venden tus ideas. "
        "Son tan parecidos a la lista del súper, que cuando los leen gastan dinero como si estuvieras comprando en el supermercado. "
        "Considéralos como pequeños headlines, así que las formulas de estos funcionan para crearlos. "
        "Ayudan a que tus textos no se vean como parrafadas, porque a nadie le gusta leer eso. "
        "Un bullet bien escrito destaca en el texto. "
        "Van enfocados en el beneficio emocional o práctico del producto."
    )

    # Generar beneficios con el producto y la audiencia como referencia
    benefits = []
    for point in focus_points:
        benefits.append(
            f"{prompt} Enfócate en: {point}. Producto: {product}. Público objetivo: {target_audience}."
        )
    return benefits

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="Quick Prompt", layout="wide")

# Leer el contenido del archivo manual.md
with open("manual.md", "r", encoding="utf-8") as file:
    manual_content = file.read()

# Mostrar el contenido del manual en el sidebar
st.sidebar.markdown(manual_content)

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Impact Bullet Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma los pensamientos de tu audiencia en beneficios persuasivos que inspiren a la acción.</h4>", unsafe_allow_html=True)

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
col1, col2 = st.columns([1, 2])  

# Columnas de entrada
with col1:
    with st.expander("Enfoques para los beneficios"):
        st.markdown("""
        1. **Curiosidad**
        - Su función es dejar al lector enganchado, queriendo saber más.
        2. **CASI Imposible**
        - Afirmaciones que parecen difíciles de creer, pero no son completamente irreales.
        3. **Autoridad y Credibilidad**
        - Establece confianza mediante hechos respaldados.
        4. **Contraste**
        - Confronta ideas para captar la atención.
        """)

    focus_points = st.multiselect(
        "Selecciona los enfoques que deseas utilizar:",
        ["Curiosidad", "CASI Imposible", "Autoridad y Credibilidad", "Contraste"],
        default=[]
    )
    product = st.text_input("Producto relacionado:", placeholder="Ejemplo: Curso de productividad")
    target_audience = st.text_input("Público objetivo:", placeholder="Ejemplo: Estudiantes universitarios")
    submit = st.button("Generar Beneficios")

# Mostrar los beneficios generados
if submit:
    if focus_points and product and target_audience:
        benefits = generate_benefits(focus_points, product, target_audience)
        formatted_benefits = '<br style="line-height: 2;">'.join(benefits)
        
        col2.markdown(f"""
            <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                <h4>Mira los beneficios generados:</h4>
                <p style="line-height: 2;">{formatted_benefits}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        col2.error("Por favor, proporciona al menos un enfoque, un producto y un público objetivo para generar beneficios.")
