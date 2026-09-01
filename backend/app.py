"""
app.py - Nirogini Flask API
Because when she's well, everyone's well.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

import auth
import health_tracker
import wellness
import companion
import hospitals
import recommendations
from database import init_db

FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend"
)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# Initialise database on startup
init_db()


def get_token():
    h = request.headers.get("Authorization", "")
    return h.split(" ", 1)[1] if h.startswith("Bearer ") else None


def require_auth():
    user = auth.get_user_from_token(get_token())
    if not user:
        return None, (jsonify({"success": False, "error": "Not authenticated."}), 401)
    return user, None


# Frontend
@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)


# Auth
@app.route("/api/signup", methods=["POST"])
def signup():
    d = request.get_json(force=True)
    result = auth.signup(
        d.get("name", "").strip(),
        d.get("email", "").strip(),
        d.get("password", ""),
        d.get("confirm_password", ""),
        d.get("language", "en")
    )
    return jsonify(result), (200 if result["success"] else 400)

@app.route("/api/login", methods=["POST"])
def login():
    d = request.get_json(force=True)
    result = auth.login(d.get("email", "").strip(), d.get("password", ""))
    return jsonify(result), (200 if result["success"] else 401)

@app.route("/api/logout", methods=["POST"])
def logout():
    return jsonify(auth.logout(get_token()))

@app.route("/api/me", methods=["GET"])
def me():
    user, err = require_auth()
    if err: return err
    return jsonify({"success": True, "user": user})

@app.route("/api/profile", methods=["PUT"])
def update_profile():
    user, err = require_auth()
    if err: return err
    data = request.get_json(force=True)
    result = auth.update_profile(user["id"], data)
    return jsonify(result)


# Health tracking
@app.route("/api/health/log", methods=["POST"])
def log_health():
    user, err = require_auth()
    if err: return err
    data = request.get_json(force=True)
    result = health_tracker.log_health(user["id"], data)
    return jsonify(result)

@app.route("/api/health/today", methods=["GET"])
def today_log():
    user, err = require_auth()
    if err: return err
    log = health_tracker.get_today_log(user["id"])
    return jsonify({"success": True, "log": log})

@app.route("/api/health/history", methods=["GET"])
def health_history():
    user, err = require_auth()
    if err: return err
    days = int(request.args.get("days", 30))
    history = health_tracker.get_health_history(user["id"], days)
    return jsonify({"success": True, "history": history})

@app.route("/api/health/stats", methods=["GET"])
def user_stats():
    user, err = require_auth()
    if err: return err
    stats = health_tracker.get_user_stats(user["id"])
    return jsonify({"success": True, "stats": stats})


# Companion chat
@app.route("/api/companion/chat", methods=["POST"])
def chat():
    user, err = require_auth()
    if err: return err
    data = request.get_json(force=True)
    message = data.get("message", "").strip()
    language = data.get("language", user.get("language", "en"))
    if not message:
        return jsonify({"success": False, "error": "Message is empty."}), 400
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return jsonify({"success": False, "error": "GROQ_API_KEY not set. Please set it and restart the server."}), 500
    result = companion.get_companion_response(user["id"], message, language)
    return jsonify(result)

@app.route("/api/companion/greeting", methods=["GET"])
def greeting():
    user, err = require_auth()
    if err: return err
    language = request.args.get("lang", user.get("language", "en"))
    result = companion.get_daily_greeting(user["id"], language)
    return jsonify(result)


# Recommendations
@app.route("/api/recommendations/daily", methods=["GET"])
def daily_recommendations():
    user, err = require_auth()
    if err: return err
    language = request.args.get("lang", user.get("language", "en"))
    today_log = health_tracker.get_today_log(user["id"])
    plan = recommendations.get_daily_plan(user, today_log, language)
    return jsonify({"success": True, "plan": plan})

@app.route("/api/recommendations/report", methods=["POST"])
def explain_report():
    user, err = require_auth()
    if err: return err
    data = request.get_json(force=True)
    language = data.get("language", user.get("language", "en"))
    report_values = data.get("report_values", "")
    if not report_values:
        return jsonify({"success": False, "error": "Please enter report values."}), 400
    result = recommendations.explain_report(report_values, language)
    return jsonify({"success": True, "explanation": result})


# Hospitals
@app.route("/api/hospitals", methods=["GET"])
def get_hospitals():
    city = request.args.get("city", "mumbai")
    budget = request.args.get("budget", "any")
    speciality = request.args.get("speciality")
    result = hospitals.get_hospitals(city, budget, speciality)
    return jsonify({"success": True, "hospitals": result})

@app.route("/api/hospitals/budget-question", methods=["GET"])
def budget_question():
    language = request.args.get("lang", "en")
    return jsonify({"success": True, "question": hospitals.get_budget_question(language)})


# Community
@app.route("/api/community/feed", methods=["GET"])
def community_feed():
    user, err = require_auth()
    if err: return err
    feed = health_tracker.get_community_feed(user["id"])
    return jsonify({"success": True, "feed": feed})

@app.route("/api/community/add-friend", methods=["POST"])
def add_friend():
    user, err = require_auth()
    if err: return err
    data = request.get_json(force=True)
    friend_email = data.get("email", "").strip()
    result = health_tracker.send_friend_request(user["id"], friend_email)
    return jsonify(result)

@app.route("/api/community/accept", methods=["POST"])
def accept_friend():
    user, err = require_auth()
    if err: return err
    data = request.get_json(force=True)
    result = health_tracker.accept_friend_request(user["id"], data.get("requester_id"))
    return jsonify(result)

@app.route("/api/community/requests", methods=["GET"])
def friend_requests():
    user, err = require_auth()
    if err: return err
    requests_list = health_tracker.get_pending_requests(user["id"])
    return jsonify({"success": True, "requests": requests_list})


# ── Menopause tracker ──────────────────────────────────────────
@app.route("/api/menopause/log", methods=["POST"])
def log_menopause():
    user, err = require_auth()
    if err: return err
    return jsonify(wellness.log_menopause(user["id"], request.get_json(force=True)))

@app.route("/api/menopause/today", methods=["GET"])
def today_menopause():
    user, err = require_auth()
    if err: return err
    return jsonify({"success": True, "log": wellness.get_today_menopause(user["id"])})

@app.route("/api/menopause/history", methods=["GET"])
def menopause_history():
    user, err = require_auth()
    if err: return err
    days = int(request.args.get("days", 30))
    return jsonify({"success": True, "history": wellness.get_menopause_history(user["id"], days)})

# ── Medicines ─────────────────────────────────────────────────
@app.route("/api/medicines", methods=["GET"])
def get_medicines():
    user, err = require_auth()
    if err: return err
    return jsonify({"success": True, "medicines": wellness.get_medicines(user["id"])})

@app.route("/api/medicines/add", methods=["POST"])
def add_medicine():
    user, err = require_auth()
    if err: return err
    return jsonify(wellness.add_medicine(user["id"], request.get_json(force=True)))

@app.route("/api/medicines/<int:med_id>/delete", methods=["DELETE"])
def delete_medicine(med_id):
    user, err = require_auth()
    if err: return err
    return jsonify(wellness.delete_medicine(user["id"], med_id))

# ── Cycle tracker ─────────────────────────────────────────────
@app.route("/api/cycle/log", methods=["POST"])
def log_cycle():
    user, err = require_auth()
    if err: return err
    return jsonify(wellness.log_cycle(user["id"], request.get_json(force=True)))

@app.route("/api/cycle/history", methods=["GET"])
def cycle_history():
    user, err = require_auth()
    if err: return err
    return jsonify({"success": True, **wellness.get_cycle_history(user["id"])})

# ── Appointments ──────────────────────────────────────────────
@app.route("/api/appointments", methods=["GET"])
def get_appointments():
    user, err = require_auth()
    if err: return err
    return jsonify({"success": True, **wellness.get_appointments(user["id"])})

@app.route("/api/appointments/add", methods=["POST"])
def add_appointment():
    user, err = require_auth()
    if err: return err
    return jsonify(wellness.add_appointment(user["id"], request.get_json(force=True)))

@app.route("/api/appointments/<int:appt_id>/complete", methods=["POST"])
def complete_appointment(appt_id):
    user, err = require_auth()
    if err: return err
    data = request.get_json(force=True)
    return jsonify(wellness.complete_appointment(user["id"], appt_id, data.get("notes","")))

@app.route("/api/appointments/<int:appt_id>/delete", methods=["DELETE"])
def delete_appointment(appt_id):
    user, err = require_auth()
    if err: return err
    return jsonify(wellness.delete_appointment(user["id"], appt_id))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
