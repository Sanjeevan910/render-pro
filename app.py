import streamlit as st
import pandas as pd
import joblib
import base64
import os

st.set_page_config(
    page_title="Employee Salary Prediction",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

BASE_DIR = os.path.dirname(__file__)
CSS_PATH = os.path.join(BASE_DIR, "style.css")
JS_PATH = os.path.join(BASE_DIR, "script.js")
IMG_PATH = os.path.join(BASE_DIR, "background.jpeg")
MODEL_PATH = os.path.join(BASE_DIR, "best_model_pipeline2.pkl")

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Error: Background image not found at {image_path}. Please ensure 'background.jpeg' is in the same directory as 'app.py'.")
        return None

def load_css(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def load_js(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

img_b64 = get_base64_image(IMG_PATH)
css_content = load_css(CSS_PATH)
js_content = load_js(JS_PATH)

if img_b64:
    page_bg_img_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    {css_content}
    </style>
    <script type="text/javascript">
    {js_content}
    </script>
    """
    if hasattr(st, 'html'):
        st.html(page_bg_img_style)
    else:
        st.markdown(page_bg_img_style, unsafe_allow_html=True)
else:
    st.warning("Background image not loaded. Using default styling.")
    fallback_css_and_scripts = f"""
    <style>
    {css_content}
    </style>
    <script type="text/javascript">
    {js_content}
    </script>
    """
    if hasattr(st, 'html'):
        st.html(fallback_css_and_scripts)
    else:
        st.markdown(fallback_css_and_scripts, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    try:
        pipeline = joblib.load(MODEL_PATH)
        return pipeline
    except FileNotFoundError:
        st.error(f"Error: Model file not found at {MODEL_PATH}. Please ensure 'best_model_pipeline2.pkl' is in the same directory as 'app.py'.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

pipeline = load_model()

if pipeline is None:
    st.stop()

# CHANGE 1: Moved the buttons to the top-right corner
st.markdown(
    """
    <div class="top-right-buttons">
        <a href="/Attribute_Explanation" target="_self" class="nav-button">
            Explain Attributes
        </a>
        <a href="/Model_Explanation" target="_self" class="nav-button">
            How Model Works
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>💰 Employee Salary Predictor 💰</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader-text'>Predicting salary based on various employee attributes.</p>", unsafe_allow_html=True)

st.markdown("---")

st.subheader("Employee Information")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 17, 75, 30)
    education_num = st.slider("Educational Years", 1, 16, 10)
    workclass = st.selectbox("Workclass", [
        "Private", "Self-emp-not-inc", "Local-gov", "State-gov",
        "Self-emp-inc", "Federal-gov", "Without-pay", "Never-worked"
    ])
    occupation = st.selectbox("Occupation", [
        "Prof-specialty", "Craft-repair", "Exec-managerial",
        "Adm-clerical", "Sales", "Other-service", "Machine-op-inspct",
        "Transport-moving", "Handlers-cleaners", "Farming-fishing",
        "Tech-support", "Protective-serv", "Priv-house-serv",
        "Armed-Forces"
    ])
    gender = st.radio("Gender", ["Male", "Female"])

with col2:
    marital_status = st.selectbox("Marital Status", [
        "Married-civ-spouse", "Never-married", "Divorced",
        "Separated", "Widowed", "Married-spouse-absent", "Married-AF-spouse"
    ])
    relationship = st.selectbox("Relationship", [
        "Husband", "Not-in-family", "Own-child", "Unmarried",
        "Wife", "Other-relative"
    ])
    race = st.selectbox("Race", [
        "White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"
    ])
    native_country = st.selectbox("Native Country", [
        "United-States", "Mexico", "Philippines", "Germany", "Canada",
        "Puerto-Rico", "El-Salvador", "India", "Cuba", "England",
        "Jamaica", "South", "China", "Italy", "Dominican-Republic",
        "Vietnam", "Guatemala", "Japan", "Poland", "Columbia",
        "Taiwan", "Haiti", "Iran", "Portugal", "Nicaragua",
        "Peru", "France", "Greece", "Ecuador", "Ireland",
        "Hong", "Cambodia", "Trinadad&Tobago", "Laos", "Thailand",
        "Yugoslavia", "Outlying-US(Guam-USVI-etc)", "Hungary",
        "Honduras", "Scotland", "Holand-Netherlands"
    ])
    hours_per_week = st.slider("Hours per Week", 1, 99, 40)
    capital_gain = st.number_input("Capital Gain", min_value=0, max_value=100000, value=0, step=100)
    capital_loss = st.number_input("Capital Loss", min_value=0, max_value=100000, value=0, step=100)
    fnlwgt = st.number_input("Fnlwgt (Final Weight)", min_value=10000, max_value=1000000, value=150000, step=1000)

# CHANGE 2: Centered the "Predict Salary Range" button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("Predict Salary Range", key="predict_button"):
    input_data = pd.DataFrame([{
        'age': age,
        'workclass': workclass,
        'fnlwgt': fnlwgt,
        'educational-num': education_num,
        'marital-status': marital_status,
        'occupation': occupation,
        'relationship': relationship,
        'race': race,
        'gender': gender,
        'capital-gain': capital_gain,
        'capital-loss': capital_loss,
        'hours-per-week': hours_per_week,
        'native-country': native_country
    }])

    try:
        prediction = pipeline.predict(input_data)[0]

        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #111111;'>Predicted Salary Range</h2>", unsafe_allow_html=True)
        
        if prediction == 0:
            st.markdown("<div style='text-align: center; font-size: 2em; color: #111111; font-weight: bold;'>&#60;=50K</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; font-size: 2em; color: #111111; font-weight: bold;'>&#62;50K</div>", unsafe_allow_html=True)
        
        st.balloons()
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        st.info("Please check your input values and ensure the model is loaded correctly.")

st.markdown("</div>", unsafe_allow_html=True) # Close the centered div

st.markdown("---")

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
