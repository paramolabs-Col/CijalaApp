import os
import uuid

from flask import Blueprint, jsonify, request

from auth import current_user_dir, login_required
from storage import get_store

task_templates_bp = Blueprint("task_templates", __name__, url_prefix="/api")

_DEFAULT_TEMPLATES = [
    {"time": "9:00 a.m.", "platform": ["fb", "igfeed"], "label": "Publicar banner", "desc": ""},
    {"time": "12:00 m.", "platform": ["igstory"], "label": "Publicar story", "desc": ""},
    {"time": "5:00 p.m.", "platform": ["wa"], "label": "Estado de WhatsApp", "desc": ""},
]


def _seed_templates():
    return [{"id": uuid.uuid4().hex[:10], **t} for t in _DEFAULT_TEMPLATES]


def _templates_store():
    return get_store(os.path.join(current_user_dir(), "task_templates.json"), _seed_templates)


def load_templates():
    return _templates_store().load()


def save_templates(templates):
    _templates_store().save(templates)


@task_templates_bp.route("/task-templates", methods=["GET"])
@login_required
def get_templates():
    templates = load_templates()
    templates.sort(key=lambda t: t.get("time", ""))
    return jsonify(templates)


@task_templates_bp.route("/task-templates", methods=["POST"])
@login_required
def create_template():
    data = request.get_json(force=True) or {}
    label = (data.get("label") or "").strip()
    if not label:
        return jsonify({"error": "falta el título de la plantilla"}), 400

    template = {
        "id": uuid.uuid4().hex[:10],
        "time": (data.get("time") or "").strip(),
        "platform": data.get("platform") or [],
        "label": label,
        "desc": (data.get("desc") or "").strip(),
    }

    store = _templates_store()
    with store.lock:
        templates = load_templates()
        templates.append(template)
        save_templates(templates)

    return jsonify(template), 201


@task_templates_bp.route("/task-templates/<template_id>", methods=["PUT"])
@login_required
def update_template(template_id):
    data = request.get_json(force=True) or {}

    store = _templates_store()
    with store.lock:
        templates = load_templates()
        template = next((t for t in templates if t["id"] == template_id), None)
        if not template:
            return jsonify({"error": "plantilla no encontrada"}), 404

        if "time" in data:
            template["time"] = (data.get("time") or "").strip()
        if "platform" in data:
            template["platform"] = data.get("platform") or []
        if "label" in data:
            template["label"] = (data.get("label") or "").strip() or template["label"]
        if "desc" in data:
            template["desc"] = (data.get("desc") or "").strip()

        save_templates(templates)

    return jsonify(template)


@task_templates_bp.route("/task-templates/<template_id>", methods=["DELETE"])
@login_required
def delete_template(template_id):
    store = _templates_store()
    with store.lock:
        templates = load_templates()
        remaining = [t for t in templates if t["id"] != template_id]
        if len(remaining) == len(templates):
            return jsonify({"error": "plantilla no encontrada"}), 404
        save_templates(remaining)

    return jsonify({"ok": True})
