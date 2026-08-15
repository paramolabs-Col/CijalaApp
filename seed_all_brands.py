"""
Carga plantillas de tarea y combos de día para DentalSync, Páramo Labs
y el Agente Multiplataforma, más plantillas genéricas por objetivo.

Uso (desde la carpeta del proyecto, con el venv activado si aplica):

    python3 seed_all_brands.py ciro0279@gmail.com

No borra nada existente: agrega solo lo que no esté ya.
Si lo corrés dos veces no duplica.
"""
import json
import os
import sys
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ---------------------------------------------------------------------------
# PLANTILLAS DE TAREA
# ---------------------------------------------------------------------------
TASK_TEMPLATES = [

    # ===== GENÉRICAS — Atracción =====
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "Post de presentación de marca",
     "desc": "Carrusel o imagen: quiénes somos, qué hacemos y para quién. CTA: síguenos o visita el perfil."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "Story: encuesta interactiva",
     "desc": "Pregunta con sticker de encuesta sobre el pain point de la audiencia. Objetivo: interacción y datos."},
    {"time": "9:00 a.m.", "platform": ["fb"], "label": "Facebook: post de alcance orgánico",
     "desc": "Dato curioso, pregunta abierta o contenido viral del sector. Optimizado para alcance sin pautar."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "Mito vs Realidad del sector",
     "desc": "Desmonta 1 creencia falsa con dato verificable. Genera confianza y diferenciación."},
    {"time": "8:00 a.m.", "platform": ["wa"], "label": "Estado WA: tip del día",
     "desc": "Imagen vertical con un tip rápido del sector. Sin CTA de venta."},

    # ===== GENÉRICAS — Educación =====
    {"time": "9:00 a.m.", "platform": ["igfeed", "igstory"], "label": "Tip rápido: valor sin vender",
     "desc": "Consejo práctico de 1 paso que se puede aplicar hoy. Posiciona como autoridad del sector."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "Dato estadístico de impacto",
     "desc": "Estadística del sector con fuente. Formato: número grande + contexto + conclusión accionable."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "Story: respuesta a pregunta frecuente",
     "desc": "Parafrasea una pregunta real del DM/comentarios y respondela en 3 slides de story."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "Lista: '3 cosas que debés saber'",
     "desc": "Carrusel con 3-5 conceptos clave del sector en lenguaje simple. Slide final con CTA a guardar."},
    {"time": "9:00 a.m.", "platform": ["wa"], "label": "WA: mini newsletter semanal",
     "desc": "Mensaje a lista: resumen de lo más útil de la semana + link o CTA a próximo contenido."},

    # ===== GENÉRICAS — Activación =====
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "Caso de éxito de cliente",
     "desc": "Historia real: situación inicial → solución → resultado con número concreto. No inventar datos."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "Story: oferta con tiempo límite",
     "desc": "Sticker de countdown o fecha visible. Beneficio claro y único. CTA directo (link, DM o swipe)."},
    {"time": "10:00 a.m.", "platform": ["wadirect"], "label": "WA directo: seguimiento a prospectos",
     "desc": "Mensaje personalizado a contactos que preguntaron pero no avanzaron. Tono cálido, no agresivo."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "Post: respuesta a objeción principal",
     "desc": "Identifica la objeción más frecuente antes de comprar y resuélvela con evidencia. Carrusel."},
    {"time": "10:00 a.m.", "platform": ["igstory"], "label": "Story: CTA directo al DM",
     "desc": "Story simple + texto + sticker 'Escríbenos'. Objetivo: abrir conversación con prospectos."},

    # ===== GENÉRICAS — Fidelización =====
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "Post de agradecimiento a comunidad",
     "desc": "Reconocimiento público a clientes/comunidad con cifra real (ej: 500 clientes, 2 años, etc.)."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "Story: encuesta de mejora",
     "desc": "Pregunta de feedback a clientes actuales. Muestra que su opinión construye el servicio."},
    {"time": "9:00 a.m.", "platform": ["wadirect"], "label": "WA directo: beneficio exclusivo VIP",
     "desc": "Mensaje individual a clientes frecuentes con acceso anticipado, descuento o regalo exclusivo."},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "Testimonio de cliente real",
     "desc": "Cita textual de cliente (con nombre si hay permiso). Alternativa: captura de WA anonimizada."},

    # ===== GENÉRICAS — Lanzamiento =====
    {"time": "9:00 a.m.", "platform": ["igstory", "igfeed"], "label": "Teaser misterioso",
     "desc": "Imagen que insinúa algo nuevo sin revelarlo. Texto: '¿Estás listo? El [fecha] llega algo...'"},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb", "igstory"], "label": "Reveal oficial de lanzamiento",
     "desc": "Anuncio completo: qué es, para quién, beneficio principal, precio si aplica, CTA. Fijar en perfil."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "Story: cuenta regresiva al lanzamiento",
     "desc": "Sticker countdown de Instagram o gráfico propio. Un beneficio diferente por día de expectativa."},
    {"time": "9:00 a.m.", "platform": ["wa", "wadirect"], "label": "Broadcast: anuncio de novedad",
     "desc": "Mensaje simultáneo a lista y contactos calientes. Primero engancha, luego informa."},

    # ===== GENÉRICAS — Reactivación =====
    {"time": "10:00 a.m.", "platform": ["wadirect"], "label": "WA: mensaje de reactivación personal",
     "desc": "Mensaje individual a contactos inactivos +90 días. Tono: '¿Cómo estás? Te tenemos algo especial'."},
    {"time": "11:00 a.m.", "platform": ["igfeed", "fb"], "label": "Post: esto cambió desde la última vez",
     "desc": "Muestra novedades y mejoras desde que el prospecto tuvo contacto. Genera razón para volver."},
    {"time": "9:00 a.m.", "platform": ["wa", "wadirect"], "label": "Oferta exclusiva de regreso",
     "desc": "Beneficio especial (descuento, bono, sesión gratis) solo para quienes vuelven. Tiempo límite real."},

    # ===== GENÉRICAS — Temporada =====
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "Apertura de campaña de temporada",
     "desc": "Anuncio visual: tema de la campaña, qué hay, cuándo termina. Diseño coherente con la fecha."},
    {"time": "9:00 a.m.", "platform": ["igstory"], "label": "Story: cuenta regresiva a fecha especial",
     "desc": "Countdown a la fecha del evento o fin de la oferta. Renovar cada día con un beneficio diferente."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb", "wa"], "label": "Día central de temporada",
     "desc": "El mensaje más fuerte de la campaña: oferta o contenido principal para el día pico."},
    {"time": "12:00 p.m.", "platform": ["igstory"], "label": "Story: cierre y agradecimiento",
     "desc": "Cierre de campaña: gracias + qué viene + invitación a quedarse para lo próximo."},

    # ===== DENTALSYNC =====
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Presentación: software dental",
     "desc": "¿Seguís agendando citas en papel? DentalSync automatiza agenda, historial y cobro. Carrusel: 3 problemas → 3 soluciones."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "[DS] Story: encuesta tiempo administrativo",
     "desc": "'¿Cuántas horas por semana dedicás a tareas administrativas?' Opciones: 1-3h / 4-8h / +8h"},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Tip: cómo reducir ausencias",
     "desc": "Las ausencias cuestan miles al mes. DentalSync envía recordatorios automáticos. Resultado: -40% de no-shows en 30 días."},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "[DS] Caso de éxito: clínica dental",
     "desc": "Historia real: cuántos pacientes maneja la clínica, qué problema tenía, cómo DentalSync lo resolvió. Número concreto al final."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Feature: agenda inteligente",
     "desc": "Agenda por silla / por dentista / recordatorios automáticos / historial en un clic. Carrusel de 4 slides."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Feature: historial del paciente",
     "desc": "Accedé al historial completo en 3 segundos: radiografías, tratamientos, pagos y notas en un solo lugar."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "[DS] Story: demo disponible",
     "desc": "'¿Querés ver DentalSync en acción? Demo de 20 min, sin costo, sin compromiso.' CTA a link o DM."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Post: Día del Odontólogo",
     "desc": "Celebración de la profesión. Dato de impacto dental + reconocimiento al gremio + CTA suave."},
    {"time": "9:00 a.m.", "platform": ["igfeed"], "label": "[DS] Tip dental para pacientes",
     "desc": "Tip de higiene bucal simple para pacientes finales. Posiciona DentalSync como marca que cuida al paciente."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Objeción: '¿Es difícil de implementar?'",
     "desc": "'En 1 día DentalSync funciona en tu clínica. Sin IT, sin instalaciones, sin contratos anuales.' Carrusel de onboarding paso a paso."},
    {"time": "9:00 a.m.", "platform": ["wa", "wadirect"], "label": "[DS] WA: actualización de versión",
     "desc": "Aviso a usuarios sobre nueva función: qué mejora, cómo activarla y beneficio concreto."},
    {"time": "11:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Post: estadística dental",
     "desc": "'6 de cada 10 pacientes no vuelven tras su primera visita.' Dato + cómo DentalSync mejora ese número."},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "[DS] Testimonio: dentista usuario",
     "desc": "'Desde que uso DentalSync, perdí cero pacientes por ausencias no recordadas.' — Dr. [Nombre], [Ciudad]."},
    {"time": "9:00 a.m.", "platform": ["igstory"], "label": "[DS] Story: prueba gratuita 30 días",
     "desc": "'30 días gratis. Sin tarjeta. Sin compromiso. Solo DentalSync funcionando en tu clínica.' Link de registro."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Lanzamiento: nueva función",
     "desc": "Reveal de nueva función de DentalSync: qué es, para quién, cuándo disponible, cómo activarla."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Post: facturación y cobros",
     "desc": "DentalSync unifica la facturación de la clínica: cobros pendientes, historial de pagos y recordatorios automáticos."},
    {"time": "11:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Comparativa: Excel vs DentalSync",
     "desc": "Carrusel visual: gestión en Excel (errores, tiempo, pérdida de datos) vs DentalSync (automatizado, seguro, rápido)."},
    {"time": "10:00 a.m.", "platform": ["igstory"], "label": "[DS] Story: casos de uso dental",
     "desc": "3 stories seguidas mostrando un día típico de una clínica con DentalSync: mañana / tarde / cierre del día."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[DS] Post: seguridad de datos del paciente",
     "desc": "Los datos de tus pacientes están protegidos con encriptación de grado médico. DentalSync cumple con la normativa de privacidad."},

    # ===== PÁRAMO LABS =====
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Presentación: Páramo Labs",
     "desc": "¿Quiénes somos? Agencia de marketing digital. Carrusel: problemas que resolvemos → cómo → resultados."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "[PL] Story: ¿Tu marketing realmente funciona?",
     "desc": "'¿Sabés cuánto cuesta conseguir un nuevo cliente?' Opciones: Sí / No / A veces. Genera conciencia del problema."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Tip: error común en redes sociales",
     "desc": "El error #1 que cometen los negocios en redes y cómo evitarlo. Post de valor puro, sin vender."},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "[PL] Caso de éxito de cliente",
     "desc": "Cliente de Páramo Labs: industria + problema + estrategia + resultado en números (alcance, leads, ventas)."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Post: tendencia de marketing digital",
     "desc": "Tendencia actual en redes + cómo Páramo Labs la aplica para sus clientes. Ejemplo concreto."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Post: pilares de una buena estrategia",
     "desc": "Carrusel educativo: los 5 pilares de una estrategia digital efectiva. Lenguaje para emprendedores."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "[PL] Story: consulta gratuita disponible",
     "desc": "'¿Querés saber por qué tu contenido no convierte? Hablemos 15 minutos.' CTA a DM o agenda."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Post: antes y después de campaña",
     "desc": "Comparativa de métricas de un cliente antes/después de trabajar con Páramo Labs. Alcance, leads o ventas."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Post: mito del marketing digital",
     "desc": "'Mito: publicar todos los días es obligatorio.' Carrusel de 3-5 mitos del sector desmontados."},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "[PL] Detrás de escena: proceso de campaña",
     "desc": "Cómo se ve el trabajo real en Páramo Labs: reunión de estrategia → contenido → análisis. Humaniza la agencia."},
    {"time": "9:00 a.m.", "platform": ["wa", "wadirect"], "label": "[PL] WA: reporte mensual a clientes",
     "desc": "Mensaje a clientes activos: resultados del mes + ajustes para el próximo + pregunta de retroalimentación."},
    {"time": "11:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Post: lanzamiento de nuevo servicio",
     "desc": "Anuncio de nuevo servicio o paquete de Páramo Labs: qué incluye, para quién es, precio o CTA."},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "[PL] Testimonio de cliente satisfecho",
     "desc": "'Páramo Labs nos llevó de 0 a [X] leads por mes en [Y] semanas.' Cita real + nombre + empresa."},
    {"time": "9:00 a.m.", "platform": ["igstory"], "label": "[PL] Story: propuesta gratuita sin compromiso",
     "desc": "'¿Querés una propuesta para mejorar tu estrategia digital? Sin costo.' CTA a DM o formulario."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Equipo Páramo Labs",
     "desc": "Presentación del equipo: nombres, roles y especialidades. Humaniza la agencia y genera confianza antes de vender."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Post: por qué el contenido no convierte",
     "desc": "Las 3 razones por las que tu contenido genera likes pero no clientes. Solución práctica para cada una."},
    {"time": "11:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Post: publicidad paga vs orgánico",
     "desc": "¿Cuándo pautar y cuándo no? Guía simple para decidir dónde invertir tu presupuesto de marketing."},
    {"time": "10:00 a.m.", "platform": ["igstory"], "label": "[PL] Story: resultados del mes",
     "desc": "Story con métricas reales de clientes de Páramo Labs. Sin nombres específicos si no hay permiso. Genera confianza."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[PL] Post: frecuencia ideal de publicación",
     "desc": "'¿Cuántas veces por semana publicar en cada red?' Guía visual por plataforma con recomendación de Páramo Labs."},

    # ===== AGENTE MULTIPLATAFORMA =====
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Presentación: Agente Multiplataforma",
     "desc": "IA que responde, agenda, filtra y convierte en WA, IG, email y más. Sin código, sin soporte 24/7."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "[AM] Story: ¿Cuántos mensajes perdés al día?",
     "desc": "'¿Cuántas consultas de clientes respondés manualmente?' 1-10 / 10-50 / +50 / Los pierdo."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Demo: respuesta automática en WA",
     "desc": "Video o GIF: pregunta del cliente → respuesta inmediata del Agente → calificación → agenda. Todo automático."},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "[AM] Caso de éxito: ahorro de tiempo",
     "desc": "Negocio que usa el Agente: X horas ahorradas/semana, Y% más respuestas en tiempo real, Z leads calificados solos."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Feature: calificación automática de leads",
     "desc": "El Agente hace las preguntas correctas, filtra interesados y envía solo leads calificados. Conversación de ejemplo."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Feature: agenda sin intervención humana",
     "desc": "Cliente escribe → Agente pregunta disponibilidad → ofrece horarios → confirma cita → envía recordatorio. Solo."},
    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "[AM] Story: prueba gratuita del Agente",
     "desc": "'Activa tu prueba gratis de 14 días y ves el Agente funcionando en tu negocio hoy.' CTA a registro."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Post: IA sin código para negocios",
     "desc": "'No necesitás saber programar. Si podés escribir un WhatsApp, podés configurarlo en 10 minutos.'"},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Mito: 'La IA no suena humana'",
     "desc": "'Mito: los chatbots suenan como robots. Realidad: el Agente se configura con tu tono y tus respuestas exactas.'"},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "[AM] Post: integraciones disponibles",
     "desc": "El Agente conecta con WA, IG, email, Calendly, Google Calendar y más. Una integración por slide con caso de uso."},
    {"time": "9:00 a.m.", "platform": ["wa", "wadirect"], "label": "[AM] WA: nueva integración disponible",
     "desc": "Aviso a usuarios: nueva integración con [plataforma]. Cómo activarla, para qué sirve, qué problema resuelve."},
    {"time": "11:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Post: ROI del Agente",
     "desc": "'Si atendés 50 consultas/día × 5 min = 4 horas diarias. El Agente las resuelve en segundos.' Cálculo visual de ROI."},
    {"time": "10:00 a.m.", "platform": ["igfeed"], "label": "[AM] Testimonio: usuario del Agente",
     "desc": "'El Agente responde mientras duermo y tengo leads calificados cuando me despierto.' — [Nombre], [Negocio]."},
    {"time": "9:00 a.m.", "platform": ["igstory"], "label": "[AM] Story: lanzamiento de nueva función",
     "desc": "Reveal de nueva función: qué hace, cuándo disponible, cómo activarla. CTA a link de actualización."},
    {"time": "10:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Lanzamiento: integración con IG DMs",
     "desc": "El Agente ahora también responde automáticamente los DMs de Instagram. Demo en carrusel o video."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Post: el costo de no automatizar",
     "desc": "'Cada lead que no respondés en los primeros 5 minutos tiene 80% menos chances de convertir.' Dato + solución = el Agente."},
    {"time": "11:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Comparativa: equipo humano vs Agente",
     "desc": "Respuestas 24/7 vs horario de oficina. Tiempo de respuesta: segundos vs minutos. Costo: fijo vs variable. Carrusel."},
    {"time": "10:00 a.m.", "platform": ["igstory"], "label": "[AM] Story: casos de uso por industria",
     "desc": "El Agente en 3 industrias diferentes: clínica dental / agencia de marketing / e-commerce. Un slide por caso."},
    {"time": "9:00 a.m.", "platform": ["igfeed", "fb"], "label": "[AM] Post: privacidad y seguridad del Agente",
     "desc": "Las conversaciones del Agente son privadas y no se comparten. Cumple con las políticas de WA Business y Meta."},
]

# ---------------------------------------------------------------------------
# COMBOS DE DÍA
# ---------------------------------------------------------------------------
DAY_TEMPLATES = [
    # GENÉRICOS
    ("Día de Expectativa (Teaser)", [
        "Teaser misterioso", "Story: cuenta regresiva al lanzamiento", "Estado WA: tip del día"
    ]),
    ("Día de Lanzamiento Oficial", [
        "Reveal oficial de lanzamiento", "Broadcast: anuncio de novedad", "Story: CTA directo al DM"
    ]),
    ("Día Educativo de Valor", [
        "Dato estadístico de impacto", "Tip rápido: valor sin vender", "Story: respuesta a pregunta frecuente"
    ]),
    ("Día de Atracción General", [
        "Post de presentación de marca", "Mito vs Realidad del sector", "Estado WA: tip del día"
    ]),
    ("Día de Activación", [
        "Caso de éxito de cliente", "Story: oferta con tiempo límite", "WA directo: seguimiento a prospectos"
    ]),
    ("Día de Cierre de Campaña", [
        "Story: oferta con tiempo límite", "WA directo: seguimiento a prospectos", "Story: cierre y agradecimiento"
    ]),
    ("Fin de Semana Suave", [
        "Story: encuesta interactiva", "Estado WA: tip del día"
    ]),
    ("Día de Fidelización", [
        "Testimonio de cliente real", "Story: encuesta de mejora", "WA directo: beneficio exclusivo VIP"
    ]),
    ("Día de Reactivación", [
        "WA: mensaje de reactivación personal", "Post: esto cambió desde la última vez", "Oferta exclusiva de regreso"
    ]),
    ("Día de Temporada — Pico", [
        "Apertura de campaña de temporada", "Story: cuenta regresiva a fecha especial", "Día central de temporada"
    ]),

    # DENTALSYNC
    ("DS: Día de Atracción", [
        "[DS] Presentación: software dental",
        "[DS] Story: encuesta tiempo administrativo",
        "Estado WA: tip del día"
    ]),
    ("DS: Día Educativo", [
        "[DS] Tip: cómo reducir ausencias",
        "[DS] Post: estadística dental",
        "[DS] Feature: agenda inteligente"
    ]),
    ("DS: Día de Activación", [
        "[DS] Caso de éxito: clínica dental",
        "[DS] Story: demo disponible",
        "[DS] Objeción: '¿Es difícil de implementar?'"
    ]),
    ("DS: Día de Fidelización", [
        "[DS] Testimonio: dentista usuario",
        "[DS] WA: actualización de versión",
        "Story: encuesta de mejora"
    ]),
    ("DS: Día de Feature", [
        "[DS] Feature: agenda inteligente",
        "[DS] Feature: historial del paciente",
        "[DS] Story: prueba gratuita 30 días"
    ]),
    ("DS: Día de Lanzamiento", [
        "[DS] Lanzamiento: nueva función",
        "[DS] Story: demo disponible",
        "Broadcast: anuncio de novedad"
    ]),
    ("DS: Fin de Semana", [
        "[DS] Tip dental para pacientes",
        "[DS] Story: encuesta tiempo administrativo"
    ]),

    # PÁRAMO LABS
    ("PL: Día de Atracción", [
        "[PL] Presentación: Páramo Labs",
        "[PL] Story: ¿Tu marketing realmente funciona?",
        "Estado WA: tip del día"
    ]),
    ("PL: Día Educativo", [
        "[PL] Tip: error común en redes sociales",
        "[PL] Post: tendencia de marketing digital",
        "[PL] Post: mito del marketing digital"
    ]),
    ("PL: Día de Activación", [
        "[PL] Caso de éxito de cliente",
        "[PL] Story: consulta gratuita disponible",
        "[PL] Post: antes y después de campaña"
    ]),
    ("PL: Día de Fidelización", [
        "[PL] Testimonio de cliente satisfecho",
        "[PL] WA: reporte mensual a clientes",
        "Story: encuesta de mejora"
    ]),
    ("PL: Día de Lanzamiento", [
        "[PL] Post: lanzamiento de nuevo servicio",
        "[PL] Equipo Páramo Labs",
        "[PL] Story: propuesta gratuita sin compromiso"
    ]),
    ("PL: Fin de Semana", [
        "[PL] Story: resultados del mes",
        "[PL] Post: frecuencia ideal de publicación"
    ]),

    # AGENTE MULTIPLATAFORMA
    ("AM: Día de Atracción", [
        "[AM] Presentación: Agente Multiplataforma",
        "[AM] Story: ¿Cuántos mensajes perdés al día?",
        "Estado WA: tip del día"
    ]),
    ("AM: Día Educativo", [
        "[AM] Demo: respuesta automática en WA",
        "[AM] Mito: 'La IA no suena humana'",
        "[AM] Post: IA sin código para negocios"
    ]),
    ("AM: Día de Activación", [
        "[AM] Caso de éxito: ahorro de tiempo",
        "[AM] Story: prueba gratuita del Agente",
        "[AM] Post: ROI del Agente"
    ]),
    ("AM: Día de Feature", [
        "[AM] Feature: calificación automática de leads",
        "[AM] Feature: agenda sin intervención humana",
        "[AM] Post: integraciones disponibles"
    ]),
    ("AM: Día de Lanzamiento", [
        "[AM] Lanzamiento: integración con IG DMs",
        "[AM] Story: lanzamiento de nueva función",
        "Broadcast: anuncio de novedad"
    ]),
    ("AM: Fin de Semana", [
        "[AM] Story: casos de uso por industria",
        "[AM] Post: el costo de no automatizar"
    ]),
]


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def find_user_id(email):
    users_path = os.path.join(DATA_DIR, "users.json")
    if not os.path.exists(users_path):
        sys.exit("No existe data/users.json — registrate primero en la app.")
    with open(users_path, "r", encoding="utf-8") as f:
        users = json.load(f)
    user = next((u for u in users if u["email"] == email.strip().lower()), None)
    if not user:
        sys.exit(f"No encontré usuario con email {email}")
    return user["id"]


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 seed_all_brands.py tu@email.com")

    user_id = find_user_id(sys.argv[1])
    user_dir = os.path.join(DATA_DIR, "users", user_id)

    # — Plantillas de tarea —
    tpl_path = os.path.join(user_dir, "task_templates.json")
    templates = load_json(tpl_path, [])
    existing_labels = {t["label"] for t in templates}
    label_to_id = {t["label"]: t["id"] for t in templates}

    added_tpl = 0
    for t in TASK_TEMPLATES:
        if t["label"] in existing_labels:
            continue
        entry = {"id": uuid.uuid4().hex[:10], **t}
        templates.append(entry)
        label_to_id[t["label"]] = entry["id"]
        existing_labels.add(t["label"])
        added_tpl += 1

    save_json(tpl_path, templates)

    # — Combos de día —
    dt_path = os.path.join(user_dir, "day_templates.json")
    day_tpls = load_json(dt_path, [])
    existing_names = {d["name"] for d in day_tpls}

    added_combos = 0
    all_task_defs = {t["label"]: t for t in TASK_TEMPLATES}

    for name, labels in DAY_TEMPLATES:
        if name in existing_names:
            continue
        tasks = []
        for label in labels:
            src = all_task_defs.get(label)
            if src:
                tasks.append({
                    "time": src["time"], "platform": src["platform"],
                    "label": src["label"], "desc": src["desc"],
                })
        if not tasks:
            continue
        day_tpls.append({"id": uuid.uuid4().hex[:10], "name": name, "tasks": tasks})
        existing_names.add(name)
        added_combos += 1

    save_json(dt_path, day_tpls)

    print(f"\nListo.")
    print(f"  {added_tpl} plantillas de tarea nuevas agregadas.")
    print(f"  {added_combos} combos de día nuevos agregados.")
    print(f"\nRecargá la pestaña Plantillas en la app para verlas.")
    print(f"En el editor de campaña usá 'Desde plantilla…' o 'Aplicar combo…' por día.")


if __name__ == "__main__":
    main()
