import uuid


def _t(time, platform, label, desc):
    return {"id": uuid.uuid4().hex[:8], "time": time, "platform": platform, "label": label, "desc": desc}


def _d(date_iso, phase, fair, label, tasks):
    return {"date": date_iso, "phase": phase, "fair": fair, "label": label, "tasks": tasks}


def seed_campaigns():
    """Campaña original OdontoTech 2026 como primer registro."""
    days = [
        _d("2026-07-21", 1, False, "Lanzamiento del teaser", [
            _t("9:00 a.m.", ["fb", "igfeed"], "Publicar banner \"La odontología está evolucionando, ¿y tú?\"",
               "Pieza lista (Facebook + Instagram Feed). Instala la pregunta, sin revelar el qué todavía."),
            _t("12:00 p.m.", ["igstory"], "Story: reveal de fecha",
               "\"Algo grande se viene para tu clínica. Guarda esta fecha: 28–31 jul.\""),
            _t("5:00 p.m.", ["wa"], "Estado de WhatsApp: teaser",
               "Reutilizar el banner formato WhatsApp que ya tienes listo."),
        ]),
        _d("2026-07-22", 1, False, "Feature spotlight: Agenda + Historia Clínica", [
            _t("10:00 a.m.", ["fb", "igfeed"], "Carrusel de 2 features",
               "Agenda Inteligente + Historia Clínica Digital. Armar con los íconos ya existentes del banner principal."),
            _t("4:00 p.m.", ["igstory"], "Story: \"mañana te mostramos más\"",
               "Recordatorio corto para mantener el hilo de la semana."),
        ]),
        _d("2026-07-23", 1, False, "MOLA — Inteligencia Artificial", [
            _t("10:00 a.m.", ["fb", "igfeed"], "Publicar \"MOLA lee tus radiografías\"",
               "Pieza lista, fondo oscuro. Es el diferencial tecnológico más fuerte de la marca."),
            _t("1:00 p.m.", ["igstory"], "Story con link a prueba gratis",
               "Botón \"Probar gratis\" de la pieza original, agregar liga directa."),
            _t("6:00 p.m.", ["wa"], "Estado de WhatsApp: repost MOLA", "Mismo contenido, formato vertical."),
        ]),
        _d("2026-07-24", 1, False, "Cierre de semana + cuenta regresiva", [
            _t("9:00 a.m.", ["fb", "igfeed"], "Hero de producto + \"Faltan 4 días\"",
               "Adaptar banner de laptop/dashboard con overlay de conteo regresivo."),
            _t("3:00 p.m.", ["igstory"], "Story: \"Comenta VOY si nos visitas\"",
               "Genera interacción medible antes del fin de semana."),
        ]),
        _d("2026-07-25", 2, False, "Anuncio del Plan Pionero", [
            _t("10:00 a.m.", ["fb", "igfeed"], "Publicar y fijar \"Plan Pionero OdontoTech\"",
               "2 meses gratis + acceso completo. Solo 50 cupos. Pieza lista, fijar (pin) en el perfil."),
            _t("12:00 p.m.", ["igstory"], "Story con conteo de cupos",
               "Reforzar la urgencia: \"Cupos limitados a 50 clínicas.\""),
            _t("3:00 p.m.", ["wadirect"], "Broadcast a base de clientes/leads",
               "Anuncio directo del Plan Pionero a contactos guardados."),
        ]),
        _d("2026-07-26", 2, False, "Recordatorio suave (bajo volumen B2B)", [
            _t("11:00 a.m.", ["igstory"], "Story ligera: \"Faltan 2 días\"",
               "Tono relajado de domingo. Falta crear esta pieza (mismo estilo oscuro con glow del logo)."),
        ]),
        _d("2026-07-27", 2, False, "Última llamada antes de la feria", [
            _t("9:00 a.m.", ["fb", "igfeed"], "\"Mañana comienza OdontoTech 2026\"",
               "Adaptar hero de producto con overlay de anuncio. Incluir número de stand cuando esté confirmado."),
            _t("2:00 p.m.", ["wadirect"], "Mensaje personalizado a leads",
               "Confirmar asistencia de cada contacto interesado al stand."),
            _t("6:00 p.m.", ["igstory"], "Último aviso antes de feria",
               "Cuenta regresiva final: \"Mañana nos vemos.\""),
        ]),
        _d("2026-07-28", 3, True, "¡Arrancamos! Día 1 de feria", [
            _t("8:00 a.m.", ["fb", "igfeed"], "Post ancla: infografía con QR",
               "\"Escanea y prueba DentalSync — 14 días gratis, sin tarjeta.\" Pieza más completa que tienes, ya lista."),
            _t("11:00 a.m.", ["igstory"], "Story en vivo: montaje del stand",
               "Contenido real — equipo listo, primeras fotos del espacio."),
            _t("3:00 p.m.", ["igstory"], "Story: primeras visitas", "Mostrar movimiento real en el stand."),
            _t("6:00 p.m.", ["wa"], "Estado: resumen del día 1", "Cierre del primer día de feria."),
        ]),
        _d("2026-07-29", 3, True, "Contenido en vivo desde el stand", [
            _t("9:00 a.m.", ["igstory"], "Story: \"Buenos días desde Corferias\"", "Arranque del día 2 de feria."),
            _t("12:00 p.m.", ["fb", "igfeed"], "Fotos reales + cupos restantes",
               "Requiere contenido capturado en vivo (fotos/video del stand) — asignar a alguien del equipo presente."),
            _t("4:00 p.m.", ["igstory"], "Story: testimonio de visitante",
               "Clip corto de una clínica probando la demo, si es posible."),
            _t("7:00 p.m.", ["wa"], "Estado: resumen del día 2", "Cierre del segundo día."),
        ]),
        _d("2026-07-30", 3, True, "Anticipo del cierre", [
            _t("9:00 a.m.", ["fb", "igfeed"], "\"Mañana es el último día\"",
               "Adaptar plantilla \"Último día\" cambiando el titular, mismo estilo."),
            _t("1:00 p.m.", ["wadirect"], "Recordatorio a leads del stand",
               "Contactar a quienes visitaron el stand los días 28 y 29."),
            _t("5:00 p.m.", ["igstory"], "Story: cuenta regresiva final",
               "Últimas horas antes del cierre de la feria."),
        ]),
        _d("2026-07-31", 3, True, "ÚLTIMO DÍA — cierre de campaña", [
            _t("8:00 a.m.", ["igstory", "wa"], "\"Hoy es el último día\"", "Pieza \"ÚLTIMO DÍA\" lista, formato story."),
            _t("12:00 p.m.", ["fb", "igfeed"], "Post ancla: \"Hoy cierra el beneficio\"",
               "2 meses gratis + acceso full se van con la feria. Pieza lista."),
            _t("4:00 p.m.", ["igstory"], "Story: \"Quedan pocas horas\"",
               "Presión final antes del cierre de Corferias."),
            _t("7:00 p.m.", ["igstory", "wa"], "Cierre de campaña",
               "\"Se acaba la feria, se acaba el beneficio.\" Último llamado a la acción."),
        ]),
    ]

    return [{
        "id": "odontotech-2026",
        "name": "DentalSync × OdontoTech 2026",
        "month": "Julio 2026",
        "days": days,
    }]
