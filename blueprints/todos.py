import os
import uuid
from datetime import datetime

from flask import Blueprint, jsonify, request

from auth import current_user_dir, login_required
from storage import get_store

todos_bp = Blueprint("todos", __name__, url_prefix="/api")

VALID_PRIORITIES = {"urgent", "medium", "low"}


def _todos_store():
    return get_store(os.path.join(current_user_dir(), "todos.json"), list)


def load_todos():
    return _todos_store().load()


def save_todos(todos):
    _todos_store().save(todos)


@todos_bp.route("/todos", methods=["GET"])
@login_required
def get_todos():
    return jsonify(load_todos())


@todos_bp.route("/todos", methods=["POST"])
@login_required
def create_todo():
    data = request.get_json(force=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "falta el texto de la tarea"}), 400

    todo = {
        "id": uuid.uuid4().hex[:10],
        "text": text,
        "priority": data.get("priority", "medium") if data.get("priority") in VALID_PRIORITIES else "medium",
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    store = _todos_store()
    with store.lock:
        todos = load_todos()
        todos.append(todo)
        save_todos(todos)

    return jsonify(todo), 201


@todos_bp.route("/todos/<todo_id>", methods=["PUT"])
@login_required
def update_todo(todo_id):
    data = request.get_json(force=True) or {}
    store = _todos_store()
    with store.lock:
        todos = load_todos()
        todo = next((t for t in todos if t["id"] == todo_id), None)
        if not todo:
            return jsonify({"error": "tarea no encontrada"}), 404
        if "done" in data:
            todo["done"] = bool(data["done"])
        if "text" in data:
            todo["text"] = (data["text"] or "").strip() or todo["text"]
        if "priority" in data and data["priority"] in VALID_PRIORITIES:
            todo["priority"] = data["priority"]
        save_todos(todos)
    return jsonify(todo)


@todos_bp.route("/todos/<todo_id>", methods=["DELETE"])
@login_required
def delete_todo(todo_id):
    store = _todos_store()
    with store.lock:
        todos = load_todos()
        remaining = [t for t in todos if t["id"] != todo_id]
        if len(remaining) == len(todos):
            return jsonify({"error": "tarea no encontrada"}), 404
        save_todos(remaining)
    return jsonify({"ok": True})
