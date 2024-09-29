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
def generate_bullets(number_of_bullets):
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
Quick Prompt está diseñado para ayudarte a crear bullets informativos que resalten los beneficios, dolores y curiosidades para atraer a tu audiencia.

### ¿Por qué son importantes estos bullets?
Estos bullets son elementos clave para captar la atención de tu audiencia y motivarles a tomar acción. Aquí te mostramos ejemplos de cada categoría:
- **Beneficios**: Mejora tu productividad diaria con técnicas efectivas.
- **Puntos de Dolor**: ¿Te sientes abrumado por la falta de organización?
- **Datos Curiosos**: ¿Sabías que el 70% de las personas no logran sus objetivos anuales?

### ¿Cómo utilizar Quick Prompt?
Sigue estos pasos para obtener resultados efectivos:

1. **Define tu público objetivo**  
   Reflexiona sobre quiénes son y qué necesitan.

2. **Especifica el número de bullets que deseas generar**  
   Determina cuántos bullets necesitas para tu mensaje.

3. **Generar los bullets**  
   Haz clic en el botón para obtener los bullets informativos.
""")

# Footer del manual
st.sidebar.write("Transforma tu mensaje con bullets que conectan con tu audiencia.")

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Quick Prompt</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Genera bullets que cautiven y motiven a tu audiencia.</h4>", unsafe_allow_html=True)

# Crear columnas
col1, col2 = st.columns([1, 2])  

# Columnas de entrada
with col1:
    number_of_bullets = st.selectbox("Número de bullets informativos", options=[1, 2, 3, 4, 5], index=2)
    
    # Botón de enviar
    submit = st.button("Generar Bullets")

# Mostrar los bullets generados
if submit:
    try:
        # Obtener la respuesta del modelo
        generated_bullets = generate_bullets(number_of_bullets)
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
