"""
AgriSmart Pro - Crop Quality Prediction System
Main Streamlit Application - COMPLETE ENHANCED VERSION
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


# Import custom modules
from models import CropPredictor, FertilizerCalculator, IrrigationCalculator, ProfitCalculator
from utils import (
    fetch_weather_data, save_to_history, load_history, get_statistics, export_data,
    create_radar_chart, create_comparison_chart, create_yield_comparison_chart,
    create_history_trend_chart, create_cost_breakdown_pie, create_npk_comparison_chart,
    create_weather_forecast_chart
)
from config import CROP_PARAMETERS, REGIONAL_DATA, QUALITY_COLORS

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="AgriSmart Pro - Crop Quality Predictor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
    footer, header {visibility: hidden;}
    h1, h2, h3, h4, h5, h6, p, div, span, label { color: white !important; }
    .custom-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 20px; padding: 30px; margin-bottom: 20px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .section-header {
        color: #10b981 !important; font-size: 1.8rem; font-weight: 700;
        margin-bottom: 25px; text-transform: uppercase; letter-spacing: 1px;
    }
    .info-box {
        background: rgba(0, 0, 0, 0.4); border-radius: 12px; padding: 18px;
        margin: 10px 0; border-left: 4px solid #10b981; transition: all 0.3s;
    }
    .info-box:hover {
        background: rgba(0, 0, 0, 0.6); border-left: 4px solid #84cc16;
        transform: translateX(5px);
    }
    .info-label {
        color: #10b981 !important; font-size: 0.75rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;
    }
    .info-value { color: #ffffff !important; font-size: 1rem; font-weight: 500; }
    .stButton > button {
        width: 100%; background: linear-gradient(90deg, #10b981, #84cc16) !important;
        color: black !important; font-weight: 700; font-size: 1.1rem; padding: 15px;
        border-radius: 15px; border: none; transition: all 0.3s;
        text-transform: uppercase; letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px); box-shadow: 0 10px 25px rgba(16, 185, 129, 0.5);
    }
    .stSlider > div > div > div > div { background: linear-gradient(90deg, #10b981, #84cc16) !important; }
    .stSlider > div > div > div { background: rgba(255, 255, 255, 0.1) !important; }
    .stSelectbox > div > div {
        background-color: rgba(0, 0, 0, 0.5) !important; border-radius: 12px;
        border: 1px solid rgba(16, 185, 129, 0.3) !important; color: white !important;
    }
    .stSelectbox label, .stNumberInput label {
        color: #94a3b8 !important; font-weight: 600;
        text-transform: uppercase; font-size: 0.85rem;
    }
    .stNumberInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: white !important; border-radius: 10px;
    }
    .metric-container {
        background: rgba(0, 0, 0, 0.3); border-radius: 12px; padding: 20px;
        text-align: center; border: 1px solid rgba(16, 185, 129, 0.2);
    }
    .metric-label {
        color: #94a3b8 !important; font-size: 0.85rem; font-weight: 600;
        text-transform: uppercase; margin-bottom: 10px;
    }
    .metric-value { color: #10b981 !important; font-size: 2rem; font-weight: 700; }
    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #94a3b8 !important; border: 1px solid rgba(148, 163, 184, 0.2);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #10b981, #84cc16) !important;
        color: black !important;
    }
    hr { border-color: rgba(100, 116, 139, 0.2) !important; margin: 30px 0; }
    
    /* Enhanced Insight Card Styles */
    .insight-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(132, 204, 22, 0.15) 100%);
        border: 2px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
    }
    .insight-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(132, 204, 22, 0.6);
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.4);
    }
    .insight-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.5s;
    }
    .insight-card:hover::before {
        left: 100%;
    }
    .insight-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    .insight-title {
        color: #10b981 !important;
        font-size: 1.1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    .insight-text {
        color: #e2e8f0 !important;
        font-size: 1rem;
        line-height: 1.8;
        font-weight: 500;
    }
    .insight-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background: linear-gradient(135deg, #10b981, #84cc16);
        color: black;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .insights-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }
    
    /* Timeline Styles for Fertilizer Schedule */
    .timeline-container {
        position: relative;
        padding: 40px 20px;
    }
    .timeline-line {
        position: absolute;
        left: 50%;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #10b981 0%, #3b82f6 50%, #f59e0b 100%);
        transform: translateX(-50%);
        border-radius: 10px;
    }
    .timeline-item {
        position: relative;
        margin-bottom: 80px;
    }
    .timeline-dot {
        position: absolute;
        left: 50%;
        top: 30px;
        transform: translateX(-50%);
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5rem;
        box-shadow: 0 0 0 8px rgba(0, 0, 0, 0.3);
        animation: pulse-dot 2s infinite;
        z-index: 10;
    }
    @keyframes pulse-dot {
        0%, 100% { box-shadow: 0 0 0 8px rgba(0, 0, 0, 0.3), 0 0 0 16px rgba(16, 185, 129, 0.1); }
        50% { box-shadow: 0 0 0 8px rgba(0, 0, 0, 0.3), 0 0 0 24px rgba(16, 185, 129, 0.2); }
    }
    .timeline-content-left {
        width: 45%;
        margin-right: auto;
        padding-right: 60px;
    }
    .timeline-content-right {
        width: 45%;
        margin-left: auto;
        padding-left: 60px;
    }
    .stage-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(16, 185, 129, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
    }
    .stage-card:hover {
        transform: scale(1.03) translateY(-10px);
        box-shadow: 0 20px 60px rgba(16, 185, 129, 0.4);
        border-color: rgba(132, 204, 22, 0.6);
    }
    .stage-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
        color: black;
    }
    .tip-item {
        padding: 12px 15px;
        margin: 8px 0;
        background: rgba(16, 185, 129, 0.1);
        border-left: 3px solid #10b981;
        border-radius: 8px;
        font-size: 0.9rem;
        transition: all 0.3s;
    }
    .tip-item:hover {
        background: rgba(16, 185, 129, 0.2);
        transform: translateX(10px);
    }
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if 'page' not in st.session_state: st.session_state['page'] = 'input'
if 'prediction' not in st.session_state: st.session_state['prediction'] = None
if 'history' not in st.session_state: st.session_state['history'] = []
if 'weather' not in st.session_state: st.session_state['weather'] = None
if 'cost_data' not in st.session_state:
    st.session_state['cost_data'] = {'seed_cost': 5000, 'fertilizer_cost': 8000, 
        'labor_cost': 15000, 'irrigation_cost': 6000, 'expected_price': 25}
if 'input_params' not in st.session_state:
    st.session_state['input_params'] = {'location': 'West Bengal', 'crop_type': 'wheat',
        'nitrogen': 50, 'phosphorus': 50, 'potassium': 50, 'ph': 6.5,
        'temperature': 25, 'humidity': 65, 'rainfall': 100}
if 'comparison_results' not in st.session_state: st.session_state['comparison_results'] = None

# INITIALIZE MODELS
predictor = CropPredictor()
fert_calculator = FertilizerCalculator()
irrig_calculator = IrrigationCalculator()
profit_calculator = ProfitCalculator()

def navigate_to(page_name):
    st.session_state['page'] = page_name
    st.rerun()

# HEADER
st.markdown("""
<div style='text-align: center; padding: 40px 20px 20px 20px;'>
    <div style='font-size: 3.5rem; font-weight: 900; 
                background: linear-gradient(90deg, #10b981, #84cc16, #22c55e);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        🌾 AgriSmart Pro
    </div>
    <div style='color: #10b981; font-size: 1rem; font-weight: 600; 
                letter-spacing: 2px; text-transform: uppercase;'>
        ⚡ Advanced Crop Quality & Management System
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# NAVIGATION
menu_cols = st.columns(6)
pages = [("📝 Input", 'input'), ("🔮 Prediction", 'prediction'), ("⚖️ Compare", 'compare'),
         ("🌱 Fertilizer", 'fertilizer'), ("💧 Irrigation", 'irrigation'), ("💰 Profit", 'profit')]
for col, (label, page) in zip(menu_cols, pages):
    with col:
        if st.button(label, use_container_width=True, 
                     type="primary" if st.session_state['page'] == page else "secondary"):
            navigate_to(page)
st.markdown("---")

# ============= INPUT PAGE =============
if st.session_state['page'] == 'input':
    st.markdown('<div class="section-header">📝 INPUT PARAMETERS</div>', unsafe_allow_html=True)
    st.markdown("Enter your farm conditions and soil parameters")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📍 LOCATION INFORMATION</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        location = st.selectbox("Select State", list(REGIONAL_DATA.keys()),
            index=list(REGIONAL_DATA.keys()).index(st.session_state['input_params']['location']))
        st.session_state['input_params']['location'] = location
    with col2:
        if st.button("🌤️ Fetch Live Weather", use_container_width=True, type="primary", key="weather_btn"):
            with st.spinner("Fetching weather data..."):
                weather_data = fetch_weather_data(location)
                st.session_state['weather'] = weather_data
                st.session_state['input_params']['temperature'] = int(weather_data['temperature'])
                st.session_state['input_params']['humidity'] = int(weather_data['humidity'])
                st.session_state['input_params']['rainfall'] = int(weather_data['rainfall'])
                st.success("✅ Weather data updated!")
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    if location in REGIONAL_DATA:
        region_info = REGIONAL_DATA[location]
        cols = st.columns(4)
        info_items = [
            ("Suitable Crops", ', '.join(region_info['suitable_crops'])),
            ("Season", region_info['season']),
            ("Rainfall Pattern", region_info['rainfall_pattern']),
            ("Soil Type", region_info['soil_type'])
        ]
        for col, (label, value) in zip(cols, info_items):
            with col:
                st.markdown(f"""
                <div class="info-box">
                    <div class="info-label">{label}</div>
                    <div class="info-value">{value}</div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">🌾 CROP SELECTION</h3>', unsafe_allow_html=True)
    crop_type = st.selectbox("Select Crop Type",
        ['wheat', 'rice', 'maize', 'cotton', 'sugarcane', 'potato', 'tomato', 'soybean'],
        index=['wheat', 'rice', 'maize', 'cotton', 'sugarcane', 'potato', 'tomato', 'soybean'].index(
            st.session_state['input_params']['crop_type']))
    st.session_state['input_params']['crop_type'] = crop_type
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 25px;">🧪 SOIL PARAMETERS</h3>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nitrogen = st.number_input("Nitrogen (N) - kg/ha", 0, 140, 
            st.session_state['input_params']['nitrogen'], 5)
        st.session_state['input_params']['nitrogen'] = nitrogen
    with col2:
        phosphorus = st.number_input("Phosphorus (P) - kg/ha", 0, 100,
            st.session_state['input_params']['phosphorus'], 5)
        st.session_state['input_params']['phosphorus'] = phosphorus
    with col3:
        potassium = st.number_input("Potassium (K) - kg/ha", 0, 100,
            st.session_state['input_params']['potassium'], 5)
        st.session_state['input_params']['potassium'] = potassium
    with col4:
        ph = st.slider("pH Level", 3.0, 10.0, float(st.session_state['input_params']['ph']), 0.1)
        st.session_state['input_params']['ph'] = ph
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 25px;">🌡️ CLIMATE PARAMETERS</h3>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        temperature = st.slider("Temperature (°C)", 0, 50, 
            st.session_state['input_params']['temperature'], 1)
        st.session_state['input_params']['temperature'] = temperature
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Current Temperature</div>
            <div class="metric-value">{temperature}°C</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        humidity = st.slider("Humidity (%)", 0, 100,
            st.session_state['input_params']['humidity'], 5)
        st.session_state['input_params']['humidity'] = humidity
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Current Humidity</div>
            <div class="metric-value">{humidity}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        rainfall = st.slider("Rainfall (mm)", 0, 300,
            st.session_state['input_params']['rainfall'], 10)
        st.session_state['input_params']['rainfall'] = rainfall
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Current Rainfall</div>
            <div class="metric-value">{rainfall}mm</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state['weather']:
        weather = st.session_state['weather']
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">🌤️ CURRENT WEATHER CONDITIONS</h3>', unsafe_allow_html=True)
        cols = st.columns(5)
        metrics = [("🌡️ Temperature", f"{weather['temperature']}°C"),
                   ("💧 Humidity", f"{weather['humidity']}%"),
                   ("🌧️ Rainfall", f"{weather['rainfall']}mm"),
                   ("☁️ Condition", weather['condition']),
                   ("💨 Wind", f"{weather['wind_speed']} km/h")]
        for col, (label, value) in zip(cols, metrics):
            with col: st.metric(label, value)
        if 'forecast' in weather:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### 📅 5-Day Forecast")
            forecast_chart = create_weather_forecast_chart(weather['forecast'])
            if forecast_chart: st.plotly_chart(forecast_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    alerts = predictor.generate_alerts(nitrogen, phosphorus, potassium,
                                        temperature, humidity, ph, rainfall)
    if alerts:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #f59e0b; margin-bottom: 20px;">⚠️ ALERTS & WARNINGS</h3>', unsafe_allow_html=True)
        for alert in alerts:
            if alert['type'] == 'critical': st.error(f"🚨 {alert['message']}")
            else: st.warning(f"⚠️ {alert['message']}")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 ANALYZE CROP QUALITY", use_container_width=True, type="primary", key="analyze_btn"):
            input_data = {'nitrogen': nitrogen, 'phosphorus': phosphorus, 'potassium': potassium,
                          'temperature': temperature, 'humidity': humidity, 'ph': ph,
                          'rainfall': rainfall, 'crop_type': crop_type}
            with st.spinner("🔮 Analyzing crop quality..."):
                prediction = predictor.predict(input_data)
                st.session_state['prediction'] = prediction
                record = save_to_history(prediction, input_data)
                st.session_state['history'].insert(0, record)
            st.success("✅ Analysis complete!")
            st.balloons()
            navigate_to('prediction')

# ============= PREDICTION PAGE WITH ENHANCED INSIGHTS =============
elif st.session_state['page'] == 'prediction':
    st.markdown('<div class="section-header">🔮 CROP QUALITY PREDICTION RESULTS</div>', unsafe_allow_html=True)
    
    if st.session_state['prediction']:
        pred = st.session_state['prediction']
        params = st.session_state['input_params']
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        quality_color = QUALITY_COLORS.get(pred['quality'], '#888888')
        
        with col1:
            st.markdown(f"""
            <div style='height: 220px; display: flex; align-items: center; justify-content: center;'>
                <svg viewBox="0 0 200 200" style='width: 100%; max-width: 200px;'>
                    <polygon points="100,10 175,55 175,145 100,190 25,145 25,55" 
                             fill="{quality_color}" opacity="0.15" stroke="{quality_color}" stroke-width="3"/>
                    <polygon points="100,10 175,55 175,145 100,190 25,145 25,55" 
                             fill="none" stroke="{quality_color}" stroke-width="8" 
                             stroke-dasharray="{pred['score']*6} 1000"
                             transform="rotate(-90 100 100)" stroke-linecap="round"/>
                    <text x="100" y="85" text-anchor="middle" fill="white" font-size="13" font-weight="600">Quality Score</text>
                    <text x="100" y="115" text-anchor="middle" fill="{quality_color}" font-size="38" font-weight="bold">{pred['score']}%</text>
                    <text x="100" y="140" text-anchor="middle" fill="white" font-size="16" font-weight="600">{pred['quality']}</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='height: 220px; display: flex; align-items: center; justify-content: center;'>
                <svg viewBox="0 0 200 200" style='width: 100%; max-width: 200px;'>
                    <circle cx="100" cy="100" r="80" fill="rgba(59, 130, 246, 0.15)" stroke="#3b82f6" stroke-width="3"/>
                    <circle cx="100" cy="100" r="80" fill="none" stroke="#3b82f6" stroke-width="8" 
                            stroke-dasharray="{pred['yield_percentage']*5} 500" stroke-dashoffset="125"
                            transform="rotate(-90 100 100)" stroke-linecap="round"/>
                    <text x="100" y="80" text-anchor="middle" fill="white" font-size="13" font-weight="600">Expected Yield</text>
                    <text x="100" y="112" text-anchor="middle" fill="#3b82f6" font-size="34" font-weight="bold">{pred['estimated_yield']}</text>
                    <text x="100" y="135" text-anchor="middle" fill="white" font-size="12">tonnes/hectare</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='height: 220px; display: flex; align-items: center; justify-content: center;'>
                <svg viewBox="0 0 200 200" style='width: 100%; max-width: 200px;'>
                    <polygon points="100,20 180,100 100,180 20,100" 
                             fill="rgba(139, 92, 246, 0.15)" stroke="#8b5cf6" stroke-width="3"/>
                    <polygon points="100,20 180,100 100,180 20,100" 
                             fill="none" stroke="#8b5cf6" stroke-width="6" 
                             stroke-dasharray="{pred['yield_percentage']*6.4} 1000"/>
                    <text x="100" y="85" text-anchor="middle" fill="white" font-size="13" font-weight="600">Yield %</text>
                    <text x="100" y="115" text-anchor="middle" fill="#8b5cf6" font-size="36" font-weight="bold">{pred['yield_percentage']}%</text>
                    <text x="100" y="140" text-anchor="middle" fill="white" font-size="13">of Optimal</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='height: 220px; display: flex; align-items: center; justify-content: center;'>
                <svg viewBox="0 0 200 200" style='width: 100%; max-width: 200px;'>
                    <path d="M100,20 L170,50 L170,110 Q170,160 100,185 Q30,160 30,110 L30,50 Z" 
                          fill="rgba(16, 185, 129, 0.15)" stroke="#10b981" stroke-width="3"/>
                    <text x="100" y="85" text-anchor="middle" fill="white" font-size="13" font-weight="600">Crop Type</text>
                    <text x="100" y="115" text-anchor="middle" fill="#10b981" font-size="22" font-weight="bold">{params['crop_type'].title()}</text>
                    <text x="100" y="140" text-anchor="middle" fill="white" font-size="13">{params['location']}</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if 'growth_duration' in pred:
            st.info(f"🕐 **Estimated Growth Duration:** {pred['growth_duration']} {pred.get('growth_duration_unit', 'days')}")
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown('<h3 style="color: #10b981; margin-bottom: 25px;">📊 FACTOR PERFORMANCE MATRIX</h3>', unsafe_allow_html=True)
            for factor in pred['factors']:
                score = factor['score']
                if score >= 80: color, status = "#10b981", "Excellent"
                elif score >= 65: color, status = "#3b82f6", "Good"
                elif score >= 50: color, status = "#f59e0b", "Average"
                else: color, status = "#ef4444", "Poor"
                
                segments = ''.join([f'<div style="width: 10%; height: 100%; background: {color}; '
                                    f'opacity: {1 if score >= (i+1)*10 else 0.15}; margin: 0 1px;"></div>' 
                                    for i in range(10)])
                
                st.markdown(f"""
                <div style='margin-bottom: 25px;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <div>
                            <span style='font-weight: 700; color: white; font-size: 1rem;'>{factor['name']}</span>
                            <span style='color: #94a3b8; font-size: 0.85rem; margin-left: 10px;'>
                                Current: {factor['current']} | Optimal: {factor['optimal']}
                            </span>
                        </div>
                        <span style='color: {color}; font-weight: bold; font-size: 1.1rem;'>{score}% - {status}</span>
                    </div>
                    <div style='display: flex; background: rgba(30, 41, 59, 0.5); border-radius: 8px; 
                                padding: 3px; height: 28px; overflow: hidden;'>
                        {segments}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<h3 style="color: #10b981; margin-bottom: 25px;">🎯 QUICK STATS</h3>', unsafe_allow_html=True)
            for factor in pred['factors'][:4]:
                score = factor['score']
                color = "#10b981" if score >= 80 else "#3b82f6" if score >= 65 else "#f59e0b" if score >= 50 else "#ef4444"
                st.markdown(f"""
                <div style='margin-bottom: 20px; display: flex; align-items: center; gap: 15px;'>
                    <svg width="60" height="60">
                        <circle cx="30" cy="30" r="25" fill="none" stroke="rgba(148, 163, 184, 0.2)" stroke-width="5"/>
                        <circle cx="30" cy="30" r="25" fill="none" stroke="{color}" stroke-width="5" 
                                stroke-dasharray="{score*1.57} 157" stroke-dashoffset="39.25"
                                transform="rotate(-90 30 30)"/>
                        <text x="30" y="35" text-anchor="middle" fill="{color}" font-size="14" font-weight="bold">{score}</text>
                    </svg>
                    <div>
                        <div style='color: white; font-weight: 600; font-size: 0.95rem;'>{factor['name']}</div>
                        <div style='color: #94a3b8; font-size: 0.8rem;'>{factor['current']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ENHANCED ACTIONABLE INSIGHTS SECTION
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; margin-bottom: 35px;'>
            <h2 style='color: #10b981; font-size: 2.2rem; font-weight: 800; 
                       text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;'>
                💡 ACTIONABLE INSIGHTS
            </h2>
            <p style='color: #94a3b8; font-size: 1rem; font-weight: 500;'>
                Expert recommendations tailored to optimize your crop performance
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced insight cards with icons and badges
        icons = ['🌱', '💧', '🌡️', '⚡', '🎯', '📊']
        priority_levels = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        
        st.markdown('<div class="insights-grid">', unsafe_allow_html=True)
        for idx, rec in enumerate(pred['recommendations']):
            icon = icons[idx % len(icons)]
            priority = priority_levels[min(idx, len(priority_levels)-1)]
            
            # Determine priority color
            if priority == 'CRITICAL': priority_color = '#ef4444'
            elif priority == 'HIGH': priority_color = '#f59e0b'
            elif priority == 'MEDIUM': priority_color = '#3b82f6'
            else: priority_color = '#10b981'
            
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-badge" style="background: {priority_color};">{priority}</div>
                <div class="insight-icon">{icon}</div>
                <div class="insight-title">Recommendation {idx + 1}</div>
                <div class="insight-text">{rec}</div>
                <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(16, 185, 129, 0.2);'>
                    <span style='color: #84cc16; font-size: 0.85rem; font-weight: 600;'>
                        ✓ ACTION REQUIRED
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👈 **Please go to Input Parameters and run analysis first**")
        if st.button("📝 Go to Input Parameters", type="primary"):
            navigate_to('input')

# ============= COMPARE PAGE =============
elif st.session_state['page'] == 'compare':
    st.markdown('<div class="section-header">⚖️ MULTI-CROP COMPARISON</div>', unsafe_allow_html=True)
    st.markdown("Compare quality predictions for different crops under the same conditions")
    st.markdown("<br>", unsafe_allow_html=True)
    
    params = st.session_state['input_params']
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">🌾 SELECT CROPS TO COMPARE</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    crops = ['wheat', 'rice', 'maize', 'cotton', 'sugarcane', 'potato', 'tomato', 'soybean']
    with col1: crop1 = st.selectbox("Select Crop 1", crops, key='crop1')
    with col2: crop2 = st.selectbox("Select Crop 2", crops, index=1, key='crop2')
    with col3: crop3 = st.selectbox("Select Crop 3", crops, index=2, key='crop3')
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 COMPARE CROPS", use_container_width=True, type="primary"):
        comparison_results = []
        for crop in [crop1, crop2, crop3]:
            input_data = {**{k: params[k] for k in ['nitrogen', 'phosphorus', 'potassium', 
                            'temperature', 'humidity', 'ph', 'rainfall']}, 'crop_type': crop}
            pred = predictor.predict(input_data)
            comparison_results.append({'crop': crop, 'score': pred['score'], 
                                       'quality': pred['quality'], 'yield': pred['estimated_yield']})
        st.session_state['comparison_results'] = comparison_results
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state['comparison_results']:
        results = st.session_state['comparison_results']
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📊 COMPARISON RESULTS</h3>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for idx, result in enumerate(results):
            with cols[idx]:
                color = QUALITY_COLORS.get(result['quality'], '#888888')
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                            padding: 25px; border-radius: 20px; text-align: center; color: white; 
                            height: 320px; border: 1px solid rgba(255,255,255,0.1);'>
                    <h2 style='margin: 0; color: white; text-transform: capitalize; font-size: 1.8rem;'>{result['crop']}</h2>
                    <hr style='border: 1px solid rgba(255,255,255,0.3); margin: 20px 0;'>
                    <div style='margin: 25px 0;'>
                        <p style='margin: 5px 0; font-size: 0.9rem; opacity: 0.9;'>Quality Score</p>
                        <h1 style='margin: 5px 0; font-size: 3.5rem;'>{result['score']}%</h1>
                    </div>
                    <div style='margin: 25px 0;'>
                        <p style='margin: 5px 0; font-size: 0.9rem; opacity: 0.9;'>Quality Grade</p>
                        <h3 style='margin: 5px 0; font-size: 1.5rem;'>{result['quality']}</h3>
                    </div>
                    <div style='margin: 25px 0;'>
                        <p style='margin: 5px 0; font-size: 0.9rem; opacity: 0.9;'>Expected Yield</p>
                        <h3 style='margin: 5px 0; font-size: 1.3rem;'>{result['yield']} t/ha</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📊 QUALITY SCORE COMPARISON</h3>', unsafe_allow_html=True)
            comparison_chart = create_comparison_chart(results)
            st.plotly_chart(comparison_chart, use_container_width=True)
        with col2:
            st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📈 YIELD COMPARISON</h3>', unsafe_allow_html=True)
            yield_chart = create_yield_comparison_chart(results)
            st.plotly_chart(yield_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">🏆 BEST CROP RECOMMENDATION</h3>', unsafe_allow_html=True)
        best_crop = max(results, key=lambda x: x['score'])
        st.success(f"""
            ### 🎯 Recommended: {best_crop['crop'].title()}
            
            Based on current conditions, **{best_crop['crop'].title()}** shows the best performance:
            - **Quality Score:** {best_crop['score']}%
            - **Quality Grade:** {best_crop['quality']}
            - **Expected Yield:** {best_crop['yield']} tonnes/hectare
        """)
        st.markdown('</div>', unsafe_allow_html=True)

# ============= FERTILIZER PAGE WITH ENHANCED TIMELINE =============
elif st.session_state['page'] == 'fertilizer':
    st.markdown('<div class="section-header">🌱 FERTILIZER CALCULATOR</div>', unsafe_allow_html=True)
    st.markdown("Calculate NPK requirements and costs")
    st.markdown("<br>", unsafe_allow_html=True)
    
    params = st.session_state['input_params']
    fert_needs = fert_calculator.calculate(params['crop_type'], params['nitrogen'],
                                           params['phosphorus'], params['potassium'])
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 25px;">📊 NPK STATUS OVERVIEW</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    npk_data = [
        ('Nitrogen (N)', '#10b981', 'N'),
        ('Phosphorus (P)', '#3b82f6', 'P'),
        ('Potassium (K)', '#8b5cf6', 'K')
    ]
    for col, (name, color, key) in zip([col1, col2, col3], npk_data):
        with col:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                        padding: 25px; border-radius: 15px; color: white; 
                        border: 1px solid rgba(255,255,255,0.1);'>
                <h3 style='margin: 0; color: white;'>{name}</h3>
                <hr style='border: 1px solid rgba(255,255,255,0.3); margin: 15px 0;'>
                <p style='margin: 8px 0;'><strong>Required:</strong> {fert_needs['required'][key]} kg/ha</p>
                <p style='margin: 8px 0;'><strong>Current:</strong> {fert_needs['current'][key]} kg/ha</p>
                <p style='margin: 8px 0;'><strong>Deficit:</strong> 
                   <span style='font-size: 1.8rem; font-weight: bold;'>{fert_needs['deficit'][key]} kg/ha</span></p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">💰 COST ANALYSIS</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                    padding: 35px; border-radius: 15px; color: white; text-align: center;
                    border: 1px solid rgba(255,255,255,0.1);'>
            <h3 style='margin: 0; color: white;'>Total Fertilizer Cost</h3>
            <h1 style='margin: 20px 0; font-size: 4rem; color: white;'>₹{fert_needs['total_cost']:,.2f}</h1>
            <p style='margin: 0; font-size: 1.2rem;'>per hectare</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("#### Cost Breakdown")
        for nutrient, cost in fert_needs['cost_breakdown'].items():
            st.info(f"**{nutrient.title()}:** ₹{cost:,.2f}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📊 NPK COMPARISON CHART</h3>', unsafe_allow_html=True)
        npk_chart = create_npk_comparison_chart(fert_needs)
        st.plotly_chart(npk_chart, use_container_width=True)
    with col2:
        st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📋 QUICK SUMMARY</h3>', unsafe_allow_html=True)
        total_deficit = sum(fert_needs['deficit'][k] for k in ['N', 'P', 'K'])
        if total_deficit == 0: st.success("✅ All nutrients are at optimal levels!")
        else: st.warning(f"⚠️ Total nutrient deficit: {total_deficit} kg/ha")
        st.metric("Total NPK Required", f"{sum(fert_needs['required'][k] for k in ['N', 'P', 'K'])} kg/ha")
        st.metric("Current NPK Level", f"{sum(fert_needs['current'][k] for k in ['N', 'P', 'K'])} kg/ha")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ENHANCED FERTILIZER APPLICATION TIMELINE
    schedule = fert_calculator.get_application_schedule()

    css = """
    <style>
      html, body { margin: 0; padding: 0; background: transparent; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; color: #e2e8f0; }
      .custom-card { background: linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius: 20px; padding: 30px; border: 1px solid rgba(16,185,129,0.2); box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
      .timeline-container { position: relative; padding: 40px 20px; }
      .timeline-line { position: absolute; left: 50%; top: 0; bottom: 0; width: 4px; background: linear-gradient(180deg, #10b981 0%, #3b82f6 50%, #f59e0b 100%); transform: translateX(-50%); border-radius: 10px; }
      .timeline-item { position: relative; margin-bottom: 80px; }
      .timeline-dot { position: absolute; left: 50%; top: 30px; transform: translateX(-50%); width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; box-shadow: 0 0 0 8px rgba(0, 0, 0, 0.3); }
      .timeline-content-left { width: 45%; margin-right: auto; padding-right: 60px; }
      .timeline-content-right { width: 45%; margin-left: auto; padding-left: 60px; }
      .stage-card { background: linear-gradient(135deg, rgba(30,41,59,0.95) 0%, rgba(51,65,85,0.95) 100%); border-radius: 20px; padding: 30px; border: 2px solid rgba(16,185,129,0.3); }
      .stage-badge { display: inline-block; padding: 8px 16px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; color: black; }
      .tip-item { padding: 12px 15px; margin: 8px 0; background: rgba(16,185,129,0.1); border-left: 3px solid #10b981; border-radius: 8px; font-size: 0.9rem; }
    </style>
    """

    timeline_items = []
    for idx, stage in enumerate(schedule):
        position_class = 'timeline-content-left' if idx % 2 == 0 else 'timeline-content-right'
        tips_html = ''.join([
            f'<div class="tip-item">\n'
            f'    <span style="color: #84cc16; margin-right: 8px;">✓</span>\n'
            f'    <span style="color: #e2e8f0;">{tip}</span>\n'
            f'</div>' for tip in stage['tips']
        ])
        item_html = f"""
        <div class=\"timeline-item\">
            <div class=\"timeline-dot\" style=\"background: {stage['color']};\">{stage['icon']}</div>
            <div class=\"{position_class}\">
                <div class=\"stage-card\">
                    <div style=\"display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;\">
                        <div>
                            <span class=\"stage-badge\" style=\"background: {stage['color']};\">Stage {idx + 1}</span>
                            <h3 style=\"color: white; font-size: 1.5rem; font-weight: 700; margin: 10px 0 5px 0;\">{stage['stage']}</h3>
                            <p style=\"color: #94a3b8; font-size: 0.9rem; margin: 0;\">{stage['subtitle']}</p>
                        </div>
                        <div style=\"text-align: right;\">
                            <svg width=\"80\" height=\"80\" viewBox=\"0 0 100 100\">
                                <circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"none\" stroke=\"rgba(148, 163, 184, 0.2)\" stroke-width=\"8\"/>
                                <circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"none\" stroke=\"{stage['color']}\" stroke-width=\"8\" stroke-dasharray=\"{stage['percentage'] * 2.51} 251\" stroke-dashoffset=\"62.75\" transform=\"rotate(-90 50 50)\" stroke-linecap=\"round\"/>
                                <text x=\"50\" y=\"55\" text-anchor=\"middle\" fill=\"{stage['color']}\" font-size=\"20\" font-weight=\"bold\">{stage['percentage']}%</text>
                            </svg>
                        </div>
                    </div>
                    <div style=\"background: rgba(0, 0, 0, 0.3); padding: 20px; border-radius: 12px; margin: 15px 0;\">
                        <div style=\"display: grid; grid-template-columns: 1fr 1fr; gap: 15px;\">
                            <div>
                                <p style=\"color: #94a3b8; font-size: 0.8rem; margin: 0;\">⏰ TIMING</p>
                                <p style=\"color: white; font-size: 1.1rem; font-weight: 600; margin: 5px 0;\">{stage['timing']}</p>
                                <p style=\"color: #84cc16; font-size: 0.85rem; margin: 0;\">{stage['timing_detail']}</p>
                            </div>
                            <div>
                                <p style=\"color: #94a3b8; font-size: 0.8rem; margin: 0;\">🌱 APPLICATION</p>
                                <p style=\"color: white; font-size: 1.1rem; font-weight: 600; margin: 5px 0;\">{stage['fertilizer']}</p>
                                <p style=\"color: #84cc16; font-size: 0.85rem; margin: 0;\">{stage['npk_ratio']}</p>
                            </div>
                        </div>
                    </div>
                    <div style=\"margin: 20px 0;\">
                        <p style=\"color: #e2e8f0; font-size: 1rem; line-height: 1.6; margin: 0;\">{stage['description']}</p>
                    </div>
                    <div style=\"margin-top: 20px; padding-top: 20px; border-top: 2px solid rgba(16, 185, 129, 0.2);\">
                        <p style=\"color: #10b981; font-size: 0.9rem; font-weight: 700; text-transform: uppercase; margin-bottom: 10px;\">💡 Application Tips</p>
                        {tips_html}
                    </div>
                </div>
            </div>
        </div>
        """
        timeline_items.append(item_html)

    timeline_html = f"""
    <html>
    <head>{css}</head>
    <body>
      <div class=\"custom-card\">
        <div style='text-align: center; margin-bottom: 40px;'>
          <h2 style='color: #10b981; font-size: 2.2rem; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;'>📅 FERTILIZER APPLICATION TIMELINE</h2>
          <p style='color: #94a3b8; font-size: 1rem; font-weight: 500;'>Strategic fertilizer application schedule for optimal crop growth</p>
        </div>
        <div class=\"timeline-container\">
          <div class=\"timeline-line\"></div>
          {''.join(timeline_items)}
        </div>
      </div>
    </body>
    </html>
    """

    st.components.v1.html(timeline_html, height=max(800, 280 + 320 * len(schedule)), scrolling=True)

# ============= IRRIGATION PAGE =============
elif st.session_state['page'] == 'irrigation':
    st.markdown('<div class="section-header">💧 IRRIGATION MANAGEMENT PLANNER</div>', unsafe_allow_html=True)
    st.markdown("Plan optimal irrigation schedule")
    st.markdown("<br>", unsafe_allow_html=True)
    
    params = st.session_state['input_params']
    irrig_needs = irrig_calculator.calculate(params['crop_type'], params['rainfall'])
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 25px;">💦 WATER REQUIREMENT OVERVIEW</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    water_data = [
        ('Total Water Need', '#3b82f6', irrig_needs['total_needed'], 'mm per season'),
        ('Rainfall', '#10b981', irrig_needs['rain_contribution'], f"mm ({irrig_needs['efficiency_percentage']}%)"),
        ('Irrigation Needed', '#f59e0b', irrig_needs['irrigation_needed'], 'mm additional')
    ]
    for col, (title, color, value, subtitle) in zip([col1, col2, col3], water_data):
        with col:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                        padding: 30px; border-radius: 15px; color: white; text-align: center;
                        border: 1px solid rgba(255,255,255,0.1);'>
                <h3 style='margin: 0; color: white;'>{title}</h3>
                <h1 style='margin: 20px 0; font-size: 3.5rem; color: white;'>{value}</h1>
                <p style='margin: 0; font-size: 1.1rem;'>{subtitle}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📅 WEEKLY IRRIGATION SCHEDULE</h3>', unsafe_allow_html=True)
    st.info(f"**Recommended Frequency:** {irrig_needs['frequency']} times per week")
    st.markdown("<br>", unsafe_allow_html=True)
    
    schedule_cols = st.columns(len(irrig_needs['schedule']))
    for idx, day in enumerate(irrig_needs['schedule']):
        with schedule_cols[idx]:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); 
                        padding: 25px; border-radius: 15px; color: white; text-align: center;
                        border: 1px solid rgba(255,255,255,0.1);'>
                <h2 style='margin: 0; color: white; font-size: 1.5rem;'>{day}</h2>
                <hr style='border: 1px solid rgba(255,255,255,0.3); margin: 15px 0;'>
                <p style='margin: 5px 0; font-size: 0.9rem;'>💧 Irrigation Day</p>
                <h3 style='margin: 10px 0; color: white; font-size: 1.5rem;'>{irrig_needs['water_per_session']} mm</h3>
                <p style='margin: 0; font-size: 0.85rem;'>per session</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">💡 IRRIGATION BEST PRACTICES</h3>', unsafe_allow_html=True)
    tips = irrig_calculator.get_irrigation_tips()
    tip_cols = st.columns(2)
    for idx, tip in enumerate(tips):
        with tip_cols[idx % 2]: st.success(tip)
    st.markdown('</div>', unsafe_allow_html=True)

# ============= PROFIT PAGE =============
elif st.session_state['page'] == 'profit':
    st.markdown('<div class="section-header">💰 PROFIT & COST ANALYSIS</div>', unsafe_allow_html=True)
    st.markdown("Calculate profitability and ROI")
    st.markdown("<br>", unsafe_allow_html=True)
    
    params = st.session_state['input_params']
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📝 ENTER COST DETAILS</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        seed_cost = st.number_input("💵 Seed Cost (₹/ha)", 0, value=st.session_state['cost_data']['seed_cost'], step=500)
        fertilizer_cost = st.number_input("🌱 Fertilizer Cost (₹/ha)", 0, value=st.session_state['cost_data']['fertilizer_cost'], step=500)
    with col2:
        labor_cost = st.number_input("👷 Labor Cost (₹/ha)", 0, value=st.session_state['cost_data']['labor_cost'], step=1000)
        irrigation_cost = st.number_input("💧 Irrigation Cost (₹/ha)", 0, value=st.session_state['cost_data']['irrigation_cost'], step=500)
    
    expected_price = st.number_input("💲 Expected Price (₹/quintal)", 0, value=st.session_state['cost_data']['expected_price'], step=5)
    st.session_state['cost_data'] = {'seed_cost': seed_cost, 'fertilizer_cost': fertilizer_cost,
                                      'labor_cost': labor_cost, 'irrigation_cost': irrigation_cost,
                                      'expected_price': expected_price}
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state['prediction']:
        pred = st.session_state['prediction']
        costs = {'seed_cost': seed_cost, 'fertilizer_cost': fertilizer_cost,
                 'labor_cost': labor_cost, 'irrigation_cost': irrigation_cost}
        profit_analysis = profit_calculator.calculate(costs, expected_price, pred['estimated_yield'])
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; margin-bottom: 25px;">📊 FINANCIAL SUMMARY</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        financial_data = [
            ('Total Cost', '#ef4444', profit_analysis['total_cost']),
            ('Expected Revenue', '#3b82f6', profit_analysis['revenue']),
            ('Net Profit', '#10b981' if profit_analysis['profit'] >= 0 else '#ef4444', profit_analysis['profit']),
            ('ROI', '#8b5cf6' if profit_analysis['roi'] >= 0 else '#f59e0b', f"{profit_analysis['roi']:.1f}%")
        ]
        for col, (title, color, value) in zip([col1, col2, col3, col4], financial_data):
            with col:
                display_value = f"₹{value:,.0f}" if isinstance(value, (int, float)) else value
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                            padding: 30px; border-radius: 15px; color: white; text-align: center;
                            border: 1px solid rgba(255,255,255,0.1);'>
                    <h4 style='margin: 0; color: white; font-size: 1.1rem;'>{title}</h4>
                    <h2 style='margin: 20px 0; font-size: 2.5rem; color: white;'>{display_value}</h2>
                    <p style='margin: 0; font-size: 1rem;'>per hectare</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📈 COST BREAKDOWN</h3>', unsafe_allow_html=True)
            cost_pie = create_cost_breakdown_pie(profit_analysis['cost_breakdown'])
            st.plotly_chart(cost_pie, use_container_width=True)
        with col2:
            st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">📊 KEY METRICS</h3>', unsafe_allow_html=True)
            st.metric("Expected Yield", f"{profit_analysis['yield_tonnes']} tonnes",
                     f"{profit_analysis['yield_quintals']} quintals")
            st.metric("Break-even Yield", f"{profit_analysis['break_even_yield']:.2f} tonnes")
            profit_margin = (profit_analysis['profit'] / profit_analysis['revenue'] * 100) if profit_analysis['revenue'] > 0 else 0
            st.metric("Profit Margin", f"{profit_margin:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #10b981; margin-bottom: 20px;">🎯 PROFITABILITY ASSESSMENT</h3>', unsafe_allow_html=True)
        if profit_analysis['roi'] >= 50:
            st.success(f"### ✅ Highly Profitable\nROI: **{profit_analysis['roi']:.1f}%** - Excellent profitability!\nNet Profit: ₹{profit_analysis['profit']:,.0f}/ha")
        elif profit_analysis['roi'] >= 20:
            st.info(f"### ℹ️ Moderately Profitable\nROI: **{profit_analysis['roi']:.1f}%** - Reasonable profitability\nNet Profit: ₹{profit_analysis['profit']:,.0f}/ha")
        elif profit_analysis['roi'] >= 0:
            st.warning(f"### ⚠️ Low Profitability\nROI: **{profit_analysis['roi']:.1f}%** - Tight margins\nNet Profit: ₹{profit_analysis['profit']:,.0f}/ha")
        else:
            st.error(f"### ❌ Not Profitable\nROI: **{profit_analysis['roi']:.1f}%** - Potential loss\nNet Loss: ₹{abs(profit_analysis['profit']):,.0f}/ha")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👈 **Please run a prediction first**")
        if st.button("📝 Go to Input Parameters", type="primary"):
            navigate_to('input')

