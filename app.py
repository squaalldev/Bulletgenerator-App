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

# Ejemplos de llamados a la acción por tipo
cta_types = {
    "directos": [
        "Descargar la guía para mejorar mi productividad diaria.",
        "Suscribirme para recibir actualizaciones y promociones exclusivas.",
        "Unirme a la prueba gratis de 14 días y descubrir nuevas funciones.",
        "Registrarme para acceder a contenido premium y estrategias efectivas.",
        "Comprar ahora y obtener un regalo especial con mi pedido."
    ],
    "urgencia": [
        "Inscribirme ahora para asegurar mi lugar antes de que se agoten las plazas.",
        "Comenzar mi transformación hoy y no perder más tiempo."
    ],
    "descuento": [
        "Aprovechar el 50% de descuento y comprar por tiempo limitado.",
        "Hacer mi pedido ahora y obtener un 30% de descuento adicional."
    ],
    "exclusividad": [
        "Acceder a contenido exclusivo solo para miembros.",
        "Ser parte de un grupo selecto y disfrutar de beneficios únicos."
    ],
    "beneficio_claro": [
        "Mejorar mi productividad en solo una semana.",
        "Transformar mi carrera profesional con herramientas avanzadas."
    ],
    "personalización": [
        "Descubrir cómo personalizar esta oferta para mis necesidades.",
        "Elegir las opciones que mejor se adapten a mis necesidades."
    ]
}

# Función para que el modelo elija automáticamente el tipo de CTA y el CTA específico
def get_random_cta():
    cta_type = random.choice(list(cta_types.keys()))  # Selección aleatoria del tipo de CTA
    cta = random.choice(cta_types[cta_type])  # Selección aleatoria del CTA dentro del tipo
    return cta

# Función para generar llamados a la acción
def generate_ctas(number_of_ctas, target_audience, product, call_to_action, temperature):
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
        model_name="gemini-1.5-flash",  # Nombre del modelo que estamos utilizando
        generation_config=generation_config,  # Configuración de generación
        system_instruction=(
            f"Eres un experto copywriter especializado en escribir mensajes o textos que atraen la atención de {target_audience} para promover {product} que soluciona los problemas de {target_audience}. "
            "Tu tarea es ayudarme a escribir llamados a la acción (CTA) para mi [página web, landing, correo],"
            f"teniendo en cuenta los puntos dolorosos de mi {target_audience} y el {product} y la {call_to_action} a realizar."
            "Recuerda que un buen CTA debe tener:\n\n"
            "1. **Acción**: Palabras que invitan a realizar un movimiento (e.g., 'Descargar', 'Suscribirse').\n"
            "2. **Valor**: Explicar el beneficio que el usuario obtendrá al realizar la acción.\n\n"
            "Asegúrate de que cada llamado a la acción siga la estructura de 'Acción + conector + Valor', y evita incluir explicaciones como 'Acción: Descubrir' o 'Valor: Un oasis de paz en medio del caos'.\n"
            "Important: Only answer CTAs, never include explanations or categories, like this: 'Registrarme ahora y descubrir cómo encontrar un poco de paz en medio del caos. (Este CTA apela al deseo de Han Solo de encontrar un momento de tranquilidad en su vida agitada.).'\n"
            "Los llamados de acción deben de ser cortos y concisos, basate en estos ejemplos para realizar tu tarea de crear los CTA's:\n\n"
            "**Ejemplos de CTAs en Voz Activa en Primera Persona:**\n"
            "- 'Descargar la guía para mejorar mi productividad diaria'\n"
            "- 'Suscribirme para recibir actualizaciones y promociones exclusivas'\n"
            "- 'Unirme a la prueba gratis de 14 días y descubrir nuevas funciones'\n"
            "Usa estos lineamientos para generar CTAs de alta conversión en español."
        )
    )

    # Selección aleatoria de tipos de CTA, manteniendo variedad en la salida
    selected_types = random.sample(list(cta_types.keys()), min(number_of_ctas, len(cta_types)))

    # Crear un mensaje para el modelo que incluye los CTAs generados según los tipos seleccionados
    ctas_instruction = (
        f"Tu tarea es crear {number_of_ctas} llamados a la acción efectivos dirigidos a {target_audience}, "
        f"para promover {call_to_action} usa la siguiente mención: {mention_instruction}. "
        "Asegúrate de que cada llamado a la acción siga la estructura de 'Acción + conector + Valor', "
        "como los ejemplos proporcionados anteriormente."
    )

    # Generar el resultado utilizando el modelo con la instrucción de CTA específica
    try:
        response = model.generate_content([ctas_instruction])
        
        # Extraer el texto de la respuesta
        generated_ctas = response.candidates[0].content.parts[0].text.strip()  # Modificado aquí
        
        # Retornar el resultado
        return generated_ctas
    except Exception as e:
        raise ValueError(f"Error al generar los CTA: {str(e)}")

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="QuickPrompt", layout="wide")

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Quick Prompt</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma tu mensaje en llamados de acción que inspiren a tu audiencia a tomar decisiones al instante.</h4>", unsafe_allow_html=True)

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
    number_of_ctas = st.selectbox("Número de llamados a la acción", options=[1, 2, 3, 4, 5], index=2)
    temperature = st.slider("Creatividad", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    # Botón de enviar
    submit = st.button("Generar Llamados a la Acción")

# Mostrar los llamados a la acción generados
if submit:
    if target_audience and product and call_to_action:
        try:
            # Obtener la respuesta del modelo
            generated_ctas = generate_ctas(number_of_ctas, target_audience, product, call_to_action, temperature)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Mira los llamados a la acción generados:</h4>
                    <p style="font-size: 22px;">{generated_ctas}</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al generar los llamados a la acción: {str(e)}")
    else:
        st.error("Por favor, completa todos los campos.") 
