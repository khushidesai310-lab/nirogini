"""
companion.py - Nirogini's AI companion powered by Groq
Bilingual (Hindi/English), sisterly tone, health-aware.
"""

import os
import json
import requests
from database import get_db

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"

SYSTEM_EN = """You are Nirogini, a warm and caring AI health companion — like a younger sister who genuinely cares about women's health.

You are talking to a woman who is probably in her 40s or 50s, likely Indian, who puts everyone else before herself.

Your personality:
- Friendly, casual, like texting a close friend
- Never preachy or lecturing
- Celebrate small wins enthusiastically
- Never make her feel guilty
- Connect her health to her family's wellbeing naturally
- When she mentions symptoms, listen first, then gently guide
- Only suggest hospital when genuinely necessary
- Keep responses short — she is busy

Your health knowledge:
- You know her complete health profile and history
- You understand perimenopause and menopause symptoms
- You know Indian diet and lifestyle context
- You suggest budget-friendly options naturally
- You know government health schemes like Ayushman Bharat

Rules:
- Never use em-dashes (—) or double dashes (--) in responses. Use plain sentences.
- Never diagnose
- Always recommend doctor for serious symptoms
- Keep it conversational — max 4-5 sentences unless she asks for more
- Use emojis naturally but not excessively
- Address her by name + ji (e.g. Priya ji)"""

SYSTEM_HI = """आप Nirogini हैं — एक caring AI health companion, जैसे एक छोटी बहन जो सच में care करती है।

आप एक ऐसी महिला से बात कर रहे हैं जो शायद 40-50 साल की है, भारतीय है, और हमेशा सबको खुद से पहले रखती है।

आपकी personality:
- Friendly और casual — जैसे WhatsApp पर किसी close friend को message करना
- कभी lecture मत दो
- छोटी-छोटी जीत भी celebrate करो
- Guilty feel मत कराओ
- उनकी health को family की wellbeing से naturally connect करो
- जब वो symptoms बताएं — पहले सुनो, फिर gently guide करो
- Hospital तभी suggest करो जब सच में जरूरी हो

Rules:
- Response में em-dash (—) या double dash (--) use मत करो।
- कभी diagnose मत करो
- Serious symptoms के लिए हमेशा doctor recommend करो
- Short रखो — max 4-5 sentences
- Emojis naturally use करो
- उनके नाम के साथ जी लगाओ (e.g. Priya जी)"""


def get_companion_response(user_id, message, language="en"):
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return {"success": False, "error": "User not found."}

        history = conn.execute(
            """SELECT role, message FROM chat_history
               WHERE user_id = ? ORDER BY timestamp DESC LIMIT 20""",
            (user_id,)
        ).fetchall()

        health_context = _build_health_context(conn, user_id, dict(user))
        system = (SYSTEM_HI if language == "hi" else SYSTEM_EN) + f"\n\nUSER HEALTH PROFILE:\n{health_context}"

        messages = [{"role": "system", "content": system}]
        for h in reversed(history):
            messages.append({"role": h["role"], "content": h["message"]})
        messages.append({"role": "user", "content": message})

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return {"success": False, "error": "GROQ_API_KEY not set."}

        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL, "messages": messages,
                  "max_tokens": 400, "temperature": 0.8},
            timeout=30,
        )
        resp.raise_for_status()
        reply = resp.json()["choices"][0]["message"]["content"]

        conn.execute(
            "INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)",
            (user_id, "user", message)
        )
        conn.execute(
            "INSERT INTO chat_history (user_id, role, message) VALUES (?, ?, ?)",
            (user_id, "assistant", reply)
        )
        conn.commit()
        return {"success": True, "reply": reply}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except requests.exceptions.HTTPError as e:
        if e.response and e.response.status_code == 401:
            return {"success": False, "error": "Invalid API key."}
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()


def get_daily_greeting(user_id, language="en"):
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return {"success": False, "error": "User not found"}

        from datetime import date
        today_log = conn.execute(
            "SELECT * FROM health_logs WHERE user_id = ? AND date = ?",
            (user_id, date.today().isoformat())
        ).fetchone()

        health_context = _build_health_context(conn, user_id, dict(user))
        name = user["name"].split()[0]

        if language == "hi":
            prompt = f"""Generate a warm, friendly good morning greeting for {name} जी in casual Hindi (not shudh Hindi — like texting a friend).

Include:
1. A warm greeting based on their health data
2. One gentle nudge about water or food
3. Ask how they and their family are doing

Keep it short — 3-4 lines max. Use emojis naturally.

Their health context: {health_context}
Today's log so far: {dict(today_log) if today_log else 'Nothing logged yet'}"""
        else:
            prompt = f"""Generate a warm, friendly good morning message for {name} ji.

Include:
1. A warm, personal greeting based on their health data
2. One gentle fun nudge about water, food, or movement
3. Ask how they and their family are doing

Keep it short — 3-4 lines. Casual and friendly like a caring sister. Use emojis naturally.

Their health context: {health_context}
Today's log so far: {dict(today_log) if today_log else 'Nothing logged yet'}"""

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            name = user["name"].split()[0]
            greeting = (f"Good morning {name} ji! Hope you and your family are doing well today 🌸 Don't forget to drink some water!"
                       if language == "en"
                       else f"Good morning {name} जी! आप और आपका परिवार कैसा है? 🌸 पानी पीना मत भूलना!")
            return {"success": True, "greeting": greeting}

        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 150, "temperature": 0.9},
            timeout=20,
        )
        resp.raise_for_status()
        greeting = resp.json()["choices"][0]["message"]["content"]
        return {"success": True, "greeting": greeting}
    except Exception as e:
        name = user["name"].split()[0] if user else "there"
        return {"success": True,
                "greeting": f"Good morning {name} ji! How are you and your family today? 🌸"}
    finally:
        conn.close()


def _build_health_context(conn, user_id, user):
    from datetime import date, timedelta
    recent = conn.execute(
        """SELECT * FROM health_logs WHERE user_id = ?
           ORDER BY date DESC LIMIT 7""",
        (user_id,)
    ).fetchall()

    context = f"""
Name: {user.get('name')}
Age: {user.get('age')}
City: {user.get('city')}
Medical conditions: {user.get('medical_conditions') or 'None mentioned'}
Points: {user.get('points')} | Level: {user.get('level')}
Streak: {user.get('streak_days')} days
"""
    if recent:
        last = dict(recent[0])
        context += f"""
Last logged: {last.get('date')}
BP: {last.get('bp_systolic')}/{last.get('bp_diastolic')}
Water glasses: {last.get('water_glasses')}
Steps: {last.get('steps')}
Sleep: {last.get('sleep_hours')} hours
Blood sugar: {last.get('blood_sugar')}
Mood: {last.get('mood')}/5
"""
    return context
