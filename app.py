from flask import Flask, render_template

from auth import auth_bp, init_auth, login_required
from blueprints.campaigns import campaigns_bp
from blueprints.ideas import ideas_bp
from blueprints.projects import projects_bp
from blueprints.vault import vault_bp

app = Flask(__name__)
init_auth(app)

app.register_blueprint(auth_bp)
app.register_blueprint(campaigns_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(ideas_bp)
app.register_blueprint(vault_bp)


@app.route("/")
@login_required
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
