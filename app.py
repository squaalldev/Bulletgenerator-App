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

    # Definición de system_instruction
    system_instruction = (
        f"Eres un experto copywriter especializado en escribir mensajes o textos que atraen la atención de {target_audience} para promover {product} que soluciona los problemas de {target_audience}. "
        f"Tu tarea es ayudarme a escribir {number_of_bullets} bullets que destaquen los beneficios de {product}, los cuales utilizaré para mi [página web, landing, correo], "
        f"teniendo en cuenta los puntos dolorosos de mi {target_audience} y el {product} y la {call_to_action} a realizar."
        "Recuerda que un buen bullet debe tener:\n\n"
        f"El efecto tiene que ser de atracción, de fascinar, de dejar con la curiosidad. Es más, se dice que los bullets (o balas) tienen que ser como una herida, cuya única cura sea {call_to_action}."
        "Haz bullets inusuales, creativos y fascinantes que atrapen la atención que conecten el síntoma de la {target_audience} con el beneficio que van a obtener con {call_to_action}. "
        "Los bullets deben de ser conversacionales, basate en estos ejemplos para realizar tu tarea de crear los bullets:"
        "* Bien y mal: 'Botiquín del baño es el mejor lugar para guardar la medicina, ¿verdad? Incorrecto Es el peor. Los hechos están en la página 10.'"
        "* El mejor/El Peor: 'El mejor tiempo verbal que existe para dar la sensación a tus clientes que ya te han comprado.'"
        "* Historias: 'La historia del...', 'Los misterios de...', 'La leyenda de...'"
        "* Truco: 'Un sistema tonto para escribir copy sin tratar de convencer de que me compren' [Aquí se refiere al Mecanismo Único a utilizar].'"
        "* El de la verdad: 'La verdad que nunca te han dicho en el colegio, la escuela, ni en tu casa de como vivir de la música'"
        "* Haciendo una pregunta: '¿Sabías que?'"
        "* Cuando: '¿Cuándo es buena idea decirle a una chica que te gusta? Si no lo dices justo en ese momento, despídete de que la conozcas íntimamente.'"
        "Importante: Solo responde con bullets, nunca incluyas explicaciones o categorías, así: 'Registrarme ahora y descubrir cómo encontrar un poco de paz en medio del caos.'"
        "Usa estos lineamientos para generar bullets en español."
    )    

    # Generar el resultado utilizando el modelo
    try:
        response = model.generate_content([system_instruction])
        
        # Depurar la respuesta
        st.write("Respuesta del modelo:", response)

        # Acceder al contenido generado correctamente
        generated_bullets = response.result.candidates[0].content.parts[0].text.strip()
        
        return generated_bullets

    except Exception as e:
        st.error(f"Error al generar los bullets: {str(e)}")
        raise
