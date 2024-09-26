from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función para obtener una llamada a la acción de manera probabilística
def get_random_call_to_action():
    actions = ["Directo", "Sutil", "Indirecto"]
    probabilities = [0.34, 0.33, 0.33]  
    return random.choices(actions, probabilities)[0]

# Crear la instrucción para la llamada a la acción según la opción seleccionada
def get_call_to_action_instruction(action_call):
    if action_call == "Directo":
        return "Incorporate a clear and direct call to action that motivates the reader to act immediately. The call should be compelling and highlight the urgency of taking action."
    elif action_call == "Sutil":
        return "Suggest a call to action subtly, hinting at the benefits of acting without being too obvious. The reader should feel like they are making the decision on their own."
    elif action_call == "Indirecto":
        return "Present a call to action indirectly, creating a scenario where the reader can see the action as a natural solution to their problems without naming it explicitly."
    return ""

# System Prompt - Instrucción en inglés para el modelo
system_instruction = """
You are a world-class copywriter, expert in creating benefits that connect symptoms with problems. You deeply understand the emotions, desires, and challenges of a specific audience, allowing you to design personalized marketing strategies that resonate and motivate action. You know how to use proven structures to attract your target audience, generating interest and creating a powerful connection.
Generate unusual, creative, and fascinating bullets that capture readers' attention about the product. Respond in Spanish and use a numbered list format. Important: Only answer bullets, never include explanations or categories, like this: 'La leyenda del padre soltero: Dice que nunca hay tiempo suficiente. El yoga te enseña a usar mejor el tiempo que tienes, incluso cuando te parece imposible.'.
"""

# Función para obtener una cantidad de bullets
def get_gemini_response_bullets(target_audience, num_bullets, creativity):
    action_call = get_random_call_to_action()  # Obtener la llamada a la acción aleatoria
    call_to_action_instruction = get_call_to_action_instruction(action_call)  # Definir la instrucción aquí
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
    * Good and Bad: 'The bathroom cabinet is the best place to store medicine, right? Incorrect. It's the worst. The facts are on page 10.' 
    * The Best/The Worst: 'The best verb tense that gives your clients the feeling they've already bought from you.' 
    * Stories: 'The story of...', 'The mysteries of...', 'The legend of...' 
    * Trick: 'A simple system to write copy without trying to convince them to buy.' 
    * The Truth: 'The truth that you've never been told in school, or at home, about how to make a living from music.' 
    * Asking a Question: 'Did you know that...' 
    * When: 'When is it a good idea to tell a girl you like her? If you don't say it at that moment, say goodbye to getting to know her intimately.' 
    Using {mention_instruction} when you want to mention {product}.
    """

    response = model.generate_content([full_prompt])

    if response and response.parts:
        return response.parts[0].text
    else:
        raise ValueError("Lo siento, intenta con una combinación diferente de valores.")

# Inicializar la aplicación Streamlit
st.set_page_config(page_title="Generador de Bullets", layout="wide")

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
    
    # Campos de personalización sin acordeón
    num_bullets = st.slider("Número de Bullets", min_value=1, max_value=10, value=5)
    creativity = st.selectbox("Creatividad", ["Alta", "Media", "Baja"])

    # Botón de enviar
    submit = st.button("Generar Bullets")

# Mostrar los bullets generados
if submit:
    if target_audience:
        try:
            # Obtener la respuesta del modelo
            generated_bullets = get_gemini_response_bullets(target_audience, num_bullets, creativity)  # Sin mención del producto
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Mira la magia:</h4>
                    <p>{generated_bullets}</p>
                </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            col2.error(f"Error: {str(e)}")
    else:
        col2.error("Por favor, proporciona el público objetivo y el producto.")
