from flask import Blueprint, redirect, render_template, url_for

from auth import admin_required, load_users, save_users

users_bp = Blueprint("users_admin", __name__, url_prefix="/admin")


@users_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    users = load_users()
    users.sort(key=lambda u: (u["status"] != "pending", u.get("created_at", "")))
    return render_template("admin_users.html", users=users)


@users_bp.route("/users/<user_id>/approve", methods=["POST"])
@admin_required
def approve_user(user_id):
    users = load_users()
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        user["status"] = "approved"
        save_users(users)
    return redirect(url_for("users_admin.list_users"))


@users_bp.route("/users/<user_id>/reject", methods=["POST"])
@admin_required
def reject_user(user_id):
    users = load_users()
    remaining = [u for u in users if u["id"] != user_id]
    save_users(remaining)
    return redirect(url_for("users_admin.list_users"))
