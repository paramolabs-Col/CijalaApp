# Panel de campañas e ideas

App Flask modular para DentalSync / Páramo Labs:

- **Campañas**: checklist de publicación en redes, multi-mes (duplicar y editar).
- **Ideas**: captura rápida de pensamientos, con proyectos y tags, exportable a `.md`.
- **Baúl**: contraseñas encriptadas con clave maestra.

Todo detrás de un login general.

## Estructura

```
app.py              # arma la app y registra los blueprints
auth.py              # login general del sitio
paths.py             # BASE_DIR / DATA_DIR
storage.py           # JSONStore genérico + persistencia de claves
seed_campaigns.py    # datos iniciales de campaña
blueprints/          # campaigns, projects, ideas, vault (una ruta por archivo)
templates/           # login.html, index.html + partials por sección
static/css/          # theme.css compartido + un css por sección
static/js/           # un js por sección + tabs.js
```

## Desarrollo local

```
pip install -r requirements.txt
$env:SITE_PASSWORD="tu-contraseña"
python app.py
```

## Despliegue en PythonAnywhere

1. Subir esta carpeta completa (Git o manual).
2. Configurar `SITE_PASSWORD` en Web > Environment variables.
3. Apuntar el WSGI a `app.py` (`from app import app`).
4. `data/flask_secret.key` y `data/vault.key` se generan solos en el primer arranque — hacerles backup fuera del repo (ya están en `.gitignore`, junto con el resto de `data/`).
