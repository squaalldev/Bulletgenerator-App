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
    probabilities = [0.35, 0.25, 0.40]
    return random.choices(mentions, probabilities)[0]

# Crear la instrucción de mención basada en la opción seleccionada
def get_mention_instruction(product_mention, product):
    if product_mention == "Directa":
        return f"Introduce directamente el producto '{product}' como la solución clara al problema que enfrenta el lector, de manera conversacional, no forzada."
    elif product_mention == "Indirecta":
        return f"Referencia sutilmente el producto '{product}' como una posible solución al problema del lector sin nombrarlo explícitamente."
    elif product_mention == "Metafórica":
        return f"Introduce el producto '{product}' usando una metáfora, conectándolo simbólicamente a la solución que necesita el lector."
    return ""

# Ejemplos de bullets
benefit_types = {
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
    ],
}

# Función para generar bullets
def generate_bullets(number_of_bullets, target_audience, product, call_to_action, temperature):
    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)

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
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            f"Eres un experto copywriter especializado en escribir bullets atractivos para {target_audience} sobre {product} que promueven la acción de {call_to_action}. "
            "Tu tarea es ayudarme a escribir bullets que destaquen los beneficios de {product}. "
            "Recuerda que cada bullet debe ser breve, claro y persuasivo, y seguir la estructura de:"
            "1. Algo que llame la atención del lector, pueder ser una pregunta, afirmación, dato curioso, estadistica."
            "2. Presenta la solución de manera natural, como si fuera la solución al problema anterior mencionado."
            "3. Escribe los beneficios de {product} como la solución a todos sus problemas."
             f"4. Finaliza con un llamado a la acción en donde destaques que perderían o no ganarían si no realizan la {call_to_action}."
            "Basate en este ejemplo como respuesta:"
            "¿Te sientes como un barco a la deriva en un mar de responsabilidades? 🌊"
            "El Curso online de Yoga es tu brújula para navegar las aguas turbulentas de la paternidad soltera."
            "* Reduce el estrés y la ansiedad como un ancla que te mantiene firme en medio de la tormenta."
            "* Aumenta tu energía y concentración para navegar con mayor seguridad y precisión."
            "* Mejora tu flexibilidad y movilidad para adaptarte a cualquier situación con mayor agilidad."
            "* Encuentra la paz interior como un faro que te guía hacia la calma en medio del caos."
            "* Conecta contigo mismo para descubrir tu propio rumbo y navegar con mayor confianza."
            "* Aprende técnicas para gestionar el tiempo y la energía para optimizar tu viaje y disfrutar de cada momento."
            "¡Asiste al webinar GRATIS para descubrir cómo el Curso online de Yoga puede ser tu brújula hacia una vida más equilibrada y plena! 'Beneficio + Conector + Valor'. "
            "Los bullets deben inspirar interés y motivar al lector a tomar acción. "
        )
    )

    # Selección aleatoria de tipos de beneficios, manteniendo variedad en la salida
    selected_types = random.sample(list(benefit_types.keys()), min(number_of_bullets, len(benefit_types)))

    # Crear un mensaje para el modelo que incluye los bullets generados según los tipos seleccionados
    benefits_instruction = (
        f"Tu tarea es crear {number_of_bullets} bullets efectivos dirigidos a {target_audience}, "
        f"para promover {call_to_action} usando la siguiente mención: {mention_instruction}. "
        "Asegúrate de que cada bullet siga la estructura de los ejemplos proporcionados anteriormente."
    )

    # Generar el resultado utilizando el modelo con la instrucción de bullets específica
    try:
        response = model.generate_content([benefits_instruction])
        
        # Extraer el texto de la respuesta
        generated_bullets = response.candidates[0].content.parts[0].text.strip()  
        
        # Retornar el resultado
        return generated_bullets
    except Exception as e:
        raise ValueError(f"Error al generar los bullets: {str(e)}")

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="Quick Prompt", layout="wide")

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

# Crear columnas
col1, col2 = st.columns([1, 2])  

# Columnas de entrada
with col1:
    target_audience = st.text_input("¿Quién es tu público objetivo?", placeholder="Ejemplo: Estudiantes Universitarios")
    product = st.text_input("¿Qué producto tienes en mente?", placeholder="Ejemplo: Curso de Inglés")
    call_to_action = st.text_input("¿Qué acción deseas que tomen?", placeholder="Ejemplo: Inscribirse al curso")
    number_of_bullets = st.selectbox("Número de bullets", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=2)
    temperature = st.slider("Creatividad", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    # Botón de enviar
    submit = st.button("Generar Beneficios")

# Mostrar los beneficios generados
if submit:
    if target_audience and product and call_to_action:
        try:
            # Obtener la respuesta del modelo
            generated_bullets = generate_bullets(number_of_bullets, target_audience, product, call_to_action, temperature)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Mira los bullets generados:</h4>
                    <p style="font-size: 22px;">{generated_bullets}</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al generar los bullets: {str(e)}")
    else:
        st.error("Por favor, completa todos los campos.")
