from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función para obtener una cantidad de bullets
def get_gemini_response_bullets(target_audience, product, num_bullets, temperature):

    # Configuración del modelo generativo y las instrucciones del sistema
    generation_config = {
        "temperature": temperature,
        "top_p": 0.9,  # Aumentar para permitir una mayor diversidad en las opciones generadas
        "top_k": 90,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",  # Nombre del modelo que estamos utilizando
        generation_config=generation_config,  # Configuración de generación
        system_instruction=(
            f"Imagina que estás charlando con un amigo que está buscando {product}. "
            "Tu tarea es ayudarme a escribir bullets orientados a beneficios de obtener, descargar, asistir o comprar {product}, los cuales utilizaré para mi [página web, landing, correo, post, etc.],"
            f"teniendo en cuenta los puntos dolorosos de mi {target_audience} y el {product}."
            f"Genera {num_bullets} bullets que suenen naturales y amigables, como si estuvieras contándole por qué debería interesarse. "
            f"Entiendes perfectamente sus emociones y desafíos. Crea bullets que no solo informen, sino que hablen directamente al corazón de {target_audience}, "
            f"Generando curiosidad y ganas de saber más sobre {product}. "
            f"¡Haz que se sientan incluidos! Usa un tono amistoso y divertido. "
            f"Por ejemplo, si están buscando {product}, dales un motivo irresistible para seguir leyendo. "
            f"Incluye un encabezado atractivo que diga: 'Aquí tienes {num_bullets} razones por las que {target_audience} debería considerar {product}'."
        )
    )

    bullets_instruction = (
        f"Quiero que escribas {num_bullets} bullets que transmitan los beneficios de {product} de una manera que atraiga a {target_audience}. "
        f"Conecta los problemas y deseos de {target_audience} de forma conversacional, no robótico, ni utilices ':', con un estilo amigable y divertido. "
        f"Por favor, genera bullets creativos que hagan que {target_audience} se sienta emocionado por {product}."
    )

    # Generar el resultado utilizando el modelo con la instrucción específica
    try:
        response = model.generate_content([bullets_instruction])
        
        # Extraer el texto de la respuesta
        generated_bullets = response.candidates[0].content.parts[0].text.strip()
        
        # Retornar el resultado
        return generated_bullets
    except Exception as e:
        raise ValueError(f"Error al generar los bullets: {str(e)}")

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
