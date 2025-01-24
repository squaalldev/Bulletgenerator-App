from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_benefits(focus_points, product, target_audience):
    # Base del prompt para generar beneficios persuasivos
    prompt = (
        "Eres un experto en copywriting y tu objetivo es crear bullets persuasivos que destaquen los beneficios del producto, "
        "conecten emocionalmente con la audiencia y respondan a sus problemas, necesidades, deseos o situaciones específicas.\n\n"
        "Ten en cuenta lo siguiente:\n"
        "- Los bullets son pequeños anzuelos diseñados para captar la atención de inmediato, como tráilers de películas que dejan a la audiencia queriendo más.\n"
        "- Ayudan a evitar textos largos y monótonos, destacando tanto beneficios emocionales como prácticos.\n"
        "- Los beneficios deben ser relevantes, concisos y específicos, mostrando cómo el producto puede transformar o mejorar la vida de la audiencia.\n\n"
        "Ahora, crea una lista de beneficios para el siguiente producto y nicho objetivo. Si no se especifican problemas, necesidades, deseos o situaciones, "
        "identifica ejemplos comunes relevantes para el nicho objetivo proporcionado y asocia estos problemas con el producto.\n\n"
        "Producto: {product}\n"
        "Nicho objetivo: {target_audience}\n\n"
        "Ejemplos de problemas, necesidades, deseos o situaciones comunes para este nicho objetivo pueden incluir:\n"
        "- Desafíos comunes en el nicho, como falta de tiempo, dinero, habilidades, etc.\n"
        "- Necesidades específicas del público objetivo que el producto puede solucionar.\n"
        "- Deseos o aspiraciones que este público busca cumplir.\n\n"
        "Por ejemplo:\n"
        "Si el nicho objetivo es 'emprendedores', los problemas pueden ser: 'No saber cómo atraer clientes', 'Falta de tiempo para manejar todos los aspectos del negocio', 'Dificultad para encontrar clientes de calidad'.\n\n"
        "Si el nicho objetivo es 'madres primerizas', los problemas pueden ser: 'Falta de tiempo para balancear la vida personal y profesional', 'Preocupación por la salud del bebé', 'Estrés por la falta de apoyo'.\n\n"
        "Una vez que hayas identificado estos problemas, necesidades o deseos, crea bullets que respondan a ellos con el siguiente formato:\n\n"
        "[Beneficio práctico o emocional que resuena con la audiencia.]\n"
        "[Impacto positivo directo que el producto puede generar en la vida de la audiencia.]\n"
        "[Razón única que hace que el producto sea indispensable para resolver un problema o situación específica.]\n"
        "[Contexto realista donde el producto se convierte en la solución ideal.]\n"
        "Usa un lenguaje persuasivo y directo, destacando cómo el producto resuelve los desafíos de la audiencia de forma única y relevante.\n\n"
    )

    # Generar beneficios con el producto, público objetivo y los problemas/necesidades que se deducen
    benefits = []
    for point in focus_points:
        # Formato del prompt para cada enfoque
        focus_prompt = prompt.format(
            product=product,
            target_audience=target_audience
        )
        
        benefits.append(
            f"Enfoque: {point}.\n{focus_prompt}"
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
