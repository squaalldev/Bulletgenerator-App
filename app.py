from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de GenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función para obtener una mención del producto de manera probabilística
def get_random_product_mention():
    mentions = ["Indirecta", "Metafórica"]
    probabilities = [0.50, 0.50]
    return random.choices(mentions, probabilities)[0]

# Crear la instrucción de mención basada en la opción seleccionada
def get_mention_instruction(product_mention, product):
    if product_mention == "Indirecta":
        return f"Referencia sutilmente el producto '{product}' como una posible solución al problema del lector sin nombrarlo explícitamente."
    elif product_mention == "Metafórica":
        return f"Introduce el producto '{product}' usando una metáfora, conectándolo simbólicamente a la solución que necesita el lector."
    return ""

# Función para generar los beneficios (bullets) basados en el enfoque
def generate_benefits(focus_points, product, target_audience, creativity, num_bullets):
    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)

    # Instrucción del sistema para el modelo
    system_instruction = (
        "You are a world-class copywriter with expertise in crafting emotional and persuasive benefits that connect with the target audience. "
        "Generate highly creative and engaging benefits that resonate with the audience's desires and challenges."
    )

    # Base del prompt
    prompt_base = f"""
Eres un experto en copywriting y tu objetivo es crear {{num_bullets}} bullets persuasivos que conecten emocionalmente con la audiencia {{target_audience}}.
Cada bullet debe abordar sus problemas, deseos o situaciones, mostrando cómo se pueden mejorar o solucionar gracias a una solución específica.
La idea es resaltar el valor que aporta la solución, sin que suene como una venta forzada.
Además, menciona el producto utilizando el siguiente enfoque: {{mention_instruction}}.
Usa enfoques creativos para conectar los beneficios del producto con lo que realmente le importa a la audiencia.
Crea {{num_bullets}} bullets persuasivos que muestren cómo el producto puede transformar la situación de la audiencia.
"""

    benefits = []
    for point in focus_points[:num_bullets]:
        specific_prompt = prompt_base.format(
            num_bullets=num_bullets,
            target_audience=target_audience,
            mention_instruction=mention_instruction
        ) + f"\n\nEnfoque: {point}\n"

        # Configuración del modelo y generación de contenido
        response = genai.generate_text(
            model="gemini-1.5-flash",
            prompt=specific_prompt,
            temperature=creativity,
            top_p=0.65,
            top_k=280,
            max_output_tokens=2048,
        )

        if response and response.generations:
            bullet = response.generations[0].text.strip()
            benefits.append(bullet)
        else:
            benefits.append("No se pudo generar un beneficio para este enfoque.")

    return benefits

# Configuración de Streamlit
st.set_page_config(page_title="Impact Bullet Generator", layout="wide")

# Leer el contenido del archivo manual.md
with open("manual.md", "r", encoding="utf-8") as file:
    manual_content = file.read()

# Mostrar el contenido del manual en el sidebar
st.sidebar.markdown(manual_content)

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Impact Bullet Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma los pensamientos de tu audiencia en beneficios persuasivos que inspiren a la acción.</h4>", unsafe_allow_html=True)

# Crear columnas
col1, col2 = st.columns([1, 2])

# Columnas de entrada
with col1:
    target_audience = st.text_input("Público objetivo:", placeholder="Ejemplo: Estudiantes universitarios")
    product = st.text_input("Producto relacionado:", placeholder="Ejemplo: Curso de productividad")
    
    # Slider para la creatividad
    creativity = st.slider("Creatividad (Temperatura)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    # Slider para el número de bullets
    num_bullets = st.slider("Número de Bullets", min_value=1, max_value=10, value=5, step=1)
    
    focus_points = st.multiselect(
        "Selecciona los enfoques que deseas utilizar:",
        ["Curiosidad", "CASI Imposible", "Autoridad y Credibilidad", "Contraste"],
        default=[]
    )

    submit = st.button("Generar Beneficios")

# Mostrar los beneficios generados
with col2:
    if submit:
        if focus_points and product and target_audience:
            benefits = generate_benefits(focus_points, product, target_audience, creativity, num_bullets)
            formatted_benefits = '<br style="line-height: 2;">'.join(benefits)
            
            st.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Mira los beneficios generados:</h4>
                    <p style="line-height: 2;">{formatted_benefits}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Por favor, proporciona al menos un enfoque, un producto y un público objetivo para generar beneficios.")
