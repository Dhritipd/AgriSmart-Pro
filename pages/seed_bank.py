import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    # Custom CSS for beautiful styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.3rem;
    }
    .seed-card {
        background: white;
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    .seed-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    .seed-title {
        color: #667eea;
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 0.8rem;
    }
    .seed-detail {
        margin: 0.5rem 0;
        color: #555;
    }
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .badge-success {
        background: #d4edda;
        color: #155724;
    }
    .badge-info {
        background: #d1ecf1;
        color: #0c5460;
    }
    .badge-warning {
        background: #fff3cd;
        color: #856404;
    }
    .badge-primary {
        background: #cce5ff;
        color: #004085;
    }
    .comparison-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 12px;
        margin-top: 1rem;
    }
    .supplier-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    .supplier-card h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.3rem;
    }
    .filter-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #667eea;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🌱 Seed Bank</h1>
        <p>Your comprehensive database for seed varieties, comparisons, and certified suppliers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <p class="stat-number">1,250+</p>
            <p class="stat-label">Seed Varieties</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <p class="stat-number">45+</p>
            <p class="stat-label">Crop Types</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <p class="stat-number">200+</p>
            <p class="stat-label">Certified Suppliers</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <p class="stat-number">98%</p>
            <p class="stat-label">Success Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Seed Database", 
        "⚖️ Variety Comparison", 
        "🛡️ Disease-Resistant Seeds",
        "✅ Certified Suppliers"
    ])
    
    # Tab 1: Seed Database
    with tab1:
        st.markdown("### 📚 Explore Our Seed Database")
        
        # Filters with beautiful design
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown("**🔍 Filter Your Search**")
        col1, col2, col3 = st.columns(3)
        with col1:
            crop_filter = st.selectbox("🌾 Crop Type", 
                ["All", "Rice", "Wheat", "Maize", "Cotton", "Vegetables", "Pulses"],
                key="crop_filter")
        with col2:
            season_filter = st.selectbox("🌤️ Season", 
                ["All", "Kharif", "Rabi", "Zaid", "Year-round"],
                key="season_filter")
        with col3:
            search = st.text_input("🔎 Search", placeholder="Enter variety name...")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sample seed database
        seed_varieties = [
            {"name": "IR64", "crop": "Rice", "season": "Kharif", "duration": 120, "yield": 45, 
             "resistance": ["Blast", "BPH"], "water": "Medium", "price": "₹60/kg"},
            {"name": "Pusa Basmati 1121", "crop": "Rice", "season": "Kharif", "duration": 140, "yield": 42,
             "resistance": ["Bacterial Blight"], "water": "High", "price": "₹120/kg"},
            {"name": "BG 380", "crop": "Rice", "season": "Kharif", "duration": 135, "yield": 48,
             "resistance": ["Blast"], "water": "Medium", "price": "₹75/kg"},
            {"name": "DHM 117", "crop": "Maize", "season": "Kharif", "duration": 85, "yield": 65,
             "resistance": ["Borer"], "water": "Low", "price": "₹50/kg"},
            {"name": "Arjun", "crop": "Wheat", "season": "Rabi", "duration": 135, "yield": 52,
             "resistance": ["Rust"], "water": "Medium", "price": "₹45/kg"},
            {"name": "HD 3086", "crop": "Wheat", "season": "Rabi", "duration": 140, "yield": 58,
             "resistance": ["Rust"], "water": "Medium", "price": "₹48/kg"},
        ]
        
        # Display as beautiful cards
        for variety in seed_varieties:
            if crop_filter != "All" and variety["crop"] != crop_filter:
                continue
            if season_filter != "All" and variety["season"] != season_filter:
                continue
            if search and search.lower() not in variety["name"].lower():
                continue
                
            st.markdown(f"""
            <div class="seed-card">
                <div class="seed-title">🌱 {variety['name']}</div>
                <div class="seed-detail">
                    <span class="badge badge-primary">{variety['crop']}</span>
                    <span class="badge badge-info">{variety['season']}</span>
                    <span class="badge badge-warning">{variety['water']} Water</span>
                </div>
                <div class="seed-detail">
                    ⏱️ <strong>Duration:</strong> {variety['duration']} days | 
                    📊 <strong>Yield:</strong> {variety['yield']} q/ha | 
                    💰 <strong>Price:</strong> {variety['price']}
                </div>
                <div class="seed-detail">
                    🛡️ <strong>Resistant to:</strong> {', '.join(variety['resistance'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add new variety button
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("➕ Add New Seed Variety"):
            with st.form("add_variety_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_variety = st.text_input("Variety Name")
                    new_crop = st.selectbox("Crop Type", ["Rice", "Wheat", "Maize", "Cotton", "Vegetables", "Pulses"])
                    new_season = st.selectbox("Season", ["Kharif", "Rabi", "Zaid", "Year-round"])
                    new_duration = st.number_input("Duration (days)", min_value=30, max_value=300, value=120)
                with col2:
                    new_yield = st.number_input("Expected Yield (q/ha)", min_value=10, max_value=100, value=45)
                    new_resistance = st.text_input("Disease Resistance", placeholder="e.g., Blast, BPH")
                    new_water = st.selectbox("Water Requirement", ["Low", "Medium", "High"])
                    new_price = st.text_input("Price", placeholder="e.g., ₹60/kg")
                
                if st.form_submit_button("✅ Add Variety", use_container_width=True):
                    st.success(f"🎉 {new_variety} added successfully to the database!")
    
    # Tab 2: Variety Comparison
    with tab2:
        st.markdown("### ⚖️ Compare Seed Varieties Side-by-Side")
        
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown("**Select varieties to compare:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            variety1 = st.selectbox("🌱 Variety 1", 
                ["IR64", "Pusa Basmati 1121", "BG 380", "Swarna", "DHM 117"], key="v1")
        with col2:
            variety2 = st.selectbox("🌱 Variety 2", 
                ["IR64", "Pusa Basmati 1121", "BG 380", "Swarna", "DHM 117"], index=1, key="v2")
        with col3:
            variety3 = st.selectbox("🌱 Variety 3 (Optional)", 
                ["None", "IR64", "Pusa Basmati 1121", "BG 380", "Swarna", "DHM 117"], key="v3")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔍 Compare Now", use_container_width=True):
            st.markdown('<div class="comparison-container">', unsafe_allow_html=True)
            
            comparison_data = {
                "📋 Parameter": ["Crop Type", "Season", "Duration", "Yield", "Disease Resistance", 
                               "Water Need", "Soil Type", "Price", "Market Demand"],
                f"🌱 {variety1}": ["Rice", "Kharif", "120 days", "45 q/ha", "Blast, BPH", 
                                   "Medium", "Clay loam", "₹60/kg", "High"],
                f"🌱 {variety2}": ["Rice", "Kharif", "140 days", "42 q/ha", "Bacterial Blight", 
                                   "High", "Loamy", "₹120/kg", "Very High"],
            }
            
            if variety3 != "None":
                comparison_data[f"🌱 {variety3}"] = ["Rice", "Kharif", "135 days", "48 q/ha", "Blast", 
                                                      "Medium", "All types", "₹75/kg", "High"]
            
            comp_df = pd.DataFrame(comparison_data)
            st.dataframe(comp_df, use_container_width=True, hide_index=True)
            
            # Visualization
            st.markdown("#### 📊 Visual Comparison")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Yield Difference", "6 q/ha", delta="14% higher")
            with col2:
                st.metric("Price Difference", "₹60", delta="100% premium")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recommendations
            st.info("""
            💡 **Smart Recommendations**:
            - **IR64**: Best for areas with medium water availability and blast-prone regions
            - **Pusa Basmati 1121**: Premium quality, higher market price, needs more water
            - Consider local disease prevalence and irrigation facilities before selecting
            """)
    
    # Tab 3: Disease-Resistant Seeds
    with tab3:
        st.markdown("### 🛡️ Disease-Resistant Seed Varieties")
        
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        disease_filter = st.selectbox("🔍 Filter by Disease Resistance", 
            ["All Diseases", "Blast", "Bacterial Blight", "Brown Plant Hopper (BPH)", 
             "Rust", "Borer", "Leaf Blight"], key="disease_filter")
        st.markdown('</div>', unsafe_allow_html=True)
        
        disease_varieties = [
            {"name": "IR64", "crop": "Rice", "resistant": ["Blast", "BPH"], "level": "High", 
             "yield_impact": "No loss", "description": "Excellent resistance to blast and BPH"},
            {"name": "BG 380", "crop": "Rice", "resistant": ["Blast"], "level": "Moderate", 
             "yield_impact": "Minimal", "description": "Good blast resistance with stable yield"},
            {"name": "Swarna", "crop": "Rice", "resistant": ["BPH"], "level": "High", 
             "yield_impact": "No loss", "description": "Superior BPH tolerance"},
            {"name": "Arjun", "crop": "Wheat", "resistant": ["Rust"], "level": "High", 
             "yield_impact": "No loss", "description": "Highly resistant to all rust types"},
            {"name": "HD 3086", "crop": "Wheat", "resistant": ["Rust"], "level": "Moderate", 
             "yield_impact": "Minimal", "description": "Good rust resistance for most regions"},
        ]
        
        for variety in disease_varieties:
            # Filter logic
            show_variety = disease_filter == "All Diseases" or any(disease_filter in r for r in variety["resistant"])
            if not show_variety:
                continue
            
            resistance_badges = ''.join([f'<span class="badge badge-success">{r}</span>' for r in variety["resistant"]])
            level_color = "success" if variety["level"] == "High" else "warning"
            
            st.markdown(f"""
            <div class="seed-card">
                <div class="seed-title">🛡️ {variety['name']} - {variety['crop']}</div>
                <div class="seed-detail">
                    <strong>Resistant to:</strong> {resistance_badges}
                </div>
                <div class="seed-detail">
                    🎯 <strong>Resistance Level:</strong> <span class="badge badge-{level_color}">{variety['level']}</span>
                    📊 <strong>Yield Impact:</strong> {variety['yield_impact']}
                </div>
                <div class="seed-detail">
                    📝 {variety['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Disease Information
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📖 Learn About Common Crop Diseases"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **🔴 Blast Disease (Rice)**
                - Fungal disease causing lesions
                - *Prevention*: Resistant varieties, water management
                - *Symptoms*: Diamond-shaped lesions on leaves
                
                **🟡 Bacterial Blight (Rice)**
                - Bacterial infection
                - *Prevention*: Avoid excessive nitrogen
                - *Symptoms*: Water-soaked lesions
                """)
            with col2:
                st.markdown("""
                **🟠 Brown Plant Hopper (Rice)**
                - Insect pest causing hopper burn
                - *Prevention*: BPH-resistant varieties
                - *Symptoms*: Yellowing and drying of plants
                
                **🟤 Rust (Wheat)**
                - Fungal disease with rust-colored pustules
                - *Prevention*: Timely sowing, resistant varieties
                - *Symptoms*: Orange-brown pustules on leaves
                """)
    
    # Tab 4: Certified Suppliers
    with tab4:
        st.markdown("### ✅ Certified Seed Suppliers")
        
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            state_filter = st.selectbox("📍 Filter by State", 
                ["All States", "West Bengal", "Punjab", "Haryana", "Uttar Pradesh", "Maharashtra", "Karnataka"])
        with col2:
            crop_supplier = st.selectbox("🌾 Filter by Crop Specialty", 
                ["All Crops", "Rice", "Wheat", "Maize", "Vegetables", "Multi-crop"])
        st.markdown('</div>', unsafe_allow_html=True)
        
        suppliers = [
            {"name": "National Seeds Corporation", "location": "Pan India", "cert": "ICAR Certified",
             "specialty": "Multi-crop", "contact": "1800-123-4567", "rating": 5},
            {"name": "State Seed Corporation (WB)", "location": "Kolkata, West Bengal", "cert": "State Certified",
             "specialty": "Rice, Jute", "contact": "033-2234-5678", "rating": 4},
            {"name": "Punjab Agro Industries", "location": "Ludhiana, Punjab", "cert": "ISO Certified",
             "specialty": "Wheat, Rice", "contact": "0161-234-5678", "rating": 5},
            {"name": "Bayer CropScience", "location": "Pan India", "cert": "ICAR Certified",
             "specialty": "Multi-crop", "contact": "1800-222-3333", "rating": 5},
            {"name": "Syngenta India", "location": "Pan India", "cert": "ICAR Certified",
             "specialty": "Multi-crop", "contact": "1800-419-2244", "rating": 5},
            {"name": "Kaveri Seeds", "location": "Secunderabad, Telangana", "cert": "ICAR Certified",
             "specialty": "Cotton, Maize", "contact": "040-2345-6789", "rating": 4},
        ]
        
        for supplier in suppliers:
            # Filter logic
            show_supplier = (state_filter == "All States" or state_filter in supplier["location"]) and \
                           (crop_supplier == "All Crops" or crop_supplier in supplier["specialty"])
            if not show_supplier:
                continue
            
            stars = "⭐" * supplier["rating"]
            
            st.markdown(f"""
            <div class="supplier-card">
                <h3>🏢 {supplier['name']}</h3>
                <div style="margin: 0.8rem 0;">
                    <div>📍 <strong>Location:</strong> {supplier['location']}</div>
                    <div>✅ <strong>Certification:</strong> {supplier['cert']}</div>
                    <div>🌾 <strong>Specialty:</strong> {supplier['specialty']}</div>
                    <div>📞 <strong>Contact:</strong> {supplier['contact']}</div>
                    <div><strong>Rating:</strong> {stars}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Tips Section
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("""
        💡 **Tips for Buying Quality Seeds**:
        - ✅ Always check for certification labels and holograms
        - 📅 Verify seed lot number and date of packing
        - 🏪 Purchase from authorized dealers only
        - 🌱 Check germination rate (should be >80% for most crops)
        - 🌡️ Store seeds in cool, dry place (below 25°C)
        - 📦 Inspect packaging for any damage or tampering
        """)
        
        # Supplier Registration
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("➕ Register as a Certified Supplier"):
            with st.form("supplier_registration"):
                st.markdown("### 📝 Supplier Registration Form")
                col1, col2 = st.columns(2)
                with col1:
                    supp_name = st.text_input("Company Name *")
                    supp_location = st.text_input("Location *")
                    supp_cert = st.text_input("Certification Details *")
                with col2:
                    supp_crop = st.multiselect("Crop Specialties *", 
                        ["Rice", "Wheat", "Maize", "Cotton", "Vegetables", "Pulses", "Oilseeds"])
                    supp_contact = st.text_input("Contact Number *")
                    supp_email = st.text_input("Email Address *")
                
                if st.form_submit_button("🚀 Submit Registration", use_container_width=True):
                    st.success("✅ Registration submitted successfully! Our team will verify your details and contact you within 48 hours.")

# Render when used as a Streamlit multipage script
show()
