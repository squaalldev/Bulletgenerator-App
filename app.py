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
    # Crear la configuración del modelo
    generation_config = {
        "temperature": temperature,  # Usar el valor del slider aquí
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="Eres un copywriter de clase mundial, con experiencia en la creación de ganchos, titulares y líneas de asunto que capturan la atención de inmediato. Tu habilidad radica en comprender profundamente las emociones, deseos y desafíos de una audiencia específica, lo que te permite diseñar estrategias de marketing personalizadas que resuenan y motivan la acción. Sabes cómo utilizar estructuras probadas para atraer a tu audiencia objetivo, generando interés y logrando una conexión poderosa que impulsa los resultados deseados en campañas publicitarias y de contenido. Responde en español, en tipo lista numerada. Haz ganchos inusuales que atrapen la atención. No menciones el producto directamente en el gancho. No expliques el gancho o encabezado. Al responder escribe un encabezado que diga: 'Estos son tus encabezados para enganchar a {target_audience}'."
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Tu tarea es crear {number_of_headlines} ganchos o encabezados titulares llamativos diseñados para {target_audience} con el fin de generar interés en {product}. "
                    "La idea es que los ganchos sean de este tipo: "
                    "1. Secretos: 'El secreto detrás de...'; "
                    "2. Consejos: 'Consejos para que...'; "
                    "3. Historias: 'La historia del...', 'Los misterios de...', 'La leyenda de...'; "
                    "4. Deseos: 'Cómo...'; "
                    "5. Listas: '10 razones por las que...'; "
                    "6. Haciendo una pregunta: '¿Sabías que...'; "
                    "7. Curiosidad: '¿Por qué...'."
                ],
            },
        ]
    )

    response = chat_session.send_message("Genera los titulares")  # Enviar mensaje para obtener la respuesta
    return to_markdown(response.text)  # Usar to_markdown para formatear la respuesta

# Configurar la interfaz de usuario con Gradio
iface = gr.Interface(
    fn=generate_headlines,
    inputs=[
        gr.Dropdown(choices=[str(i) for i in range(1, 11)], label="Número de Titulares", value="5"),
        gr.Textbox(label="Público Objetivo", placeholder="Ejemplo: Estudiantes Universitarios"),
        gr.Textbox(label="Producto", placeholder="Ejemplo: Curso de Inglés"),
        gr.Slider(minimum=0, maximum=1, value=0, step=0.1, label="Creatividad")
    ],
    outputs=gr.Markdown(label="Titulares Generados"),  # Eliminado el placeholder
    title="Generador de Titulares",
    description="Usa el poder de Gemini AI para crear titulares atractivos. Ajusta los parámetros para generar titulares que capturen la atención de tu audiencia."
)

# Lanza la interfaz
iface.launch()
