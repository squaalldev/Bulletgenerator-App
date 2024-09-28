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
    probabilities = [0.20, 0.30, 0.50]  # Probabilidades ajustadas
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

# Función para obtener una cantidad de bullets
def get_gemini_response_bullets(target_audience, product, num_bullets, temperature):
    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)  # Define aquí
    model_choice = "gemini-1.5-flash"  # Modelo por defecto

    # Configuración del modelo generativo y las instrucciones del sistema
    model = genai.GenerativeModel(
        model_name=model_choice,  # Nombre del modelo que estamos utilizando
        generation_config={
            "temperature": temperature,  # Cambiamos creatividad por temperature
            "top_p": 0.85,       
            "top_k": 128,        
            "max_output_tokens": 2048,
            "response_mime_type": "text/plain",
        },
        system_instruction=(
            f"You are a world-class copywriter, expert in creating benefits that connect symptoms with problems of {target_audience}. "
            f"You deeply understand the emotions, desires, and challenges of {target_audience}, allowing you to design personalized copywriting that resonate and motivate action. "
            f"You know how to use proven structures to attract {target_audience}, generating interest and creating a powerful connection with {product}. "
            "Generate unusual, creative, and fascinating bullets that capturing {target_audience}'s attention. Respond in Spanish and use a numbered list format. "
            "Important: Never include explanations or categories, like this: 'La leyenda del padre soltero: Dice que nunca hay tiempo suficiente. El yoga te enseña a usar mejor el tiempo que tienes, incluso cuando te parece imposible.' "
            "Los bullets deben ser de los siguientes tipos: "
            "* 'El armario del baño es el mejor lugar para guardar medicamentos, ¿verdad? Incorrecto. Es el peor. Los hechos están en la página 10.' "
            "* 'El mejor tiempo verbal que le da a tus clientes la sensación de que ya te han comprado.' "
            "* 'La historia de...', 'Los misterios de...', 'La leyenda de...' "
            "* 'Un sistema simple para escribir textos sin intentar convencerlos de comprar.' "
            "* Verdad: 'La verdad que nunca te han contado en la escuela, o en casa, sobre cómo ganarte la vida con la música.' "
            "* '¿Sabías que...' "
            "* '¿Cuándo es una buena idea decirle a una chica que te gusta? Si no se lo dices en ese momento, despídete de conocerla íntimamente.' "
            f"Usando {mention_instruction} cuando desees mencionar {product}. "
            f"Usa las siguientes instrucciones de mención para guiar tu escritura: {mention_instruction} "
            f"Usando el tipo de mención '{product_mention}' para guiar cómo mencionar el producto en los beneficios o bullets. "
            f"Al responder, siempre incluye un encabezado que haga referencia a {target_audience} y el producto de la siguiente manera: "
            f"'Aquí tienes 5 bullets para {target_audience}, que aumenten el deseo de adquirir el {product}, usando la mención indirecta:' "
        )
    )

    # Crear el prompt para generar bullets
    bullets_instruction = (
        f"Tu tarea es escribir {num_bullets} beneficios o bullets que conecten el síntoma con el problema enfrentado por {target_audience}, "
        f"aumentando su deseo de adquirir, asistir, descargar o comprar el {product}. "
        f"Escribe los bullets con un nivel de creatividad {temperature:.1f}. "
        "Asegúrate de que la mención se adapte según este tipo: "
        "Por favor, crea los bullets ahora."
    )

    # Crear un mensaje para el modelo que incluye los bullets generados según los tipos seleccionados
    full_prompt = f"{bullets_instruction}"

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
    temperature = st.slider("Creatividad", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    # Botón de enviar
    submit = st.button("Generar Bullets")

# Mostrar los bullets generados
if submit:
    if target_audience and product:
        try:
            # Obtener la respuesta del modelo
            generated_bullets = get_gemini_response_bullets(target_audience, product, num_bullets, temperature)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Observa la magia en acción:</h4>
                    <p>{generated_bullets}</p>
                </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            col2.error(f"Error: {str(e)}")
    else:
        col2.error("Por favor, proporciona el público objetivo y el producto.")
