"""
auth.py - Authentication for Nirogini
Secure signup, login, session management.
"""

import secrets
import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db


def is_valid_email(email):
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None


def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    if not re.search(r"[!@#$%^&*]", password):
        return False, "Password must contain at least one special character."
    return True, "Strong password."


def signup(name, email, password, confirm_password, language="en"):
    if not name or not email or not password:
        return {"success": False, "error": "All fields are required."}
    if not is_valid_email(email):
        return {"success": False, "error": "Please enter a valid email address."}
    if password != confirm_password:
        return {"success": False, "error": "Passwords do not match."}
    valid, msg = is_strong_password(password)
    if not valid:
        return {"success": False, "error": msg}

    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email.lower(),)
        ).fetchone()
        if existing:
            return {"success": False, "error": "An account with this email already exists."}

        password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        conn.execute(
            """INSERT INTO users (name, email, password_hash, language)
               VALUES (?, ?, ?, ?)""",
            (name.strip(), email.lower(), password_hash, language)
        )
        conn.commit()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email.lower(),)
        ).fetchone()
        token = _create_session(conn, user["id"])
        conn.commit()
        return {
            "success": True,
            "token": token,
            "user": _user_dict(user),
        }
    finally:
        conn.close()


def login(email, password):
    if not email or not password:
        return {"success": False, "error": "Email and password are required."}
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email.lower(),)
        ).fetchone()
        if not user or not check_password_hash(user["password_hash"], password):
            return {"success": False, "error": "Invalid email or password."}
        token = _create_session(conn, user["id"])
        conn.commit()
        return {
            "success": True,
            "token": token,
            "user": _user_dict(user),
        }
    finally:
        conn.close()


def logout(token):
    conn = get_db()
    try:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
    finally:
        conn.close()
    return {"success": True}


def get_user_from_token(token):
    if not token:
        return None
    conn = get_db()
    try:
        session = conn.execute(
            "SELECT user_id FROM sessions WHERE token = ?", (token,)
        ).fetchone()
        if not session:
            return None
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()


def update_profile(user_id, data):
    conn = get_db()
    try:
        fields = ["age", "height_cm", "weight_kg", "city",
                  "language", "medical_conditions", "family_members"]
        updates = {k: data[k] for k in fields if k in data}
        if not updates:
            return {"success": True}
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [user_id]
        conn.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
        conn.commit()
        return {"success": True}
    finally:
        conn.close()


def _create_session(conn, user_id):
    token = secrets.token_hex(32)
    conn.execute(
        "INSERT INTO sessions (token, user_id) VALUES (?, ?)",
        (token, user_id)
    )
    return token


def _user_dict(user):
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "language": user["language"],
        "level": user["level"],
        "points": user["points"],
        "streak_days": user["streak_days"],
        "city": user["city"],
        "age": user["age"],
    }
