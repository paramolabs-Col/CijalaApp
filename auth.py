import os
import uuid
from datetime import datetime
from functools import wraps

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from paths import DATA_DIR
from storage import JSONStore, get_or_create_file_key

auth_bp = Blueprint("auth", __name__)

_users_store = JSONStore(os.path.join(DATA_DIR, "users.json"), default_factory=list)


def init_auth(app):
    """Configura secret_key de Flask, persistente en disco o por variable de entorno."""
    secret_key_file = os.path.join(DATA_DIR, "flask_secret.key")
    env_secret = os.environ.get("FLASK_SECRET_KEY", "")
    app.secret_key = env_secret.encode() if env_secret else get_or_create_file_key(
        secret_key_file, lambda: os.urandom(32)
    )


def load_users():
    return _users_store.load()


def save_users(users):
    _users_store.save(users)


def current_user():
    users = load_users()
    return next((u for u in users if u["id"] == session.get("user_id")), None)


def current_user_dir():
    """Carpeta de datos exclusiva del usuario logueado (campañas, ideas, baúl, etc)."""
    user_id = session.get("user_id")
    path = os.path.join(DATA_DIR, "users", user_id)
    os.makedirs(path, exist_ok=True)
    return path


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            if request.path.startswith("/api/"):
                return jsonify({"error": "no autenticado"}), 401
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("index"))
        return view(*args, **kwargs)
    return wrapped


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        pw = request.form.get("password", "")
        users = load_users()
        user = next((u for u in users if u["email"] == email), None)

        if not user or not check_password_hash(user["password_hash"], pw):
            error = "Credenciales inválidas"
        elif user["status"] != "approved":
            error = "Tu cuenta todavía no fue aprobada"
        else:
            session["user_id"] = user["id"]
            session["is_admin"] = user.get("is_admin", False)
            session.permanent = True
            return redirect(url_for("index"))

    return render_template("login.html", error=error)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        name = (request.form.get("name") or "").strip()
        role = (request.form.get("role") or "").strip()
        pw = request.form.get("password", "")
        pw2 = request.form.get("password2", "")

        if not email or not pw:
            error = "Completá email y contraseña"
        elif pw != pw2:
            error = "Las contraseñas no coinciden"
        else:
            users = load_users()
            if any(u["email"] == email for u in users):
                error = "Ya existe una cuenta con ese email"
            else:
                is_first = len(users) == 0  # el primer usuario del sistema queda admin y aprobado
                user = {
                    "id": uuid.uuid4().hex[:12],
                    "email": email,
                    "name": name,
                    "role": role,
                    "password_hash": generate_password_hash(pw),
                    "status": "approved" if is_first else "pending",
                    "is_admin": is_first,
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                }
                users.append(user)
                save_users(users)

                if is_first:
                    session["user_id"] = user["id"]
                    session["is_admin"] = True
                    session.permanent = True
                    return redirect(url_for("index"))

                success = "Cuenta creada. Un administrador debe aprobarla antes de que puedas entrar."

    return render_template("register.html", error=error, success=success)


@auth_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    user = current_user()
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        role = (request.form.get("role") or "").strip()
        users = load_users()
        u = next((x for x in users if x["id"] == user["id"]), None)
        if u:
            u["name"] = name
            u["role"] = role
            save_users(users)
        return redirect(url_for("index"))
    return render_template("account.html", user=user)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
