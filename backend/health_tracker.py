"""
health_tracker.py - Health logging, points, levels, streaks
"""

from datetime import date, datetime, timedelta
from database import get_db

LEVELS = [
    (0,    "Getting Started",    "🌱"),
    (100,  "Taking Charge",      "🌿"),
    (300,  "Glowing Up",         "🌸"),
    (600,  "Community Champion", "⭐"),
    (1000, "Nirogini",           "👑"),
]

WEEKLY_CHALLENGES = [
    {"id": "water_week",  "title": "Hydration Hero",
     "desc": "Drink 6+ glasses of water every day this week",
     "desc_hi": "इस हफ्ते हर दिन 6+ गिलास पानी पियें", "points": 50},
    {"id": "walk_week",   "title": "Step Queen",
     "desc": "Walk at least 15 minutes, 3 times this week",
     "desc_hi": "इस हफ्ते 3 बार कम से कम 15 मिनट चलें", "points": 50},
    {"id": "sleep_week",  "title": "Rest & Restore",
     "desc": "Get 7+ hours of sleep for 4 days this week",
     "desc_hi": "इस हफ्ते 4 दिन 7+ घंटे सोएं", "points": 50},
    {"id": "log_week",    "title": "Consistency Queen",
     "desc": "Log your health every day this week",
     "desc_hi": "इस हफ्ते हर दिन अपनी health log करें", "points": 75},
]


def get_level(points):
    level_info = LEVELS[0]
    for threshold, name, emoji in LEVELS:
        if points >= threshold:
            level_info = (threshold, name, emoji)
    return level_info


def log_health(user_id, data):
    conn = get_db()
    try:
        today = date.today().isoformat()
        existing = conn.execute(
            "SELECT id FROM health_logs WHERE user_id = ? AND date = ?",
            (user_id, today)
        ).fetchone()

        points = _calculate_points(data)

        if existing:
            conn.execute("""
                UPDATE health_logs SET
                    water_glasses = ?, steps = ?, sleep_hours = ?,
                    bp_systolic = ?, bp_diastolic = ?, blood_sugar = ?,
                    weight_kg = ?, mood = ?, notes = ?,
                    points_earned = ?
                WHERE user_id = ? AND date = ?
            """, (
                data.get("water_glasses", 0),
                data.get("steps", 0),
                data.get("sleep_hours", 0),
                data.get("bp_systolic"),
                data.get("bp_diastolic"),
                data.get("blood_sugar"),
                data.get("weight_kg"),
                data.get("mood", 3),
                data.get("notes", ""),
                points, user_id, today
            ))
        else:
            conn.execute("""
                INSERT INTO health_logs
                (user_id, date, water_glasses, steps, sleep_hours,
                 bp_systolic, bp_diastolic, blood_sugar, weight_kg,
                 mood, notes, points_earned)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, today,
                data.get("water_glasses", 0),
                data.get("steps", 0),
                data.get("sleep_hours", 0),
                data.get("bp_systolic"),
                data.get("bp_diastolic"),
                data.get("blood_sugar"),
                data.get("weight_kg"),
                data.get("mood", 3),
                data.get("notes", ""),
                points
            ))

        # Update user points and streak
        _update_points_and_streak(conn, user_id, points, today)
        conn.commit()
        return {"success": True, "points_earned": points}
    finally:
        conn.close()


def get_today_log(user_id):
    conn = get_db()
    try:
        today = date.today().isoformat()
        log = conn.execute(
            "SELECT * FROM health_logs WHERE user_id = ? AND date = ?",
            (user_id, today)
        ).fetchone()
        return dict(log) if log else {}
    finally:
        conn.close()


def get_health_history(user_id, days=30):
    conn = get_db()
    try:
        since = (date.today() - timedelta(days=days)).isoformat()
        logs = conn.execute(
            """SELECT * FROM health_logs
               WHERE user_id = ? AND date >= ?
               ORDER BY date ASC""",
            (user_id, since)
        ).fetchall()
        return [dict(l) for l in logs]
    finally:
        conn.close()


def get_user_stats(user_id):
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return {}

        points = user["points"]
        _, level_name, level_emoji = get_level(points)

        # Next level
        next_level = None
        for threshold, name, emoji in LEVELS:
            if threshold > points:
                next_level = {"name": name, "points_needed": threshold - points}
                break

        # Streak
        streak = _calculate_streak(conn, user_id)

        return {
            "points": points,
            "level_name": level_name,
            "level_emoji": level_emoji,
            "streak_days": streak,
            "next_level": next_level,
        }
    finally:
        conn.close()


def get_community_feed(user_id):
    conn = get_db()
    try:
        friends = conn.execute("""
            SELECT u.id, u.name, u.points, u.streak_days, u.level
            FROM connections c
            JOIN users u ON (
                CASE WHEN c.user_id = ? THEN c.friend_id ELSE c.user_id END = u.id
            )
            WHERE (c.user_id = ? OR c.friend_id = ?)
            AND c.status = 'accepted'
            ORDER BY u.points DESC
        """, (user_id, user_id, user_id)).fetchall()

        feed = []
        for f in friends:
            _, level_name, level_emoji = get_level(f["points"])
            feed.append({
                "name": f["name"],
                "points": f["points"],
                "streak_days": f["streak_days"],
                "level_name": level_name,
                "level_emoji": level_emoji,
            })
        return feed
    finally:
        conn.close()


def send_friend_request(user_id, friend_email):
    conn = get_db()
    try:
        friend = conn.execute(
            "SELECT id, name FROM users WHERE email = ?",
            (friend_email.lower(),)
        ).fetchone()
        if not friend:
            return {"success": False, "error": "No user found with this email."}
        if friend["id"] == user_id:
            return {"success": False, "error": "You cannot add yourself."}
        existing = conn.execute(
            """SELECT id FROM connections
               WHERE (user_id = ? AND friend_id = ?)
               OR (user_id = ? AND friend_id = ?)""",
            (user_id, friend["id"], friend["id"], user_id)
        ).fetchone()
        if existing:
            return {"success": False, "error": "Request already sent or already connected."}
        conn.execute(
            "INSERT INTO connections (user_id, friend_id) VALUES (?, ?)",
            (user_id, friend["id"])
        )
        conn.commit()
        return {"success": True, "message": f"Friend request sent to {friend['name']}!"}
    finally:
        conn.close()


def accept_friend_request(user_id, requester_id):
    conn = get_db()
    try:
        conn.execute(
            """UPDATE connections SET status = 'accepted'
               WHERE user_id = ? AND friend_id = ?""",
            (requester_id, user_id)
        )
        conn.commit()
        return {"success": True}
    finally:
        conn.close()


def get_pending_requests(user_id):
    conn = get_db()
    try:
        requests = conn.execute("""
            SELECT u.id, u.name, u.email, c.created_at
            FROM connections c
            JOIN users u ON c.user_id = u.id
            WHERE c.friend_id = ? AND c.status = 'pending'
        """, (user_id,)).fetchall()
        return [dict(r) for r in requests]
    finally:
        conn.close()


def _calculate_points(data):
    points = 0
    if data.get("water_glasses", 0) >= 6:
        points += 10
    elif data.get("water_glasses", 0) >= 3:
        points += 5
    if data.get("steps", 0) >= 5000:
        points += 10
    elif data.get("steps", 0) >= 2000:
        points += 5
    if data.get("sleep_hours", 0) >= 7:
        points += 10
    elif data.get("sleep_hours", 0) >= 5:
        points += 5
    if data.get("bp_systolic"):
        points += 5
    if data.get("blood_sugar"):
        points += 5
    return points


def _update_points_and_streak(conn, user_id, new_points, today):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    yesterday_log = conn.execute(
        "SELECT id FROM health_logs WHERE user_id = ? AND date = ?",
        (user_id, yesterday)
    ).fetchone()
    user = conn.execute(
        "SELECT streak_days FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    streak = (user["streak_days"] + 1) if yesterday_log else 1
    streak_bonus = 5 if streak % 7 == 0 else 0
    conn.execute(
        """UPDATE users SET
           points = points + ?,
           streak_days = ?,
           last_checkin = ?
           WHERE id = ?""",
        (new_points + streak_bonus, streak, today, user_id)
    )


def _calculate_streak(conn, user_id):
    logs = conn.execute(
        """SELECT date FROM health_logs WHERE user_id = ?
           ORDER BY date DESC LIMIT 30""",
        (user_id,)
    ).fetchall()
    if not logs:
        return 0
    streak = 0
    check_date = date.today()
    for log in logs:
        log_date = date.fromisoformat(log["date"])
        if log_date == check_date or log_date == check_date - timedelta(days=1):
            streak += 1
            check_date = log_date - timedelta(days=1)
        else:
            break
    return streak
