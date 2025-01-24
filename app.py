from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función para generar los beneficios (bullets) basados en el enfoque
def generate_benefits(focus_points, product, target_audience, creativity, num_bullets):
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Instrucción del sistema para el modelo
    system_instruction = (
        "You are a world-class copywriter, with expertise in crafting hooks, headlines, and subject lines that immediately "
        "capture the reader's attention, prompting them to open the email or continue reading. Your skill lies in deeply understanding "
        "the emotions, desires, and challenges of a specific audience. You are also an expert in creating benefits that connect symptoms "
        "with problems, allowing you to design personalized strategies that resonate and motivate action. You know how to use proven "
        "structures to attract your target audience, generating interest and creating a powerful connection. Your task is to generate "
        "unusual, creative, and fascinating subject lines or headlines that spark curiosity and encourage the reader to engage further. "
        "Respond in Spanish and use a numbered list format. Important: Only answer with subject lines, never include explanations or categories."
    )

    # Base del prompt para generar los bullets persuasivos
    prompt_base = f"""
    Eres un experto en copywriting y tu objetivo es crear {num_bullets} bullets persuasivos que conecten emocionalmente con la audiencia {target_audience}. 
    Cada bullet debe abordar sus problemas, deseos o situaciones, mostrando cómo se pueden mejorar o solucionar gracias a una solución específica. 
    Piensa en cómo puedes captar la atención de la audiencia con frases impactantes, como si estuvieras hablando directamente con ellos. La idea es resaltar el valor que aporta la solución, sin hacer que el producto suene como una venta forzada. 
    Los bullets deben ser claros, directos y generar curiosidad, invitando a la acción de manera natural. Evita la jerga técnica y mantén la simplicidad, enfocándote en cómo el producto se integra de manera natural en la vida de la audiencia para mejorarla.
    Crea {num_bullets} bullets persuasivos que muestren cómo el producto puede resolver o transformar una situación para la audiencia. 
    Hazlo con un enfoque genuino, sin forzar la mención del producto, pero asegurándote de que quede claro cómo puede ser la solución ideal.
    Usa enfoques creativos para conectar los beneficios del producto con lo que realmente le importa a la audiencia. 
    Ahora, crea una lista de {num_bullets} bullets persuasivos para el siguiente producto y nicho objetivo.\n\n
    Producto: {product}\n
    Nicho objetivo: {target_audience}\n
    """

    benefits = []
    # Crear el prompt específico para cada enfoque y enviarlo al modelo
    for point in focus_points[:num_bullets]:  # Limitar a los bullets indicados por el usuario
        # Crear el prompt para el enfoque seleccionado
        specific_prompt = prompt_base + f"\n\nEnfoque: {point}\n"

        # Configurar el modelo con parámetros de generación
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": creativity,  # Usar la creatividad para definir la temperatura
                "top_p": 0.65,  # Probabilidad de tokens para mayor diversidad
                "top_k": 280,  # Número de tokens que se consideran en cada paso
                "max_output_tokens": 2048,  # Limitar a 50 tokens para que el bullet sea corto
                "response_mime_type": "text/plain",  # Respuesta en texto plano
            },
            system_instruction=system_instruction
        )

        # Generar los beneficios con la API de Google
        response = model.generate_content([specific_prompt])

        if response and response.parts:
            bullet = response.parts[0].text.strip()
            benefits.append(bullet)
        else:
            benefits.append("Lo siento, no se pudieron generar los beneficios para este enfoque.")

    return benefits

# Configuración de Streamlit
st.set_page_config(page_title="Quick Prompt", layout="wide")

# Leer el contenido del archivo manual.md
with open("manual.md", "r", encoding="utf-8") as file:
    manual_content = file.read()

# Mostrar el contenido del manual en el sidebar
st.sidebar.markdown(manual_content)

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Impact Bullet Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma los pensamientos de tu audiencia en beneficios persuasivos que inspiren a la acción.</h4>", unsafe_allow_html=True)

# Crear columnas
col1, col2 = st.columns([1, 2])

# Columnas de entrada
with col1:
    target_audience = st.text_input("Público objetivo:", placeholder="Ejemplo: Estudiantes universitarios")
    product = st.text_input("Producto relacionado:", placeholder="Ejemplo: Curso de productividad")
    
    # Slider para la creatividad
    creativity = st.slider("Creatividad (Temperatura)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    
    # Slider para el número de bullets
    num_bullets = st.slider("Número de Bullets", min_value=1, max_value=10, value=5, step=1)
    
    focus_points = st.multiselect(
        "Selecciona los enfoques que deseas utilizar:",
        ["Curiosidad", "CASI Imposible", "Autoridad y Credibilidad", "Contraste"],
        default=[]
    )

    submit = st.button("Generar Beneficios")

# Mostrar los beneficios generados
if submit:
    if focus_points and product and target_audience:
        benefits = generate_benefits(focus_points, product, target_audience, creativity, num_bullets)
        formatted_benefits = '<br style="line-height: 2;">'.join(benefits)
        
        col2.markdown(f"""
            <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                <h4>Mira los beneficios generados:</h4>
                <p style="line-height: 2;">{formatted_benefits}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        col2.error("Por favor, proporciona al menos un enfoque, un producto y un público objetivo para generar beneficios.")
