"""
AgriSmart Pro - Main Landing Page
"""
import streamlit as st
import os

# Page Configuration
st.set_page_config(
    page_title="AgriSmart Pro - Home",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #10b981, #84cc16, #22c55e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        color: #10b981;
        font-size: 1.2rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 3rem;
    }
    .module-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 25px;
        padding: 40px 25px;
        margin: 20px 0;
        border: 3px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center;
        height: 320px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .module-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: rgba(132, 204, 22, 0.6);
        box-shadow: 0 20px 50px rgba(16, 185, 129, 0.4);
    }
    .module-icon {
        font-size: 3.5rem;
        margin-bottom: 15px;
    }
    .module-title {
        color: #10b981;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .module-description {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.5;
        margin-bottom: 15px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #10b981, #84cc16) !important;
        color: black !important;
        font-weight: 700;
        font-size: 1rem;
        padding: 10px 25px;
        border-radius: 15px;
        border: none;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.5);
    }
    
    /* Feature badges */
    .feature-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 6px 12px;
        margin: 3px;
        display: inline-block;
        color: #10b981;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    /* New module specific colors */
    .pest-alert { border-color: rgba(239, 68, 68, 0.4); }
    .soil-analyzer { border-color: rgba(120, 113, 108, 0.4); }
    .quality-grading { border-color: rgba(34, 197, 94, 0.4); }
</style>
""", unsafe_allow_html=True)

def navigate_to_page(page_name):
    """Navigate to different pages with error handling"""
    try:
        page_path = f"pages/{page_name}.py"
        if os.path.exists(page_path):
            st.switch_page(page_path)
        else:
            st.error(f"⚠️ **{page_name.replace('_', ' ').title()} Module Not Found**\n\nPlease ensure `{page_name}.py` is in the `pages/` directory.")
    except Exception as e:
        st.error(f"Navigation error: {str(e)}")

def main():
    """Main landing page"""
    
    # Header
    st.markdown('<div class="main-header">🌾 AgriSmart Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">⚡ Complete Agricultural Intelligence Platform</div>', unsafe_allow_html=True)

    st.markdown("---")

    # First Row of Modules
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="module-card">
            <div class="module-icon">🔮</div>
            <div class="module-title">Crop Prediction</div>
            <div class="module-description">
                Advanced AI-powered crop quality prediction, 
                fertilizer recommendations, irrigation planning, 
                and profitability analysis.
            </div>
            <div>
                <span class="feature-badge">📊 Quality Analysis</span>
                <span class="feature-badge">🌱 NPK Calculator</span>
                <span class="feature-badge">💰 ROI Predictor</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Prediction", key="prediction_btn", use_container_width=True):
            navigate_to_page("app")

    with col2:
        st.markdown("""
        <div class="module-card">
            <div class="module-icon">🌱</div>
            <div class="module-title">Seed Bank</div>
            <div class="module-description">
                Browse certified seed varieties with advanced 
                filtering. Compare varieties and find disease-resistant 
                seeds perfect for your region.
            </div>
            <div>
                <span class="feature-badge">🔍 Smart Search</span>
                <span class="feature-badge">⭐ Compare Seeds</span>
                <span class="feature-badge">🛡️ Disease Resistant</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌱 Open Seed Bank", key="seed_btn", use_container_width=True):
            navigate_to_page("seed_bank")

    with col3:
        st.markdown("""
        <div class="module-card">
            <div class="module-icon">📸</div>
            <div class="module-title">Disease Detection</div>
            <div class="module-description">
                AI-powered plant disease detection using image 
                analysis. Get instant treatment recommendations 
                and prevention strategies.
            </div>
            <div>
                <span class="feature-badge">📸 Image AI</span>
                <span class="feature-badge">🔬 50+ Diseases</span>
                <span class="feature-badge">💊 Treatment Plan</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔬 Detect Diseases", key="disease_btn", use_container_width=True):
            navigate_to_page("disease_detection")

    # Second Row - New DL Features
    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class="module-card pest-alert">
            <div class="module-icon">🚨</div>
            <div class="module-title">Early Pest Alert</div>
            <div class="module-description">
                AI-powered pest risk prediction using weather patterns 
                and field images. Get early warnings and preventive 
                measures before infestation.
            </div>
            <div>
                <span class="feature-badge">🌤️ Weather Analysis</span>
                <span class="feature-badge">📈 Risk Prediction</span>
                <span class="feature-badge">🛡️ Prevention</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚨 Check Pest Risk", key="pest_btn", use_container_width=True):
            navigate_to_page("pest_alert")

    with col5:
        st.markdown("""
        <div class="module-card soil-analyzer">
            <div class="module-icon">📊</div>
            <div class="module-title">Soil Health Analyzer</div>
            <div class="module-description">
                Deep learning analysis of soil images to determine 
                texture, health score, and improvement recommendations. 
                No IoT required.
            </div>
            <div>
                <span class="feature-badge">🌱 Texture Analysis</span>
                <span class="feature-badge">📸 Image-Based</span>
                <span class="feature-badge">💡 Recommendations</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Analyze Soil", key="soil_btn", use_container_width=True):
            navigate_to_page("soil_analyzer")

    with col6:
        st.markdown("""
        <div class="module-card quality-grading">
            <div class="module-icon">🌾</div>
            <div class="module-title">Crop Quality Grading</div>
            <div class="module-description">
                Automatic quality grading of harvested crops using 
                computer vision. Get market-ready quality scores 
                and price estimations.
            </div>
            <div>
                <span class="feature-badge">⭐ A/B/C Grading</span>
                <span class="feature-badge">💰 Price Estimation</span>
                <span class="feature-badge">📈 Market Ready</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌾 Grade Quality", key="quality_btn", use_container_width=True):
            navigate_to_page("quality_grading")

    st.markdown("---")

    # Features Overview Section
    st.markdown("""
    <div style='text-align: center; margin: 50px 0;'>
        <h2 style='color: #10b981; font-size: 2rem; font-weight: 800; margin-bottom: 30px;'>
            🌟 PLATFORM FEATURES
        </h2>
    </div>
    """, unsafe_allow_html=True)

    feature_col1, feature_col2, feature_col3, feature_col4 = st.columns(4)

    with feature_col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(132, 204, 22, 0.15));
                    border: 2px solid rgba(16, 185, 129, 0.3); border-radius: 15px; padding: 25px; text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>🤖</div>
            <h3 style='color: #10b981; font-size: 1.2rem; margin-bottom: 10px;'>AI-Powered</h3>
            <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>
                Advanced deep learning algorithms for accurate predictions
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feature_col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.15));
                    border: 2px solid rgba(59, 130, 246, 0.3); border-radius: 15px; padding: 25px; text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>🌍</div>
            <h3 style='color: #3b82f6; font-size: 1.2rem; margin-bottom: 10px;'>Region-Specific</h3>
            <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>
                Tailored recommendations based on your location and climate
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feature_col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(124, 58, 237, 0.15));
                    border: 2px solid rgba(139, 92, 246, 0.3); border-radius: 15px; padding: 25px; text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>📊</div>
            <h3 style='color: #8b5cf6; font-size: 1.2rem; margin-bottom: 10px;'>Data-Driven</h3>
            <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>
                Real-time weather integration and comprehensive analytics
            </p>
        </div>
        """, unsafe_allow_html=True)

    with feature_col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.15));
                    border: 2px solid rgba(245, 158, 11, 0.3); border-radius: 15px; padding: 25px; text-align: center;'>
            <div style='font-size: 3rem; margin-bottom: 15px;'>💡</div>
            <h3 style='color: #f59e0b; font-size: 1.2rem; margin-bottom: 10px;'>Easy to Use</h3>
            <p style='color: #94a3b8; font-size: 0.95rem; margin: 0;'>
                Intuitive interface designed for farmers of all backgrounds
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # About Section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 20px; padding: 40px; margin: 30px 0;
                border: 2px solid rgba(16, 185, 129, 0.3);'>
        <h3 style='color: #10b981; text-align: center; font-size: 2rem; margin-bottom: 20px;'>
            About AgriSmart Pro
        </h3>
        <p style='color: #94a3b8; text-align: center; font-size: 1.1rem; line-height: 1.8; max-width: 900px; margin: 0 auto;'>
            A comprehensive agricultural intelligence platform combining <strong style='color: #10b981;'>AI</strong>, 
            <strong style='color: #10b981;'>machine learning</strong>, and 
            <strong style='color: #10b981;'>data analytics</strong> to help farmers make informed decisions 
            and maximize productivity. From crop quality prediction to disease detection, we provide 
            end-to-end solutions for modern agriculture.
        </p>
        <div style='text-align: center; margin-top: 30px;'>
            <span style='background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 10px 20px; 
                         border-radius: 20px; margin: 5px; display: inline-block; font-weight: 600;'>
                🌾 8+ Crop Types
            </span>
            <span style='background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 10px 20px; 
                         border-radius: 20px; margin: 5px; display: inline-block; font-weight: 600;'>
                🚨 Pest Alerts
            </span>
            <span style='background: rgba(120, 113, 108, 0.2); color: #78716c; padding: 10px 20px; 
                         border-radius: 20px; margin: 5px; display: inline-block; font-weight: 600;'>
                📊 Soil Analysis
            </span>
            <span style='background: rgba(34, 197, 94, 0.2); color: #22c55e; padding: 10px 20px; 
                         border-radius: 20px; margin: 5px; display: inline-block; font-weight: 600;'>
                🌾 Quality Grading
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()