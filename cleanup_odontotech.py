"""
Elimina cualquier campaña que tenga "OdontoTech" en el nombre o el id,
tanto del archivo global viejo (de antes del sistema de usuarios) como
de cada carpeta de usuario. No toca ninguna otra campaña.

Uso, desde la carpeta del proyecto (con el venv activado):

    python3 cleanup_odontotech.py
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def clean_file(path):
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        try:
            campaigns = json.load(f)
        except json.JSONDecodeError:
            return 0

    before = len(campaigns)
    campaigns = [
        c for c in campaigns
        if "odontotech" not in c.get("name", "").lower()
        and "odontotech" not in c.get("id", "").lower()
    ]
    removed = before - len(campaigns)

    if removed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(campaigns, f, ensure_ascii=False, indent=2)

    return removed


def main():
    total = 0

    # archivo global de antes del sistema de usuarios (si todavía existe)
    total += clean_file(os.path.join(DATA_DIR, "campaigns.json"))

    # una carpeta por usuario en el sistema nuevo
    users_dir = os.path.join(DATA_DIR, "users")
    if os.path.isdir(users_dir):
        for user_id in os.listdir(users_dir):
            total += clean_file(os.path.join(users_dir, user_id, "campaigns.json"))

    print(f"Listo. Se eliminaron {total} campaña(s) con OdontoTech en el nombre.")


if __name__ == "__main__":
    main()
