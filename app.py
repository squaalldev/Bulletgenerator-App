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

# Ángulos adicionales para generar bullets
angles = {
    "Curiosidad": "Crea bullets que despierten el interés del lector dejándolos enganchados y queriendo saber más.",
    "Casi Imposible": "Crea bullets que suenen difíciles de creer pero plausibles, asombrando al lector.",
    "Autoridad y Credibilidad": "Crea bullets respaldados por datos o referencias que generen confianza.",
    "Contraste": "Crea bullets que presenten ideas opuestas o conceptos inesperados, captando atención con contraste."
}

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
            Crea bullets con beneficios específicos y atractivos que conectan emocionalmente con {target_audience}.
        """,
        "examples": [
            "5 métodos simples para duplicar tus ventas en menos de 30 días.",
            "8 trucos secretos para que tu perro obedezca en una semana.",
            "10 técnicas fáciles que mejorarán tu relación antes de un mes."
        ]
    }
}
def generate_bullets_with_angles(angle, number_of_bullets, target_audience, product, temperature):
    """
    Genera bullets utilizando diferentes ángulos específicos.

    Args:
        angle (str): Ángulo seleccionado (Curiosidad, Casi Imposible, Autoridad y Credibilidad, Contraste).
        number_of_bullets (int): Número de bullets a generar.
        target_audience (str): Público objetivo.
        product (str): Producto para el cual se generan los bullets.
        temperature (float): Temperatura para controlar la creatividad del modelo

    Returns:
        str: Texto con los bullets generados.
    """
    angles_descriptions = {
        "Curiosidad": (
            "Crea bullets que despierten el interés del lector dejándolos enganchados y queriendo saber más. "
            "El objetivo es que piensen '¿Qué será eso?' o 'Necesito saber más'."
        ),
        "Casi Imposible": (
            "Crea bullets que suenen difíciles de creer o 'casi imposibles', pero que sean plausibles. "
            "El lector debería tener una reacción de asombro y querer probar si es posible."
        ),
        "Autoridad y Credibilidad": (
            "Crea bullets que respalden la información con autoridad, incluyendo referencias a expertos, datos, o ejemplos relevantes. "
            "Construye contexto para generar confianza."
        ),
        "Contraste": (
            "Crea bullets que presenten ideas opuestas o conceptos inesperados, forzando al lector a detenerse y reconsiderar. "
            "El objetivo es captar la atención al confrontar ideas tradicionales."
        ),
    }

    # Ejemplos inspiradores para cada ángulo
    examples = {
        "Curiosidad": [
            "La bebida que probablemente estás tomando todos los días y que podría estar agotando tu energía.",
            "El error número 1 que el 90% de los freelancers comete sin saberlo.",
            "Las 3 preguntas que los reclutadores usan para decidir si contratarte o no (sin decirte).",
        ],
        "Casi Imposible": [
            "Cómo duplicar tus ingresos trabajando menos de 4 horas al día.",
            "La forma en que puedes aprender un nuevo idioma en menos de 30 días sin gastar un centavo.",
            "Cómo arreglar tu computadora en casa sin ningún conocimiento técnico.",
        ],
        "Autoridad y Credibilidad": [
            "El secreto que Steve Jobs usaba para convencer a millones (y cómo puedes aplicarlo hoy).",
            "Lo que Einstein recomendaba hacer cada mañana para resolver problemas más rápido.",
            "La técnica de respiración usada por los monjes tibetanos para reducir el estrés en 5 minutos.",
        ],
        "Contraste": [
            "El hábito 'saludable' que podría estar saboteando tu pérdida de peso.",
            "Por qué un simple cambio en tu rutina puede ahorrarte miles de dólares al año.",
            "El alimento 'sano' que podría ser peor que el azúcar para tu cuerpo.",
        ],
    }

    # Validar el ángulo seleccionado
    if angle not in angles_descriptions:
        raise ValueError(f"Ángulo no válido. Selecciona entre: {list(angles_descriptions.keys())}")

    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)

    # Crear la instrucción para el modelo
    angle_instruction = (
        f"Ángulo seleccionado: {angle}\n\n"
        f"Descripción: {angles_descriptions[angle]}\n\n"
        f"Inspírate en estos ejemplos:\n"
        + "\n".join(f"- {example}" for example in examples[angle])
    )

    # Crear configuración de generación para el modelo
    generation_config = {
        "temperature": temperature,  
        "top_p": 0.65,
        "top_k": 360,
        "max_output_tokens": 8196,
        "response_mime_type": "text/plain",
    }

    # Crear el prompt para el modelo
    prompt = (
        f"Genera {number_of_bullets} bullets en español diseñados para {target_audience} sobre {product}. "
        f"Cada bullet debe seguir el ángulo '{angle}' explicado a continuación:\n\n{angle_instruction}\n\n"
        f"Asegúrate de que cada bullet sea relevante, convincente, y conecte emocionalmente con la audiencia."
        f"Integrando esta instrucción: {mention_instruction}."
    )

    # Usar el modelo de generación
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are a world-class copywriter, with expertise in crafting bullets that connect emotionally."
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)

    # Regresar los bullets generados como texto
    return response.text

# Función para generar bullets
def generate_bullets(number_of_bullets, target_audience, product, temperature, selected_formula, selected_angle):
    # Usar la función generate_bullets_with_angles si se ha seleccionado un ángulo
    if selected_angle:
        return generate_bullets_with_angles(selected_angle, number_of_bullets, target_audience, product, temperature)

    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)

    # Crear la configuración del modelo
    generation_config = {
        "temperature": temperature,  
        "top_p": 0.65,
        "top_k": 360,
        "max_output_tokens": 8196,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are a world-class copywriter, with expertise in crafting bullets that connect emotionally."
    )

    # Crear un mensaje para el modelo
    bullets_instruction = (
        f"Tu tarea es crear {number_of_bullets} bullets diseñados para {target_audience}. "
        f"El objetivo es mostrar cómo {product} puede transformar la vida del lector, conectando de forma natural y emocional. "
        f"Usa la fórmula seleccionada: \n\n{selected_formula['description']}\n\n"
        f"Inspírate en estos ejemplos:\n"
        f"- {selected_formula['examples'][0]}\n"
        f"- {selected_formula['examples'][1]}\n"
        f"- {selected_formula['examples'][2]}\n\n"
        f"Integrando esta instrucción: {mention_instruction}."
    )

    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [bullets_instruction]},
        ]
    )

    response = chat_session.send_message("Genera los bullets")
    return response.text

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="Bullet Benefits Generator", layout="wide")

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Bullet Benefits Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma características en beneficios irresistibles.</h4>", unsafe_allow_html=True)

# Crear columnas
col1, col2 = st.columns([1, 2])

# Columnas de entrada
with col1:
    target_audience = st.text_input("¿Quién es tu público objetivo?", placeholder="Ejemplo: Estudiantes Universitarios")
    product = st.text_input("¿Qué producto tienes en mente?", placeholder="Ejemplo: Curso de Inglés")
    number_of_bullets = st.selectbox("Número de Bullets", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=4)

    # Crear acordeones
    with st.expander("Personaliza tus beneficios"):
        temperature = st.slider("Creatividad", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
        selected_formula_key = st.selectbox("Selecciona una fórmula", options=list(benefits_formulas.keys()))
        selected_formula = benefits_formulas[selected_formula_key]

    with st.expander("Selecciona un ángulo adicional"):
        selected_angle = st.selectbox("Selecciona un ángulo", options=["Ninguno"] + list(angles.keys()))  # Opción "Ninguno" añadida

    # Botón de enviar
    submit = st.button("Generar Bullets")

# Mostrar los bullets generados
if submit:
    if target_audience and product:
        try:
            # Si no se selecciona un ángulo, usar la función original
            if selected_angle == "Ninguno":
                generated_bullets = generate_bullets(
                    number_of_bullets, target_audience, product, temperature, selected_formula, ""  # Ángulo vacío para la función original
                )
            else:
                generated_bullets = generate_bullets_with_angles(
                    selected_angle, number_of_bullets, target_audience, product, temperature
                )
            col2.markdown(f"""
                <div style="padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
                    <h3>Bullets Generados:</h3>
                    <p>{generated_bullets}</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            col2.error(f"Error al generar bullets: {e}")
    else:
        col2.warning("Por favor, completa todos los campos antes de generar bullets.")
