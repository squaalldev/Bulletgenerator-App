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

# Fórmulas con ejemplos y explicaciones
benefits_formulas = {
    "plantilla": {
        "description": """
            Crea bullets de beneficios que respondan estas tres preguntas clave:
            1. ¿Qué es lo que el lector quiere conseguir?
            2. ¿En qué periodo de tiempo quiere conseguirlo?
            3. ¿Cuál es la objeción principal del lector que le impide lograrlo?
        """,
        "examples": [
            "Obtén tus primeros 100 clientes en 30 días, sin gastar un solo centavo en publicidad.",
            "Pierde esos 5 kilos en solo 10 minutos al día, sin dejar de disfrutar tus comidas favoritas.",
            "Ahorra para salir de viaje en tres meses, sin sacrificar esas noches de cine."
        ]
    },
    "formula_suprema_istvanova": {
        "description": """
            La estructura de la fórmula Suprema de Istvanova es: Números + Adjetivo + Palabra Clave + Razón + Promesa. 
            Crea bullets points o beneficios con beneficios específicos y atractivos que conectan emocionalmente con {target_audience} y cumple con estos elementos:
            1. **Números**: Se escriben con el fin de declarar que existen cierto números de articulos.
            2. **Adjetivo**: Añaden emoción y atractivo al mensaje.
            3. **Palabra Clave**: Reflejan el beneficio principal o tema clave.
            4. **Razón**: Justifican el beneficio o valor del producto.
            5. **Promesa**: Muestran el resultado o beneficio que el lector puede esperar.
            Cada uno de estos elementos se Integra de manera natural y no forzada cuando se crean los bullets points así como los examples. 
        """,
        "examples": [
            "5 métodos simples para duplicar tus ventas en menos de 30 días.",
            "8 trucos secretos para que tu perro obedezca en una semana.",
            "10 técnicas fáciles que mejorarán tu relación antes de un mes."
        ]
    },
    "formula_aida": {
        "description": """
            La estructura de la fórmula AIDA para crear bullets points con beneficios es: Atención + Interés + Deseo + Acción.
            Crea bullets points o beneficios que sigan estos pasos:
            - **Atención**: Captura de inmediato el interés o atención de {target_audience} por medio de un dato insólito o increíble, le habla de una situación problemática o un deseo de {target_audience}.
            - **Interés**: Detalla cómo el beneficio del {product} soluciona un problema específico o como Facilita la obtencion de un deseo de {target_audience}.
            - **Deseo**: Despierta el anhelo por lograr el resultado prometido.
            - **Acción**: Inspira al lector a actuar para obtener el beneficio.
            Todos estos elementos se integral de manera natural y no forzada al crear los bullets points o beneficios. 
        """,
        "examples": [
            "Descubre cómo atraer clientes automáticamente, sin experiencia previa.",
            "Imagina tener un cuerpo en forma disfrutando lo que te gusta comer.",
            "Empieza hoy mismo y experimenta resultados en solo 7 días."
        ]
    }
}

# Función para generar bullets de beneficios
def generate_benefits(number_of_benefits, target_audience, product, temperature, selected_formula):
    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)

    # Crear la configuración del modelo
    generation_config = {
        "temperature": temperature,  
        "top_p": 0.65,        # Considerar un poco menos de palabras probables
        "top_k": 360,        # Aumentar las palabras candidatas para más variedad
        "max_output_tokens": 8196,  # Mantenerlo igual, pero puedes aumentar si deseas más detalle
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are a world-class copywriter, with expertise in crafting benefits that connect emotionally and address the desires, problems, and motivations of {target_audience}. Your task is to generate compelling and specific benefit bullets in Spanish based on a given formula. Always respond with a numbered list format, and ensure each benefit is relevant, concise, action-oriented with a natural language and conversational way. Do not include explanations or categories in your output."
    )

    # Crear un mensaje para el modelo, destacando la audiencia, el producto, la fórmula seleccionada y los ejemplos
    benefits_instruction = (
        f"Tu tarea es crear {number_of_benefits} beneficios irresistibles diseñados para {target_audience}. "
        f"El objetivo es mostrar cómo {product} puede transformar la vida del lector, conectando de forma natural y emocional. "
        f"Evita usar menciones literales o repetitivas, y destaca soluciones concretas, mostrando cómo el producto elimina obstáculos o satisface deseos reales. "
        f"Usa la fórmula seleccionada como guía:\n\n{selected_formula['description']}\n\n"
        f"Inspírate en estos ejemplos:\n"
        f"- {selected_formula['examples'][0]}\n"
        f"- {selected_formula['examples'][1]}\n"
        f"- {selected_formula['examples'][2]}\n\n"
        f"Y no olvides integrar esta instrucción de manera fluida: {mention_instruction}. "
        f"Tu objetivo es inspirar deseo y acción, evitando explicaciones o categorías en la respuesta."
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [benefits_instruction],
            },
        ]
    )

    response = chat_session.send_message("Genera los beneficios")  # Enviar mensaje para obtener la respuesta
    return response.text  # Regresar la respuesta directamente

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="Bullet Benefits Generator", layout="wide")

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Bullet Benefits Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma características en beneficios irresistibles que conectan emocionalmente con tu audiencia.</h4>", unsafe_allow_html=True)

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
    number_of_benefits = st.selectbox("Número de Beneficios", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=4)

    # Crear un único acordeón para fórmula y creatividad
    with st.expander("Personaliza tus beneficios"):
        temperature = st.slider("Creatividad", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
        
        selected_formula_key = st.selectbox(
            "Selecciona una fórmula para tus beneficios",
            options=list(benefits_formulas.keys())
        )
        selected_formula = benefits_formulas[selected_formula_key]

    # Botón de enviar
    submit = st.button("Generar Beneficios")

# Mostrar los beneficios generados
if submit:
    if target_audience and product and selected_formula:
        try:
            # Obtener la respuesta del modelo
            generated_benefits = generate_benefits(number_of_benefits, target_audience, product, temperature, selected_formula)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Explora los beneficios generados:</h4>
                    <p>{generated_benefits}</p>
                </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            col2.error(f"Error: {str(e)}")
    else:
        col2.error("Por favor, proporciona el público objetivo, el producto y selecciona una fórmula.")