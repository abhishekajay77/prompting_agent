import streamlit as st
import streamlit.components.v1 as components
import PIL.Image
import os
import json
from dotenv import load_dotenv, set_key
from grok_engine import GrokAgenticEngine

# Page Configuration
st.set_page_config(
    page_title="Monochrome Grok Prompt Engine",
    page_icon="🌑",
    layout="wide"
)

# Custom CSS for Strict Monochrome Aesthetic
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #1A1A1A;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .secondary-text {
        color: #AAAAAA !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3.5em;
        background-color: #FFFFFF;
        color: #000000;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease-in-out;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background-color: #BFBFBF;
        color: #000000;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
    }
    
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #000000;
        color: #FFFFFF;
        border: 1px solid #1A1A1A;
    }
    
    /* Expander */
    div[data-testid="stExpander"] {
        background-color: #000000;
        border: 1px solid #1A1A1A;
        border-radius: 4px;
    }
    
    /* Image Uploader */
    section[data-testid="stFileUploadDropzone"] {
        background-color: #050505;
        border: 1px dashed #333333;
        border-radius: 4px;
    }
    
    /* Agents Visualization */
    .agent-box {
        padding: 15px;
        border-radius: 4px;
        border: 1px solid #1A1A1A;
        margin-bottom: 10px;
        background-color: #050505;
    }
    .agent-active {
        border-color: #FFFFFF;
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.05);
    }
    .agent-done {
        border-color: #333333;
        opacity: 0.6;
    }
    .agent-title {
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.8em;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

def update_env(key, value):
    env_path = ".env"
    set_key(env_path, key, value)
    os.environ[key] = value

def main():
    st.title("🌑 MONOCHROME GROK")
    st.markdown("<p class='secondary-text'>Agentic Prompt Engineering System</p>", unsafe_allow_html=True)
    
    # Sidebar Configuration
    st.sidebar.title("SYSTEM CONTROL")
    
    load_dotenv()
    
    with st.sidebar.expander("API CONFIGURATION", expanded=True):
        groq_key = st.text_input("Groq API Key", value=os.getenv("GROQ_API_KEY", ""), type="password")
        if st.button("SAVE KEY"):
            update_env("GROQ_API_KEY", groq_key)
            st.success("Configuration Saved.")
    
    st.sidebar.markdown("""
    ---
    ### AGENT LOGIC
    1. **VISION**: Analysis via `llama-4-scout`.
    2. **AUDIT**: Risk scoring via `llama-3.3-70b`.
    3. **REFINE**: Iterative loops until risks < 20%.
    """)
    
    # Check for Groq key
    current_key = groq_key or os.getenv("GROQ_API_KEY")

    if not current_key:
         st.warning("Please provide a valid Groq API Key in the sidebar.")
         st.stop()
    
    os.environ["GROQ_API_KEY"] = current_key

    uploaded_file = st.file_uploader("UPLOAD IMAGE FOR ANALYSIS", type=["jpg", "jpeg", "png", "webp", "jfif", "pjpeg", "pjs"])

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("### SOURCE MATERIAL")
            image = PIL.Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            
        with col2:
            st.markdown("### AGENTIC PIPELINE")
            
            # Placeholder for agent status
            status_placeholder = st.empty()
            
            def update_pipeline_ui(msg, agent_id=""):
                with status_placeholder.container():
                    st.markdown(f"""
                    <div class="agent-box {'agent-active' if agent_id else ''}">
                        <div class="agent-title">{agent_id.replace('_', ' ') if agent_id else 'SYSTEM STATUS'}</div>
                        <div style="font-size: 0.9em;">{msg}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if st.button("INITIATE AUTONOMOUS LOOP"):
                try:
                    # Save uploaded file to temp path
                    temp_path = "temp_image." + uploaded_file.name.split('.')[-1]
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Initialize Engine
                    engine = GrokAgenticEngine(api_key=current_key)
                    
                    # Run Loop
                    result = engine.run_engine(temp_path, status_callback=update_pipeline_ui)
                    
                    # Clean up temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    # Display Results
                    st.success("PIPELINE COMPLETE")
                    st.markdown("### FINAL REFINED PROMPT")
                    
                    st.code(result, language="text")
                    
                    # Pro Tips Section as requested by USER
                    st.markdown("""
                    <div style="background-color: #1a1a1a; border: 1px solid #FFFFFF; padding: 15px; border-radius: 5px; margin-top: 20px;">
                        <h3 style="color: #FFFFFF; margin-top: 0;">🚀 PRO TIPS FOR MASTER GENERATION</h3>
                        <ul style="color: #AAAAAA; list-style-type: none; padding-left: 0;">
                            <li>• <b>Aspect Ratio</b>: For cinematic results, use <code>--ar 16:9</code> or <code>--ar 21:9</code>.</li>
                            <li>• <b>Negative Prompting</b>: Explicitly exclude 'blurry, cartoonish, low-res' in your generator settings.</li>
                            <li>• <b>Lighting</b>: If the result is too flat, add 'volumetric god rays' or 'hard rim lighting' to the prompt.</li>
                            <li>• <b>Resolution</b>: Specify 'shot on 35mm film' or '8k octane render' for extreme texture definition.</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.text_area("RAW TEXT (COPY-READY)", value=result, height=250)
                    
                except Exception as e:
                    st.error(f"PIPELINE FAILURE: {e}")

    else:
        st.info("Awaiting visual input...")
        
    st.markdown("---")
    st.markdown("<div style='text-align: center; color: #333; font-size: 0.7em;'>STRICT MONOCHROME DESIGN • POWERED BY XAI GROK</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
