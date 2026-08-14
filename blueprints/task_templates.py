import os
import uuid

from flask import Blueprint, jsonify, request

from auth import login_required
from paths import DATA_DIR
from storage import JSONStore

task_templates_bp = Blueprint("task_templates", __name__, url_prefix="/api")

_templates_store = JSONStore(os.path.join(DATA_DIR, "task_templates.json"), default_factory=list)


def load_templates():
    return _templates_store.load()


def save_templates(templates):
    _templates_store.save(templates)


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

    with _templates_store.lock:
        templates = load_templates()
        templates.append(template)
        save_templates(templates)

    return jsonify(template), 201


@task_templates_bp.route("/task-templates/<template_id>", methods=["PUT"])
@login_required
def update_template(template_id):
    data = request.get_json(force=True) or {}

    with _templates_store.lock:
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
    with _templates_store.lock:
        templates = load_templates()
        remaining = [t for t in templates if t["id"] != template_id]
        if len(remaining) == len(templates):
            return jsonify({"error": "plantilla no encontrada"}), 404
        save_templates(remaining)

    return jsonify({"ok": True})
