from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Diccionario de ejemplos de bullets
bullets_examples = {
    "1": "El armario del baño es el mejor lugar para guardar medicamentos, ¿verdad? Incorrecto. Es el peor. Los hechos están en la página 10.",
    "2": "El mejor tiempo verbal que le da a tus clientes la sensación de que ya te han comprado.",
    "3": "La historia de un joven emprendedor que transformó su vida aplicando esta técnica simple pero poderosa.",
    "4": "Los misterios de cómo algunas personas parecen tener éxito sin esfuerzo, mientras otras luchan. La clave está en esta pequeña diferencia.",
    "5": "La leyenda de aquellos que dominaron la productividad con un solo hábito. ¿Te atreves a descubrirlo?",
    "6": "Un sistema simple para escribir textos sin intentar convencerlos de comprar.",
    "7": "La verdad que nunca te han contado en la escuela, o en casa, sobre cómo ganarte la vida con la música.",
    "8": "La historia de un padre ocupado que, con solo 10 minutos al día, logró transformar su salud y bienestar.",
    "9": "Los misterios de cómo una técnica sencilla te permite reducir el estrés al instante, sin necesidad de dejar tu trabajo o cambiar tu estilo de vida.",
    "10": "¿Sabías que muchas personas están usando este método y han mejorado su bienestar en solo 7 días?",
    "11": "¿Cuándo es una buena idea decirle a una chica que te gusta? Si no se lo dices en ese momento, despídete de conocerla íntimamente."
}

# Función para obtener una cantidad de bullets
def get_gemini_response_bullets(target_audience, product, num_bullets, temperature):
    model_choice = "gemini-1.5-flash"  # Modelo por defecto

    # Seleccionar un bullet aleatorio de los ejemplos
    selected_bullet = random.choice(list(bullets_examples.values()))

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
            f"Eres un copywriter excepcional, experto en conectar con {target_audience}. "
            f"Entiendes perfectamente sus emociones y desafíos. Crea bullets que no solo informen, sino que hablen directamente al corazón de {target_audience}, "
            f"generando curiosidad y ganas de saber más sobre {product}. "
            f"¡Haz que se sientan incluidos! Usa un tono amistoso y divertido. "
            f"Por ejemplo, si están buscando {product}, dales un motivo irresistible para seguir leyendo. "
            f"Incluye un encabezado atractivo que diga: 'Aquí tienes {num_bullets} razones por las que {target_audience} debería considerar {product}'."
        )
    )

    # Crear la instrucción para generar bullets
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Quiero que escribas {num_bullets} bullets que transmitan los beneficios de {product} de una manera que atraiga a {target_audience}. "
                    f"Conecta los problemas y deseos de {target_audience} de forma natural y con un estilo amigable y divertido. "
                    f"Recuerda usar este ejemplo como inspiración: {selected_bullet}. "
                    "Aquí tienes un par de ideas para que te inspires:\n"
                    "1. ¿Sabías que...? Esto cambiará tu perspectiva sobre... \n"
                    "2. Imagina si pudieras... ¡Lo que estás buscando está aquí!\n"
                    f"Por favor, genera bullets creativos que hagan que {target_audience} se sienta emocionado por {product}."
                ],
            },
        ]
    )

    # Crear un mensaje para el modelo que incluye los bullets generados
    response = model.generate_content(chat_session.history)  # Aquí usamos el historial del chat

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
