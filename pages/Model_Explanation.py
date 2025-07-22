import streamlit as st
import base64
import os

PARENT_DIR = os.path.dirname(os.path.dirname(__file__))
CSS_PATH = os.path.join(PARENT_DIR, "style.css")
JS_PATH = os.path.join(PARENT_DIR, "script.js")
IMG_PATH = os.path.join(PARENT_DIR, "background.jpeg")

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
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

st.set_page_config(
    page_title="How Model Works",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

img_b64 = get_base64_image(IMG_PATH)
css_content = load_css(CSS_PATH)
js_content = load_js(JS_PATH)

if img_b64:
    page_bg_img_and_scripts = f"""
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
        st.html(page_bg_img_and_scripts)
    else:
        st.markdown(page_bg_img_and_scripts, unsafe_allow_html=True)
else:
    st.warning("Background image not loaded for this page. Using default styling.")
    fallback_css_and_scripts = f"""
    <style>
    .stApp {{
        background-color: white;
    }}
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

st.markdown("<h1 style='text-align: center; color: #111111;'>🧠 How the Model Works 🧠</h1>", unsafe_allow_html=True)
st.markdown("<p class='explanation-text'>A step-by-step guide to our salary prediction model.</p>", unsafe_allow_html=True)

st.markdown("---")

st.subheader("1. Data Collection and Preprocessing")
st.write("""
    The first step involved collecting and preparing the raw data. This included:
    * Handling potential parsing errors and explicitly converting data types.
    * Addressing missing values.
    * Dropping irrelevant columns, such as 'education', as we used 'educational-num' instead.
    
    A preprocessing pipeline with a `ColumnTransformer` was then defined to automatically handle the one-hot encoding of categorical features. This ensures consistency for both training and future predictions.
""")
try:
    st.image(os.path.join(PARENT_DIR, "employee salary presentation slide 2.png"), caption="Initial Data Distribution", use_column_width=True)
    st.image(os.path.join(PARENT_DIR, "employee salary presentation slide 3.png"), caption="Categorical Feature Breakdown", use_column_width=True)
except Exception as e:
    st.error(f"Error loading initial data images: {e}. Please ensure the files are in the correct directory.")

st.markdown("---")

st.subheader("2. Model Training and Evaluation")
st.write("""
    We trained and evaluated several initial machine learning models. To further improve their performance, we performed hyperparameter tuning on the **Random Forest** and **Gradient Boosting** models using advanced search techniques (`GridSearchCV` and `RandomizedSearchCV`).
""")
try:
    st.image(os.path.join(PARENT_DIR, "employee salary presentation slide 4.png"), caption="Initial Model Performance Comparison", use_column_width=True)
except Exception as e:
    st.error(f"Error loading model performance image: {e}. Please ensure the file is in the correct directory.")

st.markdown("---")

st.subheader("3. The Final Ensemble Model")
st.write("""
    To achieve the best possible performance, we built an **Ensemble Model**. This model combines the best-tuned versions of our Random Forest and Gradient Boosting pipelines using a `Voting Classifier`. This approach leverages the strengths of both models to make a more robust prediction.

    Based on the evaluation, this Ensemble Model demonstrated the best overall performance, with strong metrics particularly in F1-score.
""")
try:
    st.image(os.path.join(PARENT_DIR, "employee salary presentation slide 5.png"), caption="Ensemble Model Performance Metrics", use_column_width=True)
    st.image(os.path.join(PARENT_DIR, "employee salary presentation slide 6,7.png"), caption="Feature Importance and Confusion Matrix", use_column_width=True)
except Exception as e:
    st.error(f"Error loading Ensemble Model images: {e}. Please ensure the files are in the correct directory.")

st.markdown("---")

st.subheader("4. Deployment")
st.write("""
    For deployment, we saved the entire **Ensemble Model Pipeline** as a single pickle file (`best_model_pipeline.pkl`). This allows the application to load the entire pipeline, including all preprocessing steps, ensuring that new data is handled identically to the training data for consistent and reliable predictions.
""")

st.markdown("---")

st.markdown(
    """
    <div style="text-align: center; margin-top: 30px;">
        <a href="/" target="_self" class="explanation-button">
            Go Back to Predictor
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

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
