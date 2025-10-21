import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import streamlit.components.v1 as components
from scipy import ndimage  # ← ADD THIS LINE
# Enhanced CSS for Soil Analyzer Module with brown theme
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
    .soil-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(120, 113, 108, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .soil-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(120, 113, 108, 0.5);
        border-color: rgba(161, 161, 170, 0.6);
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, rgba(120, 113, 108, 0.15) 0%, rgba(161, 161, 170, 0.15) 100%);
        border: 2px solid rgba(120, 113, 108, 0.4);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(120, 113, 108, 0.2);
    }
    
    /* Tips card */
    .tips-card {
        background: rgba(87, 83, 78, 0.1);
        border-left: 4px solid #78716c;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Soil library card */
    .library-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #78716c;
        transition: all 0.3s ease;
    }
    
    .library-card:hover {
        transform: translateX(10px);
        border-left-color: #a1a1aa;
    }
    
    /* Health badges */
    .health-excellent {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .health-good {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .health-poor {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    /* Health meter */
    .health-meter {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        height: 30px;
        overflow: hidden;
        position: relative;
    }
    
    .health-fill {
        background: linear-gradient(90deg, #78716c, #a1a1aa);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    /* Improvement steps */
    .improvement-step {
        background: rgba(120, 113, 108, 0.1);
        border-left: 4px solid #78716c;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .improvement-step:hover {
        background: rgba(120, 113, 108, 0.2);
        transform: translateX(10px);
    }
    
    /* Soil type cards */
    .soil-sandy {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.2));
        border: 2px solid rgba(245, 158, 11, 0.4);
        border-radius: 15px;
        padding: 20px;
    }
    
    .soil-clay {
        background: linear-gradient(135deg, rgba(120, 113, 108, 0.2), rgba(87, 83, 78, 0.2));
        border: 2px solid rgba(120, 113, 108, 0.4);
        border-radius: 15px;
        padding: 20px;
    }
    
    .soil-loamy {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(22, 163, 74, 0.2));
        border: 2px solid rgba(34, 197, 94, 0.4);
        border-radius: 15px;
        padding: 20px;
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
        background: linear-gradient(135deg, #78716c, #a1a1aa);
        color: black;
    }
    
    /* Upload guidelines */
    .guidelines-box {
        background: linear-gradient(135deg, rgba(120, 113, 108, 0.15), rgba(161, 161, 170, 0.15));
        border: 2px solid rgba(120, 113, 108, 0.3);
        border-radius: 20px;
        padding: 25px;
    }
</style>
""", unsafe_allow_html=True)

def soil_analyzer_page():
    # Beautiful header
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px 20px 20px;'>
        <div style='font-size: 3.5rem; font-weight: 900; 
                    background: linear-gradient(90deg, #78716c, #a1a1aa, #57534e);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            📊 AI SOIL ANALYZER
        </div>
        <div style='color: #78716c; font-size: 1rem; font-weight: 600; 
                    letter-spacing: 2px; text-transform: uppercase; margin-top: 10px;'>
            ⚡ Image-Based Soil Health Assessment
        </div>
        <p style='color: #94a3b8; font-size: 1.1rem; max-width: 800px; 
                  margin: 20px auto 0 auto; line-height: 1.6;'>
            Upload soil images for AI-powered texture analysis and health assessment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Analyze Soil", "🌱 Soil Types", "📚 Soil Health", "💡 Improvement Guide"])
    
    with tab1:
        analyze_soil_tab()
    
    with tab2:
        soil_types_tab()
    
    with tab3:
        soil_health_tab()
    
    with tab4:
        improvement_guide_tab()

def is_soil_image(image):
    """Check if uploaded image contains soil"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) != 3:
            return False
        # Check for typical soil colors (brown, black, red, yellow)
        brown_pixels = np.sum((img_array[:, :, 0] > 80) & (img_array[:, :, 1] > 60) & (img_array[:, :, 2] < 120))
        black_pixels = np.sum(np.mean(img_array, axis=2) < 50)
        total_pixels = img_array.shape[0] * img_array.shape[1]
        soil_ratio = (brown_pixels + black_pixels) / total_pixels
        return soil_ratio > 0.3
    except:
        return False

def check_image_quality(image):
    """Basic image quality checks"""
    try:
        width, height = image.size
        if width < 250 or height < 250:
            return "Image too small. Please upload a higher resolution image for accurate soil analysis."
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            brightness = np.mean(img_array)
            if brightness < 40:
                return "Image too dark. Please upload a well-lit image for proper texture analysis."
        return None
    except:
        return "Unable to process image quality."
    
def is_soil_image(image):
    """Enhanced check if uploaded image contains soil with better exclusion of non-soil images"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) != 3:
            return False
        
        height, width = img_array.shape[:2]
        
        # Enhanced soil color detection with better thresholds
        brown_mask = (img_array[:, :, 0] > 80) & (img_array[:, :, 1] > 60) & (img_array[:, :, 2] < 120)
        black_mask = np.mean(img_array, axis=2) < 60
        red_soil_mask = (img_array[:, :, 0] > 120) & (img_array[:, :, 1] < 80) & (img_array[:, :, 2] < 80)
        yellow_soil_mask = (img_array[:, :, 0] > 180) & (img_array[:, :, 1] > 160) & (img_array[:, :, 2] < 100)
        gray_soil_mask = (np.abs(img_array[:, :, 0] - img_array[:, :, 1]) < 30) & \
                        (np.abs(img_array[:, :, 1] - img_array[:, :, 2]) < 30) & \
                        (img_array[:, :, 0] < 150)
        
        # EXCLUSION: Skin tones (human faces)
        skin_mask = (img_array[:, :, 0] > 150) & \
                   (img_array[:, :, 1] > 100) & (img_array[:, :, 1] < 200) & \
                   (img_array[:, :, 2] < 150) & \
                   (np.abs(img_array[:, :, 0] - img_array[:, :, 1]) < 50)
        
        # EXCLUSION: Blue-dominated images (sky, water, etc.)
        blue_mask = (img_array[:, :, 2] > img_array[:, :, 0] + 20) & \
                   (img_array[:, :, 2] > img_array[:, :, 1] + 20)
        
        # EXCLUSION: Man-made objects (uniform colors)
        uniform_mask = (np.std(img_array, axis=2) < 20)  # Low color variance
        
        soil_pixels = np.sum(brown_mask | black_mask | red_soil_mask | yellow_soil_mask | gray_soil_mask)
        skin_pixels = np.sum(skin_mask)
        blue_pixels = np.sum(blue_mask)
        uniform_pixels = np.sum(uniform_mask)
        total_pixels = height * width
        
        soil_ratio = soil_pixels / total_pixels
        skin_ratio = skin_pixels / total_pixels
        blue_ratio = blue_pixels / total_pixels
        uniform_ratio = uniform_pixels / total_pixels
        
        # Texture analysis - soil has characteristic texture patterns
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
            
        # Check for soil-like texture (moderate variance)
        texture_variance = np.var(gray)
        
        # Soil typically has moderate texture variance (not too smooth, not too busy)
        has_soil_texture = 200 < texture_variance < 3000  # Narrowed range
        
        # Color diversity check - soil has natural color variations
        color_diversity = np.std(img_array, axis=(0, 1))
        has_natural_colors = np.mean(color_diversity) > 20
        
        # Combined criteria with exclusions:
        # - Sufficient soil-colored pixels
        # - Soil-like texture
        # - Natural color variations
        # - NOT skin-toned (faces)
        # - NOT blue-dominated (sky/water)
        # - NOT uniform (man-made objects)
        return (soil_ratio > 0.4 and 
                has_soil_texture and 
                has_natural_colors and
                skin_ratio < 0.1 and    # Exclude faces
                blue_ratio < 0.2 and    # Exclude sky/water
                uniform_ratio < 0.3)    # Exclude man-made objects
        
    except Exception as e:
        print(f"Soil detection error: {e}")
        return False

def analyze_soil_tab():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 20px; padding: 30px; margin: 20px 0;
                border: 2px solid rgba(120, 113, 108, 0.3);'>
        <h2 style='color: #78716c; margin: 0; font-size: 1.8rem;'>
            📤 UPLOAD SOIL IMAGES
        </h2>
        <p style='color: #94a3b8; margin: 10px 0 0 0;'>
            Upload clear photos of soil samples from different depths and locations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_images = st.file_uploader("", 
                                       type=['jpg', 'jpeg', 'png'],
                                       accept_multiple_files=True,
                                       help="Upload soil images from different depths and field locations",
                                       label_visibility="collapsed")
        
        if uploaded_images:
            # Display first image in a styled container
            image = Image.open(uploaded_images[0])
            st.markdown("""
            <div style='background: rgba(0, 0, 0, 0.3); border-radius: 15px; 
                        padding: 15px; border: 2px solid rgba(120, 113, 108, 0.2);'>
            """, unsafe_allow_html=True)
            st.image(image, caption="📷 Soil Sample Image", use_column_width=True)
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
            
            # Soil detection check
            if not is_soil_image(image):
                st.markdown("""
                <div style='background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444;
                            border-radius: 15px; padding: 25px; margin: 20px 0;'>
                    <h3 style='color: #ef4444; margin: 0 0 15px 0;'>
                        ❌ This doesn't appear to be a soil image
                    </h3>
                    <p style='color: #fca5a5; margin: 10px 0;'>
                        <strong>Please upload clear photos of:</strong>
                    </p>
                    <ul style='color: #fca5a5; margin: 10px 0; padding-left: 20px;'>
                        <li>🌱 Soil samples from different depths</li>
                        <li>📏 Close-ups showing texture</li>
                        <li>💡 Natural lighting for color accuracy</li>
                        <li>📍 Multiple field locations</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                return
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Field information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style='background: rgba(120, 113, 108, 0.1); border-radius: 12px; 
                            padding: 15px; border: 1px solid rgba(120, 113, 108, 0.3); margin-bottom: 20px;'>
                    <p style='color: #78716c; margin: 0; font-weight: 600;'>
                        🏞️ Field Information
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                location = st.text_input("Field Location", "North Field")
                last_crop = st.selectbox("Previous Crop", 
                                       ["Rice", "Wheat", "Maize", "Vegetables", "Pulses", "None"])
            
            with col2:
                st.markdown("""
                <div style='background: rgba(87, 83, 78, 0.1); border-radius: 12px; 
                            padding: 15px; border: 1px solid rgba(87, 83, 78, 0.3); margin-bottom: 20px;'>
                    <p style='color: #57534e; margin: 0; font-weight: 600;'>
                        💧 Irrigation Type
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                irrigation = st.selectbox("Irrigation Method", 
                                        ["Flood", "Drip", "Sprinkler", "Rainfed"])
                farming_method = st.selectbox("Farming Method", 
                                           ["Conventional", "Organic", "Mixed"])
            
            if st.button("🔬 ANALYZE SOIL HEALTH", type="primary", use_container_width=True):
                with st.spinner("🔄 Analyzing soil texture and health parameters..."):
                    result = analyze_soil_health(uploaded_images)
                    display_soil_results(result, uploaded_images)
    
    with col2:
        guidelines_html = """
        <div class='guidelines-box'>
            <h3 style='color: #78716c; margin: 0 0 20px 0; font-size: 1.3rem;'>
                📸 SOIL IMAGE GUIDELINES
            </h3>
            
            <div style='margin: 20px 0;'>
                <p style='color: #78716c; font-weight: 700; margin-bottom: 10px;'>
                    ✅ IDEAL SAMPLES:
                </p>
                <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li>Soil from 6-8 inch depth</li>
                    <li>Natural lighting conditions</li>
                    <li>Show soil structure clearly</li>
                    <li>Multiple field locations</li>
                    <li>Undisturbed soil samples</li>
                </ul>
            </div>
            
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #ef4444; font-weight: 700; margin-bottom: 10px;'>
                    ❌ AVOID:
                </p>
                <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li>Wet/muddy soil</li>
                    <li>Mixed with debris</li>
                    <li>Poor lighting</li>
                    <li>Only surface soil</li>
                    <li>Blurry images</li>
                </ul>
            </div>
            
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #a1a1aa; font-weight: 700; margin-bottom: 10px;'>
                    🔍 ANALYSIS PARAMETERS:
                </p>
                <div style='color: #94a3b8; font-size: 0.9rem; line-height: 1.6;'>
                    • Soil texture type<br>
                    • Organic matter content<br>
                    • Moisture level estimation<br>
                    • Color analysis<br>
                    • Structure assessment
                </div>
            </div>
        </div>
        """
        components.html(guidelines_html, height=520, scrolling=True)

def analyze_soil_health(images):
    """Analyze soil images for health assessment"""
    # Mock analysis - replace with actual model
    textures = ["Sandy", "Clay", "Loamy", "Silty"]
    texture_probs = [0.2, 0.3, 0.4, 0.1]
    
    texture = np.random.choice(textures, p=texture_probs)
    
    texture_details = {
        "Sandy": {"health_score": 65, "organic_matter": 2.5, "moisture": 25, "drainage": "Excellent"},
        "Clay": {"health_score": 70, "organic_matter": 3.2, "moisture": 45, "drainage": "Poor"},
        "Loamy": {"health_score": 85, "organic_matter": 4.5, "moisture": 35, "drainage": "Good"},
        "Silty": {"health_score": 75, "organic_matter": 3.8, "moisture": 40, "drainage": "Moderate"}
    }
    
    details = texture_details[texture]
    
    return {
        "texture": texture,
        "health_score": details["health_score"],
        "organic_matter": details["organic_matter"],
        "moisture_level": details["moisture"],
        "drainage": details["drainage"],
        "sample_count": len(images),
        "recommendations": [
            f"Add organic compost for {texture} soil improvement",
            "Consider cover cropping to build soil structure",
            "Test pH levels for precise nutrient management",
            "Implement crop rotation for soil health"
        ],
        "suitable_crops": get_suitable_crops(texture),
        "improvement_timeline": "3-6 months with proper management"
    }

def get_suitable_crops(soil_type):
    """Get suitable crops based on soil type"""
    crop_suggestions = {
        "Sandy": ["Carrots", "Potatoes", "Radishes", "Sweet Potatoes"],
        "Clay": ["Cabbage", "Broccoli", "Spinach", "Kale"],
        "Loamy": ["Most crops - ideal soil", "Tomatoes", "Corn", "Beans"],
        "Silty": ["Lettuce", "Beans", "Peas", "Onions"]
    }
    return crop_suggestions.get(soil_type, ["Various crops"])

def display_soil_results(result, uploaded_images):
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Health score display
    health_class = "health-excellent" if result['health_score'] > 80 else "health-good" if result['health_score'] > 60 else "health-poor"
    health_color = "🟢" if result['health_score'] > 80 else "🟡" if result['health_score'] > 60 else "🔴"
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #78716c 0%, #a1a1aa 100%);
                padding: 25px; border-radius: 20px; margin: 20px 0;
                box-shadow: 0 10px 30px rgba(120, 113, 108, 0.4);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h2 style='color: black; margin: 0; font-size: 1.5rem;'>
                    ✅ SOIL ANALYSIS COMPLETE
                </h2>
                <p style='color: rgba(0,0,0,0.7); margin: 5px 0 0 0; font-weight: 600;'>
                    {result['sample_count']} samples analyzed • {result['health_score']}/100 health score
                </p>
            </div>
            <div style='background: black; color: #78716c; padding: 15px 25px; 
                        border-radius: 15px; font-size: 2rem; font-weight: 800;'>
                {result['health_score']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Soil analysis cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='soil-card'>
            <h3 style='color: #78716c; margin: 0 0 20px 0;'>🌱 SOIL PROPERTIES</h3>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Soil Texture</p>
                <p style='color: #e2e8f0; margin: 5px 0 0 0; font-weight: 700; font-size: 1.3rem;'>
                    {result['texture']}
                </p>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Health Score</p>
                <div style='display: flex; align-items: center; gap: 15px; margin-top: 10px;'>
                    <span class='{health_class}'>{result['health_score']}/100</span>
                    <div style='background: rgba(0,0,0,0.3); border-radius: 10px; height: 20px; flex: 1; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #78716c, #a1a1aa); 
                                    height: 100%; width: {result['health_score']}%; border-radius: 10px;'></div>
                    </div>
                </div>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Drainage Capacity</p>
                <p style='color: #84cc16; margin: 5px 0 0 0; font-weight: 600; font-size: 1.1rem;'>
                    💧 {result['drainage']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='soil-card'>
            <h3 style='color: #78716c; margin: 0 0 20px 0;'>📊 SOIL COMPOSITION</h3>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Organic Matter</p>
                <div style='display: flex; align-items: center; gap: 10px; margin-top: 10px;'>
                    <div style='background: rgba(120, 113, 108, 0.3); border-radius: 10px; height: 20px; flex: 1; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #57534e, #78716c); 
                                    height: 100%; width: {min(result['organic_matter'] * 20, 100)}%; border-radius: 10px;'></div>
                    </div>
                    <span style='color: #e2e8f0; font-weight: 700;'>{result['organic_matter']}%</span>
                </div>
                <p style='color: #94a3b8; font-size: 0.8rem; margin: 5px 0 0 0;'>
                    {'⭐ Good level' if result['organic_matter'] > 3.5 else '📝 Needs improvement'}
                </p>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Moisture Level</p>
                <div style='display: flex; align-items: center; gap: 10px; margin-top: 10px;'>
                    <div style='background: rgba(59, 130, 246, 0.3); border-radius: 10px; height: 20px; flex: 1; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #3b82f6, #60a5fa); 
                                    height: 100%; width: {result['moisture_level']}%; border-radius: 10px;'></div>
                    </div>
                    <span style='color: #e2e8f0; font-weight: 700;'>{result['moisture_level']}%</span>
                </div>
                <p style='color: #94a3b8; font-size: 0.8rem; margin: 5px 0 0 0;'>
                    {'💧 Optimal' if 30 <= result['moisture_level'] <= 40 else '⚠️ Adjust irrigation'}
                </p>
            </div>
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Improvement Timeline</p>
                <p style='color: #f59e0b; margin: 5px 0 0 0; font-weight: 600;'>
                    📅 {result['improvement_timeline']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Crop recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #78716c; font-size: 2rem; font-weight: 800;'>
            🌾 RECOMMENDED CROPS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(132, 204, 22, 0.15));
                border: 2px solid rgba(34, 197, 94, 0.4);
                border-radius: 20px; padding: 25px; margin: 20px 0;'>
        <h3 style='color: #22c55e; margin: 0 0 15px 0;'>🌱 Best suited crops for {result['texture']} soil</h3>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
            {"".join([f"""
            <div style='background: rgba(34, 197, 94, 0.1); padding: 15px; border-radius: 10px; 
                        border: 1px solid rgba(34, 197, 94, 0.3); text-align: center;'>
                <div style='font-size: 2rem; margin-bottom: 10px;'>🌽</div>
                <p style='color: #22c55e; margin: 0; font-weight: 600;'>{crop}</p>
            </div>
            """ for crop in result['suitable_crops']])}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Improvement recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #78716c; font-size: 2rem; font-weight: 800;'>
            💡 SOIL IMPROVEMENT RECOMMENDATIONS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    for i, recommendation in enumerate(result['recommendations'], 1):
        st.markdown(f"""
        <div class='improvement-step'>
            <div style='display: flex; gap: 15px; align-items: flex-start;'>
                <div style='background: #78716c; color: white; width: 30px; height: 30px; 
                           border-radius: 50%; display: flex; align-items: center; 
                           justify-content: center; font-weight: 700; font-size: 0.9rem; flex-shrink: 0;'>
                    {i}
                </div>
                <p style='color: #e2e8f0; margin: 0; line-height: 1.6; font-size: 1.05rem;'>
                    {recommendation}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Image gallery
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #78716c; font-size: 2rem; font-weight: 800;'>
            🖼️ ANALYZED SOIL SAMPLES
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(min(4, len(uploaded_images)))
    for idx, uploaded_file in enumerate(uploaded_images):
        with cols[idx % 4]:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Sample {idx+1}", use_column_width=True)
    
    # New analysis button
    st.markdown("---")
    if st.button("🔄 ANALYZE NEW SAMPLES", type="primary", use_container_width=True):
        st.rerun()

def soil_types_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #78716c; font-size: 2rem; font-weight: 800;'>
            🌱 SOIL TYPES GUIDE
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Understanding different soil textures and their characteristics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Soil type information
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='soil-sandy'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>🏖️</div>
                <h4 style='color: #f59e0b; margin: 10px 0; font-size: 1.3rem;'>SANDY SOIL</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 1.8; margin: 0; padding-left: 20px;'>
                <li>Large, coarse particles</li>
                <li>Excellent drainage</li>
                <li>Warms up quickly in spring</li>
                <li>Low nutrient retention</li>
                <li>Needs frequent watering</li>
                <li>Good for root vegetables</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='soil-loamy'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>⭐</div>
                <h4 style='color: #22c55e; margin: 10px 0; font-size: 1.3rem;'>LOAMY SOIL</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 1.8; margin: 0; padding-left: 20px;'>
                <li>Perfect balance of sand/silt/clay</li>
                <li>Good drainage & moisture retention</li>
                <li>Rich in organic matter</li>
                <li>Easy to work with</li>
                <li>Ideal for most crops</li>
                <li>Best overall soil type</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='soil-clay'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>🧱</div>
                <h4 style='color: #78716c; margin: 10px 0; font-size: 1.3rem;'>CLAY SOIL</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 1.8; margin: 0; padding-left: 20px;'>
                <li>Very fine particles</li>
                <li>Poor drainage</li>
                <li>High nutrient content</li>
                <li>Heavy and compact</li>
                <li>Slow to warm in spring</li>
                <li>Good for leafy vegetables</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def soil_health_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #78716c; font-size: 2rem; font-weight: 800;'>
            📚 SOIL HEALTH INDICATORS
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Key parameters for assessing and maintaining healthy soil
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Soil health parameters
    parameters = [
        {
            'parameter': 'Organic Matter',
            'ideal': '3-5%',
            'importance': 'Improves soil structure, water retention, and nutrient availability',
            'icon': '🌿'
        },
        {
            'parameter': 'Soil pH',
            'ideal': '6.0-7.0',
            'importance': 'Affects nutrient availability to plants',
            'icon': '📊'
        },
        {
            'parameter': 'Moisture',
            'ideal': '30-40%',
            'importance': 'Essential for plant growth and microbial activity',
            'icon': '💧'
        },
        {
            'parameter': 'Drainage',
            'ideal': 'Good-Moderate',
            'importance': 'Prevents waterlogging and root rot',
            'icon': '🌊'
        },
        {
            'parameter': 'Soil Structure',
            'ideal': 'Crumbly',
            'importance': 'Allows root penetration and air movement',
            'icon': '🏗️'
        },
        {
            'parameter': 'Microbial Activity',
            'ideal': 'High',
            'importance': 'Breaks down organic matter and releases nutrients',
            'icon': '🦠'
        }
    ]
    
    for param in parameters:
        st.markdown(f"""
        <div class='library-card'>
            <div style='display: flex; gap: 20px; align-items: flex-start;'>
                <div style='background: #78716c; width: 60px; height: 60px; 
                           border-radius: 15px; display: flex; align-items: center; 
                           justify-content: center; font-size: 2rem; flex-shrink: 0;'>
                    {param['icon']}
                </div>
                <div style='flex: 1;'>
                    <h4 style='color: white; margin: 0 0 10px 0; font-size: 1.3rem;'>
                        {param['parameter']}
                    </h4>
                    <p style='color: #84cc16; margin: 0 0 8px 0; font-weight: 600;'>
                        Ideal Range: {param['ideal']}
                    </p>
                    <p style='color: #94a3b8; margin: 0; line-height: 1.6; font-size: 1rem;'>
                        {param['importance']}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def improvement_guide_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #78716c; font-size: 2rem; font-weight: 800;'>
            💡 SOIL IMPROVEMENT GUIDE
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Practical strategies to improve soil health and productivity
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Improvement practices
    practices = [
        {
            'icon': '🌿',
            'title': 'Add Organic Matter',
            'desc': 'Incorporate compost, manure, or green manure crops to improve soil structure and fertility.',
            'color': '#22c55e'
        },
        {
            'icon': '🔄',
            'title': 'Crop Rotation',
            'desc': 'Rotate crops to prevent nutrient depletion and break pest/disease cycles.',
            'color': '#f59e0b'
        },
        {
            'icon': '🌱',
            'title': 'Cover Cropping',
            'desc': 'Grow cover crops like legumes to fix nitrogen and prevent soil erosion.',
            'color': '#84cc16'
        },
        {
            'icon': '🚫',
            'title': 'Reduce Tillage',
            'desc': 'Minimize soil disturbance to preserve soil structure and microbial life.',
            'color': '#78716c'
        },
        {
            'icon': '📊',
            'title': 'Soil Testing',
            'desc': 'Regular soil testing helps apply precise nutrients and amendments.',
            'color': '#3b82f6'
        },
        {
            'icon': '💧',
            'title': 'Efficient Irrigation',
            'desc': 'Use drip irrigation or mulching to conserve water and maintain soil moisture.',
            'color': '#06b6d4'
        }
    ]
    
    for practice in practices:
        st.markdown(f"""
        <div class='improvement-step'>
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

# Render when used as a Streamlit multipage script
soil_analyzer_page()