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
        return f"Introduce directamente el producto '{product}' como la solución clara al problema que enfrenta el lector."
    elif product_mention == "Indirecta":
        return f"Referencia sutilmente el producto '{product}' como una posible solución al problema del lector sin nombrarlo explícitamente."
    elif product_mention == "Metafórica":
        return f"Introduce el producto '{product}' usando una metáfora, conectándolo simbólicamente a la solución que necesita el lector."
    return ""

# Ejemplos de beneficios por tipo
benefit_types = {
    "educación": [
        "Aprenderás las estrategias más efectivas para maximizar tu tiempo.",
        "Descubrirás técnicas probadas que han ayudado a miles a alcanzar sus objetivos.",
        "Tendrás acceso a contenido exclusivo que transformará tu manera de trabajar."
    ],
    "urgencia": [
        "No te quedes atrás; asiste para no perder la oportunidad de cambiar tu vida.",
        "Inscríbete ahora y asegúrate de obtener la información más actualizada."
    ],
    "comunidad": [
        "Únete a una comunidad de personas con ideas afines y comparte tus experiencias.",
        "Conectarás con expertos que pueden guiarte en tu camino."
    ],
    "resultados": [
        "Obtendrás herramientas que te ayudarán a lograr resultados visibles en poco tiempo.",
        "Aprenderás a implementar cambios que impulsarán tu carrera profesional."
    ],
    "exclusividad": [
        "Accede a recursos que solo están disponibles para los asistentes del webinar.",
        "Sé parte de un grupo selecto que recibe información privilegiada."
    ],
}

# Función para generar bullets de beneficios
def generate_benefits(number_of_benefits, target_audience, product, call_to_action, temperature):
    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)

    # Configuración del modelo
    generation_config = {
        "temperature": temperature,  
        "top_p": 0.85,       
        "top_k": 128,        
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    # Configuración del modelo generativo y las instrucciones del sistema
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            f"Eres un experto copywriter especializado en escribir beneficios atractivos para {target_audience} sobre {product} que promueven la acción de {call_to_action}. "
            "Tu tarea es ayudarme a escribir bullets que destaquen los beneficios de asistir, descargar o inscribirme al webinar. "
            "Recuerda que cada bullet debe ser breve, claro y persuasivo, y seguir la estructura 'Beneficio + Conector + Valor'. "
            "Los bullets deben inspirar interés y motivar al lector a tomar acción. "
            "Ejemplos: '- Aprenderás a...'; '- Descubrirás cómo...'; '- Conocerás a...'."
        )
    )

    # Selección aleatoria de tipos de beneficios, manteniendo variedad en la salida
    selected_types = random.sample(list(benefit_types.keys()), min(number_of_benefits, len(benefit_types)))

    # Crear un mensaje para el modelo que incluye los beneficios generados según los tipos seleccionados
    benefits_instruction = (
        f"Tu tarea es crear {number_of_benefits} bullets efectivos dirigidos a {target_audience}, "
        f"para promover {call_to_action} usando la siguiente mención: {mention_instruction}. "
        "Asegúrate de que cada bullet siga la estructura de 'Beneficio + Conector + Valor', "
        "como los ejemplos proporcionados anteriormente."
        f"Incluye un encabezado atractivo que diga: 'Aquí tienes {number_of_benefits} razones por las que {target_audience} debería considerar {product}'."
    )

    # Generar el resultado utilizando el modelo con la instrucción de beneficios específica
    try:
        response = model.generate_content([benefits_instruction])
        
        # Extraer el texto de la respuesta
        generated_benefits = response.candidates[0].content.parts[0].text.strip()  
        
        # Retornar el resultado
        return generated_benefits
    except Exception as e:
        raise ValueError(f"Error al generar los beneficios: {str(e)}")

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="Quick Prompt", layout="wide")

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Quick Prompt</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma tu mensaje en beneficios que inspiren a tu audiencia a tomar decisiones al instante.</h4>", unsafe_allow_html=True)

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
    number_of_benefits = st.selectbox("Número de beneficios", options=[1, 2, 3, 4, 5], index=2)
    temperature = st.slider("Creatividad", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    # Botón de enviar
    submit = st.button("Generar Beneficios")

# Mostrar los beneficios generados
if submit:
    if target_audience and product and call_to_action:
        try:
            # Obtener la respuesta del modelo
            generated_benefits = generate_benefits(number_of_benefits, target_audience, product, call_to_action, temperature)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Mira los beneficios generados:</h4>
                    <p style="font-size: 22px;">{generated_benefits}</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al generar los beneficios: {str(e)}")
    else:
        st.error("Por favor, completa todos los campos.")
