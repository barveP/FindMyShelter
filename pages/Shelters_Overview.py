import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import json
import os

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Shelters Overview | Pet Adoption",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Inject CSS into parent frame via JS (avoids st.markdown style-tag stripping) ──
_CSS = """
*, *::before, *::after { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

.stApp { background: #faf9f6 !important; color: #1e1a10 !important; }
.block-container { max-width: 1280px !important; padding: 5rem 2rem 3rem 2rem !important; }

/* ── Hide sidebar + toggle at all viewport sizes ── */
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

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #faf9f6; }
::-webkit-scrollbar-thumb { background: #e0d5a0; border-radius: 3px; }

/* Nav bar */
.nav-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.85rem 1.4rem; margin-bottom: 1.2rem; margin-top: -1rem;
  background: white; border-radius: 16px;
  border: 1px solid #ede9d8;
  box-shadow: 0 2px 12px rgba(180,160,80,0.08);
}
.nav-brand { font-size: 1.1rem; font-weight: 800; color: #1e1a10; letter-spacing: -0.02em; }
.nav-brand span { color: #c9a500; }

/* Multiselect chips */
span[data-baseweb="tag"] {
  background: #fffbe6 !important; border: 1px solid #f0e080 !important;
  color: #7a5f12 !important; border-radius: 20px !important;
  font-size: 0.82rem !important; font-weight: 600 !important;
}
div[data-baseweb="select"] > div {
  background: #fffdf7 !important; border: 1.5px solid #ecd88c !important;
  border-radius: 12px !important; color: #3f3110 !important;
}
div[role="listbox"] { background: #fffdf7 !important; border: 1px solid #ecd88c !important; }
div[role="option"]  { background: #fffdf7 !important; color: #3f3110 !important; }
div[role="option"]:hover { background: #fff3bf !important; }

/* Filter bar */
.filter-bar {
  background: white; border: 1px solid #ede9d8;
  border-radius: 14px; padding: 1rem 1.4rem;
  margin-bottom: 1.2rem;
  box-shadow: 0 2px 8px rgba(180,160,80,0.06);
}

/* Section headers */
.section-header { display: flex; align-items: center; gap: 1rem; margin: 2rem 0 1rem 0; }
.section-label {
  font-size: 0.78rem; font-weight: 700; letter-spacing: 0.1em;
  color: #6b5820; text-transform: uppercase; white-space: nowrap;
}
.section-rule { flex: 1; height: 1px; background: #ede9d8; }

/* Top bar */
.top-bar { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 1.5rem; }
.top-title { font-size: 1.9rem; font-weight: 800; color: #1e1a10; letter-spacing: -0.03em; line-height: 1.1; }
.top-subtitle { font-size: 0.95rem; color: #9b8640; margin-top: 0.25rem; }
.year-badge {
  background: linear-gradient(135deg, #fffbe6, #fff3cc);
  border: 1px solid #e8d870; border-radius: 20px;
  padding: 0.4rem 1rem; font-size: 0.88rem; font-weight: 700; color: #7a5f12;
}

/* Snapshot cards */
.snapshot-card {
  background: white; border: 1px solid #ede9d8;
  border-radius: 14px; padding: 1.2rem 1.4rem;
  box-shadow: 0 4px 16px rgba(180,160,80,0.08); height: 100%;
}
.snapshot-shelter { font-size: 1.05rem; font-weight: 700; color: #1e1a10; margin-bottom: 0.75rem; }
.snapshot-row { display: flex; justify-content: space-between; margin-bottom: 0.4rem; }
.snapshot-key { font-size: 0.85rem; color: #9b8640; font-weight: 500; }
.snapshot-val { font-size: 0.88rem; font-weight: 700; color: #4b3b16; }

/* Chart cards */
.chart-card {
  background: white; border: 1px solid #ede9d8;
  border-radius: 12px; padding: 1.2rem 1.4rem 0.6rem 1.4rem;
  box-shadow: 0 4px 16px rgba(180,160,80,0.07); margin-bottom: 0.6rem;
}
.chart-title { font-size: 1rem; font-weight: 700; color: #1e1a10; margin-bottom: 0.15rem; }
.chart-desc  { font-size: 0.83rem; color: #9b8640; margin-bottom: 0.3rem; }

/* Map card */
.map-card {
  background: white; border: 1px solid #ede9d8;
  border-radius: 14px; overflow: hidden;
  box-shadow: 0 4px 16px rgba(180,160,80,0.08);
}

/* Widget labels */
label[data-testid="stWidgetLabel"] p {
  font-size: 0.88rem !important; font-weight: 600 !important; color: #5b4513 !important;
}

/* Page link nav pills */
a[data-testid="stPageLink-NavLink"] {
  border-radius: 20px !important; padding: 0.35rem 0.8rem !important;
  font-weight: 600 !important; font-size: 0.82rem !important;
  border: 1px solid #ede9d8 !important; color: #6b5820 !important;
  text-decoration: none !important; background: white !important;
  white-space: nowrap !important;
}
a[data-testid="stPageLink-NavLink"]:hover { background: #fffbe6 !important; }

/* Streamlit default spacing */
div[data-testid="stVerticalBlock"] > div { margin-bottom: 0 !important; }
.element-container { margin-bottom: 0.4rem !important; }
"""

components.html(f"""
<script>
(function() {{
  // Inject CSS into parent Streamlit frame
  var css = {json.dumps(_CSS)};
  var existing = window.parent.document.getElementById('shelters-overview-css');
  if (existing) existing.remove();
  var s = window.parent.document.createElement('style');
  s.id = 'shelters-overview-css';
  s.textContent = css;
  window.parent.document.head.appendChild(s);

  // Inject Inter font
  if (!window.parent.document.getElementById('inter-font')) {{
    var link = window.parent.document.createElement('link');
    link.id = 'inter-font';
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap';
    window.parent.document.head.appendChild(link);
  }}

  // Aggressively remove sidebar toggle from DOM
  function killSidebar() {{
    [
      '[data-testid="stSidebarCollapsedControl"]',
      '[data-testid="collapsedControl"]',
      'button[data-testid="stBaseButton-headerNoPadding"]',
      'section[data-testid="stSidebar"]',
      '[data-testid="stSidebarNav"]',
      'button[kind="header"]'
    ].forEach(function(sel) {{
      window.parent.document.querySelectorAll(sel).forEach(function(el) {{
        el.style.display = 'none';
        el.remove();
      }});
    }});
    window.parent.document.querySelectorAll('button').forEach(function(btn) {{
      var t = btn.textContent.trim();
      if (t === '«' || t === '»' || t === '<<' || t === '>>') btn.remove();
    }});
  }}
  killSidebar();
  var observer = new MutationObserver(killSidebar);
  observer.observe(window.parent.document.body, {{ childList: true, subtree: true }});
}})();
</script>
""", height=0)

# ─── Palette + helpers ────────────────────────────────────────────────────────
PALETTE = ["#c9a500","#e07b3a","#4a9e6b","#4a7fc1","#9b6b9e","#c95c5c","#6b9e9e"]
SHELTER_COLORS = {"Austin": "#c9a500", "Long Beach": "#4a7fc1", "San Jose": "#4a9e6b"}

def section(label):
    st.markdown(f"""
    <div class="section-header">
      <span class="section-label">{label}</span>
      <div class="section-rule"></div>
    </div>""", unsafe_allow_html=True)

def plotly_defaults(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#4b3b16"),
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0),
        xaxis=dict(gridcolor="rgba(180,160,80,0.10)", linecolor="rgba(180,160,80,0.2)"),
        yaxis=dict(gridcolor="rgba(180,160,80,0.10)", linecolor="rgba(180,160,80,0.2)"),
    )
    return fig

# ─── Data loading + normalization ─────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASETS = {
    "Austin":     os.path.join(BASE, "cleaned_datasets", "austin_animal_center_cleaned.csv"),
    "Long Beach": os.path.join(BASE, "cleaned_datasets", "longbeach_cleaned.csv"),
    "San Jose":   os.path.join(BASE, "cleaned_datasets", "san_jose_cleaned_dataset.csv"),
}

def normalize_sex(val):
    if pd.isna(val): return "Unknown"
    v = str(val).strip().lower()
    if "neutered" in v: return "Neutered"
    if "spayed"   in v: return "Spayed"
    if "female"   in v: return "Female"
    if "male"     in v: return "Male"
    return "Unknown"

def normalize_condition(val, shelter):
    if pd.isna(val): return "Other"
    v = str(val).strip().lower()
    if shelter == "Austin":
        if v == "normal":          return "Normal"
        if v == "injured":         return "Injured"
        if v in ("sick", "ill"):   return "Sick"
        return "Other"
    elif shelter == "Long Beach":
        if v == "normal":  return "Normal"
        if v == "injured": return "Injured"
        if v == "ill":     return "Sick"
        return "Other"
    else:  # San Jose
        if v == "healthy":         return "Normal"
        if v.startswith("med"):    return "Sick"
        if v in ("normal","nrml"): return "Normal"
        if v == "injured":         return "Injured"
        return "Other"

def normalize_animal(val):
    if pd.isna(val): return "Other"
    v = str(val).strip().lower()
    return {"cat":"Cat","dog":"Dog","rabbit":"Rabbit","bird":"Bird","wild":"Wild"}.get(v, str(val).strip().title())

@st.cache_data(show_spinner="Loading shelter data…")
def load_data():
    frames = []
    for shelter, path in DATASETS.items():
        df = pd.read_csv(path, low_memory=False)
        df["Shelter"]         = shelter
        df["AnimalType"]      = df["AnimalType"].apply(normalize_animal)
        df["Sex"]             = df["Sex"].apply(normalize_sex)
        df["IntakeCondition"] = df["IntakeCondition"].apply(lambda x: normalize_condition(x, shelter))
        df["IntakeDate"]      = pd.to_datetime(df["IntakeDate"], utc=True, errors="coerce")
        df["IntakeYear"]      = df["IntakeDate"].dt.year
        df["IntakeMonth"]     = df["IntakeDate"].dt.to_period("M").astype(str)
        df["Age_Years"]       = pd.to_numeric(df["Age"], errors="coerce") / 365
        df["LengthOfStay"]    = pd.to_numeric(df["LengthOfStay"], errors="coerce")
        df["Adopted"]         = pd.to_numeric(df["Adopted"], errors="coerce")
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

df_all = load_data()

# ─── Nav bar ──────────────────────────────────────────────────────────────────
nav_left, nav_right_1, nav_right_2 = st.columns([6, 1.6, 1.8])
with nav_left:
    st.markdown('<div class="nav-brand" style="padding:0.6rem 0;">🐾 <span>Pet</span> Adoption Finder</div>', unsafe_allow_html=True)
with nav_right_1:
    st.page_link("app.py", label="Shelter Finder")
with nav_right_2:
    st.page_link("pages/Shelters_Overview.py", label="Shelters Overview")

# Highlight active pill
components.html("""
<script>
(function() {
  function stylePills() {
    var links = window.parent.document.querySelectorAll('a[data-testid="stPageLink-NavLink"]');
    links.forEach(function(a) {
      a.style.cssText = 'border-radius:20px;padding:0.3rem 0.75rem;font-weight:600;font-size:0.82rem;border:1px solid #ecd88c;color:#6b5820;text-decoration:none;background:white;display:inline-block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%;';
      if (a.textContent.trim().includes('Shelters Overview')) {
        a.style.background = 'linear-gradient(135deg, #ffd84d, #ffe89a)';
        a.style.borderColor = '#c9a500';
        a.style.color = '#4b3b16';
        a.style.boxShadow = '0 4px 12px rgba(201,165,0,0.22)';
      }
    });
  }
  setTimeout(stylePills, 400);
  new MutationObserver(stylePills).observe(window.parent.document.body, { childList: true, subtree: true });
})();
</script>
""", height=0)

# ─── Filter bar ───────────────────────────────────────────────────────────────
st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
fc1, fc2, fc3, fc4, fc5 = st.columns([1.2, 1.2, 1, 1.2, 1.4])

all_shelters   = sorted(df_all["Shelter"].dropna().unique())
all_types      = sorted(df_all["AnimalType"].dropna().unique())
all_sexes      = ["Neutered", "Spayed", "Male", "Female", "Unknown"]
all_conditions = ["Normal", "Injured", "Sick", "Other"]
yr_min = int(df_all["IntakeYear"].dropna().min())
yr_max = int(df_all["IntakeYear"].dropna().max())

with fc1: sel_shelters   = st.multiselect("Shelter",           all_shelters,   default=all_shelters)
with fc2: sel_types      = st.multiselect("Animal Type",       all_types,      default=all_types)
with fc3: sel_sexes      = st.multiselect("Sex",               all_sexes,      default=all_sexes)
with fc4: sel_conditions = st.multiselect("Intake Condition",  all_conditions, default=all_conditions)
with fc5: sel_years      = st.slider("Intake Year", yr_min, yr_max, (yr_min, yr_max))
st.markdown('</div>', unsafe_allow_html=True)

# ─── Apply filters ────────────────────────────────────────────────────────────
df = df_all.copy()
if sel_shelters:   df = df[df["Shelter"].isin(sel_shelters)]
if sel_types:      df = df[df["AnimalType"].isin(sel_types)]
if sel_sexes:      df = df[df["Sex"].isin(sel_sexes)]
if sel_conditions: df = df[df["IntakeCondition"].isin(sel_conditions)]
df = df[df["IntakeYear"].between(sel_years[0], sel_years[1])]

# ─── Top bar ──────────────────────────────────────────────────────────────────
yr_label = f"{sel_years[0]} – {sel_years[1]}" if sel_years[0] != sel_years[1] else str(sel_years[0])
st.markdown(f"""
<div class="top-bar">
  <div>
    <div class="top-title">Shelters Overview</div>
    <div class="top-subtitle">Adoption trends, shelter performance, and intake demographics</div>
  </div>
  <div class="year-badge">📅 {yr_label}</div>
</div>""", unsafe_allow_html=True)

# ─── KPI calculations ─────────────────────────────────────────────────────────
total_animals = len(df)
adoption_rate = round(df["Adopted"].mean() * 100, 1) if len(df) else 0.0
avg_stay      = round(df["LengthOfStay"].mean(), 1)  if len(df) else 0.0
shelter_rates = df.groupby("Shelter")["Adopted"].mean()
top_shelter   = shelter_rates.idxmax() if len(shelter_rates) else "—"

# ─── Animated KPI counters ────────────────────────────────────────────────────
components.html(f"""
<style>
  .kpi-row {{ display:flex; gap:1rem; width:100%; font-family:'Inter',sans-serif; }}
  .kpi-card {{
    flex:1; background:white; border-radius:14px; padding:1.2rem 1.4rem;
    border:1px solid #ede9d8; border-top-width:4px;
    box-shadow:0 4px 16px rgba(180,160,80,0.08);
  }}
  .kpi-label {{ font-size:0.75rem; font-weight:700; letter-spacing:0.08em;
    text-transform:uppercase; color:#9b8640; margin-bottom:0.5rem; }}
  .kpi-value {{ font-size:2rem; font-weight:800; color:#1e1a10; letter-spacing:-0.03em; line-height:1.1; }}
  .kpi-sub   {{ font-size:0.8rem; color:#9b8640; margin-top:0.25rem; }}
</style>
<div class="kpi-row">
  <div class="kpi-card" style="border-top-color:#c9a500">
    <div class="kpi-label">Total Animals</div>
    <div class="kpi-value" id="k1">0</div>
    <div class="kpi-sub">filtered records</div>
  </div>
  <div class="kpi-card" style="border-top-color:#e07b3a">
    <div class="kpi-label">Adoption Rate</div>
    <div class="kpi-value" id="k2">0%</div>
    <div class="kpi-sub">of intakes adopted</div>
  </div>
  <div class="kpi-card" style="border-top-color:#4a9e6b">
    <div class="kpi-label">Avg. Length of Stay</div>
    <div class="kpi-value" id="k3">0 days</div>
    <div class="kpi-sub">days until outcome</div>
  </div>
  <div class="kpi-card" style="border-top-color:#4a7fc1">
    <div class="kpi-label">Top Shelter</div>
    <div class="kpi-value" id="k4" style="font-size:1.35rem">—</div>
    <div class="kpi-sub">highest adoption rate</div>
  </div>
</div>
<script>
(function(){{
  function ease(t) {{ return 1 - Math.pow(1 - t, 3); }}
  function countUp(id, target, isFloat, suffix, delay) {{
    setTimeout(function() {{
      var el = document.getElementById(id);
      if (!el) return;
      var dur = 1100, start = null;
      function step(ts) {{
        if (!start) start = ts;
        var p = Math.min((ts - start) / dur, 1);
        var v = ease(p) * target;
        el.textContent = (isFloat ? v.toFixed(1) : Math.floor(v).toLocaleString()) + suffix;
        if (p < 1) requestAnimationFrame(step);
      }}
      requestAnimationFrame(step);
    }}, delay);
  }}
  countUp("k1", {total_animals}, false, "",       0);
  countUp("k2", {adoption_rate}, true,  "%",     50);
  countUp("k3", {avg_stay},      true,  " days", 100);
  setTimeout(function() {{
    var el = document.getElementById("k4");
    if (el) el.textContent = "{top_shelter}";
  }}, 400);
}})();
</script>
""", height=150)

# ─── SHELTER SNAPSHOT ─────────────────────────────────────────────────────────
section("Shelter Snapshot")
snap_cols = st.columns(3)
for i, shelter in enumerate(["Austin", "Long Beach", "San Jose"]):
    sdf  = df[df["Shelter"] == shelter]
    cnt  = len(sdf)
    rate = round(sdf["Adopted"].mean() * 100, 1) if cnt else 0
    stay = round(sdf["LengthOfStay"].mean(), 1)  if cnt else 0
    color = SHELTER_COLORS.get(shelter, "#c9a500")
    with snap_cols[i]:
        st.markdown(f"""
        <div class="snapshot-card" style="border-top:4px solid {color}">
          <div class="snapshot-shelter">{shelter}</div>
          <div class="snapshot-row"><span class="snapshot-key">Animals</span><span class="snapshot-val">{cnt:,}</span></div>
          <div class="snapshot-row"><span class="snapshot-key">Adoption Rate</span><span class="snapshot-val">{rate}%</span></div>
          <div class="snapshot-row"><span class="snapshot-key">Avg. Stay</span><span class="snapshot-val">{stay} days</span></div>
        </div>""", unsafe_allow_html=True)

# ─── SHELTER LOCATIONS ────────────────────────────────────────────────────────
section("Shelter Locations")
try:
    import folium
    from streamlit_folium import st_folium

    COORDS = {
        "Austin":     (30.2672,  -97.7431),
        "Long Beach": (33.7701, -118.1937),
        "San Jose":   (37.3382, -121.8863),
    }
    CITIES = {"Austin": "Austin, TX", "Long Beach": "Long Beach, CA", "San Jose": "San Jose, CA"}

    m = folium.Map(location=[36, -108], zoom_start=5, tiles="CartoDB positron",
                   attr="© OpenStreetMap contributors © CartoDB")
    for name, (lat, lon) in COORDS.items():
        sdf  = df[df["Shelter"] == name]
        rate = round(sdf["Adopted"].mean() * 100, 1) if len(sdf) else 0
        folium.CircleMarker(
            location=[lat, lon], radius=14,
            color="#c9a500", fill=True, fill_color="#ffd84d", fill_opacity=0.85, weight=2,
            tooltip=folium.Tooltip(f"<b>{name}</b><br>{CITIES[name]}<br>Adoption Rate: {rate}%"),
        ).add_to(m)
        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=f'<div style="font-family:Inter,sans-serif;font-size:11px;font-weight:700;color:#4b3b16;white-space:nowrap;margin-top:18px;margin-left:-20px;">{name}</div>',
                icon_size=(100, 20), icon_anchor=(0, 0),
            ),
        ).add_to(m)

    st.markdown('<div class="map-card">', unsafe_allow_html=True)
    st_folium(m, width=None, height=340, returned_objects=[])
    st.markdown('</div>', unsafe_allow_html=True)
except ImportError:
    st.info("Install `folium` and `streamlit-folium` to view the map.")

# ─── ADOPTION PERFORMANCE ─────────────────────────────────────────────────────
section("Adoption Performance")
perf_c1, perf_c2 = st.columns(2)

with perf_c1:
    st.markdown('<div class="chart-card"><div class="chart-title">Adoption Rate by Shelter</div><div class="chart-desc">Percentage of animals adopted per shelter</div></div>', unsafe_allow_html=True)
    sh_rate = df.groupby("Shelter")["Adopted"].mean().reset_index()
    sh_rate["Rate"] = (sh_rate["Adopted"] * 100).round(1)
    avg_r = sh_rate["Rate"].mean()
    fig = px.bar(sh_rate, x="Shelter", y="Rate", color="Shelter",
                 color_discrete_map=SHELTER_COLORS, text="Rate")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", marker_line_width=0)
    fig.add_hline(y=avg_r, line_dash="dot", line_color="#9b8640",
                  annotation_text=f"Avg {avg_r:.1f}%", annotation_position="top right",
                  annotation_font_color="#9b8640")
    fig.update_layout(showlegend=False, yaxis_title="Adoption Rate (%)", xaxis_title="")
    plotly_defaults(fig)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with perf_c2:
    st.markdown('<div class="chart-card"><div class="chart-title">Adoption Rate by Animal Type</div><div class="chart-desc">Which animals get adopted most often</div></div>', unsafe_allow_html=True)
    type_rate = df.groupby("AnimalType")["Adopted"].mean().reset_index()
    type_rate["Rate"] = (type_rate["Adopted"] * 100).round(1)
    type_rate = type_rate.sort_values("Rate", ascending=False)
    avg_tr = type_rate["Rate"].mean()
    fig2 = px.bar(type_rate, x="AnimalType", y="Rate", color="AnimalType",
                  color_discrete_sequence=PALETTE, text="Rate")
    fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside", marker_line_width=0)
    fig2.add_hline(y=avg_tr, line_dash="dot", line_color="#9b8640",
                   annotation_text=f"Avg {avg_tr:.1f}%", annotation_position="top right",
                   annotation_font_color="#9b8640")
    fig2.update_layout(showlegend=False, yaxis_title="Adoption Rate (%)", xaxis_title="")
    plotly_defaults(fig2)
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

st.markdown('<div class="chart-card"><div class="chart-title">Adoption Rate by Sex</div><div class="chart-desc">Adoption likelihood by sex / reproductive status</div></div>', unsafe_allow_html=True)
sex_rate = df.groupby("Sex")["Adopted"].mean().reset_index()
sex_rate["Rate"] = (sex_rate["Adopted"] * 100).round(1)
sex_rate = sex_rate.sort_values("Rate")
fig_sex = px.bar(sex_rate, y="Sex", x="Rate", orientation="h",
                 color="Sex", color_discrete_sequence=PALETTE, text="Rate")
fig_sex.update_traces(texttemplate="%{text:.1f}%", textposition="outside", marker_line_width=0)
fig_sex.update_layout(showlegend=False, xaxis_title="Adoption Rate (%)", yaxis_title="")
plotly_defaults(fig_sex, height=260)
st.plotly_chart(fig_sex, use_container_width=True, config={"displayModeBar": False})


# ─── DEMOGRAPHICS ─────────────────────────────────────────────────────────────
section("Demographics")
dem_c1, dem_c2 = st.columns(2)

with dem_c1:
    st.markdown('<div class="chart-card"><div class="chart-title">Intake Condition Breakdown</div><div class="chart-desc">Proportion of animals by condition on intake</div></div>', unsafe_allow_html=True)
    cond_df = df["IntakeCondition"].value_counts().reset_index()
    cond_df.columns = ["Condition","Count"]
    fig_donut = px.pie(cond_df, names="Condition", values="Count",
                       hole=0.5, color_discrete_sequence=PALETTE)
    fig_donut.update_traces(textposition="outside", textinfo="percent+label",
                            marker=dict(line=dict(color="#faf9f6", width=2)))
    fig_donut.update_layout(showlegend=False)
    plotly_defaults(fig_donut, height=320)
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with dem_c2:
    st.markdown('<div class="chart-card"><div class="chart-title">Animal Type Mix</div><div class="chart-desc">Distribution of animal types across selected shelters</div></div>', unsafe_allow_html=True)
    type_df = df["AnimalType"].value_counts().reset_index()
    type_df.columns = ["AnimalType","Count"]
    fig_type = px.pie(type_df, names="AnimalType", values="Count",
                      hole=0.5, color_discrete_sequence=PALETTE)
    fig_type.update_traces(textposition="outside", textinfo="percent+label",
                           marker=dict(line=dict(color="#faf9f6", width=2)))
    fig_type.update_layout(showlegend=False)
    plotly_defaults(fig_type, height=320)
    st.plotly_chart(fig_type, use_container_width=True, config={"displayModeBar": False})


# ─── AGE AT INTAKE ────────────────────────────────────────────────────────────
section("Age at Intake")
st.markdown('<div class="chart-card"><div class="chart-title">Age Distribution by Outcome</div><div class="chart-desc">Age at intake for adopted vs not adopted animals (up to 15 yrs)</div></div>', unsafe_allow_html=True)
age_df = df[df["Age_Years"].between(0, 15)].copy()
age_df["Outcome"] = age_df["Adopted"].map({1:"Adopted", 0:"Not Adopted"})
fig_age = px.histogram(age_df, x="Age_Years", color="Outcome", nbins=60,
                        barmode="overlay", opacity=0.72,
                        color_discrete_map={"Adopted":"#4a9e6b","Not Adopted":"#c95c5c"})
fig_age.update_layout(xaxis_title="Age (Years)", yaxis_title="Count",
                       legend_title="", bargap=0.02)
plotly_defaults(fig_age, height=340)
st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False})

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;color:#9b8640;font-size:0.82rem;font-family:Inter,sans-serif;">
  Pet Adoption Finder · Data from Austin Animal Center, Long Beach Animal Care, San José Animal Services
</div>""", unsafe_allow_html=True)
