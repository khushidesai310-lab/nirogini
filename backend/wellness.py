"""
wellness.py - Menopause tracker, medicines, cycle, appointments
"""
from datetime import date, datetime, timedelta
from database import get_db


# ─── MENOPAUSE TRACKER ───────────────────────────────────────────

def log_menopause(user_id, data):
    conn = get_db()
    try:
        today = date.today().isoformat()
        existing = conn.execute(
            "SELECT id FROM menopause_logs WHERE user_id=? AND date=?",
            (user_id, today)
        ).fetchone()
        if existing:
            conn.execute("""
                UPDATE menopause_logs SET
                  hot_flashes=?, night_sweats=?, mood=?, sleep_quality=?,
                  joint_pain=?, brain_fog=?, anxiety=?, notes=?
                WHERE user_id=? AND date=?""",
                (data.get("hot_flashes",0), data.get("night_sweats",0),
                 data.get("mood",3), data.get("sleep_quality",3),
                 data.get("joint_pain",0), data.get("brain_fog",0),
                 data.get("anxiety",0), data.get("notes",""),
                 user_id, today))
        else:
            conn.execute("""
                INSERT INTO menopause_logs
                (user_id,date,hot_flashes,night_sweats,mood,sleep_quality,
                 joint_pain,brain_fog,anxiety,notes)
                VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (user_id, today,
                 data.get("hot_flashes",0), data.get("night_sweats",0),
                 data.get("mood",3), data.get("sleep_quality",3),
                 data.get("joint_pain",0), data.get("brain_fog",0),
                 data.get("anxiety",0), data.get("notes","")))
        conn.commit()
        return {"success": True}
    finally:
        conn.close()

def get_menopause_history(user_id, days=30):
    conn = get_db()
    try:
        since = (date.today() - timedelta(days=days)).isoformat()
        rows = conn.execute(
            "SELECT * FROM menopause_logs WHERE user_id=? AND date>=? ORDER BY date ASC",
            (user_id, since)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_today_menopause(user_id):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT * FROM menopause_logs WHERE user_id=? AND date=?",
            (user_id, date.today().isoformat())
        ).fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()


# ─── MEDICINES ────────────────────────────────────────────────────

def add_medicine(user_id, data):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO medicines(user_id,name,dosage,frequency,time_of_day) VALUES(?,?,?,?,?)",
            (user_id, data.get("name",""), data.get("dosage",""),
             data.get("frequency","daily"), data.get("time_of_day","morning"))
        )
        conn.commit()
        return {"success": True}
    finally:
        conn.close()

def get_medicines(user_id):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM medicines WHERE user_id=? AND is_active=1 ORDER BY time_of_day, name",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def delete_medicine(user_id, medicine_id):
    conn = get_db()
    try:
        conn.execute(
            "UPDATE medicines SET is_active=0 WHERE id=? AND user_id=?",
            (medicine_id, user_id)
        )
        conn.commit()
        return {"success": True}
    finally:
        conn.close()


# ─── CYCLE TRACKER ────────────────────────────────────────────────

def log_cycle(user_id, data):
    conn = get_db()
    try:
        conn.execute(
            """INSERT INTO cycle_logs(user_id,period_start,period_end,flow_level,symptoms,notes)
               VALUES(?,?,?,?,?,?)""",
            (user_id, data.get("period_start"), data.get("period_end"),
             data.get("flow_level","medium"),
             data.get("symptoms",""), data.get("notes",""))
        )
        conn.commit()
        return {"success": True}
    finally:
        conn.close()

def get_cycle_history(user_id):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM cycle_logs WHERE user_id=? ORDER BY period_start DESC LIMIT 12",
            (user_id,)
        ).fetchall()
        logs = [dict(r) for r in rows]
        # Calculate average cycle length
        avg_cycle = None
        if len(logs) >= 2:
            starts = [date.fromisoformat(l["period_start"]) for l in logs if l["period_start"]]
            if len(starts) >= 2:
                gaps = [(starts[i] - starts[i+1]).days for i in range(len(starts)-1)]
                avg_cycle = round(sum(gaps) / len(gaps))
        return {"logs": logs, "avg_cycle_days": avg_cycle}
    finally:
        conn.close()


# ─── APPOINTMENTS ─────────────────────────────────────────────────

def add_appointment(user_id, data):
    conn = get_db()
    try:
        conn.execute(
            """INSERT INTO appointments
               (user_id,doctor_name,speciality,appointment_date,appointment_time,location,questions,notes)
               VALUES(?,?,?,?,?,?,?,?)""",
            (user_id, data.get("doctor_name",""), data.get("speciality",""),
             data.get("appointment_date"), data.get("appointment_time",""),
             data.get("location",""), data.get("questions",""), data.get("notes",""))
        )
        conn.commit()
        return {"success": True}
    finally:
        conn.close()

def get_appointments(user_id):
    conn = get_db()
    try:
        today = date.today().isoformat()
        upcoming = conn.execute(
            """SELECT * FROM appointments WHERE user_id=? AND appointment_date>=? AND is_completed=0
               ORDER BY appointment_date ASC""",
            (user_id, today)
        ).fetchall()
        past = conn.execute(
            """SELECT * FROM appointments WHERE user_id=? AND (appointment_date<? OR is_completed=1)
               ORDER BY appointment_date DESC LIMIT 5""",
            (user_id, today)
        ).fetchall()
        return {"upcoming": [dict(r) for r in upcoming], "past": [dict(r) for r in past]}
    finally:
        conn.close()

def complete_appointment(user_id, appt_id, notes=""):
    conn = get_db()
    try:
        conn.execute(
            "UPDATE appointments SET is_completed=1, notes=? WHERE id=? AND user_id=?",
            (notes, appt_id, user_id)
        )
        conn.commit()
        return {"success": True}
    finally:
        conn.close()

def delete_appointment(user_id, appt_id):
    conn = get_db()
    try:
        conn.execute("DELETE FROM appointments WHERE id=? AND user_id=?", (appt_id, user_id))
        conn.commit()
        return {"success": True}
    finally:
        conn.close()
