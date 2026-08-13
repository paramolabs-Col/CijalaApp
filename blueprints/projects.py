import os
import uuid

from flask import Blueprint, jsonify, request

from auth import login_required
from paths import DATA_DIR
from storage import JSONStore

projects_bp = Blueprint("projects", __name__, url_prefix="/api")

_DEFAULT_PROJECTS = [
    {"id": "dentalsync", "name": "DentalSync"},
    {"id": "paramo-labs", "name": "Páramo Labs"},
]

_projects_store = JSONStore(os.path.join(DATA_DIR, "projects.json"), default_factory=lambda: list(_DEFAULT_PROJECTS))


def load_projects():
    return _projects_store.load()


def save_projects(projects):
    _projects_store.save(projects)


def slugify(name):
    slug = "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or uuid.uuid4().hex[:8]


@projects_bp.route("/projects", methods=["GET"])
@login_required
def get_projects():
    return jsonify(load_projects())


@projects_bp.route("/projects", methods=["POST"])
@login_required
def create_project():
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "falta el nombre del proyecto"}), 400

    with _projects_store.lock:
        projects = load_projects()
        pid = slugify(name)
        if any(p["id"] == pid for p in projects):
            return jsonify({"error": "ya existe un proyecto con ese nombre"}), 409
        project = {"id": pid, "name": name}
        projects.append(project)
        save_projects(projects)

    return jsonify(project), 201


@projects_bp.route("/projects/<project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id):
    with _projects_store.lock:
        projects = load_projects()
        remaining = [p for p in projects if p["id"] != project_id]
        if len(remaining) == len(projects):
            return jsonify({"error": "proyecto no encontrado"}), 404
        save_projects(remaining)

    return jsonify({"ok": True})
