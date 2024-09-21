import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv
from gradio import Markdown
import textwrap

# Cargar variables de entorno
load_dotenv()

# Configurar la API de Google Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def to_markdown(text):
    text = text.replace('•', '  *')  # Convertir los puntos en listas con asteriscos
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def generate_bullets(number_of_bullets, target_audience, product, temperature):
    # Crear la configuración del modelo
    generation_config = {
        "temperature": temperature,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Eres un copywriter de clase mundial, con experiencia en la creación de beneficios que conectan síntomas con problemas. Tu habilidad radica en comprender profundamente las emociones, deseos y desafíos de una audiencia específica, lo que te permite diseñar estrategias de marketing personalizadas que resuenan y motivan la acción. Sabes cómo utilizar estructuras probadas para atraer a tu audiencia objetivo, generando interés y logrando una conexión poderosa que impulsa los resultados deseados en campañas publicitarias y de contenido. Responde en español, en tipo lista numerada. Haz bullets inusuales, creativos y fascinantes que atrapen la atención de los lectores. No menciones el producto directamente en los beneficios o bullets. No expliques los benficios o bullets. Al responder escribe un encabezado que diga: 'Estos son tus bullets para convencer a {target_audience}'."
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Tu tarea es crear {number_of_bullets} beneficios o bullets que conecten el síntoma con el problema que tienen los {target_audience}, y que incrementen el deseo de adquirir el {product}"
                    "La idea es que los bullets sean de este tipo: "
                    "* Bien y mal: 'Botiquín del baño es el mejor lugar para guardar la medicina, ¿verdad? Incorrecto Es el peor. Los hechos están en la página 10.' "
                    "* El mejor/El Peor: 'El mejor tiempo verbal que existe para dar la sensación a tus clientes que ya te han comprado.' "
                    "* Historias: 'La historia del...', 'Los misterios de...', 'La leyenda de...' "
                    "* Truco: 'Un sistema tonto para escribir copy sin tratar de convencer de que me compren.' "
                    "* El de la verdad: 'La verdad que nunca te han dicho en el colegio, la escuela, ni en tu casa de cómo vivir de la música.' "
                    "* Haciendo una pregunta: '¿Sabías que...' "
                    "* Cuando: '¿Cuándo es buena idea decirle a una chica que te gusta? Si no lo dices justo en ese momento, despídete de que la conozcas íntimamente.' "
                ],
            },
        ]
    )

    response = chat_session.send_message("Genera los beneficios o bullets")  # Enviar mensaje para obtener la respuesta
    return to_markdown(response.text)  # Usar to_markdown para formatear la respuesta

# Configurar la interfaz de usuario con Gradio
iface = gr.Interface(
    fn=generate_bullets,
    inputs=[
        gr.Dropdown(choices=[str(i) for i in range(1, 11)], label="Número de Bullets", value="5"),
        gr.Textbox(label="Público Objetivo", placeholder="Ejemplo: Estudiantes Universitarios"),
        gr.Textbox(label="Producto", placeholder="Ejemplo: Curso de Inglés"),
        gr.Slider(minimum=0, maximum=1, value=0, step=0.1, label="Creatividad")
    ],
    outputs=gr.Markdown(label="Bullets Generados"),
    title="Generador de Bullets",
    description="Usa el poder de Gemini AI para crear bullets atractivos que conecten síntomas con problemas. Ajusta los parámetros para generar bullets que capturen la atención de tu audiencia."
)

# Lanza la interfaz
iface.launch()
