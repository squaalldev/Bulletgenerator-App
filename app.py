from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

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

    # Configuración del modelo generativo
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Definición de system_instruction fuera de la configuración del modelo
    system_instruction = (
        f"Eres un experto copywriter especializado en escribir mensajes o textos que atraen la atención de {target_audience} para promover {product} que soluciona los problemas de {target_audience}. "
        f"Tu tarea es ayudarme a escribir {number_of_bullets} bullets que destaquen los beneficios de {product}, los cuales utilizare para mi [página web, landing, correo], "
        f"teniendo en cuenta los puntos dolorosos de mi {target_audience} y el {product} y la {call_to_action} a realizar."
        "Recuerda que un buen bullet debe tener:\n\n"
        f"El efecto tiene que ser de atracción, de fascinar, de dejar con la curiosidad. Es más, se dice que los bullets (o balas) tienen que ser como una herida, cuya única cura sea {call_to_action}."
        "Haz bullets inusuales, creativos y fascinantes que atrapen la atención que conecten el síntoma de la {target_audience} con el beneficio que van a obtener con {call_to_action}. "
        "Los bullets deben de ser conversacionales, basate en estos ejemplos para realizar tu tarea de crear los bullets:"
        "* Bien y mal: 'Botiquín del baño es el mejor lugar para guardar la medicina, ¿verdad? Incorrecto Es el peor. Los hecho estan en la página 10.'"
        "* El mejor/El Peor: 'El mejor tiempo verbal que existe para dar la sensación a tus clientes que ya te han comprado.'"
        "* Historias: 'La historia del...', 'Los misterios de...', 'La leyenda de...'"
        "* Truco: 'Un sistema tonto para escribir copy sin tratar de convencer de que me compren' [Aquí se refiere al Mecanismo Único a utilizar].'"
        "* El de la verdad: 'La verdad que nunca te han dicho en el colegio, la escuela, ni en tu casa de como vivir de la música'"
        "* Haciendo una pregunta: '¿Sabías que?'"
        "* Cuando: '¿Cuándo es buena idea decirle a una chica que te gusta? Si no lo dices justo en ese momento, despídete de que la conozcas íntimamente.'"
        "Important: Only answer bullets, never include explanations or categories, like this: 'Registrarme ahora y descubrir cómo encontrar un poco de paz en medio del caos. (Este CTA apela al deseo de Han Solo de encontrar un momento de tranquilidad en su vida agitada.).'"
        "Usa estos lineamientos para generar bullets en español."
    )    

    # Generar el resultado utilizando el modelo
    try:
        response = model.generate_content([system_instruction])
        
        # Verificar que la respuesta tenga el formato esperado
        if isinstance(response, tuple) and len(response) > 0:
            generated_bullets = response[0].text.strip()
            return generated_bullets
        else:
            raise ValueError("Respuesta inesperada del modelo.")

    except Exception as e:
        st.error(f"Error al generar los bullets: {str(e)}")
        raise

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
    number_of_bullets = st.selectbox("Número de bullets", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=4)
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
