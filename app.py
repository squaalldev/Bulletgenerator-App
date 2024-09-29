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
    mention_instruction = get_mention_instruction(product_mention, product)
    model_choice = "gemini-1.5-flash"  # Modelo por defecto

    # Configuración del modelo generativo y las instrucciones del sistema
    model = genai.GenerativeModel(
        model_name=model_choice,  
        generation_config={
            "temperature": temperature,  
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
            f"When responding, always include a heading referencing {target_audience} and the product as follows:" f"'Aquí hay {num_bullets} bullets para convencer a {target_audience}, de [beneficio de comprar, asistir, descargar, adquirir,] {product}' "
        )
    )

    # Crear la instrucción para generar bullets
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Tu tarea es escribir {num_bullets} bullets que denoten los beneficios del {product} y que tienen la cualidad de fascinar y por lo tanto, fomentan el deseo de adquirir, asistir, descargar o comprar el {product}."
                    f"Un buen bullet conecta los síntomas con los problemas enfrentados por {target_audience} de una manera natural, que no se note como manipuladora."
                    f"Escribe bullets creativos, en un estilo conversacional, que no sean aburridos, sino mas bien divertidos. "
                    f"Sé sutil a la hora de crear los bullets para referirte a los beneficios del {product}. "
                    "1. **Connection**: Words that highlight the relationship between the product and the benefit for the user (e.g., 'Improve,' 'Transform').\n"
                    "2. **Benefit**: Explain how the user will benefit by attending, downloading, or purchasing the product.\n\n"
                    "Ensure each bullet follows the structure of 'Connection + connector + Benefit,' and avoid including explanations like 'Connection: Improve' or 'Benefit: Increase my happiness.'\n"
                    "Important: Only respond with bullets, never include explanations or categories, like this example: 'Attend the masterclass and discover techniques to boost your professional career. (This bullet appeals to the desire for personal and professional growth.)'\n"
                    "Use these guidelines to generate high-converting bullets in Spanish."
                    "Important: Never include explanations or categories, like this: 'La leyenda del padre soltero: Dice que nunca hay tiempo suficiente. El yoga te enseña a usar mejor el tiempo que tienes, incluso cuando te parece imposible.' "
                    "Bullets should vary, based on these examples to guide your task of creating bullets:\n\n"
                    "* 'El armario del baño es el mejor lugar para guardar medicamentos, ¿verdad? Incorrecto. Es el peor. Los hechos están en la página 10.' "
                    "* 'El mejor tiempo verbal que le da a tus clientes la sensación de que ya te han comprado.' "
                    "* 'La historia de un joven emprendedor que transformó su vida aplicando esta técnica simple pero poderosa.' " 
                    "* 'Los misterios de cómo algunas personas parecen tener éxito sin esfuerzo, mientras otras luchan. La clave está en esta pequeña diferencia.' "
                    "* 'La leyenda de aquellos que dominaron la productividad con un solo hábito. ¿Te atreves a descubrirlo?' "
                    "* 'Un sistema simple para escribir textos sin intentar convencerlos de comprar.' "
                    "* 'La verdad que nunca te han contado en la escuela, o en casa, sobre cómo ganarte la vida con la música.' "
                    "* 'La historia de un padre ocupado que, con solo 10 minutos al día, logró transformar su salud y bienestar.' "
                    "* 'Los misterios de cómo una técnica sencilla te permite reducir el estrés al instante, sin necesidad de dejar tu trabajo o cambiar tu estilo de vida.' "
                    "* '¿Sabías que muchas personas están usando este método y han mejorado su bienestar en solo 7 días?'"
                    "* '¿Cuándo es una buena idea decirle a una chica que te gusta? Si no se lo dices en ese momento, despídete de conocerla íntimamente.' "
                    "Por favor, crea los bullets ahora."
                ],
            },
        ]
    )

    # Crear un mensaje para el modelo que incluye los bullets generados según los tipos seleccionados
    full_prompt = f"{mention_instruction}"

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
                    <h4>🧙🏻‍♂️ Mira la magia en acción:</h4>
                    <pre style="white-space: pre-wrap;">{generated_bullets}</pre>
                </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            st.error(str(e))
    else:
        st.error("Por favor, completa todos los campos.")
