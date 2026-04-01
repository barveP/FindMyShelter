import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from recommendation import recommend_shelter

st.set_page_config(
    page_title="Pet Adoption Shelter Finder",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Inject CSS + kill sidebar + style pills (all in one JS call) ──────────────
_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

*, *::before, *::after { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* Background */
.stApp {
    background:
        radial-gradient(circle at top left, rgba(255, 244, 184, 0.65), transparent 28%),
        radial-gradient(circle at bottom right, rgba(255, 230, 160, 0.45), transparent 24%),
        linear-gradient(180deg, #fffdf6 0%, #fff9e8 100%) !important;
    color: #4b3b16 !important;
}

.block-container {
    max-width: 1180px !important;
    padding-top: 5rem !important;
    padding-bottom: 2rem !important;
}

/* Hide sidebar + toggle at all viewport sizes */
section[data-testid="stSidebar"],
div[data-testid="stSidebarCollapsedControl"],
div[data-testid="collapsedControl"],
button[data-testid="stBaseButton-headerNoPadding"],
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
.st-emotion-cache-1cypcdb,
.st-emotion-cache-dvne4q,
button[kind="header"],
div[class*="collapsedControl"],
div[class*="SidebarCollapsed"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    pointer-events: none !important;
}

/* Global text color */
h1,h2,h3,h4,h5,h6,p,label,div,span { color: #4b3b16 !important; }

/* Hero card */
.hero-card {
    padding: 2rem;
    border-radius: 30px;
    background: linear-gradient(135deg, #fff8dc, #fff2b8);
    border: 1px solid rgba(190,150,52,0.18);
    box-shadow: 0 14px 40px rgba(196,163,82,0.18);
    margin-bottom: 1.25rem;
}
.hero-title {
    font-size: 3.1rem;
    font-weight: 800;
    line-height: 1.02;
    letter-spacing: -0.04em;
    margin-bottom: 0.45rem;
    color: #5b4513 !important;
}
.hero-subtitle {
    font-size: 1.04rem;
    line-height: 1.65;
    max-width: 640px;
    color: #7b6424 !important;
    margin-bottom: 0;
}

/* Panel card */
.panel-card {
    padding: 1.35rem;
    border-radius: 28px;
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(190,150,52,0.16);
    box-shadow: 0 12px 34px rgba(196,163,82,0.12);
}
.section-title {
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
    color: #5b4513 !important;
}
.section-subtitle {
    font-size: 0.94rem;
    margin-bottom: 1rem;
    color: #8b7230 !important;
}

/* Form */
div[data-testid="stForm"] { background: transparent !important; border: none !important; padding: 0 !important; }

/* Widget labels */
label[data-testid="stWidgetLabel"] p {
    font-size: 0.96rem !important;
    font-weight: 600 !important;
    color: #5b4513 !important;
}

/* Selects + inputs */
div[data-baseweb="select"] > div,
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background: #fffdf7 !important;
    color: #3f3110 !important;
    border: 1.5px solid #ecd88c !important;
    border-radius: 18px !important;
    min-height: 3.2rem !important;
    box-shadow: none !important;
}
div[data-baseweb="select"] svg,
div[data-testid="stNumberInput"] button { color: #6c561d !important; }
div[role="listbox"] { background: #fffdf7 !important; border: 1px solid #ecd88c !important; color: #3f3110 !important; }
div[role="option"]  { background: #fffdf7 !important; color: #3f3110 !important; }
div[role="option"]:hover { background: #fff3bf !important; color: #2f240b !important; }
.st-bq,.st-br,.st-bs,.st-bt,.st-bu { color: #3f3110 !important; }

/* Submit button */
.stButton > button {
    width: 100%;
    min-height: 3.35rem;
    border-radius: 18px !important;
    border: none !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #4b3b16 !important;
    background: linear-gradient(135deg, #ffd84d, #ffe89a) !important;
    box-shadow: 0 10px 24px rgba(214,173,45,0.24) !important;
    transition: filter 0.15s;
}
.stButton > button:hover { filter: brightness(1.04); }

/* Metrics */
div[data-testid="metric-container"] {
    background: #fffdf7 !important;
    border: 1px solid rgba(190,150,52,0.18) !important;
    padding: 1rem 1rem 0.85rem 1rem !important;
    border-radius: 22px !important;
    box-shadow: 0 8px 24px rgba(196,163,82,0.10) !important;
}
div[data-testid="metric-container"] label { color: #8b7230 !important; }

/* Result boxes */
.result-good {
    padding: 1rem 1.1rem; border-radius: 20px; margin-top: 0.7rem;
    font-weight: 600; border: 1px solid rgba(190,150,52,0.16);
    background: #eefbe7; color: #325d1e !important;
}
.result-soft {
    padding: 1rem 1.1rem; border-radius: 20px; margin-top: 0.7rem;
    font-weight: 600; border: 1px solid rgba(190,150,52,0.16);
    background: #fff6d8; color: #7a5f12 !important;
}

/* Pet illustration */
.pet-wrap {
    height: 100%; min-height: 500px;
    display: flex; align-items: center; justify-content: center;
}
.pet-stage { position: relative; width: 320px; height: 360px; }
.glow {
    position: absolute; width: 260px; height: 260px; left: 30px; top: 30px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,232,154,0.85), rgba(255,232,154,0.10));
    filter: blur(6px);
}
.floaty { animation: bob 3.2s ease-in-out infinite; position: absolute; inset: 0; }
@keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
.paw { position: absolute; font-size: 1.4rem; opacity: 0.58; animation: drift 5s ease-in-out infinite; }
.paw1{top:18px;left:30px} .paw2{top:42px;right:24px;animation-delay:1s} .paw3{bottom:34px;left:12px;animation-delay:2s}
@keyframes drift { 0%,100%{transform:translateY(0) rotate(-6deg)} 50%{transform:translateY(-8px) rotate(6deg)} }
.pet-svg { position: absolute; left: 15px; top: 40px; width: 290px; height: 290px; }
.tiny-note { text-align: center; margin-top: 1rem; color: #8b7230 !important; font-size: 0.95rem; }

/* Progress bar */
.stProgress > div > div > div > div { background-color: #ffd84d !important; }

/* Nav pill base (page_link) */
a[data-testid="stPageLink-NavLink"] {
    border-radius: 20px !important; padding: 0.35rem 0.8rem !important;
    font-weight: 600 !important; font-size: 0.82rem !important;
    border: 1px solid #ecd88c !important; color: #6b5820 !important;
    text-decoration: none !important; background: white !important;
    white-space: nowrap !important;
}
a[data-testid="stPageLink-NavLink"]:hover { background: #fffbe6 !important; }
"""

import json
components.html(f"""
<script>
(function() {{
  // Inject CSS into parent frame
  var css = {json.dumps(_CSS)};
  var old = window.parent.document.getElementById('app-css');
  if (old) old.remove();
  var s = window.parent.document.createElement('style');
  s.id = 'app-css';
  s.textContent = css;
  window.parent.document.head.appendChild(s);

  // Kill sidebar toggle
  function kill() {{
    [
      '[data-testid="stSidebarCollapsedControl"]',
      '[data-testid="collapsedControl"]',
      'button[data-testid="stBaseButton-headerNoPadding"]',
      'section[data-testid="stSidebar"]',
      '[data-testid="stSidebarNav"]',
      'button[kind="header"]'
    ].forEach(function(sel) {{
      window.parent.document.querySelectorAll(sel).forEach(function(el) {{ el.remove(); }});
    }});
    // Also remove any button containing << or >>
    window.parent.document.querySelectorAll('button').forEach(function(btn) {{
      if (btn.textContent.trim() === '«' || btn.textContent.trim() === '»' ||
          btn.textContent.trim() === '<<' || btn.textContent.trim() === '>>') {{
        btn.remove();
      }}
    }});
  }}

  // Style active pill
  function stylePills() {{
    window.parent.document.querySelectorAll('a[data-testid="stPageLink-NavLink"]').forEach(function(a) {{
      a.style.cssText = 'border-radius:20px;padding:0.3rem 0.75rem;font-weight:600;font-size:0.82rem;border:1px solid #ecd88c;color:#6b5820;text-decoration:none;background:white;display:inline-block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;';
      if (a.textContent.trim() === 'Shelter Finder') {{
        a.style.background = 'linear-gradient(135deg,#ffd84d,#ffe89a)';
        a.style.borderColor = '#c9a500';
        a.style.color = '#4b3b16';
        a.style.boxShadow = '0 4px 12px rgba(201,165,0,0.22)';
      }}
    }});
  }}

  kill();
  setTimeout(function() {{ kill(); stylePills(); }}, 200);
  setTimeout(function() {{ kill(); stylePills(); }}, 600);
  new MutationObserver(function() {{ kill(); stylePills(); }})
    .observe(window.parent.document.body, {{ childList: true, subtree: true }});
}})();
</script>
""", height=0)

# ── Nav bar ───────────────────────────────────────────────────────────────────
nav_l, nav_r1, nav_r2 = st.columns([6, 1.6, 1.8])
with nav_l:
    st.markdown(
        '<div style="padding:0.55rem 0;font-size:1.05rem;font-weight:800;color:#4b3b16 !important;">🐾 Pet Adoption Finder</div>',
        unsafe_allow_html=True,
    )
with nav_r1:
    st.page_link("app.py", label="Shelter Finder")
with nav_r2:
    st.page_link("pages/Shelters_Overview.py", label="Shelters Overview")

# ── Main layout ───────────────────────────────────────────────────────────────
left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.markdown("""
    <div class="hero-card">
        <div class="hero-title">Pet Adoption Shelter Finder</div>
        <div class="hero-subtitle">
            Enter your pet's details to find the shelter where it has
            the highest chance of being adopted quickly.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="panel-card">
        <div class="section-title">Pet Details</div>
        <div class="section-subtitle">Fill in the profile and find the best shelter.</div>
    """, unsafe_allow_html=True)

    with st.form("prediction_form", border=False):
        c1, c2 = st.columns(2)
        with c1:
            animal_type = st.selectbox("Animal Type", ["dog", "cat", "bird", "rabbit", "guinea pig", "reptile", "other"])
            primary_color = st.selectbox("Primary Color", ["black", "brown", "white", "gray", "orange", "tan", "multicolor", "other"])
        with c2:
            sex = st.selectbox("Sex", ["neutered", "spayed", "male", "female", "unknown"])
            intake_condition = st.selectbox("Intake Condition", ["normal", "ill", "injured", "behavior", "other"])

        age_c1, age_c2 = st.columns(2)
        with age_c1:
            age_years = st.number_input("Age (years)", min_value=0, max_value=25, value=1, step=1)
        with age_c2:
            age_months = st.number_input("Age (months)", min_value=0, max_value=11, value=0, step=1)

        age = age_years * 365 + age_months * 30
        submitted = st.form_submit_button("Find Best Shelter")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        results, best_shelter = recommend_shelter(animal_type, primary_color, sex, age, intake_condition)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='result-good'>🏆 Recommended Shelter: <strong>{best_shelter}</strong></div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Adoption Probability by Shelter</div>", unsafe_allow_html=True)

        cols = st.columns(len(results))
        for col, (shelter, prob) in zip(cols, results.items()):
            with col:
                st.metric(shelter, f"{prob}%")
                st.progress(float(prob / 100))

with right:
    st.markdown("""
    <div class="pet-wrap">
        <div class="pet-stage">
            <div class="glow"></div>
            <div class="paw paw1">🐾</div>
            <div class="paw paw2">🐾</div>
            <div class="paw paw3">🐾</div>
            <div class="floaty">
                <svg class="pet-svg" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
                    <ellipse cx="150" cy="255" rx="82" ry="20" fill="#f1de9a"/>
                    <circle cx="150" cy="138" r="74" fill="#ffe7a3"/>
                    <ellipse cx="102" cy="86" rx="24" ry="42" transform="rotate(-24 102 86)" fill="#ffd45e"/>
                    <ellipse cx="198" cy="86" rx="24" ry="42" transform="rotate(24 198 86)" fill="#ffd45e"/>
                    <circle cx="150" cy="146" r="48" fill="#fff7db"/>
                    <circle cx="124" cy="130" r="6" fill="#4b3b16"/>
                    <circle cx="176" cy="130" r="6" fill="#4b3b16"/>
                    <ellipse cx="150" cy="149" rx="9" ry="7" fill="#7b6424"/>
                    <path d="M140 164 Q150 174 160 164" stroke="#7b6424" stroke-width="5" fill="none" stroke-linecap="round"/>
                    <path d="M112 148 H86" stroke="#b08a2f" stroke-width="3" stroke-linecap="round"/>
                    <path d="M114 157 H84" stroke="#b08a2f" stroke-width="3" stroke-linecap="round"/>
                    <path d="M188 148 H214" stroke="#b08a2f" stroke-width="3" stroke-linecap="round"/>
                    <path d="M186 157 H216" stroke="#b08a2f" stroke-width="3" stroke-linecap="round"/>
                    <ellipse cx="116" cy="226" rx="20" ry="16" fill="#ffd45e"/>
                    <ellipse cx="184" cy="226" rx="20" ry="16" fill="#ffd45e"/>
                </svg>
            </div>
        </div>
    </div>
    <div class="tiny-note">Find the best home for your found pet.</div>
    """, unsafe_allow_html=True)
