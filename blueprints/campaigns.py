import os
import uuid
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request

from auth import login_required
from paths import DATA_DIR
from seed_campaigns import seed_campaigns
from storage import JSONStore

campaigns_bp = Blueprint("campaigns", __name__, url_prefix="/api")

_campaigns_store = JSONStore(os.path.join(DATA_DIR, "campaigns.json"), default_factory=list)
_state_store = JSONStore(os.path.join(DATA_DIR, "state.json"), default_factory=dict)


def load_campaigns():
    campaigns = _campaigns_store.load()
    if not campaigns:
        campaigns = seed_campaigns()
        _campaigns_store.save(campaigns)
    return campaigns


def save_campaigns(campaigns):
    _campaigns_store.save(campaigns)


# ---------------- Campañas ----------------
@campaigns_bp.route("/campaigns", methods=["GET"])
@login_required
def get_campaigns():
    return jsonify(load_campaigns())


@campaigns_bp.route("/campaigns", methods=["POST"])
@login_required
def create_campaign():
    data = request.get_json(force=True) or {}
    name = (data.get("name") or "").strip()
    month = (data.get("month") or "").strip()
    source_id = data.get("source_id")
    start_date = (data.get("start_date") or "").strip()
    duration_days = int(data.get("duration_days") or 0)
    shift_days = int(data.get("shift_days") or 0)

    if not name:
        return jsonify({"error": "falta el nombre de la campaña"}), 400

    with _campaigns_store.lock:
        campaigns = load_campaigns()
        new_days = []

        if source_id:
            source = next((c for c in campaigns if c["id"] == source_id), None)
            if not source:
                return jsonify({"error": "campaña origen no encontrada"}), 404

            # si dieron fecha de inicio, se calcula el desplazamiento contra el primer día de la fuente
            if start_date and source["days"]:
                first_source_date = datetime.strptime(source["days"][0]["date"], "%Y-%m-%d")
                shift_days = (datetime.strptime(start_date, "%Y-%m-%d") - first_source_date).days

            for day in source["days"]:
                new_date = datetime.strptime(day["date"], "%Y-%m-%d") + timedelta(days=shift_days)
                new_tasks = [
                    {"id": uuid.uuid4().hex[:8], "time": t["time"], "platform": list(t["platform"]),
                     "label": t["label"], "desc": t["desc"]}
                    for t in day["tasks"]
                ]
                new_days.append({
                    "date": new_date.strftime("%Y-%m-%d"),
                    "phase": day["phase"],
                    "fair": day["fair"],
                    "label": day["label"],
                    "tasks": new_tasks,
                })

        elif start_date and duration_days > 0:
            # campaña en blanco: genera los días del rango, sin tareas — se llenan en el editor
            first_day = datetime.strptime(start_date, "%Y-%m-%d")
            for i in range(duration_days):
                day_date = first_day + timedelta(days=i)
                new_days.append({
                    "date": day_date.strftime("%Y-%m-%d"),
                    "phase": 1,
                    "fair": False,
                    "label": "",
                    "tasks": [],
                })

        campaign = {
            "id": uuid.uuid4().hex[:10],
            "name": name,
            "month": month,
            "days": new_days,
        }
        campaigns.append(campaign)
        save_campaigns(campaigns)

    return jsonify(campaign), 201


@campaigns_bp.route("/campaigns/<campaign_id>", methods=["PUT"])
@login_required
def update_campaign(campaign_id):
    data = request.get_json(force=True) or {}

    with _campaigns_store.lock:
        campaigns = load_campaigns()
        campaign = next((c for c in campaigns if c["id"] == campaign_id), None)
        if not campaign:
            return jsonify({"error": "campaña no encontrada"}), 404

        if "name" in data:
            campaign["name"] = (data.get("name") or "").strip() or campaign["name"]
        if "month" in data:
            campaign["month"] = (data.get("month") or "").strip()
        if "days" in data:
            clean_days = []
            for day in data["days"] or []:
                tasks = []
                for t in day.get("tasks", []):
                    tasks.append({
                        "id": t.get("id") or uuid.uuid4().hex[:8],
                        "time": (t.get("time") or "").strip(),
                        "platform": t.get("platform") or [],
                        "label": (t.get("label") or "").strip(),
                        "desc": (t.get("desc") or "").strip(),
                    })
                clean_days.append({
                    "date": day.get("date"),
                    "phase": int(day.get("phase") or 1),
                    "fair": bool(day.get("fair")),
                    "label": (day.get("label") or "").strip(),
                    "tasks": tasks,
                })
            clean_days.sort(key=lambda dd: dd["date"] or "")
            campaign["days"] = clean_days

        save_campaigns(campaigns)

    return jsonify(campaign)


@campaigns_bp.route("/campaigns/<campaign_id>", methods=["DELETE"])
@login_required
def delete_campaign(campaign_id):
    with _campaigns_store.lock:
        campaigns = load_campaigns()
        remaining = [c for c in campaigns if c["id"] != campaign_id]
        if len(remaining) == len(campaigns):
            return jsonify({"error": "campaña no encontrada"}), 404
        save_campaigns(remaining)

    return jsonify({"ok": True})


# ---------------- Progreso de checklist ----------------
@campaigns_bp.route("/state", methods=["GET"])
@login_required
def get_state():
    return jsonify(_state_store.load())


@campaigns_bp.route("/toggle", methods=["POST"])
@login_required
def toggle():
    data = request.get_json(force=True) or {}
    task_id = data.get("id")
    checked = bool(data.get("checked", False))

    if not task_id:
        return jsonify({"error": "falta el id de la tarea"}), 400

    with _state_store.lock:
        state = _state_store.load()
        state[task_id] = checked
        _state_store.save(state)

    return jsonify({"ok": True, "id": task_id, "checked": checked})


@campaigns_bp.route("/reset", methods=["POST"])
@login_required
def reset():
    data = request.get_json(silent=True) or {}
    campaign_id = data.get("campaign_id")

    with _state_store.lock:
        if campaign_id:
            state = _state_store.load()
            state = {k: v for k, v in state.items() if not k.startswith(f"{campaign_id}::")}
            _state_store.save(state)
        else:
            _state_store.save({})

    return jsonify({"ok": True})
