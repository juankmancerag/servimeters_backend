# interpretar_wisc.py
from dynamo.actualizar_json import (
    actualizar_verbal_comprehension,
    actualizar_perceptual_reasoning,
    actualizar_working_memory,
    actualizar_processing_speed, 
    actualizar_recomendacion_general, 
    actualizar_conclusion_general,
    actualizar_estado_evaluacion
    )

def execute(input_data, context):
    index_scores = input_data.get("scoreConversion", {}).get("indexScores", {})
    scaled_scores = input_data.get("scoreConversion", {}).get("scaledScores", {})
    test_id = input_data.get("testId", "N/A")
    bio_data = input_data.get("biographicData", {})

    def get_subtest_score(nombre):
        for k, v in scaled_scores.items():
            if nombre.lower() in k.lower():
                return v
        return "N/A"

    def interpretar_comprension_verbal(cv_data):
        ic = cv_data.get("indiceCompuesto", "N/A")
        interpretacion = cv_data.get("interpretacion", "N/A")
        interpretacion_lower = interpretacion.lower()
        
        desempeno_general = "por debajo del promedio" if interpretacion_lower == "promedio bajo" else "dentro del promedio"

        semejanzas = get_subtest_score("similarities")  # puntaje numérico
        vocabulario = get_subtest_score("vocabulary")
        comprension = get_subtest_score("comprehension")

        calif_semejanzas = "habilidades adecuadas"  # comodín
        calif_vocabulario = "ligeras dificultades"   # comodín
        calif_comprension = "ligeras dificultades"   # comodín

        return (
            f"<<<INICIO-APTITUD-VERBAL>>>\n"
            f"COMPRENSIÓN VERBAL ({ic}– {interpretacion})\n"
            f"En las habilidades referidas a la formación de conceptos y razonamiento de información verbal, "
            f"riqueza y precisión en la definición de vocablos, así como, comprensión social, juicio práctico, "
            f"conocimientos adquiridos y agilidad e intuición verbal, el paciente tiende a estar {desempeno_general} "
            f"para su edad y etapa del desarrollo. Teniendo como resultado {calif_semejanzas} en la prueba de "
            f"Semejanzas={semejanzas}, en la cual se mide la capacidad de abstraer y generalizar a partir de dos conceptos dados. "
            f"Por otro lado, se identifica {calif_vocabulario} en la prueba de Vocabulario={vocabulario}, la cual mide el conocimiento léxico, "
            f"la precisión conceptual y la capacidad expresiva verbal; y en Comprensión={comprension}, la cual mide razonamiento y juicio social "
            f"frente a la solución de problemas cotidianos, conocimiento de normas sociales y sentido común.\n"
            f"<<<FIN-APTITUD-VERBAL>>>"
        )


    def interpretar_razonamiento_perceptual(rp_data):
        ic = rp_data.get("indiceCompuesto", "N/A")
        interpretacion = rp_data.get("interpretacion", "N/A").lower()
        desempeno = "por debajo del promedio" if interpretacion == "promedio bajo" else "dentro del promedio"

        cubos = get_subtest_score("blockDesign")
        conceptos = get_subtest_score("pictureConcepts")
        matrices = get_subtest_score("matrixReasoning")
        figuras = get_subtest_score("figurasIncompletas")

        return (
            f"<<<INICIO-RAZONAMIENTO-PERCEPTUAL>>>\n"
            f"RAZONAMIENTO PERCEPTUAL  ({ic}– {interpretacion})\n"
            f"En cuanto a las tareas que involucran habilidades relacionadas con el procesamiento espacial y la integración visomotora, "
            f"así como habilidades práxicas constructivas, formación y clasificación de conceptos no-verbales, análisis visual y procesamiento simultáneo, "
            f"el paciente tiende a estar {desempeno} para su edad y etapa del desarrollo. "
            f"Teniendo como resultado RESULTADO SOBRESALIENTE en la prueba de Diseño con cubos={cubos}, en la cual se mide análisis, síntesis y organización visoespacial, "
            f"a tiempo controlado con relación a la manipulación de objetos tridimensionales. "
            f"Por otro lado, se identifica HABILIDADES ADECUADAS en las pruebas de Conceptos con dibujos={conceptos}, la cual mide la formación de conceptos y categorías "
            f"a partir de material visual; y en Matrices={matrices}, la cual mide el razonamiento por analogías visuales e implica integración de información visual; "
            f"finalmente, presenta DIFUCULTAD en la prueba complementaria de Figuras incompletas={figuras}, la cual mide las capacidades de reconocimiento y organización perceptiva a tiempo controlado. "
            f"Por otra parte, se toma en cuenta la subprueba complementaria de figuras incompletas en vez de diseño con cubos, para obtener de manera más homogénea el cálculo del índice.\n"
            f"<<<FIN-RAZONAMIENTO-PERCEPTUAL>>>"
        )


    def interpretar_memoria_trabajo(wm_data):
        ic = wm_data.get("indiceCompuesto", "N/A")
        interpretacion = wm_data.get("interpretacion", "N/A").lower()
        desempeno = "debajo del promedio" if interpretacion == "promedio bajo" else "dentro del promedio"
        digitos = get_subtest_score("digitSpan")
        sucesion = get_subtest_score("letterNumber")

        return (
            f"<<<INICIO-MEMORIA-TRABAJO>>>\n"
            f"MEMORIA DE TRABAJO  ({ic}– {interpretacion.title()})\n"
            f"En tareas que requieren retención, almacenamiento y manipulación de información a corto plazo, "
            f"así como operar mentalmente con dicha información, transformarla y generar una nueva; el paciente "
            f"tiende a estar {desempeno} para su edad y etapa del desarrollo. "
            f"Teniendo como resultado habilidades adecuadas en la prueba de Retención de dígitos={digitos}, "
            f"en la cual se mide los procesos de memoria inmediata y memoria de trabajo, secuenciación, "
            f"planificación, alerta y flexibilidad cognitiva. "
            f"Por otro lado, se identifica dificultad en la prueba de Sucesión de números y letras={sucesion}, "
            f"la cual mide la capacidad de retener y combinar dos tipos de información, organizarla y elaborar "
            f"un conjunto organizado según las indicaciones presentadas.\n"
            f"<<<FIN-MEMORIA-TRABAJO>>>"
        )


    def interpretar_velocidad_procesamiento(ps_data):
        ic = ps_data.get("indiceCompuesto", "N/A")
        interpretacion = ps_data.get("interpretacion", "N/A").lower()
        desempeno = "en el margen inferior" if "límite" in interpretacion else "dentro del promedio"
        claves = get_subtest_score("symbolSearch") or get_subtest_score("coding")
        registros = get_subtest_score("cancellation")
        busqueda = get_subtest_score("symbolSearch")
        return (
            f"<<<INICIO-VELOCIDAD-PROCESAMIENTO>>>\n"
            f"VELOCIDAD DE PROCESAMIENTO  ({ic}– {interpretacion.title()})\n"
            f"En relación con las tareas que involucran la capacidad para focalizar la atención, explorar, ordenar y discriminar información visual con rapidez y eficacia, "
            f"el paciente se encuentra {desempeno} para su edad y etapa del desarrollo. "
            f"Teniendo como resultado dificultades considerables en las pruebas de Claves={claves}, en la cual se mide la rapidez y destreza visomotora del niño, el manejo del lápiz y papel, "
            f"también la capacidad de aprendizaje asociativo, atención alternante, la forma en la que explora, ordena y discrimina información visual; "
            f"y en la prueba complementaria de Registros={registros}, la cual mide la atención selectiva, y planificación en la búsqueda ordenada versus desordenada de información. "
            f"Por otro lado, se identifica ligeras dificultades en la prueba de Búsqueda de símbolos={busqueda}, la cual mide la rapidez y precisión perceptiva que tienen los pacientes junto con la velocidad para procesar información visual simple, "
            f"resistencia frente a tareas repetitivas, habilidades de atención alternante, memoria visual a corto plazo y rastreo visual. "
            f"Por otra parte, debido al bajo puntaje de la subprueba obligatoria que compone la presente escala, se toma en cuenta la puntuación de la subprueba complementaria de registros en vez de la subprueba de claves, "
            f"debido a que el paciente presentó dificultad a la hora de realizar la prueba y fue en la que se obtuvo una menor puntuación.\n"
            f"<<<FIN-VELOCIDAD-PROCESAMIENTO>>>"
        )
    
    def interpretar_recomendacion_general():
        return (
            "<<<INICIO-RECOMENDACION-GENERAL>>>\n"
            "Equipo médico y terapéutico, Institución educativa:, Paciente y su familia\n"
            "<<<FIN-RECOMENDACION-GENERAL>>>"
        )
    
    def interpretar_conclusiones(nombre, con_data):
        clasificacion = con_data.get("interpretacion", "N/A")
        cit = con_data.get("indiceCompuesto", "N/A")
        rango_min = 74
        rango_max = 78
        percentil = con_data.get("percentil", "N/A")
        return (
            "<<<INICIO-CONCLUSIONES>>>\n"
            f"De acuerdo con los resultados presentados anteriormente en la evaluación del coeficiente intelectual, "
            f"se puede evidenciar que {nombre} presenta un desempeño clasificado {clasificacion.upper()}, para una persona de su edad y proceso de escolarización, "
            f"con un CIT de {cit}, localizándose así con el XX% de probabilidad en un rango de {rango_min}-{rango_max}, lo cual indica que obtuvo una mejor puntuación que el {percentil}% "
            f"de otros niños de la misma edad en la muestra de estandarización.\n"
            "<<<FIN-CONCLUSIONES>>>"
        )


    # Generar interpretaciones
    verbal_text = interpretar_comprension_verbal(index_scores.get("comprensionVerbal", {}))
    rp_text = interpretar_razonamiento_perceptual(index_scores.get("razonamientoPerceptual", {}))
    wm_text = interpretar_memoria_trabajo(index_scores.get("memoriaTrabajo", {}))
    ps_text = interpretar_velocidad_procesamiento(index_scores.get("velocidadProcesamiento", {}))
    rec_general = interpretar_recomendacion_general()
    conclusiones = interpretar_conclusiones(bio_data.get("name", "Paciente Desconocido"), index_scores.get("escalaTotal", "N/A"),
        
    )
    # Unir interpretaciones en un solo texto
    texto_final = "\n\n".join([verbal_text, rp_text, wm_text, ps_text,rec_general, conclusiones])

    # Guardar en Dynamo
    if test_id != "N/A":
        actualizar_verbal_comprehension(test_id, verbal_text)
        actualizar_perceptual_reasoning(test_id, rp_text)
        actualizar_working_memory(test_id, wm_text)
        actualizar_processing_speed(test_id, ps_text)
        actualizar_recomendacion_general(test_id, rec_general)
        actualizar_conclusion_general(test_id, conclusiones)
        actualizar_estado_evaluacion(test_id)

    return {"interpretacion": texto_final}
