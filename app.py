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

def generate_headlines(number_of_headlines, target_audience, product, temperature):
    try:
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
            system_instruction="Eres un copywriter de clase mundial..."
        )

        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        f"Tu tarea es crear {number_of_headlines} ganchos o encabezados titulares llamativos..."
                    ],
                },
            ]
        )

        response = chat_session.send_message("Genera los titulares")
        return to_markdown(response.text)

    except Exception as e:
        return f"Error al generar los titulares: {str(e)}"

# Configurar la interfaz de usuario con Gradio
iface = gr.Interface(
    fn=generate_headlines,
    inputs=[
        gr.Dropdown(choices=[str(i) for i in range(1, 11)], label="Número de Titulares", value="5"),
        gr.Textbox(label="Público Objetivo", placeholder="Ejemplo: Estudiantes Universitarios"),
        gr.Textbox(label="Producto", placeholder="Ejemplo: Curso de Inglés"),
        gr.Slider(minimum=0, maximum=1, value=0, step=0.1, label="Creatividad")
    ],
    outputs=gr.Markdown(label="Titulares Generados"),
    title="Generador de Titulares",
    description="Usa el poder de Gemini AI para crear titulares atractivos. Ajusta los parámetros para generar titulares que capturen la atención de tu audiencia."
)

# Lanza la interfaz
iface.launch()
