from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Ejemplos de beneficios, dolores y datos curiosos
benefits = [
    "Mejora tu productividad diaria con técnicas efectivas.",
    "Descubre cómo simplificar tus tareas y ganar tiempo.",
    "Transforma tu carrera profesional con habilidades clave.",
    "Accede a recursos exclusivos que te ayudarán a destacar.",
    "Aprende a manejar tu tiempo para reducir el estrés."
]

pain_points = [
    "¿Te sientes abrumado por la falta de organización?",
    "¿Tus días se sienten interminables y sin propósito?",
    "¿Te gustaría aumentar tu enfoque y evitar distracciones?",
    "¿Te cuesta encontrar tiempo para lo que realmente importa?",
    "¿Sientes que tu carrera no avanza como esperabas?"
]

curiosities = [
    "¿Sabías que el 70% de las personas no logran sus objetivos anuales?",
    "Estudios muestran que la gestión del tiempo mejora la salud mental.",
    "El 80% de la productividad se logra en el 20% del tiempo.",
    "Las personas que establecen metas tienen un 10 veces más de probabilidad de tener éxito.",
    "Aprender a priorizar tareas puede aumentar tu eficacia en un 300%."
]

# Función para generar bullets informativos
def generate_bullets(target_audience, product, call_to_action, number_of_bullets):
    bullets = []
    
    for _ in range(number_of_bullets):
        category = random.choice(['benefit', 'pain_point', 'curiosity'])
        if category == 'benefit':
            bullet = random.choice(benefits)
        elif category == 'pain_point':
            bullet = random.choice(pain_points)
        else:
            bullet = random.choice(curiosities)
        bullets.append(bullet)
    
    return bullets

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="QuickPrompt", layout="wide")

# Agregar el manual en el sidebar con mejor diseño
st.sidebar.markdown("## **Manual de Usuario para Quick Prompt**")
st.sidebar.write("""
**Bienvenido a Quick Prompt**  
Quick Prompt está diseñado para ayudarte a crear bullets informativos que resalten los beneficios, dolores y curiosidades relevantes para tu audiencia.

### ¿Por qué los bullets son importantes?
Los bullets ayudan a presentar información clave de manera clara y concisa. Aquí te mostramos algunos ejemplos de información que puedes incluir:
- Beneficios de tu producto o servicio
- Problemas comunes que enfrenta tu audiencia
- Datos curiosos que capturan la atención

### ¿Cómo utilizar Quick Prompt?
Sigue estos pasos para sacar el máximo provecho de la herramienta:

1. **Define tu público objetivo**  
   Piensa en quiénes son y qué necesitan. Por ejemplo:
   - Estudiantes universitarios
   - Emprendedores
   - Profesionales en busca de desarrollo personal

2. **Especifica tu producto o servicio**  
   Asegúrate de que el producto esté claro y relacionado con los bullets. Ejemplos:
   - Herramientas de productividad
   - Cursos de marketing digital
   - Recursos de gestión del tiempo

3. **Determina la acción deseada**  
   Define cuál es la acción específica que deseas que realice tu audiencia:
   - Inscribirse en un curso
   - Descargar un recurso gratuito
   - Participar en un evento exclusivo

### Consejos adicionales:
- Asegúrate de que cada bullet sea claro y directo al punto.
- Utiliza datos y ejemplos concretos para hacer tus bullets más impactantes.
""")

# Footer del manual
st.sidebar.write("Con Quick Prompt, comunicarte con claridad y eficacia es más fácil que nunca.")

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Quick Prompt</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma tu mensaje en bullets informativos que resalten lo esencial para tu audiencia.</h4>", unsafe_allow_html=True)

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
    number_of_bullets = st.selectbox("Número de bullets informativos", options=[1, 2, 3, 4, 5], index=2)

    # Botón de enviar
    submit = st.button("Generar Bullets")

# Mostrar los bullets generados
if submit:
    if target_audience and product and call_to_action:
        try:
            # Obtener la respuesta del modelo
            generated_bullets = generate_bullets(target_audience, product, call_to_action, number_of_bullets)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Bullets Generados:</h4>
                    <ul>
                        {''.join(f'<li>{bullet}</li>' for bullet in generated_bullets)}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            col2.error(f"Error inesperado: {str(e)}")
    else:
        col2.warning("Por favor, completa todos los campos.")
