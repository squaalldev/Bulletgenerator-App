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
    probabilities = [0.20, 0.30, 0.50]  # Mayor probabilidad para Metafórica
    return random.choices(mentions, probabilities)[0]

# Crear la instrucción de mención basada en la opción seleccionada
def get_mention_instruction(product_mention, product):
    if product_mention == "Directa":
        return f"""
        Presenta el producto '{product}' como la solución clara al problema que enfrenta el lector. Destaca sus beneficios clave y demuestra cómo aborda directamente el problema. La mención debe sentirse natural e integrada en la narrativa.
        """
    elif product_mention == "Indirecta":
        return f"""
        Haz referencia al producto '{product}' como una posible solución al problema del lector sin nombrarlo explícitamente. Integra los beneficios del producto en la descripción de cómo el lector puede superar el problema, creando una conexión implícita entre la solución y el producto.
        """
    elif product_mention == "Metafórica":
        return f"""
        Introduce el producto '{product}' utilizando una metáfora, conectándolo simbólicamente a la solución que necesita el lector. La metáfora debe relacionarse con el problema discutido y sugerir creativamente cómo el producto ofrece una resolución sin mencionarlo explícitamente.
        """
    return ""

# Función para obtener una cantidad de bullets orientados a la acción
def get_action_oriented_bullets(product):
    return [
        f"¿Sabías que el {product} puede transformar tu rutina diaria? Descúbrelo ahora.",
        f"No dejes pasar la oportunidad: el {product} está diseñado para facilitarte la vida.",
        f"Imagina lo que podrías lograr con el {product} en tu arsenal. ¡Actúa y pruébalo hoy!"
    ]

# System Prompt - Instrucción en inglés para el modelo
system_instruction = """
You are a world-class copywriter, expert in creating benefits that connect symptoms with problems. You deeply understand the emotions, desires, and challenges of a specific audience, allowing you to design personalized marketing strategies that resonate and motivate action. You know how to use proven structures to attract your target audience, generating interest and creating a powerful connection.
Generate unusual, creative, and fascinating bullets that capture readers' attention about the product. Respond in Spanish and use a numbered list format. Important: Only answer bullets, never include explanations or categories, like this: 'La leyenda del padre soltero: Dice que nunca hay tiempo suficiente. El yoga te enseña a usar mejor el tiempo que tienes, incluso cuando te parece imposible(este bullet es cursioso).'.
"""

# Función para obtener los bullets
def get_gemini_response_bullets(target_audience, product, num_bullets, creativity):
    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)  # Define aquí
    model_choice = "gemini-1.5-flash"  # Modelo por defecto

    model = genai.GenerativeModel(model_choice)

    # System Prompt - Instrucción en inglés para el modelo
    system_instruction = """
    You are a world-class copywriter, expert in creating benefits that connect symptoms with problems. You deeply understand the emotions, desires, and challenges of a specific audience, allowing you to design personalized marketing strategies that resonate and motivate action. You know how to use proven structures to attract your target audience, generating interest and creating a powerful connection. 
    Generate unusual, creative, and fascinating bullets that subtly hint at the product without direct mention, capturing readers' attention. Respond in Spanish and use a numbered list format. Important: Never include explanations or categories, like this: 'La leyenda del padre soltero: Dice que nunca hay tiempo suficiente. El yoga te enseña a usar mejor el tiempo que tienes, incluso cuando te parece imposible.'.
   """

    # Crear el prompt para generar bullets
    full_prompt = f"""
    {system_instruction}
    Your task is to create {num_bullets} benefits or bullets that connect the symptom with the problem faced by {target_audience}, increasing their desire to acquire the {product}. 
    Infuse your responses with a creativity level of {creativity}. The bullets should be of the following types: 
    * 'The bathroom cabinet is the best place to store medicine, right? Incorrect. It's the worst. The facts are on page 10.' 
    * 'The best verb tense that gives your clients the feeling they've already bought from you.' 
    * 'The story of...', 'The mysteries of...', 'The legend of...' 
    * 'A simple system to write copy without trying to convince them to buy.' 
    * Truth: 'The truth that you've never been told in school, or at home, about how to make a living from music.' 
    * 'Did you know that...' 
    * 'When is it a good idea to tell a girl you like her? If you don't say it at that moment, say goodbye to getting to know her intimately.' 
    Using {mention_instruction} when you want to mention {product}.
    Use the following mention instructions to guide your writing: {mention_instruction}
    Using the mention type '{product_mention}' to guide how to mention the product in the benefits or bullets. Ensure the mention is adapted based on this type:
    - Direct: Clearly highlight the product as the solution.
    - Indirect: Subtly suggest the product without naming it.
    - Metaphorical: Use a metaphor to connect the product to the solution.
    When responding, always include a headline that references the {target_audience} and the product in the following way: 'Aquí tienes 5 bullets para Papás solteros, que aumenten el deseo de adquirir el Aceite multigrado, usando la mención indirecta:' 
    Please create the bullets now.
    """

    response = model.generate_content([full_prompt])

    if response and response.parts:
        return response.parts[0].text
    else:
        raise ValueError("Lo sentimos, intenta con una combinación diferente de entradas.")

# Inicializar la aplicación Streamlit
st.set_page_config(page_title="Generador de Bullets", layout="wide")

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Impact Bullet Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma los pensamientos de tu audiencia en balas persuasivas que inspiren a la acción.</h4>", unsafe_allow_html=True)

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
    
    # Campos de personalización sin acordeón
    num_bullets = st.slider("Número de Bullets", min_value=1, max_value=15, value=5)
    creativity = st.selectbox("Creatividad", ["Alta", "Media", "Baja"])

    # Botón de enviar
    submit = st.button("Generar Bullets")

# Mostrar los bullets generados
if submit:
    if target_audience and product:
        try:
            # Obtener la respuesta del modelo
            generated_bullets = get_gemini_response_bullets(target_audience, product, num_bullets, creativity)
            action_bullets = get_action_oriented_bullets(product)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Observa la magia en acción:</h4>
                    <p>{generated_bullets}</p>
                    <h4>Bullets orientados a la acción:</h4>
                    <p>{'<br>'.join(action_bullets)}</p>
                </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            col2.error(f"Error: {str(e)}")
    else:
        col2.error("Por favor, proporciona el público objetivo y el producto.")
