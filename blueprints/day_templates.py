import os
import uuid

from flask import Blueprint, jsonify, request

from auth import current_user_dir, login_required
from storage import get_store

day_templates_bp = Blueprint("day_templates", __name__, url_prefix="/api")


def _day_templates_store():
    return get_store(os.path.join(current_user_dir(), "day_templates.json"), list)


def load_day_templates():
    return _day_templates_store().load()


def save_day_templates(templates):
    _day_templates_store().save(templates)


@day_templates_bp.route("/day-templates", methods=["GET"])
@login_required
def get_day_templates():
    return jsonify(load_day_templates())


@day_templates_bp.route("/day-templates", methods=["POST"])
@login_required
def create_day_template():
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    tasks_in = data.get("tasks") or []

    if not name:
        return jsonify({"error": "falta el nombre de la plantilla de día"}), 400
    if not tasks_in:
        return jsonify({"error": "elegí al menos una tarea para el combo"}), 400

    tasks = [
        {
            "time": (t.get("time") or "").strip(),
            "platform": t.get("platform") or [],
            "label": (t.get("label") or "").strip(),
            "desc": (t.get("desc") or "").strip(),
        }
        for t in tasks_in
    ]

    template = {"id": uuid.uuid4().hex[:10], "name": name, "tasks": tasks}

    store = _day_templates_store()
    with store.lock:
        templates = load_day_templates()
        templates.append(template)
        save_day_templates(templates)

    return jsonify(template), 201


@day_templates_bp.route("/day-templates/<template_id>", methods=["DELETE"])
@login_required
def delete_day_template(template_id):
    store = _day_templates_store()
    with store.lock:
        templates = load_day_templates()
        remaining = [t for t in templates if t["id"] != template_id]
        if len(remaining) == len(templates):
            return jsonify({"error": "plantilla no encontrada"}), 404
        save_day_templates(remaining)

    return jsonify({"ok": True})
