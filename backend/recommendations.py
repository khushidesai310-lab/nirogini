"""
recommendations.py - Personalised daily health recommendations
Budget-aware, family-focused, Indian context.
"""

import os
import requests

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"


def get_daily_plan(user_profile, today_log, language="en"):
    name = user_profile.get("name", "").split()[0]
    age = user_profile.get("age", 45)
    medical = user_profile.get("medical_conditions", "None")
    water = today_log.get("water_glasses", 0)
    steps = today_log.get("steps", 0)
    sleep = today_log.get("sleep_hours", 0)

    if language == "hi":
        prompt = f"""आप Nirogini हैं — एक caring health companion।

{name} जी के लिए एक personalized daily health plan बनाएं।

उनकी details:
- Age: {age} years
- Medical conditions: {medical}
- आज का log: पानी {water} गिलास, steps {steps}, नींद {sleep} घंटे

JSON में respond करें (कोई extra text नहीं, em-dash नहीं):
{{
  "water_tip": "पानी के बारे में fun और friendly tip (1-2 lines)",
  "food_tip": "आज का meal suggestion जो family के लिए भी अच्छा हो — Indian food, budget-friendly (2-3 lines)",
  "movement_tip": "Easy movement suggestion — realistic for a busy woman (1-2 lines)",
  "self_care": "एक छोटा self-care tip (1 line)",
  "family_recipe": {{
    "name": "Recipe name in Hindi",
    "why": "यह क्यों healthy है — {name} जी और family दोनों के लिए",
    "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"],
    "quick_method": "Simple 2-3 line method"
  }}
}}"""
    else:
        prompt = f"""You are Nirogini, a caring health companion for Indian women.

Create a personalised daily health plan for {name} ji.

Her details:
- Age: {age} years
- Medical conditions: {medical}
- Today's log so far: water {water} glasses, steps {steps}, sleep {sleep} hours

Respond in JSON only (no extra text, no em-dashes):
{{
  "water_tip": "Fun, friendly water tip based on what she has logged today (1-2 lines)",
  "food_tip": "Today's meal suggestion that works for the whole family — Indian food, budget-friendly (2-3 lines)",
  "movement_tip": "Realistic movement suggestion for a busy woman (1-2 lines)",
  "self_care": "One small self-care tip she can actually do today (1 line)",
  "family_recipe": {{
    "name": "Recipe name",
    "why": "Why this is healthy for {name} ji and her family",
    "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"],
    "quick_method": "Simple 2-3 line cooking method"
  }}
}}"""

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return _fallback_plan(language)

    try:
        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 600, "temperature": 0.7},
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"].strip()
        if "```" in raw:
            raw = raw.split("```")[1].lstrip("json").strip()
        import json
        return json.loads(raw)
    except Exception:
        return _fallback_plan(language)


def explain_report(report_values, language="en"):
    if language == "hi":
        prompt = f"""आप एक friendly health educator हैं।

इन lab report values को simple Hindi में explain करें:
{report_values}

JSON में respond करें:
{{
  "summary": "Overall report के बारे में 2-3 lines — simple language में",
  "values": [
    {{
      "name": "Test name",
      "value": "User की value",
      "normal_range": "Normal range (Indian standards के according)",
      "status": "normal/borderline/high/low",
      "meaning": "इसका क्या मतलब है — simple Hindi में",
      "action": "क्या करना चाहिए"
    }}
  ],
  "questions_for_doctor": ["Doctor से यह पूछें", "और यह भी पूछें"],
  "disclaimer": "Disclaimer in Hindi"
}}"""
    else:
        prompt = f"""You are a friendly health educator explaining lab reports to Indian women.

Explain these lab report values in simple, plain English:
{report_values}

Respond in JSON only:
{{
  "summary": "2-3 line plain English summary of overall report",
  "values": [
    {{
      "name": "Test name",
      "value": "User's value",
      "normal_range": "Normal range per Indian standards",
      "status": "normal/borderline/high/low",
      "meaning": "What this means in simple language",
      "action": "What she should do"
    }}
  ],
  "questions_for_doctor": ["Ask your doctor this", "And this"],
  "disclaimer": "This is for educational purposes only. Always consult your doctor."
}}"""

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {"error": "API key not configured"}

    try:
        resp = requests.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {api_key}",
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 800, "temperature": 0.3},
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"].strip()
        if "```" in raw:
            raw = raw.split("```")[1].lstrip("json").strip()
        import json
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e)}


def _fallback_plan(language):
    if language == "hi":
        return {
            "water_tip": "दिन में कम से कम 8 गिलास पानी पियें। 💧",
            "food_tip": "आज lunch में dal chawal बनाएं — protein और carbs का perfect balance।",
            "movement_tip": "15 minute walk लें — घर के आस-पास भी चल सकती हैं। 🚶‍♀️",
            "self_care": "आज 5 minute के लिए सिर्फ बैठें और deep breath लें। 🌸",
            "family_recipe": {
                "name": "Dal Palak",
                "why": "Iron और protein से भरपूर — आपके लिए और बच्चों के लिए दोनों के लिए best",
                "ingredients": ["1 cup dal", "2 cups palak", "Spices"],
                "quick_method": "Dal cook करें। Palak डालें। Simple tadka लगाएं। Ready!"
            }
        }
    return {
        "water_tip": "You've had some water today — keep it going! Aim for 8 glasses. 💧",
        "food_tip": "Try dal with roti for lunch today — protein-rich and great for the whole family!",
        "movement_tip": "Even a 15-minute walk around your building counts. You've got this! 🚶‍♀️",
        "self_care": "Take 5 minutes just for yourself today — sit quietly and breathe. 🌸",
        "family_recipe": {
            "name": "Dal Palak",
            "why": "Rich in iron and protein — perfect for you and the kids",
            "ingredients": ["1 cup lentils", "2 cups spinach", "Spices to taste"],
            "quick_method": "Cook lentils until soft. Add spinach. Simple tadka with cumin and garlic. Done!"
        }
    }
