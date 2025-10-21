import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
from scipy import ndimage
import re
import streamlit.components.v1 as components

# Enhanced CSS for Pest Alert Module with orange/red theme
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Keep sidebar visible */
    [data-testid="stSidebar"] {
        /* sidebar visible */
    }
    
    /* Custom card styles */
    .pest-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(245, 158, 11, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .pest-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(245, 158, 11, 0.5);
        border-color: rgba(251, 191, 36, 0.6);
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(217, 119, 6, 0.15) 100%);
        border: 2px solid rgba(245, 158, 11, 0.4);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2);
    }
    
    /* Tips card */
    .tips-card {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Pest library card */
    .library-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #f59e0b;
        transition: all 0.3s ease;
    }
    
    .library-card:hover {
        transform: translateX(10px);
        border-left-color: #fbbf24;
    }
    
    /* Risk badges */
    .risk-high {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #84cc16, #65a30d);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    /* Confidence meter */
    .confidence-meter {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        height: 30px;
        overflow: hidden;
        position: relative;
    }
    
    .confidence-fill {
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    /* Prevention steps */
    .prevention-step {
        background: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .prevention-step:hover {
        background: rgba(245, 158, 11, 0.2);
        transform: translateX(10px);
    }
    
    /* Emergency steps */
    .emergency-step {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .emergency-step:hover {
        background: rgba(239, 68, 68, 0.2);
        transform: translateX(10px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 15px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        color: #94a3b8;
        font-weight: 600;
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f59e0b, #fbbf24);
        color: black;
    }
    
    /* Upload guidelines */
    .guidelines-box {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.15));
        border: 2px solid rgba(245, 158, 11, 0.3);
        border-radius: 20px;
        padding: 25px;
    }
</style>
""", unsafe_allow_html=True)

def pest_alert_page():
    # Beautiful header
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px 20px 20px;'>
        <div style='font-size: 3.5rem; font-weight: 900; 
                    background: linear-gradient(90deg, #f59e0b, #fbbf24, #f97316);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🚨 AI PEST ALERT SYSTEM
        </div>
        <div style='color: #f59e0b; font-size: 1rem; font-weight: 600; 
                    letter-spacing: 2px; text-transform: uppercase; margin-top: 10px;'>
            ⚡ Early Pest Detection & Prevention
        </div>
        <p style='color: #94a3b8; font-size: 1.1rem; max-width: 800px; 
                  margin: 20px auto 0 auto; line-height: 1.6;'>
            Upload field images for AI-powered pest risk analysis and get immediate prevention strategies
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Detect Pest Risk", "📝 Manual Entry", "🐛 Pest Library", "🛡️ Prevention Guide"])
    
    with tab1:
        detect_pest_tab()
    
    with tab2:
        manual_entry_tab()
    
    with tab3:
        pest_library_tab()
    
    with tab4:
        prevention_guide_tab()

def is_field_image(image):
    """Basic check if uploaded image contains field/plant content"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) != 3:
            return False
        # Check for green content (plants) or brown content (soil)
        green_pixels = np.sum((img_array[:, :, 1] > img_array[:, :, 0]) & 
                             (img_array[:, :, 1] > img_array[:, :, 2]))
        brown_pixels = np.sum((img_array[:, :, 0] > 100) & (img_array[:, :, 1] > 80) & 
                             (img_array[:, :, 2] < 100))
        total_pixels = img_array.shape[0] * img_array.shape[1]
        field_ratio = (green_pixels + brown_pixels) / total_pixels
        return field_ratio > 0.1
    except:
        return False

def check_image_quality(image):
    """Basic image quality checks"""
    try:
        width, height = image.size
        if width < 200 or height < 200:
            return "Image too small. Please upload a higher resolution image."
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            brightness = np.mean(img_array)
            if brightness < 50:
                return "Image too dark. Please upload a well-lit image."
        return None
    except:
        return "Unable to process image quality."
    
def is_field_image(image):
    """Enhanced check if uploaded image contains agricultural field/plants"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) != 3:
            return False
        
        height, width = img_array.shape[:2]
        
        # Enhanced plant/field detection with better color analysis
        # Look for green vegetation with proper thresholds
        green_mask = (img_array[:, :, 1] > img_array[:, :, 0] + 15) & \
                    (img_array[:, :, 1] > img_array[:, :, 2] + 15) & \
                    (img_array[:, :, 1] > 60)  # Minimum green intensity
        
        # Look for soil/brown areas but exclude skin tones
        brown_mask = (img_array[:, :, 0] > 80) & \
                    (img_array[:, :, 1] > 60) & \
                    (img_array[:, :, 2] < 120) & \
                    (np.abs(img_array[:, :, 0] - img_array[:, :, 1]) > 10)  # Exclude uniform colors (like skin)
        
        # Exclude skin tones specifically (human faces)
        skin_mask = (img_array[:, :, 0] > 150) & \
                   (img_array[:, :, 1] > 100) & \
                   (img_array[:, :, 1] < 200) & \
                   (img_array[:, :, 2] < 150) & \
                   (np.abs(img_array[:, :, 0] - img_array[:, :, 1]) < 50)  # Skin has close R-G values
        
        total_pixels = height * width
        green_ratio = np.sum(green_mask) / total_pixels
        brown_ratio = np.sum(brown_mask) / total_pixels
        skin_ratio = np.sum(skin_mask) / total_pixels
        
        # Field typically has significant green vegetation
        has_vegetation = green_ratio > 0.2
        
        # Or mixed field with soil but NOT skin-like
        is_mixed_field = (green_ratio + brown_ratio) > 0.3 and skin_ratio < 0.1
        
        # Texture analysis - fields have natural texture patterns
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
            
        # Calculate texture variance
        texture_variance = np.var(gray)
        
        # Natural scenes have moderate to high texture variance
        # Faces have more uniform texture
        has_natural_texture = texture_variance > 500  # Higher threshold to exclude faces
        
        # Color diversity check - fields have diverse colors, faces are more uniform
        color_diversity = np.std(img_array, axis=(0, 1))
        has_color_diversity = np.mean(color_diversity) > 25
        
        # Combined criteria: looks like vegetation/field AND has natural texture AND diverse colors
        # AND specifically excludes skin-toned images
        return (has_vegetation or is_mixed_field) and has_natural_texture and has_color_diversity and (skin_ratio < 0.15)
        
    except Exception as e:
        print(f"Field detection error: {e}")
        return False

def detect_pest_tab():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 20px; padding: 30px; margin: 20px 0;
                border: 2px solid rgba(245, 158, 11, 0.3);'>
        <h2 style='color: #f59e0b; margin: 0; font-size: 1.8rem;'>
            📤 UPLOAD FIELD IMAGES
        </h2>
        <p style='color: #94a3b8; margin: 10px 0 0 0;'>
            Upload multiple photos from different field areas for comprehensive pest risk analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_images = st.file_uploader("", 
                                       type=['jpg', 'jpeg', 'png'],
                                       accept_multiple_files=True,
                                       help="Upload 3-8 images from different parts of your field",
                                       label_visibility="collapsed")
        
        if uploaded_images:
            # Display first image in a styled container
            image = Image.open(uploaded_images[0])
            st.markdown("""
            <div style='background: rgba(0, 0, 0, 0.3); border-radius: 15px; 
                        padding: 15px; border: 2px solid rgba(245, 158, 11, 0.2);'>
            """, unsafe_allow_html=True)
            st.image(image, caption="📷 Sample Uploaded Image", use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Quality check
            quality_issue = check_image_quality(image)
            if quality_issue:
                st.markdown(f"""
                <div style='background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444;
                            border-radius: 15px; padding: 20px; margin: 20px 0;'>
                    <h3 style='color: #ef4444; margin: 0;'>❌ Image Quality Issue</h3>
                    <p style='color: #fca5a5; margin: 10px 0 0 0;'>{quality_issue}</p>
                </div>
                """, unsafe_allow_html=True)
                return
            
            # Field detection check
            if not is_field_image(image):
                st.markdown("""
                <div style='background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444;
                            border-radius: 15px; padding: 25px; margin: 20px 0;'>
                    <h3 style='color: #ef4444; margin: 0 0 15px 0;'>
                        ❌ This doesn't appear to be a field image
                    </h3>
                    <p style='color: #fca5a5; margin: 10px 0;'>
                        <strong>Please upload clear photos of:</strong>
                    </p>
                    <ul style='color: #fca5a5; margin: 10px 0; padding-left: 20px;'>
                        <li>🌿 Plant leaves and stems</li>
                        <li>🐛 Close-ups of suspicious areas</li>
                        <li>📏 Different field sections</li>
                        <li>💡 Well-lit agricultural scenes</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                return
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Crop selection with styled container
            st.markdown("""
            <div style='background: rgba(245, 158, 11, 0.1); border-radius: 12px; 
                        padding: 15px; border: 1px solid rgba(245, 158, 11, 0.3); margin-bottom: 20px;'>
                <p style='color: #f59e0b; margin: 0; font-weight: 600;'>
                    🌾 Select Your Crop Type
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            crop_type = st.selectbox("", 
                                   ["Rice", "Wheat", "Maize", "Cotton", "Tomato", "Potato", "Vegetables", "Fruits", "Other"],
                                   label_visibility="collapsed")
            
            if st.button("🔍 ANALYZE PEST RISK", type="primary", use_container_width=True):
                with st.spinner("🔄 Scanning images for pest indicators..."):
                    result = analyze_pest_risk(uploaded_images, crop_type)
                    display_pest_results(result, uploaded_images)
    
    with col2:
        guidelines_html = """
        <div class='guidelines-box'>
            <h3 style='color: #f59e0b; margin: 0 0 20px 0; font-size: 1.3rem;'>
                📸 UPLOAD GUIDELINES
            </h3>
            
            <div style='margin: 20px 0;'>
                <p style='color: #f59e0b; font-weight: 700; margin-bottom: 10px;'>
                    ✅ DO UPLOAD:
                </p>
                <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li>3-8 images from different areas</li>
                    <li>Close-ups of leaf damage</li>
                    <li>Visible insects or eggs</li>
                    <li>Chewing/biting patterns</li>
                    <li>Different field sections</li>
                </ul>
            </div>
            
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #ef4444; font-weight: 700; margin-bottom: 10px;'>
                    ❌ DON'T UPLOAD:
                </p>
                <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li>Single image only</li>
                    <li>Blurry/dark photos</li>
                    <li>Non-agricultural images</li>
                    <li>Only soil without plants</li>
                </ul>
            </div>
            
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #fbbf24; font-weight: 700; margin-bottom: 10px;'>
                    🎯 QUICK TIPS:
                </p>
                <div style='color: #94a3b8; font-size: 0.9rem; line-height: 1.6;'>
                    • Morning light works best<br>
                    • Capture both sides of leaves<br>
                    • Include scale reference<br>
                    • Show healthy areas too
                </div>
            </div>
        </div>
        """
        components.html(guidelines_html, height=520, scrolling=True)

def analyze_pest_risk(images, crop_type):
    """Analyze images for pest risk"""
    # Mock analysis - replace with actual model
    pests = ["Aphids", "Whiteflies", "Caterpillars", "Spider Mites", "Leaf Miners", 
             "Bollworms", "Stem Borers", "Thrips", "Mealybugs"]
    
    # Simulate risk analysis based on number of images
    risk_score = min(0.1 + len(images) * 0.1, 0.95)
    risk_level = "High" if risk_score > 0.7 else "Medium" if risk_score > 0.4 else "Low"
    
    detected_pests = np.random.choice(pests, size=min(3, len(images)), replace=False).tolist()
    
    return {
        'risk_level': risk_level,
        'risk_score': risk_score,
        'confidence': np.random.uniform(0.75, 0.95),
        'detected_pests': detected_pests,
        'affected_areas': len(images),
        'immediate_actions': [
            "Isolate heavily infected plants immediately",
            "Apply neem oil spray to affected areas",
            "Remove and destroy severely damaged leaves",
            "Increase field monitoring frequency"
        ],
        'preventive_measures': [
            "Introduce beneficial insects like ladybugs and lacewings",
            "Use yellow sticky traps for flying pests",
            "Apply organic pesticides weekly",
            "Maintain proper plant spacing for air circulation"
        ],
        'monitoring_schedule': "Check every 3 days for 2 weeks",
        'risk_factors': f"High humidity, {crop_type} susceptibility, current season conditions"
    }

def display_pest_results(result, uploaded_images):
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Risk level display
    risk_class = f"risk-{result['risk_level'].lower()}"
    risk_color = "🔴" if result['risk_level'] == "High" else "🟡" if result['risk_level'] == "Medium" else "🟢"
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
                padding: 25px; border-radius: 20px; margin: 20px 0;
                box-shadow: 0 10px 30px rgba(245, 158, 11, 0.4);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h2 style='color: black; margin: 0; font-size: 1.5rem;'>
                    ✅ PEST RISK ANALYSIS COMPLETE
                </h2>
                <p style='color: rgba(0,0,0,0.7); margin: 5px 0 0 0; font-weight: 600;'>
                    Analysis successful with {result['confidence']:.1%} confidence
                </p>
            </div>
            <div style='background: black; color: #f59e0b; padding: 15px 25px; 
                        border-radius: 15px; font-size: 2rem; font-weight: 800;'>
                {result['confidence']:.0%}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk overview cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='pest-card'>
            <h3 style='color: #f59e0b; margin: 0 0 20px 0;'>⚠️ RISK ASSESSMENT</h3>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Overall Risk Level</p>
                <div style='display: flex; align-items: center; gap: 15px; margin-top: 10px;'>
                    <span class='{risk_class}'>{result['risk_level']}</span>
                    <span style='color: #e2e8f0; font-weight: 700;'>{result['risk_score']:.1%}</span>
                </div>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Affected Areas</p>
                <p style='color: #fbbf24; margin: 5px 0 0 0; font-weight: 600; font-size: 1.1rem;'>
                    📍 {result['affected_areas']} field sections show concerns
                </p>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Risk Factors</p>
                <p style='color: #e2e8f0; line-height: 1.5; font-size: 0.95rem;'>
                    {result['risk_factors']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='pest-card'>
            <h3 style='color: #f59e0b; margin: 0 0 20px 0;'>🐛 DETECTED PEST RISKS</h3>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 15px 0;'>Potential Pests Identified:</p>
                {"".join([f"<div style='background: rgba(239, 68, 68, 0.1); padding: 10px 15px; border-radius: 10px; margin: 8px 0; border-left: 3px solid #ef4444;'><p style='color: #fca5a5; margin: 0; font-weight: 600;'>• {pest}</p></div>" for pest in result['detected_pests']])}
            </div>
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Monitoring Schedule</p>
                <p style='color: #fbbf24; margin: 5px 0 0 0; font-weight: 600;'>
                    📅 {result['monitoring_schedule']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Emergency actions for high risk
    if result['risk_level'] == "High":
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(220, 38, 38, 0.15));
                    border: 2px solid #ef4444;
                    border-radius: 20px; padding: 25px; margin: 20px 0;'>
            <h3 style='color: #ef4444; margin: 0 0 20px 0; font-size: 1.5rem;'>
                🚨 IMMEDIATE ACTIONS REQUIRED
            </h3>
        """, unsafe_allow_html=True)
        
        for i, action in enumerate(result['immediate_actions'], 1):
            st.markdown(f"""
            <div class='emergency-step'>
                <div style='display: flex; gap: 15px; align-items: flex-start;'>
                    <div style='background: #ef4444; color: white; width: 30px; height: 30px; 
                               border-radius: 50%; display: flex; align-items: center; 
                               justify-content: center; font-weight: 700; font-size: 0.9rem; flex-shrink: 0;'>
                        {i}
                    </div>
                    <p style='color: #e2e8f0; margin: 0; line-height: 1.6; font-size: 1.05rem;'>
                        {action}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Preventive measures
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #f59e0b; font-size: 2rem; font-weight: 800;'>
            🛡️ PREVENTIVE STRATEGIES
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    for i, measure in enumerate(result['preventive_measures'], 1):
        st.markdown(f"""
        <div class='prevention-step'>
            <div style='display: flex; gap: 15px; align-items: flex-start;'>
                <div style='background: #f59e0b; color: black; width: 30px; height: 30px; 
                           border-radius: 50%; display: flex; align-items: center; 
                           justify-content: center; font-weight: 700; font-size: 0.9rem; flex-shrink: 0;'>
                    {i}
                </div>
                <p style='color: #e2e8f0; margin: 0; line-height: 1.6; font-size: 1.05rem;'>
                    {measure}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Image gallery
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #f59e0b; font-size: 2rem; font-weight: 800;'>
            🖼️ ANALYZED FIELD IMAGES
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(min(4, len(uploaded_images)))
    for idx, uploaded_file in enumerate(uploaded_images):
        with cols[idx % 4]:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Field Area {idx+1}", use_column_width=True)
    
    # New analysis button
    st.markdown("---")
    if st.button("🔄 ANALYZE NEW FIELD IMAGES", type="primary", use_container_width=True):
        st.rerun()

def manual_entry_tab():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                border-radius: 20px; padding: 25px; border: 2px solid rgba(245,158,11,0.3); margin: 20px 0;'>
        <h2 style='color:#f59e0b; margin:0 0 10px 0;'>📝 Manual Pest Symptom Entry</h2>
        <p style='color:#94a3b8; margin:0;'>Describe visible pest damage and symptoms for risk assessment.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        crop_type = st.selectbox("Select Crop", 
                               ["Rice", "Wheat", "Maize", "Cotton", "Tomato", "Potato", "Vegetables", "Fruits", "Other"],
                               key="manual_crop")
        
        st.markdown("""
        <div style='background: rgba(245, 158, 11, 0.1); border-radius: 12px; 
                    padding: 15px; border: 1px solid rgba(245, 158, 11, 0.3); margin: 20px 0;'>
            <p style='color: #f59e0b; margin: 0; font-weight: 600;'>
                🐛 Describe Pest Symptoms
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        symptoms = st.text_area("", 
                              placeholder="Describe what you see:\n• Chewed leaves\n• Visible insects\n• Discoloration\n• Webbing\n• Holes in leaves",
                              height=150,
                              label_visibility="collapsed")
    
    with col2:
        st.markdown("""
        <div style='background: rgba(59, 130, 246, 0.1); border-radius: 12px; 
                    padding: 20px; border: 1px solid rgba(59, 130, 246, 0.3); height: 100%;'>
            <h4 style='color: #3b82f6; margin: 0 0 15px 0;'>💡 Common Symptoms</h4>
            <ul style='color: #94a3b8; line-height: 1.8; margin: 0; padding-left: 20px;'>
                <li>Holes in leaves</li>
                <li>Chewed edges</li>
                <li>Yellowing spots</li>
                <li>Webbing on plants</li>
                <li>Sticky residue</li>
                <li>Visible insects</li>
                <li>Wilting plants</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🔍 ANALYZE SYMPTOMS", type="primary", use_container_width=True):
        if symptoms:
            with st.spinner("Analyzing described symptoms..."):
                result = analyze_manual_symptoms(symptoms, crop_type)
                display_pest_results(result, [])
        else:
            st.warning("Please describe the pest symptoms you're observing.")

def analyze_manual_symptoms(symptoms, crop_type):
    """Analyze manually entered symptoms"""
    pests_db = load_pest_database()
    crop_pests = pests_db[pests_db['crop_type'] == crop_type] if crop_type != "Other" else pests_db
    
    # Simple keyword matching
    symptom_lower = symptoms.lower()
    matched_pests = []
    
    for _, pest in crop_pests.iterrows():
        keywords = pest['symptoms'].lower().split() + pest['common_names'].lower().split()
        if any(keyword in symptom_lower for keyword in keywords if len(keyword) > 3):
            matched_pests.append(pest)
    
    if matched_pests:
        pest = matched_pests[0]
        risk_score = 0.7 if len(matched_pests) > 2 else 0.5 if len(matched_pests) > 1 else 0.3
        
        return {
            'risk_level': "High" if risk_score > 0.6 else "Medium" if risk_score > 0.3 else "Low",
            'risk_score': risk_score,
            'confidence': 0.75,
            'detected_pests': [pest['pest_name']],
            'affected_areas': 1,
            'immediate_actions': pest['immediate_actions'].split('; '),
            'preventive_measures': pest['preventive_measures'].split('; '),
            'monitoring_schedule': "Check every 2-3 days",
            'risk_factors': f"Based on symptom description for {crop_type}"
        }
    else:
        return {
            'risk_level': "Low",
            'risk_score': 0.2,
            'confidence': 0.65,
            'detected_pests': ["General pest risk"],
            'affected_areas': 1,
            'immediate_actions': [
                "Monitor plants closely for changes",
                "Take clear photos for better analysis",
                "Check undersides of leaves"
            ],
            'preventive_measures': [
                "Apply general organic pest control",
                "Maintain field hygiene",
                "Regular plant inspection"
            ],
            'monitoring_schedule': "Weekly checks recommended",
            'risk_factors': "General description provided"
        }

def pest_library_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #f59e0b; font-size: 2rem; font-weight: 800;'>
            📚 PEST DATABASE
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Comprehensive information about common agricultural pests
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        crop_filter = st.selectbox("🌾 Filter by Crop", 
                                 ["All", "Rice", "Wheat", "Maize", "Cotton", "Tomato", "Potato", "Vegetables", "Fruits"])
    with col2:
        season_filter = st.selectbox("🌡️ Filter by Active Season", 
                                   ["All", "Summer", "Monsoon", "Winter", "All Year"])
    
    pests_df = load_pest_database()
    
    if crop_filter != "All":
        pests_df = pests_df[pests_df['crop_type'] == crop_filter]
    if season_filter != "All":
        pests_df = pests_df[pests_df['active_season'] == season_filter]
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
                padding: 15px 25px; border-radius: 12px; margin: 20px 0;
                text-align: center;'>
        <p style='color: black; margin: 0; font-weight: 800; font-size: 1.1rem;'>
            📊 Showing {len(pests_df)} pests
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display pest cards
    for idx, pest in pests_df.iterrows():
        risk_class = f"risk-{pest['risk_level'].lower()}"
        st.markdown(f"""
        <div class='library-card'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                <div>
                    <h3 style='color: white; margin: 0; font-size: 1.5rem;'>
                        🐛 {pest['pest_name']}
                    </h3>
                    <p style='color: #94a3b8; margin: 5px 0 0 0;'>
                        🌾 {pest['crop_type']} • 🌡️ {pest['active_season']} • 📏 {pest['damage_level']}
                    </p>
                </div>
                <span class='{risk_class}'>{pest['risk_level']}</span>
            </div>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Also known as:</p>
                <p style='color: #fbbf24; margin: 5px 0; font-weight: 600;'>{pest['common_names']}</p>
            </div>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Symptoms:</p>
                <p style='color: #e2e8f0; margin: 5px 0; line-height: 1.5;'>{pest['symptoms']}</p>
            </div>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;'>
                <div style='background: rgba(239, 68, 68, 0.1); padding: 12px; border-radius: 8px;'>
                    <p style='color: #ef4444; font-size: 0.85rem; margin: 0;'>🚨 Immediate Actions</p>
                    <p style='color: #94a3b8; font-size: 0.9rem; margin: 5px 0 0 0;'>{pest['immediate_actions'][:60]}...</p>
                </div>
                <div style='background: rgba(245, 158, 11, 0.1); padding: 12px; border-radius: 8px;'>
                    <p style='color: #f59e0b; font-size: 0.85rem; margin: 0;'>🛡️ Prevention</p>
                    <p style='color: #94a3b8; font-size: 0.9rem; margin: 5px 0 0 0;'>{pest['preventive_measures'][:60]}...</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def prevention_guide_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #f59e0b; font-size: 2rem; font-weight: 800;'>
            🛡️ PEST PREVENTION GUIDE
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Proactive strategies to protect your crops from pest infestations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Prevention practices
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 20px; padding: 35px; margin: 25px 0;
                border: 2px solid rgba(245, 158, 11, 0.3);'>
        <h3 style='color: #f59e0b; margin: 0 0 25px 0; font-size: 1.6rem;'>
            🌱 INTEGRATED PEST MANAGEMENT
        </h3>
    """, unsafe_allow_html=True)
    
    practices = [
        {
            'icon': '🔄',
            'title': 'Crop Rotation',
            'desc': 'Break pest life cycles by rotating crops. Avoid planting same crop family consecutively to disrupt pest habitats.',
            'color': '#f59e0b'
        },
        {
            'icon': '🪴',
            'title': 'Companion Planting',
            'desc': 'Plant pest-repelling crops like marigolds, basil, or garlic alongside main crops to naturally deter pests.',
            'color': '#84cc16'
        },
        {
            'icon': '🐞',
            'title': 'Biological Control',
            'desc': 'Introduce beneficial insects like ladybugs, lacewings, and parasitic wasps that prey on common pests.',
            'color': '#ef4444'
        },
        {
            'icon': '🌿',
            'title': 'Organic Sprays',
            'desc': 'Use neem oil, garlic spray, or chili solutions as natural pesticides that are safe for beneficial insects.',
            'color': '#10b981'
        },
        {
            'icon': '🚫',
            'title': 'Physical Barriers',
            'desc': 'Use floating row covers, sticky traps, and netting to physically prevent pests from reaching plants.',
            'color': '#3b82f6'
        },
        {
            'icon': '👁️',
            'title': 'Regular Monitoring',
            'desc': 'Conduct weekly field inspections. Early detection allows for timely intervention before major damage occurs.',
            'color': '#8b5cf6'
        }
    ]
    
    for practice in practices:
        st.markdown(f"""
        <div class='prevention-step'>
            <div style='display: flex; gap: 20px; align-items: flex-start;'>
                <div style='background: {practice['color']}; width: 60px; height: 60px; 
                           border-radius: 15px; display: flex; align-items: center; 
                           justify-content: center; font-size: 2rem; flex-shrink: 0;'>
                    {practice['icon']}
                </div>
                <div style='flex: 1;'>
                    <h4 style='color: white; margin: 0 0 10px 0; font-size: 1.3rem;'>
                        {practice['title']}
                    </h4>
                    <p style='color: #94a3b8; margin: 0; line-height: 1.7; font-size: 1rem;'>
                        {practice['desc']}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def load_pest_database():
    """Load pest database"""
    try:
        return pd.read_csv('data/pest_database.csv')
    except:
        data = {
            'pest_name': ['Aphids', 'Whiteflies', 'Caterpillars', 'Spider Mites', 'Bollworms'],
            'common_names': ['Plant lice, Greenflies', 'White flies', 'Armyworms, Cutworms', 'Red spider mites', 'American bollworm'],
            'crop_type': ['Vegetables', 'Tomato', 'Maize', 'Cotton', 'Cotton'],
            'symptoms': [
                'Clusters of small insects on new growth, sticky honeydew, curled leaves',
                'Tiny white insects flying when disturbed, yellowing leaves, sooty mold',
                'Chewed leaves, holes in foliage, frass (droppings) on leaves',
                'Fine webbing on leaves, yellow stippling, leaf drop',
                'Holes in bolls, larvae inside fruits, flower damage'
            ],
            'active_season': ['All Year', 'Summer', 'Monsoon', 'Summer', 'Flowering'],
            'damage_level': ['Moderate', 'High', 'Severe', 'Moderate', 'Severe'],
            'risk_level': ['Medium', 'High', 'High', 'Medium', 'High'],
            'immediate_actions': [
                'Spray neem oil; Use strong water jet; Apply insecticidal soap',
                'Yellow sticky traps; Neem oil spray; Remove heavily infested leaves',
                'Handpick caterpillars; Apply Bt (Bacillus thuringiensis); Use bird perches',
                'Spray water to dislodge; Apply miticide; Increase humidity',
                'Handpick infected bolls; Apply recommended insecticides; Use pheromone traps'
            ],
            'preventive_measures': [
                'Introduce ladybugs; Plant repellent herbs; Avoid over-fertilizing',
                'Use reflective mulch; Maintain weed-free field; Regular monitoring',
                'Install bird perches; Practice crop rotation; Use light traps',
                'Maintain proper humidity; Avoid water stress; Regular spraying',
                'Deep summer plowing; Timely sowing; Use resistant varieties'
            ]
        }
        
        return pd.DataFrame(data)

# Render when used as a Streamlit multipage script
pest_alert_page()