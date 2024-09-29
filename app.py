from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Ejemplos de bullets por tipo
bullets_types = {
    "directos": [
        "El armario del baño es el mejor lugar para guardar medicamentos, ¿verdad? Incorrecto. Es el peor. Los hechos están en la página 10.",
        "El mejor tiempo verbal que le da a tus clientes la sensación de que ya te han comprado.",
        "La historia de un joven emprendedor que transformó su vida aplicando esta técnica simple pero poderosa."
    ],
    "misterios": [
        "Los misterios de cómo algunas personas parecen tener éxito sin esfuerzo, mientras otras luchan. La clave está en esta pequeña diferencia.",
        "Los misterios de cómo una técnica sencilla te permite reducir el estrés al instante, sin necesidad de dejar tu trabajo o cambiar tu estilo de vida."
    ],
    "leyendas": [
        "La leyenda de aquellos que dominaron la productividad con un solo hábito. ¿Te atreves a descubrirlo?",
        "La verdad que nunca te han contado en la escuela, o en casa, sobre cómo ganarte la vida con la música."
    ],
    "historias_personales": [
        "La historia de un padre ocupado que, con solo 10 minutos al día, logró transformar su salud y bienestar.",
        "¿Sabías que muchas personas están usando este método y han mejorado su bienestar en solo 7 días?"
    ],
    "preguntas_retoricas": [
        "¿Cuándo es una buena idea decirle a una chica que te gusta? Si no se lo dices en ese momento, despídete de conocerla íntimamente."
    ]
}

# Función para seleccionar bullets aleatorios
def get_random_bullets(num_bullets):
    selected_bullets = []
    # Selección aleatoria de tipos de bullet, manteniendo variedad en la salida
    selected_types = random.sample(list(bullets_types.keys()), min(num_bullets, len(bullets_types)))

    for bullet_type in selected_types:
        bullet = random.choice(bullets_types[bullet_type])
        selected_bullets.append(bullet)
        
    return selected_bullets

# Función para obtener una cantidad de bullets
def get_gemini_response_bullets(target_audience, product, num_bullets, temperature):
    # Seleccionar bullets aleatorios usando la nueva función
    selected_bullets = get_random_bullets(num_bullets)

    # Configuración del modelo
    generation_config = {
        "temperature": temperature,  
        "top_p": 0.90,       
        "top_k": 128,        
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    # Configuración del modelo generativo y las instrucciones del sistema
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",  # Nombre del modelo que estamos utilizando
        generation_config=generation_config,  # Configuración de generación
        system_instruction=(
            f"You are a world-class copywriter, expert in creating bullets. "
            f"You deeply understand the emotions, desires, and challenges of {target_audience}, allowing you to design personalized bullets that resonate and motivate action. "
            "Generate unusual, creative, and fascinating bullets with a format conversational that capture {target_audience}'s attention like this:" 
    "directos": [
        "El armario del baño es el mejor lugar para guardar medicamentos, ¿verdad? Incorrecto. Es el peor. Los hechos están en la página 10.",
        "El mejor tiempo verbal que le da a tus clientes la sensación de que ya te han comprado.",
        "La historia de un joven emprendedor que transformó su vida aplicando esta técnica simple pero poderosa."
    ],
    "misterios": [
        "Los misterios de cómo algunas personas parecen tener éxito sin esfuerzo, mientras otras luchan. La clave está en esta pequeña diferencia.",
        "Los misterios de cómo una técnica sencilla te permite reducir el estrés al instante, sin necesidad de dejar tu trabajo o cambiar tu estilo de vida."
    ],
    "leyendas": [
        "La leyenda de aquellos que dominaron la productividad con un solo hábito. ¿Te atreves a descubrirlo?",
        "La verdad que nunca te han contado en la escuela, o en casa, sobre cómo ganarte la vida con la música."
    ],
    "historias_personales": [
        "La historia de un padre ocupado que, con solo 10 minutos al día, logró transformar su salud y bienestar.",
        "¿Sabías que muchas personas están usando este método y han mejorado su bienestar en solo 7 días?"
    ],
    "preguntas_retoricas": [
        "¿Cuándo es una buena idea decirle a una chica que te gusta? Si no se lo dices en ese momento, despídete de conocerla íntimamente."
            "Respond in Spanish and use a numbered list format. "
            "Never respond like this: 'Crea momentos inolvidables: Comparte la experiencia de cocinar con tus hijos, fomentando la unión familiar y creando recuerdos especiales.'"
            f"When responding, always include a heading referencing {target_audience} as follows: 'Aquí hay {num_bullets} bullets para convencer a {target_audience}.'"
     ],
       )
    )

    # Crear la instrucción para generar bullets
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Tu tarea es escribir {num_bullets} bullets que denoten los beneficios al hablar de {product} que resolverán los problemas de {target_audience}. "
                    "Por favor, crea los bullets ahora."
                ],
            },
        ]
    )

    # Crear un mensaje para el modelo que incluye los bullets generados
    response = model.generate_content(chat_session.history)

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
    num_bullets = st.slider("Número de Bullets", min_value=1, max_value=10, value=5)
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
