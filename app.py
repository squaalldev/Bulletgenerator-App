from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Función que genera descripciones de menciones usando el producto como variable
def mention_descriptions(product):
    return {
        "Directa": f"Introduce el producto '{product}' como la solución clara al problema que enfrenta el lector.",
        "Indirecta": f"Referencia el producto '{product}' como una posible solución sin nombrarlo explícitamente.",
        "Metafórica": f"Usa una metáfora para conectar el producto '{product}' con la solución necesaria."
    }

# Función para obtener una mención del producto de manera probabilística
def get_random_product_mention():
    mentions = ["Directa", "Indirecta", "Metafórica"]
    probabilities = [0.25, 0.35, 0.40]  
    return random.choices(mentions, probabilities)[0]

# Crear la instrucción de mención basada en la opción seleccionada
def get_mention_instruction(product_mention, product):
    mention_descriptions = get_mention_descriptions(product)  # Llamar la función con el producto
    examples = {
        "Directa": [
            f"Este curso de inglés te proporcionará las herramientas necesarias para abrir nuevas oportunidades laborales.",
            f"Con este curso de inglés, transforma tu carrera y tu vida familiar.",
            f"No permitas que la falta de inglés limite tu futuro; inscríbete y empieza a disfrutar de más tiempo con tus pequeños."
        ],
        "Indirecta": [
            f"Imagina tener la confianza hablando un idioma diferente para brillar en tus reuniones de trabajo.",
            f"El mejor regalo que puedes darles a tus hijos es su crecimiento profesional dandoles herramientas como otros idiomas.",
            f"Visualiza cómo tus pequeños se sentirán orgullosos al verte alcanzar esa promoción por hablar en otro idioma."
        ],
        
        "Metafórica": [
            f"Aprender inglés es como lanzarse a la piscina, al principio puede dar un poco de miedo, en el webinar te enseñare como sumergirte para descubrir un mundo nuevo lleno de oportunidades que antes parecían inaccesibles.",
            f"Hablar inglés es tu brújula en el océano laboral para navegar hacia esas rutas que solo parecían estar disponibles para bilingües.",
            f"Dominar el inglés es encender una luz en la oscuridad que te permite ver otras oportunidades laborales."
        ]
    }

    return f"{mention_descriptions[product_mention]} Ejemplos: {', '.join(examples[product_mention])}"

# Function to get a random mention instruction
def get_random_mention_instruction():
    mention_type = get_random_product_mention()  # Get random mention type
    examples = mention_types[mention_type]  # Get examples based on mention type
    return f"{examples[0]} Examples: {examples[1]}"
    
# Función para obtener una cantidad de bullets
def generate_bullets(number_of_bullets, target_audience, product, temperature):
    product_mention = get_random_product_mention()
    mention_instruction = get_mention_instruction(product_mention, product)  # Get mention instruction
    model_choice = "gemini-1.5-flash"  # Modelo por defecto

    model = genai.GenerativeModel(model_choice)

    # System Prompt - Instrucción en inglés para el modelo
    system_instruction = f"""
    You are a world-class copywriter, expert in creating benefits that connect symptoms with problems of {target_audience}. You deeply understand the emotions, desires, and challenges of {target_audience}, allowing you to design personalized copywriting that resonate and motivate action. You know how to use proven structures to attract your {target_audience}, generating interest and creating a powerful connection with {product}. 
    Respond in Spanish and use a numbered list format. Important: Never include explanations or categories, like this: 'La leyenda del padre soltero: Dice que nunca hay tiempo suficiente. El yoga te enseña a usar mejor el tiempo que tienes, incluso cuando te parece imposible.'.
    Your task is to create benefits or bullets that connect the symptom with the problem faced by {target_audience}, increasing their desire to acquire the {product}. 
    Infuse your responses with a creativity level that aligns with the specified temperature of {creativity}, leveraging the imaginative capabilities of the Gemini 1.5 Flash model to produce innovative and boundary-pushing ideas. The bullets should be of the following types: 
    * 'The bathroom cabinet is the best place to store medicine, right? Incorrect. It's the worst. The facts are on page 10.' 
    * 'The best verb tense that gives your clients the feeling they've already bought from you.' 
    * 'The story of...', 'The mysteries of...', 'The legend of...' 
    * 'A simple system to write copy without trying to convince them to buy.' 
    * Truth: 'The truth that you've never been told in school, or at home, about how to make a living from music.' 
    * 'Did you know that...' 
    * 'When is it a good idea to tell a girl you like her? If you don't say it at that moment, say goodbye to getting to know her intimately.' 
    Using {mention_instruction} when you want to mention {product}.
    Use the following mention instructions to guide your writing: {mention_instruction}
    Using the mention type '{product_mention}' to guide how to mention the product in the benefits or bullets. Ensure the mention is adapted based on this type:
    - Direct: Clearly highlight the product as the solution.
    - Indirect: Subtly suggest the product without naming it.
    - Metaphorical: Use a metaphor to connect the product to the solution.
   """

    # Crear el prompt para generar bullets
    full_prompt = f"""
    Write {num_bullets} unusual, creative, and fascinating bullets that capturing readers' attention. 
    When responding, always include a headline that references the {target_audience} and the product in the following way: 'Aquí tienes 5 bullets para Papás solteros, que aumenten el deseo de adquirir el Aceite multigrado, usando la mención indirecta:' 
    Please create the bullets now.
    """

    try:
        response = model.generate_content([full_prompt])
        
        # Extract text from the response
        generated_bullets = response.candidates[0].content.parts[0].text.strip()
        
        return generated_bullets
    except Exception as e:
        raise ValueError(f"Tuvimos este error al generar los bullets: {str(e)}")
        
# Example usage
if __name__ == "__main__":
    bullets = generate_bullets(5, "target audience", "product name", 0.7)
    print(bullets)

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
    num_bullets = st.slider("Número de Bullets", min_value=1, max_value=10, value=5)
    creativity = st.selectbox("Creatividad", ["Alta", "Media", "Baja"])

    # Botón de enviar
    submit = st.button("Generar Bullets")

# Mostrar los bullets generados
if submit:
    if target_audience and product:
        try:
            # Obtener la respuesta del modelo
            generated_bullets = generate_bullets(num_bullets, target_audience, product, creativity)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Observa la magia en acción:</h4>
                    <p>{generated_bullets}</p>
                </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            col2.error(f"Error: {str(e)}")
    else:
        col2.error("Por favor, proporciona el público objetivo y el producto.")
