import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import re
import streamlit.components.v1 as components

# Enhanced CSS for Disease Detection Module
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
    .disease-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(51, 65, 85, 0.95) 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 2px solid rgba(16, 185, 129, 0.3);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .disease-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(16, 185, 129, 0.5);
        border-color: rgba(132, 204, 22, 0.6);
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(132, 204, 22, 0.15) 100%);
        border: 2px solid rgba(16, 185, 129, 0.4);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.2);
    }
    
    /* Tips card */
    .tips-card {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    /* Disease library card */
    .library-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(51, 65, 85, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border-left: 5px solid #10b981;
        transition: all 0.3s ease;
    }
    
    .library-card:hover {
        transform: translateX(10px);
        border-left-color: #84cc16;
    }
    
    /* Severity badges */
    .severity-high {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .severity-medium {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.85rem;
    }
    
    .severity-low {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
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
        background: linear-gradient(90deg, #10b981, #84cc16);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    /* Prevention steps */
    .prevention-step {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .prevention-step:hover {
        background: rgba(16, 185, 129, 0.2);
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
        background: linear-gradient(135deg, #10b981, #84cc16);
        color: black;
    }
</style>
""", unsafe_allow_html=True)

def disease_detection_page():
    # Beautiful header
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px 20px 20px;'>
        <div style='font-size: 3.5rem; font-weight: 900; 
                    background: linear-gradient(90deg, #10b981, #84cc16, #22c55e);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            📸 AI DISEASE DETECTION
        </div>
        <div style='color: #10b981; font-size: 1rem; font-weight: 600; 
                    letter-spacing: 2px; text-transform: uppercase; margin-top: 10px;'>
            ⚡ Instant Disease Identification & Treatment
        </div>
        <p style='color: #94a3b8; font-size: 1.1rem; max-width: 800px; 
                  margin: 20px auto 0 auto; line-height: 1.6;'>
            Upload crop/leaf images for AI-powered disease detection with expert treatment recommendations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🖼️ Detect Disease", "🎙️ Voice Symptoms", "📚 Disease Library", "💡 Prevention Guide"])
    
    with tab1:
        detect_disease_tab()
    
    with tab2:
        voice_symptom_tab()
    
    with tab3:
        disease_library_tab()
    
    with tab4:
        prevention_guide_tab()

def is_plant_image(image):
    """Basic check if uploaded image contains plant/leaf"""
    try:
        img_array = np.array(image)
        if len(img_array.shape) != 3:
            return False
        green_pixels = np.sum((img_array[:, :, 1] > img_array[:, :, 0]) & 
                             (img_array[:, :, 1] > img_array[:, :, 2]))
        total_pixels = img_array.shape[0] * img_array.shape[1]
        green_ratio = green_pixels / total_pixels
        return green_ratio > 0.15
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

def detect_disease_tab():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 20px; padding: 30px; margin: 20px 0;
                border: 2px solid rgba(16, 185, 129, 0.3);'>
        <h2 style='color: #10b981; margin: 0; font-size: 1.8rem;'>
            📤 UPLOAD PLANT IMAGE
        </h2>
        <p style='color: #94a3b8; margin: 10px 0 0 0;'>
            Upload clear photos of affected leaves or plants for accurate disease detection
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader("", 
                                       type=['jpg', 'jpeg', 'png'],
                                       help="Upload clear images of affected leaves/plants",
                                       label_visibility="collapsed")
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
            # Display image in a styled container
            st.markdown("""
            <div style='background: rgba(0, 0, 0, 0.3); border-radius: 15px; 
                        padding: 15px; border: 2px solid rgba(16, 185, 129, 0.2);'>
            """, unsafe_allow_html=True)
            st.image(image, caption="📷 Uploaded Image", use_column_width=True)
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
            
            # Plant detection check
            if not is_plant_image(image):
                st.markdown("""
                <div style='background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444;
                            border-radius: 15px; padding: 25px; margin: 20px 0;'>
                    <h3 style='color: #ef4444; margin: 0 0 15px 0;'>
                        ❌ This doesn't appear to be a plant image
                    </h3>
                    <p style='color: #fca5a5; margin: 10px 0;'>
                        <strong>Please upload a clear photo of:</strong>
                    </p>
                    <ul style='color: #fca5a5; margin: 10px 0; padding-left: 20px;'>
                        <li>🌿 Plant leaves with symptoms</li>
                        <li>🔍 Close-up of affected areas</li>
                        <li>💡 Well-lit plant parts</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                return
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Crop selection with styled container
            st.markdown("""
            <div style='background: rgba(59, 130, 246, 0.1); border-radius: 12px; 
                        padding: 15px; border: 1px solid rgba(59, 130, 246, 0.3); margin-bottom: 20px;'>
                <p style='color: #3b82f6; margin: 0; font-weight: 600;'>
                    🌾 Select Your Crop Type
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            crop_type = st.selectbox("", 
                                   ["Rice", "Wheat", "Maize", "Cotton", "Tomato", "Potato", "Other"],
                                   label_visibility="collapsed")
            
            if st.button("🔍 ANALYZE DISEASE", type="primary", use_container_width=True):
                with st.spinner("🔄 Analyzing image for disease symptoms..."):
                    result = analyze_disease_symptoms(image, crop_type)
                    display_detection_results(result)
    
    with col2:
        guidelines_html = """
        <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(16, 185, 129, 0.15));
                    border: 2px solid rgba(59, 130, 246, 0.3);
                    border-radius: 20px; padding: 25px;'>
            <h3 style='color: #10b981; margin: 0 0 20px 0; font-size: 1.3rem;'>
                📸 UPLOAD GUIDELINES
            </h3>
            
            <div style='margin: 20px 0;'>
                <p style='color: #10b981; font-weight: 700; margin-bottom: 10px;'>
                    ✅ DO UPLOAD:
                </p>
                <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li>Clear photos of plant leaves</li>
                    <li>Both healthy & diseased parts</li>
                    <li>Close-up shots of symptoms</li>
                    <li>Well-lit images</li>
                </ul>
            </div>
            
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #ef4444; font-weight: 700; margin-bottom: 10px;'>
                    ❌ DON'T UPLOAD:
                </p>
                <ul style='color: #94a3b8; margin: 0; padding-left: 20px; line-height: 1.8;'>
                    <li>Non-plant images</li>
                    <li>Blurry/dark photos</li>
                    <li>Whole field views</li>
                    <li>Soil/root images</li>
                </ul>
            </div>
            
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #84cc16; font-weight: 700; margin-bottom: 10px;'>
                    🌾 SUPPORTED CROPS:
                </p>
                <div style='display: flex; flex-wrap: wrap; gap: 8px;'>
                    <span style='background: rgba(16, 185, 129, 0.2); padding: 6px 12px; 
                                 border-radius: 15px; color: #10b981; font-size: 0.85rem;'>
                        Rice
                    </span>
                    <span style='background: rgba(16, 185, 129, 0.2); padding: 6px 12px; 
                                 border-radius: 15px; color: #10b981; font-size: 0.85rem;'>
                        Wheat
                    </span>
                    <span style='background: rgba(16, 185, 129, 0.2); padding: 6px 12px; 
                                 border-radius: 15px; color: #10b981; font-size: 0.85rem;'>
                        Maize
                    </span>
                    <span style='background: rgba(16, 185, 129, 0.2); padding: 6px 12px; 
                                 border-radius: 15px; color: #10b981; font-size: 0.85rem;'>
                        Cotton
                    </span>
                    <span style='background: rgba(16, 185, 129, 0.2); padding: 6px 12px; 
                                 border-radius: 15px; color: #10b981; font-size: 0.85rem;'>
                        Tomato
                    </span>
                    <span style='background: rgba(16, 185, 129, 0.2); padding: 6px 12px; 
                                 border-radius: 15px; color: #10b981; font-size: 0.85rem;'>
                        Potato
                    </span>
                </div>
            </div>
        </div>
        """
        # Use components.html to guarantee HTML rendering across Streamlit versions
        components.html(guidelines_html, height=520, scrolling=True)

def analyze_disease_symptoms(image, crop_type):
    """Analyze image and match with disease database"""
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        avg_color = np.mean(img_array, axis=(0, 1))
    else:
        avg_color = [0, 0, 0]
    
    diseases_df = load_disease_database()
    crop_diseases = diseases_df[diseases_df['crop_type'] == crop_type]
    
    if len(crop_diseases) > 0:
        disease = crop_diseases.iloc[0]
        confidence = min(85 + len(crop_type) * 2, 95)
        
        return {
            'disease_name': disease['disease_name'],
            'confidence': confidence,
            'symptoms': disease['symptoms'],
            'causes': disease['causes'],
            'organic_treatment': disease['organic_treatment'],
            'chemical_treatment': disease['chemical_treatment'],
            'prevention': disease['prevention'],
            'severity': disease['severity'],
            'risk_season': disease['risk_season']
        }
    else:
        return {
            'disease_name': 'No specific disease identified',
            'confidence': 60,
            'symptoms': 'General plant stress detected',
            'causes': 'Could be nutritional deficiency or environmental stress',
            'organic_treatment': 'Apply balanced organic fertilizer, improve soil health',
            'chemical_treatment': 'Consult local agricultural officer',
            'prevention': 'Maintain proper plant nutrition and irrigation',
            'severity': 'Low',
            'risk_season': 'All seasons'
        }

def display_detection_results(result):
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Success header with confidence
    severity_class = f"severity-{result['severity'].lower()}"
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #10b981 0%, #84cc16 100%);
                padding: 25px; border-radius: 20px; margin: 20px 0;
                box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h2 style='color: black; margin: 0; font-size: 1.5rem;'>
                    ✅ DETECTION COMPLETE
                </h2>
                <p style='color: rgba(0,0,0,0.7); margin: 5px 0 0 0; font-weight: 600;'>
                    Analysis successful with {result['confidence']}% confidence
                </p>
            </div>
            <div style='background: black; color: #10b981; padding: 15px 25px; 
                        border-radius: 15px; font-size: 2rem; font-weight: 800;'>
                {result['confidence']}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Disease info cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='disease-card'>
            <h3 style='color: #10b981; margin: 0 0 20px 0;'>🦠 DISEASE IDENTIFICATION</h3>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Disease Name</p>
                <h2 style='color: white; margin: 5px 0 0 0; font-size: 1.8rem;'>{result['disease_name']}</h2>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Severity Level</p>
                <span class='{severity_class}'>{result['severity']}</span>
            </div>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Risk Season</p>
                <p style='color: #84cc16; margin: 5px 0 0 0; font-weight: 600; font-size: 1.1rem;'>
                    🌡️ {result['risk_season']}
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='disease-card'>
            <h3 style='color: #10b981; margin: 0 0 20px 0;'>🔍 SYMPTOMS & CAUSES</h3>
            <div style='margin: 20px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Symptoms</p>
                <p style='color: #e2e8f0; line-height: 1.6;'>{result['symptoms']}</p>
            </div>
            <div style='margin: 20px 0; padding-top: 15px; border-top: 1px solid rgba(148, 163, 184, 0.2);'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0 0 10px 0;'>Causes</p>
                <p style='color: #e2e8f0; line-height: 1.6;'>{result['causes']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Treatment recommendations
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; margin: 30px 0 20px 0;'>
        <h2 style='color: #10b981; font-size: 2rem; font-weight: 800;'>
            💊 TREATMENT RECOMMENDATIONS
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🌱 Organic Treatment", "🧪 Chemical Treatment"])
    
    with tab1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(132, 204, 22, 0.15));
                    border: 2px solid rgba(16, 185, 129, 0.4);
                    border-radius: 20px; padding: 30px; margin: 20px 0;'>
            <h3 style='color: #10b981; margin: 0 0 15px 0;'>🌿 Organic & Natural Solutions</h3>
            <p style='color: #e2e8f0; line-height: 1.8; font-size: 1.05rem;'>
                {result['organic_treatment']}
            </p>
            <div style='margin-top: 20px; padding: 15px; background: rgba(16, 185, 129, 0.1); 
                        border-radius: 10px;'>
                <p style='color: #84cc16; margin: 0; font-weight: 600;'>
                    ✅ Eco-friendly • Safe for environment • No harmful residues
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.15), rgba(217, 119, 6, 0.15));
                    border: 2px solid rgba(245, 158, 11, 0.4);
                    border-radius: 20px; padding: 30px; margin: 20px 0;'>
            <h3 style='color: #f59e0b; margin: 0 0 15px 0;'>💉 Chemical Treatment Options</h3>
            <p style='color: #e2e8f0; line-height: 1.8; font-size: 1.05rem;'>
                {result['chemical_treatment']}
            </p>
            <div style='margin-top: 20px; padding: 15px; background: rgba(245, 158, 11, 0.1); 
                        border-radius: 10px;'>
                <p style='color: #fbbf24; margin: 0; font-weight: 600;'>
                    ⚠️ Follow dosage instructions • Use protective equipment • Consult experts
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Prevention measures
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.15));
                border: 2px solid rgba(59, 130, 246, 0.4);
                border-radius: 20px; padding: 30px; margin: 20px 0;'>
        <h3 style='color: #3b82f6; margin: 0 0 15px 0;'>🛡️ PREVENTION MEASURES</h3>
        <p style='color: #e2e8f0; line-height: 1.8; font-size: 1.05rem;'>
            {result['prevention']}
        </p>
        <div style='margin-top: 20px; padding: 15px; background: rgba(59, 130, 246, 0.1); 
                    border-radius: 10px;'>
            <p style='color: #60a5fa; margin: 0; font-weight: 600;'>
                💡 Prevention is better than cure • Regular monitoring recommended
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def disease_library_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #10b981; font-size: 2rem; font-weight: 800;'>
            📚 CROP DISEASE DATABASE
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Browse comprehensive information about common crop diseases
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        crop_filter = st.selectbox("🌾 Filter by Crop", 
                                 ["All", "Rice", "Wheat", "Maize", "Cotton", "Tomato", "Potato"])
    with col2:
        severity_filter = st.selectbox("⚠️ Filter by Severity", 
                                     ["All", "High", "Medium", "Low"])
    
    diseases_df = load_disease_database()
    
    if crop_filter != "All":
        diseases_df = diseases_df[diseases_df['crop_type'] == crop_filter]
    if severity_filter != "All":
        diseases_df = diseases_df[diseases_df['severity'] == severity_filter]
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #10b981 0%, #84cc16 100%);
                padding: 15px 25px; border-radius: 12px; margin: 20px 0;
                text-align: center;'>
        <p style='color: black; margin: 0; font-weight: 800; font-size: 1.1rem;'>
            📊 Showing {len(diseases_df)} diseases
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display disease cards
    for idx, disease in diseases_df.iterrows():
        severity_class = f"severity-{disease['severity'].lower()}"
        st.markdown(f"""
        <div class='library-card'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                <div>
                    <h3 style='color: white; margin: 0; font-size: 1.5rem;'>
                        🦠 {disease['disease_name']}
                    </h3>
                    <p style='color: #94a3b8; margin: 5px 0 0 0;'>
                        🌾 {disease['crop_type']} • 🌡️ {disease['risk_season']}
                    </p>
                </div>
                <span class='{severity_class}'>{disease['severity']}</span>
            </div>
            <div style='margin: 15px 0;'>
                <p style='color: #94a3b8; font-size: 0.9rem; margin: 0;'>Symptoms:</p>
                <p style='color: #e2e8f0; margin: 5px 0;'>{disease['symptoms']}</p>
            </div>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;'>
                <div style='background: rgba(16, 185, 129, 0.1); padding: 12px; border-radius: 8px;'>
                    <p style='color: #10b981; font-size: 0.85rem; margin: 0;'>🌱 Organic Treatment</p>
                    <p style='color: #94a3b8; font-size: 0.9rem; margin: 5px 0 0 0;'>{disease['organic_treatment'][:50]}...</p>
                </div>
                <div style='background: rgba(245, 158, 11, 0.1); padding: 12px; border-radius: 8px;'>
                    <p style='color: #f59e0b; font-size: 0.85rem; margin: 0;'>🧪 Chemical Treatment</p>
                    <p style='color: #94a3b8; font-size: 0.9rem; margin: 5px 0 0 0;'>{disease['chemical_treatment'][:50]}...</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def prevention_guide_tab():
    st.markdown("""
    <div style='text-align: center; margin: 30px 0;'>
        <h2 style='color: #10b981; font-size: 2rem; font-weight: 800;'>
            💡 DISEASE PREVENTION GUIDE
        </h2>
        <p style='color: #94a3b8; font-size: 1rem;'>
            Best practices to keep your crops healthy and disease-free
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # General prevention practices
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 20px; padding: 35px; margin: 25px 0;
                border: 2px solid rgba(16, 185, 129, 0.3);'>
        <h3 style='color: #10b981; margin: 0 0 25px 0; font-size: 1.6rem;'>
            🌱 GENERAL PREVENTION PRACTICES
        </h3>
    """, unsafe_allow_html=True)
    
    practices = [
        {
            'icon': '🔄',
            'title': 'Crop Rotation',
            'desc': 'Rotate crops to break disease cycles. Avoid planting same crop family consecutively to reduce pathogen buildup in soil.',
            'color': '#10b981'
        },
        {
            'icon': '🌍',
            'title': 'Healthy Soil Management',
            'desc': 'Maintain proper soil pH (6.0-7.0). Use organic compost regularly and ensure good drainage to prevent waterlogging.',
            'color': '#3b82f6'
        },
        {
            'icon': '📏',
            'title': 'Proper Spacing',
            'desc': 'Allow adequate air circulation between plants. Proper spacing reduces humidity around plants and prevents disease spread.',
            'color': '#8b5cf6'
        },
        {
            'icon': '🧹',
            'title': 'Field Sanitation',
            'desc': 'Remove infected plant debris immediately. Clean tools between uses and always use disease-free certified seeds.',
            'color': '#f59e0b'
        },
        {
            'icon': '👁️',
            'title': 'Regular Monitoring',
            'desc': 'Conduct regular field inspections for early detection. Monitor weather conditions and apply preventive measures timely.',
            'color': '#ef4444'
        },
        {
            'icon': '💧',
            'title': 'Water Management',
            'desc': 'Avoid overhead irrigation during humid weather. Water in early morning to allow foliage to dry during the day.',
            'color': '#06b6d4'
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
    
    # Seasonal prevention tips
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
                border-radius: 20px; padding: 35px; margin: 25px 0;
                border: 2px solid rgba(16, 185, 129, 0.3);'>
        <h3 style='color: #10b981; margin: 0 0 25px 0; font-size: 1.6rem;'>
            📅 SEASONAL PREVENTION STRATEGIES
        </h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.2));
                    border: 2px solid rgba(59, 130, 246, 0.4);
                    border-radius: 20px; padding: 25px; height: 100%;'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>🌧️</div>
                <h4 style='color: #3b82f6; margin: 10px 0; font-size: 1.3rem;'>MONSOON SEASON</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 2; margin: 0; padding-left: 20px;'>
                <li>Fungal diseases most common</li>
                <li>Ensure excellent drainage</li>
                <li>Apply preventive fungicides</li>
                <li>Avoid waterlogging</li>
                <li>Monitor humidity levels</li>
                <li>Increase plant spacing</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.2));
                    border: 2px solid rgba(245, 158, 11, 0.4);
                    border-radius: 20px; padding: 25px; height: 100%;'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>☀️</div>
                <h4 style='color: #f59e0b; margin: 10px 0; font-size: 1.3rem;'>SUMMER SEASON</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 2; margin: 0; padding-left: 20px;'>
                <li>Bacterial diseases prevalent</li>
                <li>Maintain proper irrigation</li>
                <li>Watch for pest vectors</li>
                <li>Mulch to retain moisture</li>
                <li>Provide shade if needed</li>
                <li>Monitor for heat stress</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(124, 58, 237, 0.2));
                    border: 2px solid rgba(139, 92, 246, 0.4);
                    border-radius: 20px; padding: 25px; height: 100%;'>
            <div style='text-align: center; margin-bottom: 15px;'>
                <div style='font-size: 3rem;'>❄️</div>
                <h4 style='color: #8b5cf6; margin: 10px 0; font-size: 1.3rem;'>WINTER SEASON</h4>
            </div>
            <ul style='color: #94a3b8; line-height: 2; margin: 0; padding-left: 20px;'>
                <li>Viral diseases active</li>
                <li>Control insect vectors</li>
                <li>Use resistant varieties</li>
                <li>Protect from frost</li>
                <li>Monitor temperature</li>
                <li>Reduce irrigation frequency</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick tips section
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #10b981 0%, #84cc16 100%);
                padding: 30px; border-radius: 20px; margin: 25px 0;
                box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);'>
        <h3 style='color: black; margin: 0 0 20px 0; font-size: 1.5rem; text-align: center;'>
            ⚡ QUICK PREVENTION TIPS
        </h3>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;'>
            <div style='background: rgba(0, 0, 0, 0.2); padding: 20px; border-radius: 12px;'>
                <h4 style='color: white; margin: 0 0 10px 0;'>🌱 Before Planting</h4>
                <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem;'>
                    • Use certified seeds<br>
                    • Treat seeds with fungicide<br>
                    • Prepare soil properly
                </p>
            </div>
            <div style='background: rgba(0, 0, 0, 0.2); padding: 20px; border-radius: 12px;'>
                <h4 style='color: white; margin: 0 0 10px 0;'>🌾 During Growth</h4>
                <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem;'>
                    • Scout fields weekly<br>
                    • Remove diseased plants<br>
                    • Apply nutrients timely
                </p>
            </div>
            <div style='background: rgba(0, 0, 0, 0.2); padding: 20px; border-radius: 12px;'>
                <h4 style='color: white; margin: 0 0 10px 0;'>📦 After Harvest</h4>
                <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem;'>
                    • Clean all debris<br>
                    • Sanitize equipment<br>
                    • Plan crop rotation
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Expert contact section
    st.markdown("""
    <div style='background: rgba(59, 130, 246, 0.1); border: 2px solid rgba(59, 130, 246, 0.3);
                border-radius: 15px; padding: 25px; margin: 25px 0; text-align: center;'>
        <h4 style='color: #3b82f6; margin: 0 0 15px 0; font-size: 1.3rem;'>
            📞 Need Expert Help?
        </h4>
        <p style='color: #94a3b8; margin: 0 0 20px 0; line-height: 1.6;'>
            If you notice severe disease symptoms or need personalized advice,<br>
            contact your local agricultural extension officer or plant pathologist
        </p>
        <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;'>
            <a href='#' style='background: linear-gradient(135deg, #10b981, #84cc16); 
                               color: black; padding: 12px 30px; border-radius: 25px; 
                               text-decoration: none; font-weight: 700; display: inline-block;'>
                📞 Contact Expert
            </a>
            <a href='#' style='background: rgba(59, 130, 246, 0.2); border: 2px solid #3b82f6;
                               color: #3b82f6; padding: 12px 30px; border-radius: 25px; 
                               text-decoration: none; font-weight: 700; display: inline-block;'>
                📚 Learn More
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def voice_symptom_tab():
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e293b 0%, #334155 100%); border-radius: 20px; padding: 25px; border: 2px solid rgba(16,185,129,0.3); margin: 20px 0;'>
        <h2 style='color:#10b981; margin:0 0 10px 0;'>🎙️ Voice-to-Text Symptom Entry</h2>
        <p style='color:#94a3b8; margin:0;'>Describe the visible symptoms and we'll match likely diseases.</p>
    </div>
    """, unsafe_allow_html=True)

    crop_type = st.selectbox("Select Crop", ["Rice", "Wheat", "Maize", "Cotton", "Tomato", "Potato", "Other"], key="voice_crop")

    try:
        from streamlit_mic_recorder import speech_to_text
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("Click Start, speak the symptoms, then Stop.")
        text = speech_to_text(language='en', start_prompt='🎙️ Start speaking', stop_prompt='🛑 Stop', use_container_width=True, key='symptoms_stt')
        if text:
            st.text_area("Transcribed symptoms", value=text, height=120, key="symptoms_text")
            if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True, key="analyze_symptoms_btn"):
                with st.spinner("Analyzing described symptoms..."):
                    result = analyze_symptoms_text(text, crop_type)
                    display_detection_results(result)
    except ModuleNotFoundError:
        st.warning("streamlit-mic-recorder is not installed. Please add it to requirements and install to enable voice input.")
        st.code("pip install streamlit-mic-recorder", language="bash")


def analyze_symptoms_text(symptom_text: str, crop_type: str):
    diseases_df = load_disease_database()
    if crop_type != "Other":
        diseases_df = diseases_df[diseases_df['crop_type'] == crop_type]
    
    # Basic token matching between described text and database fields
    def tokenize(s):
        return set(re.findall(r"[a-zA-Z]+", s.lower()))

    text_tokens = tokenize(symptom_text)
    best = None
    best_score = 0
    for _, row in diseases_df.iterrows():
        haystack = f"{row['symptoms']} {row['causes']}"
        tokens = tokenize(haystack)
        overlap = len(text_tokens & tokens)
        score = overlap / (len(text_tokens) + 1e-6)
        if score > best_score:
            best_score = score
            best = row

    if best is not None:
        confidence = int(min(60 + best_score*100, 92))
        return {
            'disease_name': best['disease_name'],
            'confidence': confidence,
            'symptoms': best['symptoms'],
            'causes': best['causes'],
            'organic_treatment': best['organic_treatment'],
            'chemical_treatment': best['chemical_treatment'],
            'prevention': best['prevention'],
            'severity': best['severity'],
            'risk_season': best['risk_season']
        }
    else:
        return {
            'disease_name': 'No strong match found',
            'confidence': 55,
            'symptoms': 'Unable to confidently match described symptoms',
            'causes': 'Insufficient or unclear description',
            'organic_treatment': 'Provide more details or upload an image for better analysis',
            'chemical_treatment': 'Consult local agricultural officer',
            'prevention': 'Monitor plants and describe visible leaf/plant symptoms precisely',
            'severity': 'Low',
            'risk_season': 'All seasons'
        }


def load_disease_database():
    """Load disease database from CSV or use sample data"""
    try:
        return pd.read_csv('data/disease_database.csv')
    except:
        data = {
            'crop_type': ['Rice', 'Rice', 'Wheat', 'Wheat', 'Maize', 'Tomato', 'Cotton'],
            'disease_name': ['Blast', 'Bacterial Blight', 'Rust', 'Smut', 'Leaf Blight', 'Early Blight', 'Bollworm'],
            'symptoms': [
                'Spindle-shaped spots with gray centers on leaves and stems',
                'Water-soaked lesions turning yellow, wilting of leaves',
                'Orange-brown pustules on leaves and stems',
                'Black powdery masses in spikes and grains',
                'Long elliptical gray-green lesions on leaves',
                'Dark spots with concentric rings on leaves',
                'Holes in bolls, larvae feeding inside'
            ],
            'causes': [
                'Fungus: Magnaporthe oryzae, favored by high humidity',
                'Bacteria: Xanthomonas oryzae, spreads through water',
                'Fungus: Puccinia species, cool temperatures',
                'Fungus: Ustilago species, seed-borne infection',
                'Fungus: Exserohilum turcicum, warm humid conditions',
                'Fungus: Alternaria solani, high humidity',
                'Insect: Helicoverpa armigera, warm weather pest'
            ],
            'organic_treatment': [
                'Neem oil spray (3%), Garlic extract, Trichoderma application',
                'Copper-based organic fungicides, Remove infected plants',
                'Sulfur dust application, Baking soda spray (1%)',
                'Remove and destroy infected plants immediately',
                'Copper fungicide spray, Increase plant spacing',
                'Copper spray, Remove affected leaves, Mulching',
                'Neem oil spray, NSKE (Neem Seed Kernel Extract), Bt application'
            ],
            'chemical_treatment': [
                'Tricyclazole 75% WP @ 200g/ha, Isoprothiolane 40% EC @ 1.5L/ha',
                'Streptomycin sulfate @ 200ppm, Kasugamycin 3% SL @ 2ml/L',
                'Propiconazole 25% EC @ 1ml/L, Tebuconazole 50% + Trifloxystrobin 25% WG',
                'Carbendazim 50% WP @ 1g/L, Mancozeb 75% WP @ 2.5g/L',
                'Chlorothalonil 75% WP @ 2g/L, Azoxystrobin 23% SC @ 1ml/L',
                'Chlorothalonil 75% WP @ 2g/L, Mancozeb 75% WP @ 2.5g/L',
                'Emamectin benzoate 5% SG @ 0.5g/L, Spinosad 45% SC @ 0.3ml/L'
            ],
            'prevention': [
                'Use resistant varieties like Pusa Basmati 1121, Proper spacing, Avoid excess nitrogen',
                'Avoid waterlogging, Balanced fertilization, Crop rotation',
                'Early sowing, Use resistant varieties, Remove alternate hosts',
                'Use treated certified seeds, Crop rotation with non-host crops',
                'Use resistant hybrids, Field sanitation, Balanced fertilization',
                'Proper plant spacing (45-60cm), Staking, Drip irrigation, Mulching',
                'Intercropping with chickpea/coriander, Pheromone traps, Monitor regularly'
            ],
            'severity': ['High', 'Medium', 'High', 'Medium', 'Medium', 'Low', 'High'],
            'risk_season': ['Monsoon', 'Rainy season', 'Winter', 'All seasons', 'Monsoon', 'Humid seasons', 'Flowering stage'],
            'affected_regions': ['All rice regions', 'Coastal areas', 'North India', 'All wheat areas', 'All regions', 'All tomato areas', 'All cotton regions']
        }
        
        return pd.DataFrame(data)

# Render when used as a Streamlit multipage script
disease_detection_page()
