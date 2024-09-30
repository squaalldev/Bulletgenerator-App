from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import langchain

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Generar el resultado utilizando el modelo con la instrucción de bullets específica
def generate_bullets(number_of_bullets, target_audience, product, call_to_action, temperature):
    # Configuración del modelo
    generation_config = {
        "temperature": temperature,
        "top_p": 0.85,
        "top_k": 128,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    # Crear la instrucción del sistema
    system_instruction = (
        f"Eres un experto copywriter especializado en escribir bullets atractivos, curiosos e inusuales para {target_audience} sobre {product} que promueven la acción de {call_to_action}. "
        f"Tu tarea es ayudarme a escribir {number_of_bullets} bullets que destaquen los beneficios de {product}. "
        f"Utiliza las siguientes menciones y ejemplos como inspiración en tu respuesta: "
        "El armario del baño es el mejor lugar para guardar medicamentos, ¿verdad? Incorrecto. Es el peor. Los hechos están en la página 10.",
        "El mejor tiempo verbal que le da a tus clientes la sensación de que ya te han comprado.",
        "La historia de un joven emprendedor que transformó su vida aplicando esta técnica simple pero poderosa.",
        "Los misterios de cómo algunas personas parecen tener éxito sin esfuerzo, mientras otras luchan. La clave está en esta pequeña diferencia.",
        "La leyenda de aquellos que dominaron la productividad con un solo hábito. ¿Te atreves a descubrirlo?",
        "La historia de un padre ocupado que, con solo 10 minutos al día, logró transformar su salud y bienestar.",
        "¿Cuándo es una buena idea decirle a una chica que te gusta? Si no se lo dices en ese momento, despídete de conocerla íntimamente."
        f"Cuando respondas, utiliza la mayor cantidad de variaciones."
    )

    # Configuración del modelo generativo
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Generar el resultado utilizando el modelo
    try:
        response = model.generate_content([system_instruction])
        
        # Verificar que la respuesta tenga el formato esperado
        if response.candidates and response.candidates[0].content.parts:
            generated_bullets = response.candidates[0].content.parts[0].text.strip()
            return generated_bullets
        else:
            raise ValueError("No se generaron bullets válidos.")
    except Exception as e:
        raise ValueError(f"Error al generar los bullets: {str(e)}")

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="Impact Bullet Generator", layout="wide")

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
    number_of_bullets = st.selectbox("Número de bullets", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], value=5)
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
