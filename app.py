from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Cargar las variables de entorno
load_dotenv()

# Configurar la API de Google
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Fórmulas con ejemplos y explicaciones
benefits_formulas = {
    "GPS": {
        "description": """
            Crea bullets de beneficios que respondan estas tres preguntas clave:
            1. ¿Qué es lo que el lector quiere conseguir?
            2. ¿En qué periodo de tiempo quiere conseguirlo?
            3. ¿Cuál es la objeción principal del lector que le impide lograrlo?
        """,
        "examples": [
            "Obtén tus primeros 100 clientes en 30 días, sin gastar un solo centavo en publicidad.",
            "Pierde esos 5 kilos en solo 10 minutos al día, sin dejar de disfrutar tus comidas favoritas.",
            "Ahorra para salir de viaje en tres meses, sin sacrificar esas noches de cine."
        ]
    },
    "Númerica Suprema": {
    "description": """
        La Fórmula Suprema de Istvanova combina 5 elementos clave más artículos plurales para crear bullets persuasivos:

        1. **Artículos Plurales** (Art):
           - Los (para masculino plural)
           - Las (para femenino plural)
           - Dan naturalidad y autoridad al texto
           - Ejemplos: "Los 7 métodos...", "Las 3 técnicas..."

        2. **Números** (N):
           - Específicos y creíbles (3, 5, 7, 10...)
           - Crean estructura y expectativas claras
           - Se combinan con artículos: "Los 5...", "Las 3..."

        3. **Adjetivo** (A):
           - Emocionales y descriptivos
           - Conectan con deseos/miedos
           - Ejemplos: poderosos, simples, efectivos, revolucionarios

        4. **Palabra Clave** (P):
           - Término central del beneficio en plural
           - Fácil de entender y recordar
           - Ejemplos: métodos, estrategias, técnicas, secretos

        5. **Razón** (R):
           - Justifica el beneficio
           - Añade credibilidad
           - Conecta con la motivación del lector

        6. **Promesa** (P):
           - Resultado específico y medible
           - Timeframe realista
           - Beneficio final atractivo

        Formatos:
        - Corto: Art plural + N + A + P + P
        - Medio: Art plural + N + A + P + R + P
        - Largo: Art plural + N + A + P + R detallada + P específica
    """,
    "examples": [
        "Los 3 rituales probados para dormir mejor.",
        "Las 5 rutinas efectivas para fortalecer tu core.",
        "Los 7 hábitos esenciales para aumentar productividad.",
        "Las 3 técnicas comprobadas para dormir mejor basadas en neurociencia.",
        "Los 5 movimientos efectivos para fortalecer tu core sin equipamiento.",
        "Las 7 estrategias esenciales para aumentar productividad sin estrés.",
        "Los 3 métodos científicos para dormir mejor basados en los últimos descubrimientos de la neurociencia del sueño que transformarán tus noches.",
        "Las 5 secuencias efectivas para fortalecer tu core descubiertas por fisioterapeutas olímpicos que puedes hacer en casa.",
        "Los 7 sistemas revolucionarios para aumentar productividad desarrollados por CEOs que duplicarán tus resultados."
    ],
    "variaciones_estructura": {
        "básica": "Art plural + N + A + P + P",
        "intermedia": "Art plural + N + A + P + R + P",
        "avanzada": "Art plural + N + A + P + R detallada + P específica"
    },
    "uso_articulos_plurales": {
        "masculino_plural": {
            "artículo": "los",
            "ejemplos_palabras": "métodos, sistemas, pasos, secretos, trucos, hábitos"
        },
        "femenino_plural": {
            "artículo": "las",
            "ejemplos_palabras": "técnicas, estrategias, rutinas, tácticas, claves"
        }
    },
    "consejos_uso": [
        "Usa siempre la forma plural para mayor impacto",
        "Alterna entre 'los' y 'las' según la palabra clave",
        "Mantén coherencia en el género a lo largo del bullet",
        "Combina artículos con números de forma natural",
        "Asegura que la palabra clave esté en plural"
    ]
},
    "AIDA": {
    "description": """
        La fórmula AIDA se aplica de manera flexible y estratégica, combinando 1-4 elementos para crear bullets impactantes y naturales:

        1. **Atención** (A):
           Ganchos de apertura poderosos:
           - "¿Sabías que...?" + dato sorprendente
           - Mini-historia disruptiva
           - Idea contraintuitiva
           - Descubrimiento inesperado
           - Analogía poderosa
           - "La mayoría no sabe que..."
           - "Contrario a lo que piensas..."
           - "Me sorprendió descubrir que..."

        2. **Interés** (I):
           Desarrollo del gancho inicial:
           - Detalles específicos y relevantes
           - Conexión problema-solución inesperada
           - Beneficios únicos y memorables
           - Puente situación actual-resultado
           - "La razón es simple..."
           - "Lo fascinante es que..."
           - "Y lo mejor de todo..."
           - "Lo que hace la diferencia es..."

        3. **Deseo** (D):
           Amplificación emocional:
           - Imagen vivida del resultado
           - Experiencia personalizada
           - Prueba social natural
           - Toque de exclusividad
           - Conexión emocional profunda
           - "Imagina poder..."
           - "Piensa cómo sería..."
           - "Esto significa que podrás..."

        4. **Acción** (A):
           Cierre natural:
           - Siguiente paso simple
           - Baja fricción para comenzar
           - Gratificación inmediata
           - Primer paso sencillo
           - Seguridad fluida
           - "Pruébalo hoy mismo..."
           - "Comienza con un simple..."
           - "Solo necesitas..."

        Combinaciones estratégicas:
        - A + I: Para despertar curiosidad y explicar el valor
        - A + D: Para conectar problema con deseo
        - I + D: Para construir deseo desde la lógica
        - I + D + A: Para construir convicción y motivar
        - A + I + D: Para educar, intrigar y crear anhelo

        Cada bullet debe mantener un tono conversacional y evitar parecer una fórmula obvia.
    """,
    "examples": [
        "• Un estudio con deportistas de élite reveló algo sorprendente los atletas que menos entrenaban tenían mejores resultados. La clave está en un ritual de recuperación de 8 minutos que ahora puedes usar en casa.", # A (dato sorprendente) + I (conexión problema-solución)

        "• Mi cliente más exitoso solía dormir solo 4 horas por noche. Ahora duerme 8 y factura el doble, todo gracias a una rutina matutina que cambió su forma de trabajar.", # A (mini-historia) + I (beneficio único) + D (prueba social)

        "• Como el bambú chino, que parece no crecer durante años y de repente se dispara hacia arriba, tu negocio está a punto de experimentar ese momento de explosión.", # A (analogía poderosa) + D (imagen vivida)

        "• La técnica que transformó mi productividad apareció en el lugar más inesperado una clase de cocina italiana. Descubre cómo este método tan simple puede revolucionar tu forma de trabajar.", # A (descubrimiento inesperado) + I (beneficio único)

        "• Los expertos en productividad estaban equivocados. Las mañanas no son el momento más importante del día. Descubre cuándo ocurre realmente la magia y aprovecha ese momento desde hoy.", # A (contraintuitivo) + I (detalle específico) + A (siguiente paso)

        "• Imagina despertar cada mañana con tu bandeja de entrada vacía y tus tareas importantes ya organizadas. Este pequeño truco de 5 minutos lo hace posible.", # D (imagen vivida) + I (beneficio) + A (simplicidad)
    ]
},
    "3 en 1": {
        "description": """
            La fórmula 3 en 1 para empezar a conectar con las personas combina:
            1. **Característica**: Describe las propiedades tangibles del producto o servicio. Por ejemplo, "Este software tiene una función de automatización única".
            2. **Para qué**: El beneficio inmediato que resuelve un problema o cumple una necesidad. Por ejemplo, "Para que puedas enfocarte en tareas más importantes sin distracciones".
            3. **Con lo que**: El impacto emocional o práctico a largo plazo que obtiene el cliente. Por ejemplo, "Con lo que podrás disfrutar de un día más productivo y menos estresante".
            Crea bullets points que integren estos elementos para mostrar beneficios de forma clara, emocional y conectada al producto.
        """,
        "examples": [
            "Una batería de larga duración para que puedas trabajar todo el día con lo que mantienes tu productividad sin interrupciones.",
            "Un sistema de seguridad avanzado para que duermas tranquilo con lo que proteges lo que más valoras.",
            "Un diseño intuitivo para que aprendas rápido con lo que ahorras tiempo y esfuerzos innecesarios."
        ]
    }
}

# Función para generar bullets de beneficios
def generate_benefits(number_of_benefits, target_audience, product, temperature, selected_formula):

    # Crear la configuración del modelo
    generation_config = {
        "temperature": temperature,  
        "top_p": 0.65,        # Considerar un poco menos de palabras probables
        "top_k": 360,        # Aumentar las palabras candidatas para más variedad
        "max_output_tokens": 8196,  # Mantenerlo igual, pero puedes aumentar si deseas más detalle
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
)

# Incluir las instrucciones del sistema en el prompt principal
    system_prompt = """Eres un copywriter experto de clase mundial, con experiencia en crear beneficios que conectan emocionalmente y abordan los deseos, problemas y motivaciones de la audiencia objetivo.

OBJETIVO:
- Generar bullets de beneficios convincentes y específicos en español
- Conectar emocionalmente con la audiencia
- Abordar deseos, problemas y motivaciones reales
- Mantener un lenguaje natural y conversacional
- Orientar cada beneficio a la acción

REGLAS DE FORMATO:
- Cada beneficio debe comenzar con "• "
- Un beneficio por línea
- Sin números al inicio
- Sin explicaciones ni categorías
- Añadir un salto de línea entre cada beneficio
- Nunca incluir símbolos : en los bullets
- Cada beneficio debe ser una frase completa y concisa

ESTRUCTURA DE CADA BENEFICIO:
- Debe ser relevante para la audiencia objetivo
- Debe mostrar un resultado específico
- Debe incluir un elemento emocional
- Debe eliminar una objeción o dolor
- Debe inspirar acción inmediata

EJEMPLO DE FORMATO:
• Transforma tu negocio con estrategias probadas que duplican tus ingresos en 90 días, sin sacrificar tu tiempo en familia.

• Domina las técnicas más efectivas para conquistar tu mercado, mientras mantienes el equilibrio entre trabajo y vida personal.

• Implementa sistemas automatizados que hacen crecer tu empresa incluso mientras duermes, eliminando la necesidad de trabajar más horas.

IMPORTANTE:
- Cada beneficio debe ser único y específico
- Evitar repeticiones y generalidades
- Mantener un tono persuasivo pero honesto
- Adaptar el lenguaje al nivel de comprensión de la audiencia
- Enfocarse en resultados tangibles y medibles"""
    
    # Crear un mensaje para el modelo, destacando la audiencia, el producto, la fórmula seleccionada y los ejemplos
    benefits_instruction = (
        f"{system_prompt}\n\n"
        f"Tu tarea es crear {number_of_benefits} beneficios irresistibles diseñados para {target_audience}. "
        f"El objetivo es mostrar cómo {product} puede transformar la vida del lector, conectando de forma natural y emocional. "
        f"Evita usar menciones literales o repetitivas, y destaca soluciones concretas, mostrando cómo el producto elimina obstáculos o satisface deseos reales. "
        f"Usa la fórmula seleccionada como guía:\n\n{selected_formula['description']}\n\n"
        f"Inspírate en estos ejemplos:\n"
        f"- {selected_formula['examples'][0]}\n"
        f"- {selected_formula['examples'][1]}\n"
        f"- {selected_formula['examples'][2]}\n\n"
        f"Tu objetivo es inspirar deseo y acción, evitando explicaciones o categorías en la respuesta."
    )

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [benefits_instruction],
            },
        ]
    )

    response = chat_session.send_message("Genera los beneficios")  # Enviar mensaje para obtener la respuesta
    return response.text  # Regresar la respuesta directamente

# Configurar la interfaz de usuario con Streamlit
st.set_page_config(page_title="Bullet Benefits Generator", layout="wide")

# Leer el contenido del archivo manual.md
with open("manual.md", "r", encoding="utf-8") as file:
    manual_content = file.read()

# Mostrar el contenido del manual en el sidebar
st.sidebar.markdown(manual_content)

# Ocultar elementos de la interfaz
st.markdown("""
    <style>
        /* Ocultar menú hamburguesa */
        #MainMenu {visibility: visible;}

        /* Ocultar botón de Fork, GitHub y menú de tres puntos */
        .stDeployButton {display: none;}
        [data-testid="stToolbar"] {display: none;}
        .css-14xtw13 {display: visible;}
        .css-pkbazv {display: visible;}

        /* Ocultar footer */
        footer {visibility: hidden;}

        /* Ocultar header */
        header {visibility: visible;}

        /* Ocultar marca de agua de Streamlit */
        #stStreamlitFooterContainer {visibility: hidden;}

        /* Ocultar íconos inferiores */
        .viewerBadge_link__1S137 {display: none;}
        .viewerBadge_container__1QSob {display: none;}

        /* Reducir espacio superior */
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }

        /* Ajustar espaciado del título */
        h1 {
            margin-top: -2rem;
            padding-top: 2.5rem;
        }

        /* Ajustar espaciado del subtítulo */
        h4 {
            margin-top: 0.5rem;
            padding-top: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# Centrar el título y el subtítulo
st.markdown("<h1 style='text-align: center;'>Bullet Benefits Generator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Transforma características en beneficios irresistibles que conectan emocionalmente con tu audiencia.</h4>", unsafe_allow_html=True)

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
    number_of_benefits = st.selectbox("Número de Beneficios", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=4)

    # Crear un único acordeón para fórmula y creatividad
    with st.expander("Personaliza tus beneficios"):
        temperature = st.slider("Creatividad", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
        
        selected_formula_key = st.selectbox(
            "Selecciona una fórmula para tus beneficios",
            options=list(benefits_formulas.keys())
        )
        selected_formula = benefits_formulas[selected_formula_key]

    # Botón de enviar
    submit = st.button("Generar Beneficios")

# Mostrar los beneficios generados
if submit:
    if target_audience and product and selected_formula:
        try:
            # Obtener la respuesta del modelo
            generated_benefits = generate_benefits(number_of_benefits, target_audience, product, temperature, selected_formula)
            col2.markdown(f"""
                <div style="padding: 10px; border: 1px solid #ddd; border-radius: 8px;">
                    <h3>Beneficios Generados:</h3>
                    <p>{generated_benefits}</p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            col2.error(f"Error al generar beneficios: {e}")
    else:
        col2.warning("Por favor, completa todos los campos antes de generar beneficios.")
