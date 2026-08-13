import os
import uuid
from datetime import datetime

from cryptography.fernet import Fernet
from flask import Blueprint, jsonify, request

from auth import login_required
from paths import DATA_DIR
from storage import JSONStore, get_or_create_file_key

vault_bp = Blueprint("vault", __name__, url_prefix="/api")

_vault_store = JSONStore(os.path.join(DATA_DIR, "vault.json"), default_factory=list)

_env_key = os.environ.get("VAULT_KEY", "")
_FERNET_KEY = _env_key.encode() if _env_key else get_or_create_file_key(
    os.path.join(DATA_DIR, "vault.key"), Fernet.generate_key
)
_fernet = Fernet(_FERNET_KEY)


def load_vault():
    return _vault_store.load()


def save_vault(entries):
    _vault_store.save(entries)


def _public_entry(entry):
    return {k: v for k, v in entry.items() if k != "password_enc"}


@vault_bp.route("/vault", methods=["GET"])
@login_required
def get_vault():
    entries = load_vault()
    entries.sort(key=lambda e: e.get("name", "").lower())
    return jsonify([_public_entry(e) for e in entries])


@vault_bp.route("/vault", methods=["POST"])
@login_required
def create_vault_entry():
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    password = data.get("password") or ""
    if not name:
        return jsonify({"error": "falta el nombre"}), 400
    if not password:
        return jsonify({"error": "falta la contraseña"}), 400

    entry = {
        "id": uuid.uuid4().hex[:12],
        "name": name,
        "username": (data.get("username") or "").strip(),
        "url": (data.get("url") or "").strip(),
        "notes": (data.get("notes") or "").strip(),
        "password_enc": _fernet.encrypt(password.encode()).decode(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "updated_at": datetime.now().isoformat(timespec="seconds"),
    }

    with _vault_store.lock:
        entries = load_vault()
        entries.append(entry)
        save_vault(entries)

    return jsonify(_public_entry(entry)), 201


@vault_bp.route("/vault/<entry_id>", methods=["PUT"])
@login_required
def update_vault_entry(entry_id):
    data = request.get_json(force=True) or {}

    with _vault_store.lock:
        entries = load_vault()
        entry = next((e for e in entries if e["id"] == entry_id), None)
        if not entry:
            return jsonify({"error": "entrada no encontrada"}), 404

        if "name" in data:
            entry["name"] = (data.get("name") or "").strip() or entry["name"]
        if "username" in data:
            entry["username"] = (data.get("username") or "").strip()
        if "url" in data:
            entry["url"] = (data.get("url") or "").strip()
        if "notes" in data:
            entry["notes"] = (data.get("notes") or "").strip()
        if data.get("password"):
            entry["password_enc"] = _fernet.encrypt(data["password"].encode()).decode()
        entry["updated_at"] = datetime.now().isoformat(timespec="seconds")

        save_vault(entries)

    return jsonify(_public_entry(entry))


@vault_bp.route("/vault/<entry_id>", methods=["DELETE"])
@login_required
def delete_vault_entry(entry_id):
    with _vault_store.lock:
        entries = load_vault()
        remaining = [e for e in entries if e["id"] != entry_id]
        if len(remaining) == len(entries):
            return jsonify({"error": "entrada no encontrada"}), 404
        save_vault(remaining)

    return jsonify({"ok": True})


@vault_bp.route("/vault/<entry_id>/reveal", methods=["GET"])
@login_required
def reveal_vault_entry(entry_id):
    entries = load_vault()
    entry = next((e for e in entries if e["id"] == entry_id), None)
    if not entry:
        return jsonify({"error": "entrada no encontrada"}), 404

    password = _fernet.decrypt(entry["password_enc"].encode()).decode()
    return jsonify({"password": password})
