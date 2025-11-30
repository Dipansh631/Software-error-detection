"""
Software Defects Detection System - Streamlit App
An In-Depth Analysis of Machine Learning Methods and Static Analysis Tools
"""

import streamlit as st
import os
import json
import pandas as pd

from utils.static_analysis import analyze_code
from utils.feature_extract import metrics_to_features, load_or_train_model

# Page configuration
st.set_page_config(
    page_title="Software Defects Detection",
    page_icon="🐛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #007BFF 0%, #00C2FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .prediction-card {
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .success-card {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
    }
    .danger-card {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        color: white;
    }
    .metric-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007BFF;
        margin: 0.5rem 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #007BFF 0%, #00C2FF 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model' not in st.session_state:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, 'model', 'defect_model.pkl')
    st.session_state.model, st.session_state.model_name = load_or_train_model(model_path)

# Main header
st.markdown('<h1 class="main-header">🐛 Software Defects Detection System</h1>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #6c757d; margin-bottom: 2rem;'>
    <p style='font-size: 1.2rem;'>An In-Depth Analysis of Machine Learning Methods and Static Analysis Tools</p>
    <p>Upload your source code and get instant predictions using advanced ML models</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 About")
    st.markdown("""
    This system uses advanced Machine Learning algorithms and static analysis techniques 
    to detect potential defects in source code.
    
    **Features:**
    - 🧠 8 ML Models
    - 📊 Static Analysis
    - 🎯 High Accuracy
    - ⚡ Real-time Predictions
    """)
    
    st.header("📝 Supported Formats")
    st.markdown("""
    - Python (.py)
    - Java (.java)
    - JavaScript (.js)
    - C/C++ (.c, .cpp)
    - C# (.cs)
    - Ruby (.rb)
    - Go (.go)
    - TypeScript (.ts)
    """)
    
    st.header("ℹ️ Model Info")
    st.info(f"**Model:** {st.session_state.model_name}")

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload Code File")
    
    uploaded_file = st.file_uploader(
        "Choose a source code file",
        type=['py', 'txt', 'java', 'js', 'cpp', 'c', 'cs', 'rb', 'go', 'ts'],
        help="Upload a source code file for defect detection"
    )
    
    if uploaded_file is not None:
        # Read file content
        try:
            code_text = str(uploaded_file.read(), "utf-8")
        except UnicodeDecodeError:
            code_text = str(uploaded_file.read(), "latin-1", errors="ignore")
        
        st.success(f"✅ File uploaded: **{uploaded_file.name}**")
        
        # Show file preview
        with st.expander("📄 Preview Code"):
            st.code(code_text[:1000] + ("..." if len(code_text) > 1000 else ""), language='python')
        
        # Analyze button
        if st.button("🔍 Analyze Code", use_container_width=True):
            with st.spinner("Analyzing code and running ML prediction..."):
                # 1) Static analysis
                metrics = analyze_code(code_text)
                
                # 2) Features and model
                X = metrics_to_features(metrics)
                model = st.session_state.model
                
                # 3) Predict
                y_pred = model.predict(X)[0]
                is_defective = bool(int(y_pred))
                
                # Get prediction probability if available
                try:
                    y_proba = model.predict_proba(X)[0]
                    confidence = max(y_proba) * 100
                except:
                    confidence = None
                
                # Store results in session state
                st.session_state.result = {
                    'is_defective': is_defective,
                    'metrics': metrics,
                    'confidence': confidence,
                    'filename': uploaded_file.name
                }
                
                st.rerun()

with col2:
    st.header("📊 Analysis Results")
    
    if 'result' in st.session_state and st.session_state.result:
        result = st.session_state.result
        is_defective = result['is_defective']
        metrics = result['metrics']
        confidence = result.get('confidence')
        
        # Prediction Card
        if is_defective:
            st.markdown(f"""
            <div class="prediction-card danger-card">
                <h2 style='color: white; margin: 0;'>⚠️ Defective Code Detected</h2>
                <p style='color: white; opacity: 0.9; margin-top: 0.5rem;'>
                    The ML model has identified potential defects in your code.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="prediction-card success-card">
                <h2 style='color: white; margin: 0;'>✅ Code is Clean</h2>
                <p style='color: white; opacity: 0.9; margin-top: 0.5rem;'>
                    No defects detected. Your code appears to be clean.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Confidence score
        if confidence:
            st.metric("Confidence", f"{confidence:.1f}%")
        
        # Model info
        st.info(f"**Model Used:** {st.session_state.model_name}")
        
        # Static Analysis Metrics
        st.subheader("📈 Static Analysis Metrics")
        
        # Display metrics in columns
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric("Lines of Code (LOC)", int(metrics['loc']))
            st.metric("Number of Comments", int(metrics['num_comments']))
            st.metric("Number of Functions", int(metrics['num_functions']))
        
        with metric_col2:
            st.metric("Cyclomatic Complexity", f"{metrics['cyclomatic_complexity_estimate']:.1f}")
            st.metric("Avg Line Length", f"{metrics['avg_line_length']:.1f}")
            st.metric("TODOs/FIXMEs", int(metrics['num_todos']))
        
        # Detailed metrics JSON
        with st.expander("📋 Detailed Metrics (JSON)"):
            st.json(metrics)
        
        # Visualization
        st.subheader("📊 Metrics Visualization")
        metrics_df = pd.DataFrame([metrics])
        
        # Bar chart
        st.bar_chart(metrics_df[['loc', 'num_comments', 'num_functions', 'cyclomatic_complexity_estimate']])
        
    else:
        st.info("👆 Upload a code file and click 'Analyze Code' to see results here.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; padding: 2rem 0;'>
    <p>Built with <strong>Streamlit</strong> + <strong>scikit-learn</strong></p>
    <p style='font-size: 0.9rem;'>Demo metrics only; not a substitute for full static analysis.</p>
</div>
""", unsafe_allow_html=True)

