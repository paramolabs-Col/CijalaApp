import os
import uuid
from datetime import datetime

from flask import Blueprint, Response, jsonify, request

from auth import login_required
from blueprints.projects import load_projects
from paths import DATA_DIR
from storage import JSONStore

ideas_bp = Blueprint("ideas", __name__, url_prefix="/api")

_ideas_store = JSONStore(os.path.join(DATA_DIR, "ideas.json"), default_factory=list)


def load_ideas():
    return _ideas_store.load()


def save_ideas(ideas):
    _ideas_store.save(ideas)


@ideas_bp.route("/ideas", methods=["GET"])
@login_required
def get_ideas():
    ideas = load_ideas()
    ideas.sort(key=lambda i: i.get("created_at", ""), reverse=True)
    return jsonify(ideas)


@ideas_bp.route("/ideas", methods=["POST"])
@login_required
def create_idea():
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "falta el texto de la idea"}), 400

    tags = [t.strip() for t in (data.get("tags") or "").split(",") if t.strip()]
    project = (data.get("project") or "").strip()

    idea = {
        "id": uuid.uuid4().hex[:12],
        "text": text,
        "tags": tags,
        "project": project,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    with _ideas_store.lock:
        ideas = load_ideas()
        ideas.append(idea)
        save_ideas(ideas)

    return jsonify(idea), 201


@ideas_bp.route("/ideas/<idea_id>", methods=["PUT"])
@login_required
def update_idea(idea_id):
    data = request.get_json(force=True) or {}

    with _ideas_store.lock:
        ideas = load_ideas()
        idea = next((i for i in ideas if i["id"] == idea_id), None)
        if not idea:
            return jsonify({"error": "idea no encontrada"}), 404

        if "text" in data:
            idea["text"] = (data.get("text") or "").strip()
        if "tags" in data:
            idea["tags"] = [t.strip() for t in (data.get("tags") or "").split(",") if t.strip()]
        if "project" in data:
            idea["project"] = (data.get("project") or "").strip()
        if "done" in data:
            idea["done"] = bool(data.get("done"))

        save_ideas(ideas)

    return jsonify(idea)


@ideas_bp.route("/ideas/<idea_id>", methods=["DELETE"])
@login_required
def delete_idea(idea_id):
    with _ideas_store.lock:
        ideas = load_ideas()
        remaining = [i for i in ideas if i["id"] != idea_id]
        if len(remaining) == len(ideas):
            return jsonify({"error": "idea no encontrada"}), 404
        save_ideas(remaining)

    return jsonify({"ok": True})


@ideas_bp.route("/ideas/export", methods=["GET"])
@login_required
def export_ideas():
    ideas = load_ideas()
    ideas.sort(key=lambda i: i.get("created_at", ""))

    project_names = {p["id"]: p["name"] for p in load_projects()}

    by_project = {}
    for idea in ideas:
        by_project.setdefault(idea.get("project", ""), []).append(idea)

    lines = ["# Ideas y pensamientos", ""]
    lines.append(f"_Exportado el {datetime.now().strftime('%Y-%m-%d %H:%M')}_")
    lines.append("")

    order = list(project_names.keys()) + [pid for pid in by_project if pid not in project_names and pid] + [""]
    seen = set()
    for project in order:
        if project in seen:
            continue
        seen.add(project)
        group = by_project.get(project)
        if not group:
            continue
        heading = project_names.get(project, project or "Sin proyecto")
        lines.append(f"## {heading}")
        lines.append("")
        for idea in group:
            status = "x" if idea.get("done") else " "
            tags = " ".join(f"`#{t}`" for t in idea.get("tags", []))
            lines.append(f"- [{status}] {idea['text']} {tags}".rstrip())
            lines.append(f"  _{idea.get('created_at', '')}_")
        lines.append("")

    content = "\n".join(lines)
    return Response(
        content,
        mimetype="text/markdown",
        headers={"Content-Disposition": "attachment; filename=ideas.md"},
    )
