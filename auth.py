import os
from functools import wraps

from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from paths import DATA_DIR
from storage import get_or_create_file_key

auth_bp = Blueprint("auth", __name__)

_password_hash = None


def init_auth(app):
    """Configura secret_key de Flask y la contraseña general del sitio."""
    global _password_hash

    secret_key_file = os.path.join(DATA_DIR, "flask_secret.key")
    env_secret = os.environ.get("FLASK_SECRET_KEY", "")
    app.secret_key = env_secret.encode() if env_secret else get_or_create_file_key(
        secret_key_file, lambda: os.urandom(32)
    )

    site_password = os.environ.get("SITE_PASSWORD")
    if not site_password:
        print(
            "ADVERTENCIA: variable de entorno SITE_PASSWORD no configurada. "
            "Usando contraseña por defecto 'changeme'. "
            "Configúrala en PythonAnywhere > Web > Environment variables."
        )
        site_password = "changeme"
    _password_hash = generate_password_hash(site_password)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("authed"):
            if request.path.startswith("/api/"):
                return jsonify({"error": "no autenticado"}), 401
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        pw = request.form.get("password", "")
        if check_password_hash(_password_hash, pw):
            session["authed"] = True
            session.permanent = True
            return redirect(url_for("index"))
        error = "Contraseña incorrecta"
    return render_template("login.html", error=error)


@auth_bp.route("/logout")
def logout():
    session.pop("authed", None)
    return redirect(url_for("auth.login"))
