import streamlit as st
import requests
from datetime import datetime, timedelta
import math
import os


try:
    from streamlit_folium import st_folium
    import folium
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Weather Broadcast",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CITY DATA
# ============================================================

CITIES = {
    "Rawalpindi": {"lat": 33.6007, "lon": 73.0679},
    "Islamabad": {"lat": 33.6844, "lon": 73.0479},
    "Lahore": {"lat": 31.5204, "lon": 74.3587},
    "Karachi": {"lat": 24.8607, "lon": 67.0011},
    "Peshawar": {"lat": 34.0151, "lon": 71.5249},
    "Quetta": {"lat": 30.1798, "lon": 66.9750},
    "Multan": {"lat": 30.1575, "lon": 71.5249},
    "Faisalabad": {"lat": 31.4504, "lon": 73.1350},
    "Gujranwala": {"lat": 32.1877, "lon": 74.1945},
    "Sialkot": {"lat": 32.4945, "lon": 74.5229},
    "Hyderabad": {"lat": 25.3960, "lon": 68.3578},
    "Bahawalpur": {"lat": 29.3956, "lon": 71.6836},
    "Sargodha": {"lat": 32.0836, "lon": 72.6711},
    "Abbottabad": {"lat": 34.1688, "lon": 73.2215},
    "Mardan": {"lat": 34.1989, "lon": 72.0408},
}


# ============================================================
# SESSION STATE
# ============================================================

if "selected_city" not in st.session_state:
    st.session_state.selected_city = "Rawalpindi"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


# ============================================================
# THEME
# ============================================================

if st.session_state.dark_mode:
    BG = "#07111f"
    BG2 = "#0b1d35"
    CARD = "rgba(30,52,79,.78)"
    CARD2 = "rgba(18,35,57,.72)"
    TEXT = "#f8fafc"
    MUTED = "#8fa2bb"
    BORDER = "rgba(148,163,184,.14)"
    SIDEBAR = "#0a1426"
else:
    BG = "#eef5fb"
    BG2 = "#dbeafe"
    CARD = "rgba(255,255,255,.90)"
    CARD2 = "rgba(248,250,252,.94)"
    TEXT = "#0f172a"
    MUTED = "#52657d"
    BORDER = "rgba(71,85,105,.16)"
    SIDEBAR = "#f8fafc"


# ============================================================
# PROFESSIONAL UI THEME
# ============================================================

st.markdown(
    f"""
<style>
.stApp {{
    background:
        radial-gradient(circle at 85% 5%, rgba(56,189,248,.10), transparent 25%),
        radial-gradient(circle at 10% 25%, rgba(99,102,241,.08), transparent 28%),
        linear-gradient(135deg, {BG} 0%, {BG2} 52%, {BG} 100%);
    color: {TEXT};
}}

.block-container {{
    max-width: 1450px;
    padding: 2.2rem 3rem 3rem;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

[data-testid="stSidebar"] {{
    background: {SIDEBAR};
    border-right: 1px solid {BORDER};
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.8rem;
}}

hr {{
    border-color: {BORDER} !important;
}}

.sidebar-brand {{
    padding: 8px 4px 18px;
}}

.sidebar-logo {{
    font-size: 34px;
    margin-bottom: 4px;
}}

.sidebar-title {{
    color: {TEXT};
    font-size: 21px;
    font-weight: 800;
}}

.sidebar-subtitle {{
    color: {MUTED};
    font-size: 13px;
    margin-top: 3px;
}}

.side-label {{
    color: {TEXT};
    font-size: 14px;
    font-weight: 700;
    margin: 14px 0 8px;
}}

.side-location {{
    background: linear-gradient(135deg, rgba(37,99,235,.18), rgba(14,165,233,.10));
    border: 1px solid rgba(56,189,248,.16);
    border-radius: 12px;
    padding: 13px 14px;
    color: {TEXT};
    line-height: 1.65;
}}

.status-card {{
    background: rgba(16,185,129,.10);
    border: 1px solid rgba(52,211,153,.18);
    border-radius: 12px;
    padding: 12px 14px;
    color: #10b981;
    font-size: 13px;
    font-weight: 700;
}}

.brand-row {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 4px;
}}

.brand-icon {{
    width: 58px;
    height: 58px;
    border-radius: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    background: linear-gradient(135deg, rgba(56,189,248,.18), rgba(99,102,241,.18));
    border: 1px solid rgba(125,211,252,.16);
    box-shadow: 0 12px 35px rgba(0,0,0,.18);
}}

.main-title {{
    font-size: clamp(34px, 4vw, 50px);
    font-weight: 850;
    letter-spacing: -1.8px;
    color: {TEXT};
    line-height: 1.05;
}}

.subtitle {{
    font-size: 16px;
    color: {MUTED};
    margin: 8px 0 26px 74px;
}}

.weather-hero {{
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, {CARD}, {CARD2});
    border: 1px solid {BORDER};
    border-radius: 26px;
    padding: 28px 32px;
    margin: 12px 0 28px;
    box-shadow: 0 22px 60px rgba(0,0,0,.16);
}}

.location {{
    position: relative;
    color: #38bdf8;
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 10px;
}}

.hero-weather-icon {{
    font-size: 112px;
    line-height: 1;
    text-align: center;
    padding: 12px 0;
}}

.temperature {{
    color: {TEXT};
    font-size: clamp(62px, 7vw, 86px);
    font-weight: 850;
    letter-spacing: -3px;
    line-height: .95;
    margin-top: 10px;
}}

.condition {{
    color: {TEXT};
    opacity: .86;
    font-size: 21px;
    font-weight: 650;
    text-transform: capitalize;
    margin-top: 12px;
}}

.feels-like {{
    color: {MUTED};
    font-size: 14px;
    margin-top: 7px;
}}

.section-title {{
    color: {TEXT};
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -.4px;
    margin: 30px 0 14px;
}}

.metric-box {{
    min-height: 150px;
    padding: 22px 18px;
    text-align: center;
    border-radius: 19px;
    background: linear-gradient(145deg, {CARD}, {CARD2});
    border: 1px solid {BORDER};
    box-shadow: 0 12px 30px rgba(0,0,0,.10);
    transition: transform .2s ease, border-color .2s ease;
}}

.metric-box:hover {{
    transform: translateY(-3px);
    border-color: rgba(56,189,248,.28);
}}

.metric-icon {{
    font-size: 30px;
    margin-bottom: 7px;
}}

.metric-name {{
    color: {MUTED};
    font-size: 13px;
    font-weight: 600;
}}

.metric-number {{
    color: {TEXT};
    font-size: 25px;
    font-weight: 800;
    margin-top: 6px;
}}

.forecast-card {{
    background: linear-gradient(145deg, {CARD}, {CARD2});
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 18px 12px;
    text-align: center;
    min-height: 225px;
    box-shadow: 0 10px 28px rgba(0,0,0,.09);
}}

.forecast-day {{
    color: {TEXT};
    font-weight: 800;
    font-size: 15px;
}}

.forecast-date {{
    color: {MUTED};
    font-size: 12px;
    margin-top: 3px;
}}

.forecast-icon {{
    font-size: 42px;
    margin: 10px 0 3px;
}}

.forecast-temp {{
    color: {TEXT};
    font-size: 25px;
    font-weight: 800;
}}

.forecast-range {{
    color: {MUTED};
    font-size: 12px;
    margin-top: 3px;
}}

.forecast-condition {{
    color: {TEXT};
    opacity: .82;
    font-size: 12px;
    text-transform: capitalize;
    margin: 9px 0;
}}

.rain-badge {{
    display: inline-block;
    border-radius: 999px;
    padding: 5px 9px;
    background: rgba(56,189,248,.12);
    color: #38bdf8;
    font-size: 11px;
    font-weight: 750;
}}

.map-note {{
    color: {MUTED};
    font-size: 13px;
    margin-bottom: 10px;
}}

[data-testid="stMetric"] {{
    background: linear-gradient(145deg, {CARD}, {CARD2});
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 17px 18px;
    min-height: 88px;
}}

[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
}}

[data-testid="stMetricValue"] {{
    color: {TEXT} !important;
}}

.stButton > button {{
    width: 100%;
    border-radius: 11px;
    border: 1px solid rgba(96,165,250,.20);
    background: rgba(37,99,235,.12);
    color: {TEXT};
    font-weight: 700;
}}

.stButton > button:hover {{
    border-color: rgba(56,189,248,.45);
    background: rgba(37,99,235,.22);
}}

.footer {{
    color: {MUTED};
    text-align: center;
    font-size: 12px;
    padding: 18px 0 4px;
}}

@media (max-width: 800px) {{
    .block-container {{
        padding: 1.2rem 1rem 2rem;
    }}

    .subtitle {{
        margin-left: 0;
    }}

    .weather-hero {{
        padding: 22px 18px;
    }}

    .hero-weather-icon {{
        font-size: 82px;
    }}
}}
</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# API KEY
# ============================================================

# try:
#     with open("api_key.txt", "r") as file:
#         API_KEY = file.read().strip()
# except FileNotFoundError:
#     st.error("❌ api_key.txt was not found.")
#     st.stop()

# if not API_KEY:
#     st.error("❌ api_key.txt is empty.")
#     st.stop()


API_KEY = None

# 1. Try retrieving from Streamlit Cloud Secrets safely
try:
    if "API_KEY" in st.secrets:
        API_KEY = st.secrets["API_KEY"]
except Exception:
    # Safely skip if running locally without a local secrets.toml
    pass

# 2. Fall back to local api_key.txt if key was not found in Secrets
if not API_KEY and os.path.exists("api_key.txt"):
    try:
        with open("api_key.txt", "r") as file:
            API_KEY = file.read().strip()
    except Exception as e:
        st.error(f"❌ Error reading api_key.txt: {e}")
        st.stop()

# 3. Handle missing key error
if not API_KEY:
    st.error("❌ API Key not found in Streamlit Secrets or api_key.txt.")
    st.stop()
    
# ============================================================
# API HELPERS
# ============================================================

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"


def get_current_weather(city):
    params = {
        "q": f"{city},PK",
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(CURRENT_URL, params=params, timeout=15)
        if response.status_code != 200:
            return None, f"Current weather error: {response.status_code}"
        return response.json(), None
    except requests.exceptions.RequestException as error:
        return None, f"Connection error: {error}"


def get_onecall_forecast(lat, lon):
    """Try One Call 3.0 first. It provides daily 7-day forecast."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "exclude": "minutely,alerts"
    }

    try:
        response = requests.get(ONECALL_URL, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if data.get("daily"):
                return data["daily"][:7], "onecall"

        return None, None
    except requests.exceptions.RequestException:
        return None, None


def get_five_day_forecast(lat, lon):
    """Free fallback using the 5-day / 3-hour forecast endpoint."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(FORECAST_URL, params=params, timeout=15)

        if response.status_code != 200:
            return None, None

        data = response.json()
        return build_daily_fallback(data), "5day"
    except requests.exceptions.RequestException:
        return None, None


def build_daily_fallback(data):
    """
    Convert OpenWeather's 3-hour forecast into approximately daily cards.
    The free endpoint covers about 5 days, so the UI clearly labels it.
    """
    buckets = {}

    for item in data.get("list", []):
        date_text = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")

        if date_text not in buckets:
            buckets[date_text] = []

        buckets[date_text].append(item)

    daily = []

    for date_text, items in list(buckets.items())[:5]:
        temps = [x["main"]["temp"] for x in items]
        rain_values = [x.get("pop", 0) for x in items]

        representative = min(
            items,
            key=lambda x: abs(
                datetime.fromtimestamp(x["dt"]).hour - 12
            )
        )

        daily.append({
            "dt": items[len(items) // 2]["dt"],
            "temp": {
                "day": sum(temps) / len(temps),
                "min": min(temps),
                "max": max(temps)
            },
            "weather": representative.get("weather", []),
            "pop": max(rain_values) if rain_values else 0
        })

    return daily


def get_forecast(lat, lon):
    daily, source = get_onecall_forecast(lat, lon)

    if daily:
        return daily, source

    return get_five_day_forecast(lat, lon)


def weather_icon(code):
    icons = {
        "01d": "☀️", "01n": "🌙",
        "02d": "🌤️", "02n": "🌙",
        "03d": "☁️", "03n": "☁️",
        "04d": "☁️", "04n": "☁️",
        "09d": "🌧️", "09n": "🌧️",
        "10d": "🌦️", "10n": "🌧️",
        "11d": "⛈️", "11n": "⛈️",
        "13d": "❄️", "13n": "❄️",
        "50d": "🌫️", "50n": "🌫️"
    }
    return icons.get(code, "🌤️")


def wind_direction_text(degrees):
    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]
    return directions[round(degrees / 22.5) % 16]


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-logo">🌤️</div>
            <div class="sidebar-title">Weather Broadcast</div>
            <div class="sidebar-subtitle">Live Weather Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        '<div class="side-label">📍 Pakistan City</div>',
        unsafe_allow_html=True
    )

    city_names = list(CITIES.keys())

    selected_city = st.selectbox(
        "Choose a city",
        city_names,
        index=city_names.index(st.session_state.selected_city),
        label_visibility="collapsed"
    )

    if selected_city != st.session_state.selected_city:
        st.session_state.selected_city = selected_city
        st.rerun()

    st.markdown(
        f"""
        <div class="side-location">
            <strong>{selected_city}</strong><br>
            Pakistan 🇵🇰
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    

    if st.button("↻  Refresh Weather", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.caption("Real-time weather data")
    st.caption("Python • Streamlit • OpenWeather")


# ============================================================
# CURRENT WEATHER
# ============================================================

current, current_error = get_current_weather(st.session_state.selected_city)

if current_error:
    st.error(f"❌ {current_error}")
    st.stop()


city = current["name"]
country = current["sys"]["country"]

temperature = current["main"]["temp"]
feels_like = current["main"]["feels_like"]
temp_min = current["main"]["temp_min"]
temp_max = current["main"]["temp_max"]
humidity = current["main"]["humidity"]
pressure = current["main"]["pressure"]
wind_speed = current["wind"]["speed"]
wind_direction = current["wind"].get("deg", 0)
cloud_cover = current["clouds"]["all"]
visibility = current.get("visibility", 0)
description = current["weather"][0]["description"]
icon_code = current["weather"][0]["icon"]

sunrise = datetime.fromtimestamp(
    current["sys"]["sunrise"]
).strftime("%I:%M %p")

sunset = datetime.fromtimestamp(
    current["sys"]["sunset"]
).strftime("%I:%M %p")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    f"""
    <div class="brand-row">
        <div class="brand-icon">🌤️</div>
        <div class="main-title">Weather Broadcast</div>
    </div>
    <div class="subtitle">
        Live weather intelligence for {city}, Pakistan
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

st.markdown('<div class="weather-hero">', unsafe_allow_html=True)

st.markdown(
    f'<div class="location">📍 {city}, {country}</div>',
    unsafe_allow_html=True
)

hero_col1, hero_col2 = st.columns([1, 2])

with hero_col1:
    st.markdown(
        f'<div class="hero-weather-icon">{weather_icon(icon_code)}</div>',
        unsafe_allow_html=True
    )

with hero_col2:
    st.markdown(
        f"""
        <div class="temperature">{round(temperature)}°C</div>
        <div class="condition">{description}</div>
        <div class="feels-like">
            Feels like {round(feels_like)}°C
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CURRENT CONDITIONS
# ============================================================

st.markdown(
    '<div class="section-title">📊 Current Conditions</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

metric_data = [
    ("💧", "Humidity", f"{humidity}%"),
    ("💨", "Wind Speed", f"{wind_speed:.1f} m/s"),
    ("☁️", "Cloud Cover", f"{cloud_cover}%"),
    ("🌡️", "Pressure", f"{pressure} hPa"),
]

for col, (icon, name, value) in zip(
    [col1, col2, col3, col4],
    metric_data
):
    with col:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-icon">{icon}</div>
                <div class="metric-name">{name}</div>
                <div class="metric-number">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ADDITIONAL INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">🌡️ Additional Information</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🌡️ Minimum", f"{round(temp_min)}°C")

with col2:
    st.metric("🌡️ Maximum", f"{round(temp_max)}°C")

with col3:
    st.metric("👁️ Visibility", f"{visibility / 1000:.1f} km")

with col4:
    st.metric(
        "🧭 Wind",
        f"{wind_direction_text(wind_direction)} ({round(wind_direction)}°)"
    )


# ============================================================
# SUN INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">🌅 Sun Information</div>',
    unsafe_allow_html=True
)

sun_col1, sun_col2 = st.columns(2)

with sun_col1:
    st.metric("🌅 Sunrise", sunrise)

with sun_col2:
    st.metric("🌇 Sunset", sunset)



# ============================================================
# API INFORMATION
# ============================================================

with st.expander("🔧 API Information"):

    st.write("Weather provider: OpenWeather")

    st.write("Current weather endpoint: OpenWeather Current Weather API")


    st.write("Selected city:", city)

    st.write("Country:", country)

    st.write("Last refreshed:",
             datetime.now().strftime("%d %b %Y, %I:%M %p"))


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        🌤️ <strong>Weather Broadcast</strong>
        &nbsp;•&nbsp; Powered by OpenWeather
        &nbsp;•&nbsp; Built with Python & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
