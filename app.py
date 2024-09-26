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
        return f"""
        Directly introduce the product '{product}' as the clear solution to the problem the reader is facing. Ensure that the product is presented in a way that highlights its key benefits and demonstrates how it directly addresses the issue at hand. The mention should feel natural and seamlessly integrated into the narrative.
        """
    elif product_mention == "Indirecta":
        return f"""
        Subtly reference the product '{product}' as a potential solution to the reader's problem without naming it explicitly. Weave the product's core benefits into the description of how the reader can overcome the issue, creating an implicit connection between the solution and the product. Ensure the mention is subtle but clear enough to guide the reader towards the product.
        """
    elif product_mention == "Metafórica":
        return f"""
        Introduce the product '{product}' using a metaphor, connecting it symbolically to the solution the reader needs. The metaphor should relate to the problem being discussed and should creatively suggest how the product offers a resolution without explicitly stating its name. The metaphor should evoke the benefits of the product in a memorable and thought-provoking way.
        """
    return ""

# System Prompt - Instrucción en inglés para el modelo
system_instruction = """
You are a world-class copywriter, expert in creating benefits that connect symptoms with problems. You deeply understand the emotions, desires, and challenges of a specific audience, allowing you to design personalized marketing strategies that resonate and motivate action. You know how to use proven structures to attract your target audience, generating interest and creating a powerful connection.
Generate unusual, creative, and fascinating bullets that capture readers' attention about the product. Respond in Spanish and use a numbered list format. Important: Only answer bullets, never include explanations or categories, like this: 'La leyenda del padre soltero: Dice que nunca hay tiempo suficiente. El yoga te enseña a usar mejor el tiempo que tienes, incluso cuando te parece imposible.'.
IMPORTANT: Only write the bullets. No headers, no explanations, no types of bullets, just the bullets. 
"""

# Función para obtener una cantidad de bullets
def get_gemini_response_bullets(target_audience, product, num_bullets, creativity, desired_action):
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
    Your task is to create {num_bullets} benefits or bullets that connect the symptom with the problem faced by {target_audience}, increasing their curiosity about the {product}. 
    The ultimate goal is to inspire the audience to take the following action: {desired_action}. 
    Infuse your responses with a creativity level of {creativity}. The bullets should be of the following types: 
    * 'The bathroom cabinet is the best place to store medicine, right? Incorrect. It's the worst. The facts are on page 10.' 
    * 'The best verb tense that gives your clients the feeling they've already bought from you.' 
    * 'The story of...', 'The mysteries of...', 'The legend of...' 
    * 'A simple system to write copy without trying to convince them to buy.' 
    * 'The truth that you've never been told in school, or at home, about how to make a living from music.' 
    * 'Did you know that...' 
    * 'When is it a good idea to tell a girl you like her? If you don't say it at that moment, say goodbye to getting to know her intimately.' 
    Use the following mention instructions to guide your writing: {mention_instruction}
    Using the mention type '{product_mention}' to guide how to mention the product in the benefits or bullets. Ensure to adapt your writing based on this mention type:
    - Direct: Clearly highlight the product as the solution.
    - Indirect: Subtly suggest the product without naming it.
    - Metaphorical: Use a metaphor to connect the product to the solution.
    Please create the bullets now.
    Cuando respondas siempre escribe un titular que mencione el público objetivo, el producto de la siguiente manera: 'Aquí tienes 5 bullets para Papás solteros, que aumenten el deseo de adquirir el Aceite multigrado, usando la mención indirecta:' 
    """

    response = model.generate_content([full_prompt])

    if response and response.parts:
        return response.parts[0].text
    else:
        raise ValueError("Lo sentimos, intenta con una combinación diferente de entradas.")

# Inicializar la aplicación Streamlit
st.set_page_config(page_title="Impact Bullet Generator", layout="wide")

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

    # Añadir nuevo campo de entrada para la Acción Deseada
    desired_action = st.text_input("¿Cuál es la acción deseada?")
    
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
            generated_bullets = get_gemini_response_bullets(target_audience, product, num_bullets, creativity, desired_action)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Mira la magia en acción:</h4>
                    <p>{generated_bullets}</p>
                </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            col2.error(f"Error: {str(e)}")
    else:
        col2.error("Por favor, proporciona el público objetivo y el producto.")