# Nirogini - AI Women's Health Companion

> *Because when she's well, everyone's well*

Nirogini is a bilingual (Hindi/English) AI-powered health companion built for Indian women in their 40s and 50s, a demographic that consistently deprioritises their own health due to fear, financial anxiety, and distrust of the healthcare system.

This project is personal. It was built for my mother, who has not been for a health checkup in four years, not because she does not care, but because she is afraid of what might be found, unsure of the cost, and does not trust she will get honest answers. Nirogini is built to change that.

> 🚧 **This project is actively under development.** Core features are functional. Additional features are being added continuously.

---

## The Problem

Women in their 40s and 50s in India face a specific and underserved healthcare challenge:

- They put everyone in their family before themselves
- They avoid health checkups due to fear of bad news and hospital costs
- They keep symptoms to themselves rather than worrying their family
- They have no trusted, affordable, always-available source of health guidance
- Perimenopause and menopause symptoms often go unaddressed for years

No existing health app is built specifically for this group, in their language, understanding their context.

---

## What Nirogini Does

### Core Features

**Bilingual from the start**
Users choose Hindi or English on the first screen. Every feature works in both languages throughout.

**AI Health Companion (Groq/Llama LLM)**
A conversational AI that knows the user's complete health history and speaks like a caring younger sister — not a clinical chatbot. Responds to symptoms, provides menopause support, gives daily health advice, and connects her health to her family's wellbeing.

**Daily Health Tracker**
Log water intake, steps, sleep, mood, blood pressure, blood sugar, and weight. Gamified with points, streaks, and levels (Getting Started → Taking Charge → Glowing Up → Community Champion → Nirogini).

**Menopause Symptom Tracker**
Daily logging of hot flashes, night sweats, mood, sleep quality, joint pain, brain fog, anxiety, and headaches with Yes/No and severity options. 30-day trend charts help identify patterns. Includes symptom management tips.

**Medicine and Supplement Tracker**
Add all medicines with dosage, frequency, and time of day. Easy to manage — covers thyroid medication, vitamins, supplements, and anything else she takes daily.

**Period and Cycle Tracker**
Track periods with flow level, symptoms, and notes. Calculates average cycle length. Designed specifically for perimenopause where cycles become irregular. Includes guidance on what changes are normal versus what needs medical attention.

**Doctor Appointment Manager**
Add upcoming appointments with doctor name, speciality, location, and questions to ask. Never forget what to discuss with the doctor. Mark appointments as done and add notes after.

**Lab Report Explainer**
Upload a photo, upload a PDF, or type values manually. The AI explains each test result in plain language, compares to Indian standard ranges, and generates specific questions to ask the doctor. Includes a menopause hormone panel example.

**Trusted Hospital Finder**
Curated database of trusted hospitals across Mumbai, Delhi, Bangalore, Ahmedabad, and Kolkata. Filtered by budget preference, government hospitals listed first for cost-conscious users. Ayushman Bharat empanelled hospitals clearly marked.

**Community and Gamification**
Add friends and family members. See each other's health progress. Friendly leaderboard encourages healthy competition. Weekly challenges with bonus points.

---
## Screenshots
![Landing](screenshots/landing.png)
![Dashboard](screenshots/dashboard.png)
![Menopause Tracker](screenshots/menopause.png)
![Medicines](screenshots/medicines.png)
![Appointments](screenshots/appointments.png)
![Chat](screenshots/chat.png)

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, SQLite |
| AI / LLM | Groq API (Llama) |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Auth | PBKDF2-SHA256 password hashing |
| Languages | Hindi and English (bilingual throughout) |

---

## How to Run

**1. Clone the repository**
```
git clone https://github.com/khushidesai310-lab/nirogini.git
cd nirogini
```

**2. Set up virtual environment**
```
cd backend
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```
pip install -r requirements.txt
```

**4. Set your Groq API key**

Get a free API key at groq.com

```
export GROQ_API_KEY="your-key-here"    # Mac/Linux
$env:GROQ_API_KEY="your-key-here"      # Windows PowerShell
```

**5. Run the server**
```
python3 app.py
```

**6. Open in browser**
```
http://localhost:5001
```

---

## Project Structure

```
nirogini/
├── backend/
│   ├── app.py                  Flask API — all routes
│   ├── auth.py                 Signup, login, session management
│   ├── database.py             SQLite initialisation — 10 tables
│   ├── health_tracker.py       Daily logging, points, streaks, community
│   ├── companion.py            Groq LLM companion — bilingual
│   ├── recommendations.py      Daily plans, report explainer
│   ├── hospitals.py            Curated hospital database — 5 cities
│   ├── wellness.py             Menopause, medicines, cycle, appointments
│   └── requirements.txt
└── frontend/
    ├── index.html              Language selection landing page
    ├── signup.html             Bilingual signup with password strength
    ├── login.html              Bilingual login
    ├── onboarding.html         4-step friendly onboarding
    ├── dashboard.html          Home — greeting, goals, AI tips, chart
    ├── tracker.html            Daily health log with sliders
    ├── menopause.html          Menopause symptom tracker
    ├── medicines.html          Medicine and supplement manager
    ├── cycle.html              Period and cycle tracker
    ├── appointments.html       Doctor appointment manager
    ├── companion.html          AI chat interface
    ├── community.html          Friend circle and leaderboard
    ├── hospitals.html          Hospital finder with budget filter
    ├── reports.html            Lab report explainer
    ├── css/style.css           Full design system — coral/cream/gold
    └── js/app.js               Shared utilities and translations
```

---

## Design Principles

**1. She is not a patient, she is a woman living her life.**
Every interaction is designed to fit into her day, not add to her burden. Daily check-in takes under 2 minutes.

**2. Connect her health to her family.**
Indian women will do for their family what they will not do for themselves. Recipe suggestions, family health tips, and the "not just for you" framing make health feel relevant.

**3. Never alarm, always empower.**
The AI never diagnoses and never creates fear. It provides calm, knowledgeable guidance that helps her take action.

**4. Budget awareness without asking directly.**
Hospital recommendations are filtered by preference (government / affordable / private) without asking intrusive questions about income.

---

## Cities Covered

Mumbai · Delhi · Bangalore · Ahmedabad · Kolkata

---

## Motivation

This project was built for my mother, who has not had a health checkup in four years. And for my aunt, who was diagnosed with a benign tumor and is still avoiding surgery out of fear. And for the hundreds of millions of women like them across India who put everyone else first.

Nirogini is not just a portfolio project. It is a foundation for something real.

---

## What's Coming Next

- Mobile app version
- Real push notifications for medicine reminders
- Expanded hospital database across more Indian cities
- Family member profiles — track kids' health too
- Integration with government health schemes (Ayushman Bharat API)
- Breathing and stress management exercises

---

## Limitations

- Hospital database is curated manually — not real-time verified
- LLM responses are for educational purposes only — not medical advice
- Currently supports India only (Mumbai, Delhi, Bangalore, Ahmedabad, Kolkata)
- Push notifications require a mobile app — not yet implemented

---

*Khushi Desai*
*github.com/khushidesai310-lab*

---

**Disclaimer:** Nirogini is not a medical diagnostic tool. All health information provided is for educational purposes only. Always consult a qualified healthcare professional for medical advice, diagnosis, or treatment.
