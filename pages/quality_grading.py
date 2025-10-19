import streamlit as st
import pandas as pd
from PIL import Image
from scipy import ndimage
import numpy as np
import streamlit.components.v1 as components

# Enhanced CSS for Quality Grading Module with green theme
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
    .quality-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(34, 197, 94, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .quality-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(34, 197, 94, 0.5);
        border-color: rgba(132, 204, 22, 0.6);
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(132, 204, 22, 0.15) 100%);
        border: 2px solid rgba(34, 197, 94, 0.4);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(34, 197, 94, 0.2);
    }
    
    /* Tips card */
    .tips-card {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Grade library card */
    .library-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #22c55e;
        transition: all 0.3s ease;
    }
    
    .library-card:hover {
        transform: translateX(10px);
        border-left-color: #84cc16;
    }
    
    /* Grade badges */
    .grade-A {
        background: linear-gradient(135deg, #22c55e, #16a34a);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .grade-B {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .grade-C {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    /* Quality meter */
    .quality-meter {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        height: 30px;
        overflow: hidden;
        position: relative;
    }
    
    .quality-fill {
        background: linear-gradient(90deg, #22c55e, #84cc16);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    /* Improvement steps */
    .improvement-step {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .improvement-step:hover {
        background: rgba(34, 197, 94, 0.2);
        transform: translateX(10px);
    }
    
    /* Market cards */
    .market-premium {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(132, 204, 22, 0.2));
        border: 2px solid rgba(34, 197, 94, 0.4);
        border-radius: 15px;
        padding: 20px;
    }
    
    .market-standard {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.2));
        border: 2px solid rgba(245, 158, 11, 0.4);
        border-radius: 15px;
        padding: 20px;
    }
    
    .market-processing {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(220, 38, 38, 0.2));
        border: 2px solid rgba(239, 68, 68, 0.4);
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
        background: linear-gradient(135deg, #22c55e, #84cc16);
        color: black;
    }
    
    /* Upload guidelines */
    .guidelines-box {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(132, 204, 22, 0.15));
        border: 2px solid rgba(34, 197, 94, 0.3);
        border-radius: 20px;
        padding: 25px;
    }
</style>
""", unsafe_allow_html=True)

def quality_grading_page():
    # Beautiful header
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px 20px 20px;'>
        <div style='font-size: 3.5rem; font-weight: 900; 
                    background: linear-gradient(90deg, #22c55e, #84cc16, #16a34a);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🌾 AI QUALITY GRADING
        </div>
        <div style='color: #22c55e; font-size: 1rem; font-weight: 600; 
                    letter-spacing: 2px; text-transform: uppercase; margin-top: 10px;'>
            ⚡ Automated Crop Quality Assessment & Market Pricing
        </div>
        <p style='color: #94a3b8; font-size: 1.1rem; max-width: 800px; 
                  margin: 20px auto 0 auto; line-height: 1.6;'>
            Upload harvested crop images for AI-powered quality grading and get market-ready quality scores
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Grade Quality", "📊 Market Analysis", "⭐ Quality Standards", "💡 Improvement Guide"])
    
    with tab1:
        grade_quality_tab()
    
    with tab2:
        market_analysis_tab()
    
    with tab3:
        quality_standards_tab()
    
    with tab4:
        improvement_guide_tab()

def is_crop_image(image):
    """Check if uploaded image contains crop/harvested produce"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) != 3:
            return False
        # Check for typical crop colors (green, yellow, red, brown)
        color_variance = np.std(img_array, axis=(0, 1))
        return np.mean(color_variance) > 20  # Reasonable color variation
    except:
        return False

def check_image_quality(image):
    """Basic image quality checks"""
    try:
        width, height = image.size
        if width < 300 or height < 300:
            return "Image too small. Please upload a higher resolution image for accurate grading."
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            brightness = np.mean(img_array)
            if brightness < 60:
                return "Image too dark. Please upload a well-lit image for proper color analysis."
        return None
    except:
        return "Unable to process image quality."

def is_crop_image(image):
    """Enhanced check if uploaded image contains harvested crops"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) != 3:
            return False
        
        # Check for typical crop colors and textures
        height, width = img_array.shape[:2]
        
        # Look for crop-like colors (green, yellow, red, brown, orange)
        green_mask = (img_array[:, :, 1] > img_array[:, :, 0]) & (img_array[:, :, 1] > img_array[:, :, 2])
        yellow_mask = (img_array[:, :, 0] > 150) & (img_array[:, :, 1] > 150) & (img_array[:, :, 2] < 100)
        red_mask = (img_array[:, :, 0] > 150) & (img_array[:, :, 1] < 100) & (img_array[:, :, 2] < 100)
        brown_mask = (img_array[:, :, 0] > 100) & (img_array[:, :, 1] > 80) & (img_array[:, :, 2] < 100)
        
        crop_pixels = np.sum(green_mask | yellow_mask | red_mask | brown_mask)
        total_pixels = height * width
        crop_ratio = crop_pixels / total_pixels
        
        # Also check for texture/edge density (crops have more edges than plain backgrounds)
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
            
        # Simple edge detection
        from scipy import ndimage
        sx = ndimage.sobel(gray, axis=0, mode='constant')
        sy = ndimage.sobel(gray, axis=1, mode='constant')
        sob = np.hypot(sx, sy)
        edge_density = np.mean(sob > 50)  # Threshold for significant edges
        
        # Combined criteria: reasonable crop color ratio OR high edge density
        return crop_ratio > 0.25 or edge_density > 0.1
        
    except Exception as e:
        print(f"Crop detection error: {e}")
        return False

def grade_quality_tab():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 20px; padding: 30px; margin: 20px 0;
                border: 2px solid rgba(34, 197, 94, 0.3);'>
        <h2 style='color: #22c55e; margin: 0; font-size: 1.8rem;'>
            📤 UPLOAD HARVESTED CROP IMAGES
        </h2>
        <p style='color: #94a3b8; margin: 10px 0 0 0;'>
            Upload clear photos of your harvested crops for AI-powered quality assessment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_images = st.file_uploader("", 
                                       type=['jpg', 'jpeg', 'png'],
                                       accept_multiple_files=True,
                                       help="Upload clear images of harvested crops against plain background",
                                       label_visibility="collapsed")
        
        if uploaded_images:
            # Display first image in a styled container
            image = Image.open(uploaded_images[0])
            st.markdown("""
            <div style='background: rgba(0, 0, 0, 0.3); border-radius: 15px; 
                        padding: 15px; border: 2px solid rgba(34, 197, 94, 0.2);'>
            """, unsafe_allow_html=True)
            st.image(image, caption="📷 Sample Crop Image", use_column_width=True)
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
            
            # Crop detection check
            if not is_crop_image(image):
                st.markdown("""
                <div style='background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444;
                            border-radius: 15px; padding: 25px; margin: 20px 0;'>
                    <h3 style='color: #ef4444; margin: 0 0 15px 0;'>
                        ❌ This doesn't appear to be a crop image
                    </h3>
                    <p style='color: #fca5a5; margin: 10px 0;'>
                        <strong>Please upload clear photos of:</strong>
                    </p>
                    <ul style='color: #fca5a5; margin: 10px 0; padding-left: 20px;'>
                        <li>🌽 Harvested crops or produce</li>
                        <li>📏 Against plain background</li>
                        <li>💡 Well-lit for color accuracy</li>
                        <li>🎯 Multiple samples for batch grading</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                return
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Crop selection and details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style='background: rgba(34, 197, 94, 0.1); border-radius: 12px; 
                            padding: 15px; border: 1px solid rgba(34, 197, 94, 0.3); margin-bottom: 20px;'>
                    <p style='color: #22c55e; margin: 0; font-weight: 600;'>
                        🌾 Crop Details
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                crop_type = st.selectbox("Crop Type", 
                                       ["Rice", "Wheat", "Maize", "Tomato", "Potato", "Onion", "Carrot", "Apple", "Mango", "Other"],
                                       key="quality_crop")
                
                harvest_date = st.date_input("Harvest Date")
            
            with col2:
                st.markdown("""
                <div style='background: rgba(59, 130, 246, 0.1); border-radius: 12px; 
                            padding: 15px; border: 1px solid rgba(59, 130, 246, 0.3); margin-bottom: 20px;'>
                    <p style='color: #3b82f6; margin: 0; font-weight: 600;'>
                        💰 Market Details
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                expected_price = st.number_input("Expected Base Price (₹/kg)", 
                                               min_value=10, max_value=500, value=50)
                storage_type = st.selectbox("Storage Type", 
                                          ["Cold Storage", "Room Temperature", "Refrigerated", "Fresh Harvest"])
            
            if st.button("⭐ GRADE CROP QUALITY", type="primary", use_container_width=True):
                with st.spinner("🔄 Analyzing crop quality parameters..."):
                    result = analyze_crop_quality(uploaded_images, crop_type)
                    display_quality_results(result, uploaded_images, expected_price)
    
    with col2:
        guidelines_html = """
        <div class='guidelines-box'>
            <h3 style='color: #22c55e; margin: 0 0 20px 0; font-size: 1.3rem;'>
                📸 GRADING GUIDELINES
            </h3>
            
            <div style='margin: 20px 0;'>
                <p style='color: #22c55e; font-weight: 700; margin-bottom: 10px;'>
                    ✅ IDEAL IMAGES:
                </p>
                <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li>Plain white/neutral background</li>
                    <li>Good natural lighting</li>
                    <li>Multiple crop samples</li>
                    <li>Clear focus on details</li>
                    <li>Scale reference if possible</li>
                </ul>
            </div>
            
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #ef4444; font-weight: 700; margin-bottom: 10px;'>
                    ❌ AVOID:
                </p>
                <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li>Busy backgrounds</li>
                    <li>Poor lighting/shadow</li>
                    <li>Blurry images</li>
                    <li>Mixed crop types</li>
                    <li>Dirty/soiled samples</li>
                </ul>
            </div>
            
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #84cc16; font-weight: 700; margin-bottom: 10px;'>
                    📊 GRADING FACTORS:
                </p>
                <div style='color: #94a3b8; font-size: 0.9rem; line-height: 1.6;'>
                    • Size & uniformity<br>
                    • Color consistency<br>
                    • Surface defects<br>
                    • Ripeness level<br>
                    • Physical damage
                </div>
            </div>
        </div>
        """
        components.html(guidelines_html, height=520, scrolling=True)

def analyze_crop_quality(images, crop_type):
    """Analyze crop images for quality grading"""
    # Mock analysis - replace with actual model
    grades = ["A", "B", "C"]
    grade_weights = [0.3, 0.5, 0.2]  # Probability weights
    
    grade = np.random.choice(grades, p=grade_weights)
    
    grade_details = {
        "A": {"score": 85, "price_multiplier": 1.3, "market": "Premium Export", "defects": ["Minor variations"]},
        "B": {"score": 70, "price_multiplier": 1.0, "market": "Local Premium", "defects": ["Size variation", "Color inconsistency"]},
        "C": {"score": 55, "price_multiplier": 0.7, "market": "Processing/Wholesale", "defects": ["Surface spots", "Size variation", "Color issues"]}
    }
    
    details = grade_details[grade]
    
    return {
        "grade": grade,
        "quality_score": details["score"],
        "price_multiplier": details["price_multiplier"],
        "target_market": details["market"],
        "defects": details["defects"],
        "strengths": ["Good color uniformity", "Proper size"] if grade == "A" else ["Acceptable quality", "Market ready"],
        "improvement_tips": [
            "Harvest at optimal maturity stage",
            "Improve post-harvest handling",
            "Control storage conditions",
            "Sort and grade before marketing"
        ],
        "sample_count": len(images),
        "consistency_score": min(80 + len(images) * 3, 95)
    }

def display_quality_results(result, uploaded_images, base_price):
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quality grade display
    grade_class = f"grade-{result['grade']}"
    grade_color = "🟢" if result['grade'] == "A" else "🟡" if result['grade'] == "B" else "🔴"
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #22c55e 0%, #84cc16 100%);
                padding: 25px; border-radius: 20px; margin: 20px 0;
                box-shadow: 0 10px 30px rgba(34, 197, 94, 0.4);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h2 style='color: black; margin: 0; font-size: 1.5rem;'>
                    ✅ QUALITY GRADING COMPLETE
                </h2>
                <p style='color: rgba(0,0,0,0.7); margin: 5px 0 0 0; font-weight: 600;'>
                    {result['sample_count']} samples analyzed • {result['consistency_score']}% consistency
                </p>
            </div>
            <div style='background: black; color: #22c55e; padding: 15px 25px; 
                        border-radius: 15px; font-size: 2rem; font-weight: 800;'>
                {result['grade']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quality overview cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='quality-card'>
            <h3 style='color: #22c55e; margin: 0 0 20px 0;'>📊 QUALITY ASSESSMENT</h3>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Overall Quality Grade</p>
                <div style='display: flex; align-items: center; gap: 15px; margin-top: 10px;'>
                    <span class='{grade_class}'>{result['grade']} Grade</span>
                    <span style='color: #e2e8f0; font-weight: 700;'>{result['quality_score']}/100</span>
                </div>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Target Market</p>
                <p style='color: #84cc16; margin: 5px 0 0 0; font-weight: 600; font-size: 1.1rem;'>
                    🏪 {result['target_market']}
                </p>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Sample Consistency</p>
                <div style='background: rgba(0,0,0,0.3); border-radius: 10px; height: 20px; overflow: hidden;'>
                    <div style='background: linear-gradient(90deg, #22c55e, #84cc16); 
                                height: 100%; width: {result['consistency_score']}%; border-radius: 10px;'></div>
                </div>
                <p style='color: #94a3b8; font-size: 0.8rem; margin: 5px 0 0 0; text-align: right;'>
                    {result['consistency_score']}% uniform
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='quality-card'>
            <h3 style='color: #22c55e; margin: 0 0 20px 0;'>🔍 QUALITY ANALYSIS</h3>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Strengths</p>
                {"".join([f"<div style='background: rgba(34, 197, 94, 0.1); padding: 8px 12px; border-radius: 8px; margin: 5px 0; border-left: 3px solid #22c55e;'><p style='color: #86efac; margin: 0; font-size: 0.9rem;'>✅ {strength}</p></div>" for strength in result['strengths']])}
            </div>
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Areas for Improvement</p>
                {"".join([f"<div style='background: rgba(239, 68, 68, 0.1); padding: 8px 12px; border-radius: 8px; margin: 5px 0; border-left: 3px solid #ef4444;'><p style='color: #fca5a5; margin: 0; font-size: 0.9rem;'>❌ {defect}</p></div>" for defect in result['defects']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Price analysis
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #22c55e; font-size: 2rem; font-weight: 800;'>
            💰 PRICE ANALYSIS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: rgba(34, 197, 94, 0.1); border: 2px solid rgba(34, 197, 94, 0.3);
                    border-radius: 15px; padding: 20px; text-align: center;'>
            <p style='color: #22c55e; font-size: 0.9rem; margin: 0 0 10px 0;'>Base Price</p>
            <h3 style='color: #e2e8f0; margin: 0; font-size: 1.8rem;'>₹{base_price}/kg</h3>
            <p style='color: #94a3b8; font-size: 0.8rem; margin: 5px 0 0 0;'>Expected market rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        price_premium = ((result['price_multiplier'] - 1) * 100)
        estimated_price = base_price * result['price_multiplier']
        st.markdown(f"""
        <div style='background: rgba(245, 158, 11, 0.1); border: 2px solid rgba(245, 158, 11, 0.3);
                    border-radius: 15px; padding: 20px; text-align: center;'>
            <p style='color: #f59e0b; font-size: 0.9rem; margin: 0 0 10px 0;'>Quality Premium</p>
            <h3 style='color: #e2e8f0; margin: 0; font-size: 1.8rem;'>{price_premium:+.1f}%</h3>
            <p style='color: #94a3b8; font-size: 0.8rem; margin: 5px 0 0 0;'>Grade {result['grade']} multiplier</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: rgba(59, 130, 246, 0.1); border: 2px solid rgba(59, 130, 246, 0.3);
                    border-radius: 15px; padding: 20px; text-align: center;'>
            <p style='color: #3b82f6; font-size: 0.9rem; margin: 0 0 10px 0;'>Estimated Price</p>
            <h3 style='color: #e2e8f0; margin: 0; font-size: 1.8rem;'>₹{estimated_price:.1f}/kg</h3>
            <p style='color: #94a3b8; font-size: 0.8rem; margin: 5px 0 0 0;'>Final market value</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Improvement recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #22c55e; font-size: 2rem; font-weight: 800;'>
            💡 QUALITY IMPROVEMENT TIPS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    for i, tip in enumerate(result['improvement_tips'], 1):
        st.markdown(f"""
        <div class='improvement-step'>
            <div style='display: flex; gap: 15px; align-items: flex-start;'>
                <div style='background: #22c55e; color: white; width: 30px; height: 30px; 
                           border-radius: 50%; display: flex; align-items: center; 
                           justify-content: center; font-weight: 700; font-size: 0.9rem; flex-shrink: 0;'>
                    {i}
                </div>
                <p style='color: #e2e8f0; margin: 0; line-height: 1.6; font-size: 1.05rem;'>
                    {tip}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Image gallery
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #22c55e; font-size: 2rem; font-weight: 800;'>
            🖼️ ANALYZED CROP SAMPLES
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(min(4, len(uploaded_images)))
    for idx, uploaded_file in enumerate(uploaded_images):
        with cols[idx % 4]:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Sample {idx+1} • Grade {result['grade']}", use_column_width=True)
    
    # New analysis button
    st.markdown("---")
    if st.button("🔄 GRADE NEW SAMPLES", type="primary", use_container_width=True):
        st.rerun()

def market_analysis_tab():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                border-radius: 20px; padding: 25px; border: 2px solid rgba(34,197,94,0.3); margin: 20px 0;'>
        <h2 style='color:#22c55e; margin:0 0 10px 0;'>📊 Market Analysis & Pricing</h2>
        <p style='color:#94a3b8; margin:0;'>Understand how quality grades impact market value and pricing.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        crop_type = st.selectbox("Select Crop", 
                               ["Rice", "Wheat", "Maize", "Tomato", "Potato", "Onion", "Carrot", "Apple", "Mango"],
                               key="market_crop")
        
        current_grade = st.selectbox("Current Quality Grade", ["A", "B", "C"])
        
        st.markdown("""
        <div style='background: rgba(34, 197, 94, 0.1); border-radius: 12px; 
                    padding: 15px; border: 1px solid rgba(34, 197, 94, 0.3); margin: 20px 0;'>
            <p style='color: #22c55e; margin: 0; font-weight: 600;'>
                💰 Price Simulation
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        base_price = st.number_input("Current Market Price (₹/kg)", 
                                   min_value=10, max_value=500, value=50, key="market_price")
    
    with col2:
        # Market premium display
        grade_multipliers = {"A": 1.3, "B": 1.0, "C": 0.7}
        current_multiplier = grade_multipliers[current_grade]
        
        st.markdown(f"""
        <div class='market-premium'>
            <h4 style='color: #22c55e; margin: 0 0 15px 0; text-align: center;'>Grade {current_grade} Premium</h4>
            <div style='text-align: center;'>
                <div style='font-size: 2.5rem; color: #22c55e; font-weight: 800; margin: 10px 0;'>
                    {((current_multiplier - 1) * 100):+.1f}%
                </div>
                <p style='color: #94a3b8; margin: 0; font-size: 0.9rem;'>
                    Price multiplier for Grade {current_grade}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        estimated_price = base_price * current_multiplier
        st.metric("Estimated Price", f"₹{estimated_price:.1f}/kg")

def quality_standards_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #22c55e; font-size: 2rem; font-weight: 800;'>
            ⭐ QUALITY STANDARDS
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Understanding crop quality grading standards and specifications
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Grade standards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='market-premium'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>🟢</div>
                <h4 style='color: #22c55e; margin: 10px 0; font-size: 1.3rem;'>GRADE A</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 1.8; margin: 0; padding-left: 20px;'>
                <li>Premium export quality</li>
                <li>95%+ size uniformity</li>
                <li>Perfect color consistency</li>
                <li>No visible defects</li>
                <li>Optimal ripeness</li>
                <li>Price: +20-30% premium</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='market-standard'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>🟡</div>
                <h4 style='color: #f59e0b; margin: 10px 0; font-size: 1.3rem;'>GRADE B</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 1.8; margin: 0; padding-left: 20px;'>
                <li>Local premium markets</li>
                <li>85%+ size uniformity</li>
                <li>Minor color variations</li>
                <li>Small defects allowed</li>
                <li>Good ripeness level</li>
                <li>Price: Standard market rate</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='market-processing'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>🔴</div>
                <h4 style='color: #ef4444; margin: 10px 0; font-size: 1.3rem;'>GRADE C</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 1.8; margin: 0; padding-left: 20px;'>
                <li>Processing/wholesale</li>
                <li>70%+ size uniformity</li>
                <li>Noticeable variations</li>
                <li>Visible defects present</li>
                <li>Variable ripeness</li>
                <li>Price: 20-30% discount</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def improvement_guide_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #22c55e; font-size: 2rem; font-weight: 800;'>
            💡 QUALITY IMPROVEMENT GUIDE
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Strategies to improve crop quality and achieve better market grades
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Improvement practices
    practices = [
        {
            'icon': '🌱',
            'title': 'Optimal Harvest Timing',
            'desc': 'Harvest at peak maturity. Monitor crop development stages and harvest when quality parameters are optimal.',
            'color': '#22c55e'
        },
        {
            'icon': '👐',
            'title': 'Gentle Handling',
            'desc': 'Minimize physical damage during harvesting and handling. Use proper tools and techniques to prevent bruising.',
            'color': '#3b82f6'
        },
        {
            'icon': '🌡️',
            'title': 'Proper Storage',
            'desc': 'Maintain optimal temperature and humidity. Different crops require specific storage conditions for quality preservation.',
            'color': '#8b5cf6'
        },
        {
            'icon': '📦',
            'title': 'Efficient Packaging',
            'desc': 'Use appropriate packaging materials. Proper packaging prevents damage during transportation and maintains freshness.',
            'color': '#f59e0b'
        },
        {
            'icon': '🔍',
            'title': 'Regular Quality Checks',
            'desc': 'Implement quality control at every stage. Regular monitoring helps identify and address issues early.',
            'color': '#ef4444'
        },
        {
            'icon': '📊',
            'title': 'Market Feedback',
            'desc': 'Learn from buyer feedback. Understand market preferences and adjust practices accordingly.',
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
quality_grading_page()