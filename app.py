# Mostrar los bullets generados
if submit:
    if target_audience and product:
        try:
            # Obtener la respuesta del modelo
            generated_bullets = get_gemini_response_bullets(target_audience, product, num_bullets, creativity)
            col2.markdown(f"""
                <div style="border: 1px solid #000000; padding: 5px; border-radius: 8px; background-color: #ffffff;">
                    <h4>Aquí están tus bullets:</h4>
                    <p>{generated_bullets}</p>
                </div>
            """, unsafe_allow_html=True)
        except ValueError as e:
            col2.error(f"Error: {str(e)}")
    else:
        col2.error("Por favor, proporciona el público objetivo y el producto.")

