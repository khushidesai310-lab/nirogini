/* app.js - Shared utilities for Nirogini */

const API = "";

const Lang = {
  get: () => localStorage.getItem("nirogini_lang") || "en",
  set: (l) => localStorage.setItem("nirogini_lang", l),
};

const Auth = {
  getToken: () => localStorage.getItem("nirogini_token"),
  setToken: (t) => localStorage.setItem("nirogini_token", t),
  getUser: () => {
    const u = localStorage.getItem("nirogini_user");
    return u ? JSON.parse(u) : null;
  },
  setUser: (u) => localStorage.setItem("nirogini_user", JSON.stringify(u)),
  clear: () => {
    localStorage.removeItem("nirogini_token");
    localStorage.removeItem("nirogini_user");
  },
};

async function apiCall(path, { method = "GET", body = null, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = Auth.getToken();
    if (!token) { window.location.href = "index.html"; return null; }
    headers["Authorization"] = `Bearer ${token}`;
  }
  try {
    const res = await fetch(API + path, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    });
    const data = await res.json().catch(() => ({ success: false, error: "Server error." }));
    if (res.status === 401 && auth) {
      Auth.clear();
      window.location.href = "login.html";
      return null;
    }
    return { status: res.status, ...data };
  } catch (e) {
    return { success: false, error: "Network error. Please check your connection." };
  }
}

function requireAuth() {
  if (!Auth.getToken()) window.location.href = "login.html";
}

function showError(el, msg) {
  el.textContent = msg;
  el.className = "error-msg show";
}

function showSuccess(el, msg) {
  el.textContent = msg;
  el.className = "success-msg show";
}

function evaluatePasswordStrength(password) {
  let score = 0;
  if (password.length >= 8) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[!@#$%^&*]/.test(password)) score++;
  if (password.length >= 12) score++;
  return score;
}

function renderStrengthMeter(containerEl, hintEl, password) {
  const score = evaluatePasswordStrength(password);
  const bars = containerEl.querySelectorAll("div");
  const colors = ["#e74c3c", "#e74c3c", "#f39c12", "#f39c12", "#4CAF88"];
  bars.forEach((bar, i) => {
    bar.style.background = i < score ? colors[Math.min(score - 1, 4)] : "var(--border)";
  });
  const labels = ["Very weak", "Weak", "Fair", "Good", "Strong"];
  hintEl.textContent = password ? `Strength: ${labels[Math.max(score - 1, 0)]}` : "Use 8+ characters with uppercase, number & symbol.";
}

// UI text translations
const UI = {
  en: {
    greeting_morning: "Good morning",
    greeting_evening: "Good evening",
    water: "Water",
    steps: "Steps",
    sleep: "Sleep",
    bp: "Blood Pressure",
    sugar: "Blood Sugar",
    mood: "Mood",
    weight: "Weight",
    log_today: "Log Today",
    save: "Save",
    saving: "Saving...",
    chat_placeholder: "How are you feeling today? Tell me anything...",
    send: "Send",
    thinking: "Thinking...",
    points: "Points",
    streak: "Day Streak",
    level: "Level",
    add_friend: "Add Friend",
    find_hospitals: "Find Hospitals",
    your_plan: "Your Daily Plan",
    report_explainer: "Report Explainer",
    sign_out: "Sign Out",
    dashboard: "Home",
    tracker: "Health Log",
    companion: "Chat with Nirogini",
    community: "My Circle",
    hospitals_nav: "Find Hospitals",
    reports: "My Reports",
    profile_nav: "My Profile",
    glasses: "glasses",
    hours: "hours",
    complete: "Complete!",
  },
  hi: {
    greeting_morning: "सुप्रभात",
    greeting_evening: "शुभ संध्या",
    water: "पानी",
    steps: "कदम",
    sleep: "नींद",
    bp: "Blood Pressure",
    sugar: "Blood Sugar",
    mood: "मूड",
    weight: "वजन",
    log_today: "आज का log",
    save: "Save करें",
    saving: "Save हो रहा है...",
    chat_placeholder: "आज कैसा feel हो रहा है? कुछ भी बताएं...",
    send: "भेजें",
    thinking: "सोच रही हूं...",
    points: "Points",
    streak: "दिन की streak",
    level: "Level",
    add_friend: "Friend जोड़ें",
    find_hospitals: "Hospital खोजें",
    your_plan: "आज का plan",
    report_explainer: "Report Explainer",
    sign_out: "Sign Out",
    dashboard: "Home",
    tracker: "Health Log",
    companion: "Nirogini से बात करें",
    community: "My Circle",
    hospitals_nav: "Hospital खोजें",
    reports: "मेरी Reports",
    profile_nav: "मेरी Profile",
    glasses: "गिलास",
    hours: "घंटे",
    complete: "Complete! 🎉",
  }
};

function t(key) {
  const lang = Lang.get();
  return (UI[lang] && UI[lang][key]) || UI["en"][key] || key;
}
