from flask import Flask, render_template, session

from auth import auth_bp, current_user, init_auth, login_required
from blueprints.campaigns import campaigns_bp
from blueprints.day_templates import day_templates_bp
from blueprints.ideas import ideas_bp
from blueprints.projects import projects_bp
from blueprints.task_templates import task_templates_bp
from blueprints.users import users_bp
from blueprints.todos import todos_bp
from blueprints.vault import vault_bp

app = Flask(__name__)
init_auth(app)

app.register_blueprint(auth_bp)
app.register_blueprint(campaigns_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(ideas_bp)
app.register_blueprint(task_templates_bp)
app.register_blueprint(day_templates_bp)
app.register_blueprint(todos_bp)
app.register_blueprint(vault_bp)
app.register_blueprint(users_bp)


@app.route("/")
@login_required
def index():
    user = current_user() or {}
    return render_template(
        "index.html",
        is_admin=session.get("is_admin", False),
        user_name=user.get("name") or (user.get("email", "").split("@")[0] if user.get("email") else "Usuario"),
        user_role=user.get("role", ""),
    )


if __name__ == "__main__":
    app.run(debug=True)
