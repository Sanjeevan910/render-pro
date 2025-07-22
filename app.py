import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import base64
import time

st.set_page_config(
    page_title="Advanced Salary Predictor",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

try:
    with open('best_model_pipeline2.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error("Model file 'best_model_pipeline2.pkl' not found. Please ensure it's in the correct directory.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

img_path = "background.jpg"
img_b64 = get_base64_image(img_path)

css_and_html_injection_method = st.html if hasattr(st, 'html') else st.markdown

page_bg_img = f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{img_b64}") ;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
.stApp::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: -1;
}}

body, p, .stMarkdown, .stText, .stButton > button, label,
h1, h3, h4, h5, h6
{{
    color: white !important;
}}

h2 {{
    color: white !important;
    font-weight: bold !important;
    text-shadow: 1px 1px 4px rgba(0,0,0,0.7);
}}

label[data-testid*="stWidgetLabel"] p {{
    color: #FFD700 !important;
    font-weight: bold !important;
    font-size: 1.1em !important;
}}

.stSelectbox div[data-baseweb="select"] {{
    background-color: rgba(255, 255, 255, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.6);
    color: white !important;
}}
.stSelectbox div[data-baseweb="popover"] {{
    background-color: #333 !important;
    border: 1px solid #555 !important;
}}
.stSelectbox div[data-baseweb="popover"] div[role="option"] {{
    color: white !important;
}}
.stSelectbox div[data-baseweb="popover"] div[role="option"]:hover {{
    background-color: #555 !important;
}}

/* Current selected value on slider (thumb value) */
.stSlider div[data-testid="stThumbValue"] {{
    color: black !important;
    background-color: #FFD700 !important;
    border-radius: 5px;
    padding: 2px 5px;
    font-weight: bold !important;
}}

/* Attempt to target min/max values on the slider track */
/* This is a very aggressive selector. If it still doesn't work,
   it means Streamlit's internal rendering is heavily overriding it. */
div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(2),
div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(3)
{{
    background-color: white !important; /* White background */
    color: black !important; /* Dark black text */
    font-weight: bolder !important; /* Make them bolder */
    font-size: 1.1em !important; /* Slightly larger font size */
    padding: 2px 5px !important; /* Add padding */
    border-radius: 3px !important; /* Slightly rounded corners */
    text-shadow: none !important; /* Remove text shadow */
    width: auto !important; /* Adjust width to content */
    display: inline-block !important; /* Ensure box wraps content */
    box-sizing: border-box !important; /* Include padding in width calculation */
}}

div[data-testid*="stSlider"] div[role="slider"] > div:first-child,
.stSlider .st-bd,
.stSlider .st-be,
.stSlider .st-bf,
.stSlider .st-bg,
.stSlider .st-bh {{
    background-color: rgba(255, 255, 255, 0.5) !important;
}}
.stSlider .st-bo {{
    background-color: #FFD700 !important;
    border: 2px solid white !important;
}}

div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"] {{
    background-color: white !important;
    border: 1px solid #FFD700 !important;
    color: black !important;
    font-weight: bolder !important;
    font-size: 1.3em !important;
    text-shadow: none !important;
}}
div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]::placeholder {{
    color: black !important;
    opacity: 0.7 !important;
}}
.stNumberInput div[data-baseweb="button"] {{
    background-color: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.4);
}}
.stNumberInput div[data-baseweb="button"] svg {{
    fill: white !important;
}}

.stButton>button {{
    background-color: #FFD700;
    color: black !important;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
    font-size: 1.2em;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease-in-out;
}}
.stButton>button:hover {{
    background-color: #FFC000;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}}

#threejs-canvas {{
    background-color: rgba(0,0,0,0.4);
    border-radius: 10px;
    margin-top: 20px;
    display: block;
    width: 100%;
    height: 300px;
}}

.explanation-button-container {{
    position: fixed;
    top: 100px;
    right: 20px;
    z-index: 1000;
}}

.explanation-button {{
    display: inline-block;
    background-color: #FFD700;
    color: black !important;
    border-radius: 8px;
    border: none;
    padding: 10px 15px;
    font-size: 0.9em;
    font-weight: bold;
    text-decoration: none;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease-in-out;
    cursor: pointer;
    margin-left: 10px;
}}

.explanation-button:hover {{
    background-color: #FFC000;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}}

.explanation-text {{
    text-align: center;
    color: #ADD8E6;
    font-size: 18px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
}}

.footer {{
    position: relative;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: rgba(0,0,0,0.5);
    color: white;
    text-align: center;
    padding: 15px 0;
    font-size: 12px;
    margin-top: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.social-icons {{
    margin-top: 10px;
    display: flex;
    gap: 15px;
}}

.social-icon-link {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    background-color: #FFD700;
    text-decoration: none;
    transition: all 0.2s ease-in-out;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}}

.social-icon-link:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}}

.social-icon-svg {{
    fill: black;
    width: 20px;
    height: 20px;
}}
</style>

<script>
    function applyNumberInputStylesForcefully() {{
        const numberInputs = document.querySelectorAll('div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]');
        numberInputs.forEach(input => {{
            input.style.setProperty('color', 'black', 'important');
            input.style.setProperty('background-color', 'white', 'important');
            input.style.setProperty('font-weight', 'bolder', 'important');
            input.style.setProperty('font-size', '1.3em', 'important');
            input.style.setProperty('text-shadow', 'none', 'important');
            input.style.setProperty('border', '1px solid #FFD700', 'important');
        }});

        const styleSheet = document.createElement('style');
        styleSheet.type = 'text/css';
        styleSheet.innerText = `
            div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]::placeholder {{
                color: black !important;
                opacity: 0.7 !important;
            }}
        `;
        document.head.appendChild(styleSheet);
    }}

    function applySliderMinMaxStylesForcefully() {{
        // Attempt to find and style the min/max numbers for sliders
        // These selectors are based on common Streamlit DOM structures, but can be brittle.
        const sliderLabels = document.querySelectorAll(
            'div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(2), ' +
            'div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(3)'
        );

        sliderLabels.forEach(label => {{
            label.style.setProperty('background-color', 'white', 'important');
            label.style.setProperty('color', 'black', 'important');
            label.style.setProperty('font-weight', 'bolder', 'important');
            label.style.setProperty('font-size', '1.1em', 'important');
            label.style.setProperty('padding', '2px 5px', 'important');
            label.style.setProperty('border-radius', '3px', 'important');
            label.style.setProperty('text-shadow', 'none', 'important');
            label.style.setProperty('width', 'auto', 'important');
            label.style.setProperty('display', 'inline-block', 'important');
            label.style.setProperty('box-sizing', 'border-box', 'important');
        }});
    }}

    // Use a MutationObserver to apply styles when DOM changes (e.g., after Streamlit renders widgets)
    const observer = new MutationObserver((mutationsList, observer) => {{
        if (document.querySelector('div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]')) {{
            applyNumberInputStylesForcefully();
        }}
        // Check for slider elements to apply styles
        if (document.querySelector('div[data-testid^="stSlider"]')) {{
            applySliderMinMaxStylesForcefully();
        }}
        // Disconnect if all target elements are found and styled
        if (document.querySelector('div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]') &&
            document.querySelector('div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(2)')) {{
            observer.disconnect();
        }}
    }});

    // Start observing the body for changes
    observer.observe(document.body, {{ childList: true, subtree: true }});

    // Also try to apply styles on DOMContentLoaded for initial render
    document.addEventListener('DOMContentLoaded', () => {{
        applyNumberInputStylesForcefully();
        applySliderMinMaxStylesForcefully();
    }});
</script>
"""

if img_b64:
    css_and_html_injection_method(page_bg_img)
else:
    st.warning("Background image 'background.jpg' not found. App will use default dark background.")
    # Fallback CSS for when background image is not found.
    # Ensure this also includes the robust slider min/max styling.
    fallback_css = """
    <style>
    .stApp {{ background-color: #2F3645; }}
    body, p, .stMarkdown, .stText, .stButton > button, label, h1, h3, h4, h5, h6 {{ color: white !important; }}
    h2 {{ color: white !important; font-weight: bold !important; text-shadow: 1px 1px 4px rgba(0,0,0,0.7); }}
    label[data-testid*="stWidgetLabel"] p {{ color: #FFD700 !important; font-weight: bold !important; font-size: 1.1em !important; }}
    .stSelectbox div[data-baseweb="select"] {{ background-color: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.6); color: white !important; }}
    .stSlider div[data-testid="stThumbValue"] {{ color: black !important; background-color: #FFD700 !important; font-weight: bold !important; }}

    /* Min/Max values on the slider track in fallback */
    div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(2),
    div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(3)
    {{
        background-color: white !important;
        color: black !important;
        font-weight: bolder !important;
        font-size: 1.1em !important;
        padding: 2px 5px !important;
        border-radius: 3px !important;
        text-shadow: none !important;
        width: auto !important;
        display: inline-block !important;
        box-sizing: border-box !important;
    }}
    div[data-testid*="stSlider"] div[role="slider"] > div:first-child,
    .stSlider .st-bd,
    .stSlider .st-be,
    .stSlider .st-bf,
    .stSlider .st-bg,
    .stSlider .st-bh {{
        background-color: rgba(255, 255, 255, 0.5) !important;
    }}
    .stSlider .st-bo {{ background-color: #FFD700 !important; border: 2px solid white !important; }}
    div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"] {{ background-color: white !important; border: 1px solid #FFD700 !important; color: black !important; font-weight: bolder !important; font-size: 1.3em !important; text-shadow: none !important; }}
    div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]::placeholder {{ color: black !important; opacity: 0.7 !important; }}
    .stButton>button {{ background-color: #FFD700; color: black !important; }}
    .stButton>button:hover {{ background-color: #FFC000; }}
    #threejs-canvas {{ background-color: rgba(0,0,0,0.4); border-radius: 10px; margin-top: 20px; display: block; width: 100%; height: 300px; }}
    .explanation-button-container {{ position: fixed; top: 100px; right: 20px; z-index: 1000; }}
    .explanation-button {{ background-color: #FFD700; color: black !important; }}
    .explanation-button:hover {{ background-color: #FFC000; }}
    .explanation-text {{ text-align: center; color: #ADD8E6; font-size: 18px; text-shadow: 1px 1px 3px rgba(0,0,0,0.6); }}
    .footer {{ position: relative; width: 100%; background-color: rgba(0,0,0,0.5); color: white; text-align: center; padding: 15px 0; margin-top: 50px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .social-icons {{ margin-top: 10px; display: flex; gap: 15px; }}
    .social-icon-link {{ display: inline-flex; align-items: center; justify-content: center; width: 35px; height: 35px; border-radius: 50%; background-color: #FFD700; text-decoration: none; }}
    .social-icon-link svg {{ fill: black; width: 20px; height: 20px; }}
    </style>
    <script>
        function applyNumberInputStylesFallback() {{
            const numberInputs = document.querySelectorAll('div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]');
            numberInputs.forEach(input => {{
                input.style.setProperty('color', 'black', 'important');
                input.style.setProperty('background-color', 'white', 'important');
                input.style.setProperty('font-weight', 'bolder', 'important');
                input.style.setProperty('font-size', '1.3em', 'important');
                input.style.setProperty('text-shadow', 'none', 'important');
                input.style.setProperty('border', '1px solid #FFD700', 'important');
            }});
            const styleSheet = document.createElement('style');
            styleSheet.type = 'text/css';
            styleSheet.innerText = `
                div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]::placeholder {{
                    color: black !important;
                    opacity: 0.7 !important;
                }}
            `;
            document.head.appendChild(styleSheet);
        }}
        function applySliderMinMaxStylesFallback() {{
            const sliderLabels = document.querySelectorAll(
                'div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(2), ' +
                'div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(3)'
            );
            sliderLabels.forEach(label => {{
                label.style.setProperty('background-color', 'white', 'important');
                label.style.setProperty('color', 'black', 'important');
                label.style.setProperty('font-weight', 'bolder', 'important');
                label.style.setProperty('font-size', '1.1em', 'important');
                label.style.setProperty('padding', '2px 5px', 'important');
                label.style.setProperty('border-radius', '3px', 'important');
                label.style.setProperty('text-shadow', 'none', 'important');
                label.style.setProperty('width', 'auto', 'important');
                label.style.setProperty('display', 'inline-block', 'important');
                label.style.setProperty('box-sizing', 'border-box', 'important');
            }});
        }}
        document.addEventListener('DOMContentLoaded', () => {{
            applyNumberInputStylesFallback();
            applySliderMinMaxStylesFallback();
        }});
        const observerFallback = new MutationObserver((mutationsList, observer) => {{
            if (document.querySelector('div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]')) {{
                applyNumberInputStylesFallback();
            }}
            if (document.querySelector('div[data-testid^="stSlider"]')) {{
                applySliderMinMaxStylesFallback();
            }}
            if (document.querySelector('div[data-testid="stNumberInput"] input[data-testid="stNumberInput-input"]') &&
                document.querySelector('div[data-testid^="stSlider"] div[data-baseweb="slider"] > div > div > div > div:nth-child(2)')) {{
                observer.disconnect();
            }}
        }});
        observerFallback.observe(document.body, {{ childList: true, subtree: true }});
    </script>
"""
    css_and_html_injection_method(fallback_css)


st.markdown("<h1 style='text-align: center; color: #FFD700;'>💰 Salary Predictor Model 💰</h1>", unsafe_allow_html=True)
st.markdown("<p class='explanation-text'>Enter some details and get a potential salary bracket prediction.</p>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="explanation-button-container">
        <a href="/Attribute_Explanation" target="_self" class="explanation-button">
            Explain Attributes 📚
        </a>
        <a href="/Model_Explanation" target="_self" class="explanation-button" style="margin-top: 10px;">
            How Model Works 🧠
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.subheader("📊 Personal & Work Information")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age (17-75)", min_value=17, max_value=75, step=1, value=30)
    educational_num = st.slider("Educational Years (1-16)", min_value=1, max_value=16, step=1, value=10)
    workclass = st.selectbox(
        "Workclass",
        options=["Private", "Self-emp-not-inc", "Local-gov", "NotListed", "State-gov", "Self-emp-inc", "Federal-gov", "Without-pay", "Never-worked"],
        index=0
    )
    occupation = st.selectbox(
        "Occupation",
        options=[
            "Prof-specialty", "Craft-repair", "Exec-managerial", "Adm-clerical", "Sales",
            "Other-service", "Machine-op-inspct", "others", "Transport-moving", "Handlers-cleaners",
            "Farming-fishing", "Tech-support", "Protective-serv", "Priv-house-serv", "Armed-Forces"
        ],
        index=0
    )
    gender = st.selectbox("Gender", options=["Male", "Female"], index=0)
    marital_status = st.selectbox(
        "Marital Status",
        options=["Married-civ-spouse", "Never-married", "Divorced", "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"],
        index=0
    )

with col2:
    relationship = st.selectbox(
        "Relationship",
        options=["Husband", "Not-in-family", "Own-child", "Unmarried", "Wife", "Other-relative"],
        index=0
    )
    race = st.selectbox(
        "Race",
        options=["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"],
        index=0
    )
    native_country = st.selectbox(
        "Native Country",
        options=[
            "United-States", "Mexico", "others", "Philippines", "Germany", "Puerto-Rico", "Canada",
            "El-Salvador", "India", "Cuba", "England", "China", "South", "Jamaica", "Italy",
            "Dominican-Republic", "Japan", "Guatemala", "Poland", "Vietnam", "Columbia", "Haiti",
            "Portugal", "Taiwan", "Iran", "Greece", "Nicaragua", "Peru", "Ecuador", "France",
            "Ireland", "Hong", "Thailand", "Cambodia", "Trinadad&Tobago", "Laos", "Yugoslavia",
            "Outlying-US(Guam-USVI-etc)", "Scotland", "Honduras", "Hungary", "Holand-Netherlands"
        ],
        index=0
    )
    hours_per_week = st.slider("Hours per Week(1-99)", min_value=1, max_value=99, step=1, value=40)
    capital_gain = st.number_input("Capital Gain", step=1, value=0, format="%d", min_value=0)
    capital_loss = st.number_input("Capital Loss", step=1, value=0, format="%d", min_value=0)
    fnlwgt = st.number_input("Fnlwgt (Final Weight)", step=1, value=200000, format="%d", min_value=0)


st.markdown("---")

col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
with col_btn2:
    if st.button("💰 Predict Salary 💰"):
        with st.spinner('Predicting your salary... 🚀'):
            time.sleep(1.5)
            features = pd.DataFrame({
                'age': [age],
                'workclass': [workclass],
                'fnlwgt': [fnlwgt],
                'educational-num': [educational_num],
                'marital-status': [marital_status],
                'occupation': [occupation],
                'relationship': [relationship],
                'race': [race],
                'gender': [gender],
                'capital-gain': [capital_gain],
                'capital-loss': [capital_loss],
                'hours-per-week': [hours_per_week],
                'native-country': [native_country],
            })

            try:
                prediction = model.predict(features)[0]
                salary_label = ">50K" if prediction == 1 else "<=50K"

                st.markdown("<br>", unsafe_allow_html=True)
                if salary_label == ">50K":
                    st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>🎉 Predicted Salary: {salary_label}</h2>", unsafe_allow_html=True)
                    st.balloons()
                    st.snow()
                else:
                    st.markdown(f"<h2 style='text-align: center; color: #FF6347;'>📉 Predicted Salary: {salary_label}</h2>", unsafe_allow_html=True)
                st.info("Disclaimer: This is a model prediction and should not be taken as financial advice.")

            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")
                st.warning("Please ensure all input values are valid and the model is correctly loaded.")

st.markdown("---")

st.subheader("✨ Explore a 3D Element ✨")

three_d_col1, three_d_col2, three_d_col3 = st.columns([1,3,1])

with three_d_col2:
    st.markdown("<p style='text-align: center; color: white;'>You can interact with this 3D cube below (drag to rotate, scroll to zoom)!</p>", unsafe_allow_html=True)
    three_d_element_html = """
    <canvas id="threejs-canvas" style="width: 100%; height: 300px; display: block;"></canvas>
    <script type="module">
        import * as THREE from 'https://unpkg.com/three@0.128.0/build/three.module.js';
        import { OrbitControls } from 'https://unpkg.com/three@0.128.0/examples/jsm/controls/OrbitControls.js';

        const canvas = document.getElementById('threejs-canvas');
        if (!canvas) {{
            console.error("Canvas element not found!");
        }} else {{
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({{ canvas: canvas, antialias: true, alpha: true }});
            renderer.setSize(canvas.clientWidth, canvas.clientHeight);

            const resizeObserver = new ResizeObserver(entries => {{
                for (let entry of entries) {{
                    if (entry.target === canvas) {{
                        const width = entry.contentRect.width;
                        const height = entry.contentRect.height;
                        camera.aspect = width / height;
                        camera.updateProjectionMatrix();
                        renderer.setSize(width, height);
                    }}
                }}
            }});
            resizeObserver.observe(canvas);

            const geometry = new THREE.BoxGeometry(1, 1, 1);
            const material = new THREE.MeshLambertMaterial({{ color: 0xFFD700 }});
            const cube = new THREE.Mesh(geometry, material);
            scene.add(cube);

            const ambientLight = new THREE.AmbientLight(0x404040, 2);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
            directionalLight.position.set(1, 1, 1).normalize();
            scene.add(directionalLight);

            camera.position.z = 2;

            const controls = new OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.screenSpacePanning = false;
            controls.minDistance = 1;
            controls.maxDistance = 5;

            function animate() {{
                requestAnimationFrame(animate);

                cube.rotation.x += 0.005;
                cube.rotation.y += 0.005;

                controls.update();

                renderer.render(scene, camera);
            }}
            animate();
        }}
    </script>
    """
    css_and_html_injection_method(three_d_element_html)

st.markdown(f"""
<div class="footer">
    <p>Developed by Sanjeevan Negi | Powered by Edunet and IBM</p>
    <div class="social-icons">
        <a href="https://github.com/Sanjeevan910" target="_blank" class="social-icon-link">
            <svg class="social-icon-svg" viewBox="0 0 24 24">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.087-.731.084-.716.084-.716 1.205.082 1.839 1.235 1.839 1.235 1.07 1.835 2.809 1.305 3.492.998.108-.776.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.602.802.573 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
        </a>
        <a href="https://www.linkedin.com/in/sanjeevan-negi-5b7a09270" target="_blank" class="social-icon-link">
            <svg class="social-icon-svg" viewBox="0 0 24 24">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
        </a>
        <a href="https://www.instagram.com/sanjeevannegz" target="_blank" class="social-icon-link">
            <svg class="social-icon-svg" viewBox="0 0 24 24">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.664 1.407 4.887 4.634.062 1.305.07 1.64.07 4.85v.003c0 3.21.008 3.545-.062 4.85-.148 3.227-1.559 4.486-4.887 4.634-1.266.058-1.64.07-4.85.07s-3.585-.012-4.85-.07c-3.252-.148-4.664-1.407-4.887-4.634-.062-1.305-.07-1.64-.07-4.85v-.003c0-3.21-.008-3.545.062-4.85.148-3.227 1.559-4.486 4.887-4.634 1.266-.058 1.64-.07 4.85-.07zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.995 6.995-.058 1.281-.072 1.689-.072 4.947 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.995 6.995 1.28.058 1.689.072 4.947.072s3.668-.014 4.948-.072c4.354-.2 6.782-2.618 6.995-6.995.058-1.28.072-1.689.072-4.948 0-3.259-.014-3.667-.072-4.947-.2-4.358-2.618-6.78-6.995-6.995-1.281-.058-1.689-.072-4.947-.072zM12 7.038c-2.748 0-4.962 2.214-4.962 4.962s2.214 4.962 4.962 4.962 4.962-2.214 4.962-4.962c0-2.748-2.214-4.962-4.962-4.962zm0 8.162c-1.764 0-3.2-1.436-3.2-3.2s1.436-3.2 3.2-3.2 3.2 1.436 3.2 3.2-1.436 3.2-3.2 3.2zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.44-.645 1.44-1.44s-.645-1.44-1.44-1.44z"/>
            </svg>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
