def generate_bullets(number_of_bullets, target_audience, product, call_to_action, temperature):
    # Configuración del modelo
    generation_config = {
        "temperature": temperature,
        "top_p": 0.85,
        "top_k": 128,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    # Crear la instrucción del sistema
    system_instruction = (
        f"Eres un experto copywriter especializado en escribir bullets atractivos, curiosos e inusuales para {target_audience} sobre {product} que promueven la acción de {call_to_action}. "
        f"Tu tarea es ayudarme a escribir {number_of_bullets} bullets que destaquen los beneficios de {product}. "
        f"Utiliza las siguientes menciones y ejemplos como inspiración en tu respuesta: "
        "El armario del baño es el mejor lugar para guardar medicamentos, ¿verdad? Incorrecto. Es el peor. Los hechos están en la página 10. "
        "El mejor tiempo verbal que le da a tus clientes la sensación de que ya te han comprado. "
        "La historia de un joven emprendedor que transformó su vida aplicando esta técnica simple pero poderosa. "
        "Los misterios de cómo algunas personas parecen tener éxito sin esfuerzo, mientras otras luchan. La clave está en esta pequeña diferencia. "
        "La leyenda de aquellos que dominaron la productividad con un solo hábito. ¿Te atreves a descubrirlo? "
        "La historia de un padre ocupado que, con solo 10 minutos al día, logró transformar su salud y bienestar. "
        "¿Cuándo es una buena idea decirle a una chica que te gusta? Si no se lo dices en ese momento, despídete de conocerla íntimamente. "
        "Cuando respondas, utiliza la mayor cantidad de variaciones."
    )

    # Configuración del modelo generativo
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # Generar el resultado utilizando el modelo
    try:
        response = model.generate_content([system_instruction])
        
        # Verificar que la respuesta tenga el formato esperado
        if response.candidates and response.candidates[0].content.parts:
            generated_bullets = response.candidates[0].content.parts[0].text.strip()
            return generated_bullets
        else:
            raise ValueError("No se generaron bullets válidos.")
    except Exception as e:
        raise ValueError(f"Error al generar los bullets: {str(e)}")
