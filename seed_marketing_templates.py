"""
Carga plantillas de tarea y combos de día con contenido de marketing
(expectativa, cuenta regresiva, lanzamiento, cierre, etc.) para un usuario
que ya exista en la app.

Uso, desde la carpeta del proyecto (con el venv activado):

    python3 seed_marketing_templates.py tu@email.com

No borra nada de lo que ya tengas guardado: agrega estas plantillas al final
de tu lista actual. Si corrés el script dos veces, evita duplicar por
"label"/"name" repetido.
"""
import json
import os
import sys
import uuid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

TASK_TEMPLATES = [
    {"time": "9:00 a.m.", "platform": ["fb", "igfeed"], "label": "Banner de expectativa",
     "desc": "Pregunta o frase intrigante sin revelar el producto/beneficio todavía. Objetivo: generar curiosidad, no informar."},
    {"time": "12:00 m.", "platform": ["igstory"], "label": "Story: reveal de fecha",
     "desc": "Anunciar la fecha en que se revela la sorpresa o el lanzamiento. Refuerza la anticipación sin dar detalles."},
    {"time": "5:00 p.m.", "platform": ["wa"], "label": "Estado de WhatsApp: teaser",
     "desc": "Reutilizar el banner de expectativa en formato vertical para el estado de WhatsApp."},

    {"time": "9:00 a.m.", "platform": ["fb", "igfeed"], "label": "Post cuenta regresiva",
     "desc": "Mostrar un beneficio o feature concreto + overlay \"Faltan X días\". Cada día se cambia el número."},
    {"time": "1:00 p.m.", "platform": ["igstory"], "label": "Story cuenta regresiva",
     "desc": "Sticker de cuenta regresiva de Instagram o gráfico propio con el número de días restantes."},
    {"time": "6:00 p.m.", "platform": ["wa"], "label": "Estado: recordatorio de cuenta regresiva",
     "desc": "Mismo gráfico de cuenta regresiva del día, formato WhatsApp."},

    {"time": "10:00 a.m.", "platform": ["fb", "igfeed"], "label": "Post de lanzamiento",
     "desc": "El anuncio central de la campaña. Fijar (pin) en el perfil. CTA claro y directo (probar, registrarse, comprar)."},
    {"time": "12:00 m.", "platform": ["igstory"], "label": "Story con link directo",
     "desc": "Story con el botón o liga directa hacia la oferta/registro, reforzando el anuncio del post principal."},
    {"time": "3:00 p.m.", "platform": ["wadirect"], "label": "Broadcast a leads y clientes",
     "desc": "Mensaje directo a la base de contactos guardados anunciando la novedad u oferta."},

    {"time": "9:00 a.m.", "platform": ["fb", "igfeed"], "label": "Post \"Último día\"",
     "desc": "Urgencia: el beneficio o la oferta se cierra hoy. Reforzar qué pierden si no actúan ahora."},
    {"time": "1:00 p.m.", "platform": ["igstory"], "label": "Story: quedan pocas horas",
     "desc": "Cuenta regresiva final del día, tono de urgencia más marcado que en días anteriores."},
    {"time": "4:00 p.m.", "platform": ["wadirect"], "label": "Recordatorio final a leads",
     "desc": "Último mensaje directo antes del cierre. Personalizar si el volumen de contactos lo permite."},
    {"time": "7:00 p.m.", "platform": ["igstory", "wa"], "label": "Cierre de campaña",
     "desc": "Mensaje de cierre: \"se acabó\" + agradecimiento, o gancho hacia el próximo paso."},

    {"time": "11:00 a.m.", "platform": ["igstory"], "label": "Story ligera de mantenimiento",
     "desc": "Recordatorio de bajo perfil para mantener visibilidad sin saturar. Ideal para fines de semana o pausas entre fases."},

    {"time": "10:00 a.m.", "platform": ["fb", "igfeed"], "label": "Feature spotlight",
     "desc": "Destacar una funcionalidad específica del producto con un ejemplo de uso real, no genérico."},
    {"time": "4:00 p.m.", "platform": ["igstory"], "label": "Story: testimonio o prueba social",
     "desc": "Mostrar un testimonio, caso de éxito o dato de uso real (ej: número de clínicas usando el producto)."},
]

DAY_TEMPLATES = [
    ("Día de Expectativa", ["Banner de expectativa", "Story: reveal de fecha", "Estado de WhatsApp: teaser"]),
    ("Cuenta regresiva", ["Post cuenta regresiva", "Story cuenta regresiva", "Estado: recordatorio de cuenta regresiva"]),
    ("Día de Lanzamiento", ["Post de lanzamiento", "Story con link directo", "Broadcast a leads y clientes"]),
    ("Día de Cierre", ["Post \"Último día\"", "Story: quedan pocas horas", "Recordatorio final a leads", "Cierre de campaña"]),
    ("Recordatorio suave", ["Story ligera de mantenimiento"]),
    ("Feature spotlight", ["Feature spotlight", "Story: testimonio o prueba social"]),
]


def find_user_id(email):
    users_path = os.path.join(DATA_DIR, "users.json")
    if not os.path.exists(users_path):
        sys.exit("No existe data/users.json todavía — registrate primero en la app.")
    with open(users_path, "r", encoding="utf-8") as f:
        users = json.load(f)
    user = next((u for u in users if u["email"] == email.strip().lower()), None)
    if not user:
        sys.exit(f"No encontré ningún usuario con el email {email}")
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


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 seed_marketing_templates.py tu@email.com")

    user_id = find_user_id(sys.argv[1])
    user_dir = os.path.join(DATA_DIR, "users", user_id)

    # --- Plantillas de tarea ---
    tpl_path = os.path.join(user_dir, "task_templates.json")
    templates = load_json(tpl_path, [])
    existing_labels = {t["label"] for t in templates}

    added_templates = 0
    label_to_id = {t["label"]: t["id"] for t in templates}
    for t in TASK_TEMPLATES:
        if t["label"] in existing_labels:
            continue
        entry = {"id": uuid.uuid4().hex[:10], **t}
        templates.append(entry)
        label_to_id[t["label"]] = entry["id"]
        added_templates += 1

    save_json(tpl_path, templates)

    # --- Combos de día ---
    dt_path = os.path.join(user_dir, "day_templates.json")
    day_templates = load_json(dt_path, [])
    existing_names = {d["name"] for d in day_templates}

    added_combos = 0
    for name, labels in DAY_TEMPLATES:
        if name in existing_names:
            continue
        tasks = []
        for label in labels:
            source = next((t for t in TASK_TEMPLATES if t["label"] == label), None)
            if source:
                tasks.append({
                    "time": source["time"], "platform": source["platform"],
                    "label": source["label"], "desc": source["desc"],
                })
        day_templates.append({"id": uuid.uuid4().hex[:10], "name": name, "tasks": tasks})
        added_combos += 1

    save_json(dt_path, day_templates)

    print(f"Listo. {added_templates} plantillas de tarea nuevas, {added_combos} combos de día nuevos.")
    print("Ya deberían aparecer al recargar la pestaña 🧩 Plantillas.")


if __name__ == "__main__":
    main()
