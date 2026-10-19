"""
Van Udyan Plant AI — Web Application (Streamlit Engine)
Matching the visual aesthetics of the uploaded UI template:
- Modern dark-mode palette (#0f172a, #1e293b, #0d1520)
- Neon mint green pill buttons and headers (#9bf6d5 / #00dfa2)
- High-contrast confidence display
- Upload preview & prediction trace card
- Side-by-side taxonomy and field benchmarking tabs
"""

import streamlit as st
import json
from PIL import Image
from pathlib import Path
from app.config import (
    SPECIES_INFO,
    CONFIDENCE_THRESHOLD
)
from app.inference import inference_service

# Page config
st.set_page_config(
    page_title="Van Udyan Plant AI — Species Classifier",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS mimicking the uploaded reference image
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Overall Background */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #17253b 0%, #0c1421 100%);
        color: #e2e8f0;
    }
    
    /* Top Header Bar */
    .top-header-bar {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 16px 24px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* Pill Badges */
    .pill-badge {
        display: inline-block;
        background: #00dfa2;
        color: #0b1320;
        font-weight: 700;
        font-size: 11px;
        letter-spacing: 0.8px;
        padding: 5px 14px;
        border-radius: 20px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .pill-badge-warning {
        background: #f59e0b;
        color: #0b1320;
    }
    
    /* Result Card */
    .result-card {
        background: rgba(18, 28, 45, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 28px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        margin-top: 10px;
    }
    
    /* Confidence Text */
    .confidence-title {
        font-family: 'Outfit', sans-serif;
        font-size: 42px;
        font-weight: 800;
        color: #f7b731;
        line-height: 1.1;
        margin: 10px 0 4px 0;
    }
    
    .species-title {
        font-family: 'Outfit', sans-serif;
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    
    .sub-species-text {
        font-size: 14px;
        color: #94a3b8;
        margin-bottom: 16px;
    }
    
    /* Trace Bar */
    .trace-item {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .warning-box {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 12px;
        padding: 14px;
        margin-top: 14px;
        color: #fbbf24;
        font-size: 13px;
        line-height: 1.4;
    }
    
    /* Metrics tile */
    .metric-tile {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    .metric-number {
        font-size: 24px;
        font-weight: 800;
        color: #00dfa2;
        font-family: 'Outfit', sans-serif;
    }
    .metric-label {
        font-size: 12px;
        color: #94a3b8;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/forest.png", width=64)
    st.markdown("### **Van Udyan Plant AI**")
    st.caption("Urban Plantation Monitoring • RSWF Pune")
    
    nav_option = st.radio(
        "Navigation",
        ["🔍 Species Identifier", "📊 Evaluation & Metrics", "🌿 Supported Species (15)", "ℹ️ Project & Architecture"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("#### **Model Diagnostics**")
    model_status, model_msg = inference_service.load_model()
    if model_status and inference_service.model is not None:
        st.success("🟢 EfficientNetB0 Active")
    else:
        st.info("🟡 Standby Mode (Live Demo Ready)")
        st.caption("Place `best_van_udyan_top15.keras` in the root folder or configure Supabase Storage.")
    
    st.markdown("---")
    st.markdown("""
    **Transparency Notice:**  
    *Predictions are experimental and strictly limited to 15 supported Van Udyan species.*
    """)

# VIEW 1: Species Identifier (The UI Template Layout)
if nav_option == "🔍 Species Identifier":
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <div>
            <h2 style="margin:0; font-family:'Outfit'; font-weight:800; color:#fff;">Plant Species Identification</h2>
            <p style="margin:0; color:#94a3b8; font-size:14px;">Upload an in-situ leaf, bark, or canopy photograph for field diagnosis</p>
        </div>
        <div>
            <span style="background:rgba(0, 223, 162, 0.15); border:1px solid #00dfa2; color:#00dfa2; padding:6px 14px; border-radius:30px; font-size:12px; font-weight:700;">
                VAN UDYAN BENCHMARK READY
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top Drop & Browse Container
    st.markdown("""
    <div style="background:rgba(30,41,59,0.7); border:1px dashed rgba(255,255,255,0.2); border-radius:18px; padding:20px; text-align:center; margin-bottom:24px;">
        <span class="pill-badge">DROP IMAGE OR BROWSE</span>
        <h4 style="margin:8px 0 4px 0; color:#fff;">Upload a plant or tree photo for full prediction trace</h4>
        <p style="margin:0; color:#94a3b8; font-size:12px;">JPG, JPEG, PNG, or WEBP up to 10 MB</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload image",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )

    # Optional sample images selector
    sample_col1, sample_col2 = st.columns([1, 4])
    with sample_col1:
        use_sample = st.checkbox("Or test with a sample field image", value=False)
        
    sample_image_path = None
    if use_sample:
        # Check if local benchmark photos exist
        bench_dir = Path("data/processed_top15/test_van_udyan_benchmark")
        if bench_dir.exists():
            sample_options = list(bench_dir.glob("*/*.*"))[:8]
            if sample_options:
                chosen = st.selectbox(
                    "Choose an authentic Van Udyan field sample:",
                    sample_options,
                    format_func=lambda p: f"{p.parent.name.replace('_', ' ')} ({p.name})"
                )
                sample_image_path = chosen

    active_image = None
    if uploaded_file is not None:
        try:
            active_image = Image.open(uploaded_file)
        except Exception as e:
            st.error(f"Invalid image file: {str(e)}")
    elif sample_image_path is not None:
        active_image = Image.open(sample_image_path)

    if active_image is not None:
        # Perform inference
        result = inference_service.predict(active_image)
        
        # Two-column layout mimicking the user's provided UI reference
        col_res, col_img = st.columns([1.1, 1], gap="large")
        
        with col_res:
            st.markdown(f"""
            <div class="result-card">
                <span class="pill-badge">PREDICTION RESULT</span>
                <div class="species-title">{result['predicted_common_name']}</div>
                <div class="sub-species-text"><em>{result['predicted_scientific_name']}</em> • {result['marathi_name']}</div>
                
                <div class="confidence-title">{result['confidence_pct']}%</div>
                <div style="font-size:13px; color:#94a3b8; margin-bottom:18px;">
                    Confidence score • Architecture: EfficientNetB0
                </div>
            """, unsafe_allow_html=True)

            if result['family']:
                st.markdown(f"**Family:** `{result['family']}`  \n**Ecological Role:** {result['ecological_role']}")

            if result['warning']:
                st.markdown(f"""
                <div class="warning-box">
                    ⚠️ <strong>Notice:</strong> {result['warning']}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br><strong style='color:#cbd5e1; font-size:13px;'>TOP 3 CANDIDATES TRACE</strong>", unsafe_allow_html=True)
            for idx, cand in enumerate(result['top_3_predictions'], 1):
                pct = cand['confidence_pct']
                st.markdown(f"""
                <div class="trace-item">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <span style="font-weight:600; font-size:13px; color:#f8fafc;">#{idx} {cand['common_name']} (<em>{cand['scientific_name']}</em>)</span>
                        <span style="font-weight:700; font-size:13px; color:#00dfa2;">{pct}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(min(pct / 100.0, 1.0))
                
            st.markdown("</div>", unsafe_allow_html=True)

        with col_img:
            st.markdown("""
            <div style="background:rgba(18,28,45,0.85); border:1px solid rgba(255,255,255,0.1); border-radius:24px; padding:20px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
                <span class="pill-badge" style="background:#3b82f6; color:#fff;">CAPTURED IMAGE</span>
            """, unsafe_allow_html=True)
            st.image(active_image, use_container_width=True)
            st.caption(f"Input dimensions: {active_image.size[0]} x {active_image.size[1]} px • Preprocessed to 224x224 RGB")
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.info("👆 Upload an image or select a sample photograph above to view prediction results.")

# VIEW 2: Evaluation & Metrics
elif nav_option == "📊 Evaluation & Metrics":
    st.markdown("<h2 style='font-family:Outfit; font-weight:800;'>Empirical Evaluation & Performance Audit</h2>", unsafe_allow_html=True)
    st.markdown("All reported figures represent **actual, verified experimental outputs** executed on Google Colab GPU.")

    # High-level metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="metric-tile">
            <div class="metric-number">23.78%</div>
            <div class="metric-label">Held-Out Test Top-1 (Top-15)</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="metric-tile">
            <div class="metric-number">26.28%</div>
            <div class="metric-label">Validation Acc (EffNetB0)</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="metric-tile">
            <div class="metric-number">13.33%</div>
            <div class="metric-label">Van Udyan Benchmark Top-1</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
        <div class="metric-tile">
            <div class="metric-number">33.33%</div>
            <div class="metric-label">Van Udyan Benchmark Top-3</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Comparison Table
    st.subheader("Experiment Comparison: 38-Class Baseline vs. Top-15 Model")
    comp_data = {
        "Metric": [
            "Number of Classes",
            "Model Backbone",
            "Training Split (Images)",
            "Validation Split (Images)",
            "Held-Out Test Split (Images)",
            "Held-Out Test Top-1 Accuracy",
            "Held-Out Test Top-3 Accuracy",
            "Independent Field Benchmark Top-1",
            "Independent Field Benchmark Top-3"
        ],
        "Experiment 1 (38-Class Baseline)": [
            "38 species",
            "MobileNetV2",
            "1,050",
            "236",
            "228",
            "10.53%",
            "21.93%",
            "9.29% (on 140 images)",
            "20.00%"
        ],
        "Experiment 2 (Top-15 Focused Model)": [
            "15 species",
            "EfficientNetB0 (Selected)",
            "698 (644 iNat + 54 Field)",
            "137 (122 iNat + 15 Field)",
            "143",
            "23.78%",
            "Not Recorded (Null in saved JSON)",
            "13.33% (on 30 images)",
            "33.33%"
        ]
    }
    st.table(comp_data)

    st.markdown("---")
    st.subheader("Visual Analytics & Experimental Figures")
    fig_col1, fig_col2 = st.columns(2)
    
    with fig_col1:
        comp_img = Path("docs/figures/experimental_accuracy_comparison.png")
        if comp_img.exists():
            st.image(str(comp_img), caption="Comparative Experimental Accuracy")
            
    with fig_col2:
        dist_img = Path("docs/figures/top15_species_distribution.png")
        if dist_img.exists():
            st.image(str(dist_img), caption="Top-15 Dataset Partitioning Distribution")

# VIEW 3: Supported Species
elif nav_option == "🌿 Supported Species (15)":
    st.markdown("<h2 style='font-family:Outfit; font-weight:800;'>15 Supported Van Udyan Species</h2>", unsafe_allow_html=True)
    st.caption("Filtered and verified from Reform Social Welfare Foundation (RSWF) field inventory.")
    
    for sci, info in SPECIES_INFO.items():
        with st.expander(f"🌿 {info['common_name']} — {sci.replace('_', ' ')}"):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"**Scientific Name:**  \n*{sci.replace('_', ' ')}*")
                st.markdown(f"**Marathi Name:**  \n{info['marathi_name']}")
                st.markdown(f"**Family:**  \n`{info['family']}`")
            with c2:
                st.markdown(f"**Ecological Role in Urban Forest:**  \n{info['ecological_role']}")
                st.markdown("""
                - **Field Representation:** Documented in Zone Wise Plants inventory.
                - **Dataset Coverage:** Train + Val + Test + 2 Untouched Benchmark specimens.
                """)

# VIEW 4: Project & Architecture
elif nav_option == "ℹ️ Project & Architecture":
    st.markdown("<h2 style='font-family:Outfit; font-weight:800;'>Project Background & Deep Learning Pipeline</h2>", unsafe_allow_html=True)
    st.markdown("""
    ### Reform Social Welfare Foundation (RSWF) Van Udyan Initiative
    This system assists in continuous urban plantation monitoring at Van Udyan in Pune, Maharashtra.
    Botanical auditing across extensive urban reforestation plots is traditionally manual and prone to observer fatigue.
    
    ### Pipeline Architecture
    """)
    arch_img = Path("docs/figures/pipeline_architecture_diagram.png")
    if arch_img.exists():
        st.image(str(arch_img), caption="End-to-End System Architecture", use_container_width=True)
        
    st.markdown("""
    ### Data Ethics & Integrity Policy
    - **No Fabrication**: Unrecorded evaluation metrics are marked as null.
    - **Zero Data Leakage**: Multi-angle photographs from identical tree specimens are strictly partitioned by `observation_id`.
    - **Independent Benchmark**: 30 authentic field photos (2 per species) remain untouched and evaluated strictly post-training.
    - **Privacy Protection**: Uploaded field images are processed in-memory and never retained without explicit user authorization.
    """)
