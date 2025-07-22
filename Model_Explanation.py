import streamlit as st
import base64

st.set_page_config(
    page_title="Model Explanation",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.warning(f"Image not found at {image_path}. Please ensure all image files are in the correct directory.")
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
h1, h3, h4, h5, h6, li
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

.content-container {{
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}}

.section-title {{
    font-weight: bold;
    color: #FFD700;
    font-size: 1.3em;
    margin-top: 20px;
    margin-bottom: 10px;
}}

.section-text {{
    color: white;
    font-size: 1em;
    line-height: 1.5;
    margin-bottom: 15px;
}}

.stImage > img {{
    border-radius: 8px;
    border: 2px solid #FFD700;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    margin-top: 20px;
    margin-bottom: 20px;
}}

.stButton>button {{
    background-color: #FFD700;
    color: black !important;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
    font-size: 1.1em;
    font-weight: bold;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transition: all 0.2s ease-in-out;
}}
.stButton>button:hover {{
    background-color: #FFC000;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
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
"""

if img_b64:
    css_and_html_injection_method(page_bg_img)
else:
    st.warning("Background image 'background.jpg' not found. App will use default dark background.")
    fallback_css = """
    <style>
    .stApp {{ background-color: #2F3645; }}
    body, p, .stMarkdown, .stText, .stButton > button, label, h1, h3, h4, h5, h6, li {{ color: white !important; }}
    h2 {{ color: white !important; font-weight: bold !important; text-shadow: 1px 1px 4px rgba(0,0,0,0.7); }}
    label[data-testid*="stWidgetLabel"] p {{ color: #FFD700 !important; font-weight: bold !important; font-size: 1.1em !important; }}
    .content-container {{ background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 20px; margin-top: 20px; border: 1px solid rgba(255, 255, 255, 0.3); }}
    .section-title {{ font-weight: bold; color: #FFD700; font-size: 1.3em; margin-top: 20px; margin-bottom: 10px; }}
    .section-text {{ color: white; font-size: 1em; line-height: 1.5; margin-bottom: 15px; }}
    .stImage > img {{ border-radius: 8px; border: 2px solid #FFD700; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); margin-top: 20px; margin-bottom: 20px; }}
    .stButton>button {{ background-color: #FFD700; color: black !important; }}
    .stButton>button:hover {{ background-color: #FFC000; }}
    .footer {{ position: relative; width: 100%; background-color: rgba(0,0,0,0.5); color: white; text-align: center; padding: 15px 0; margin-top: 50px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .social-icons {{ margin-top: 10px; display: flex; gap: 15px; }}
    .social-icon-link {{ display: inline-flex; align-items: center; justify-content: center; width: 35px; height: 35px; border-radius: 50%; background-color: #FFD700; text-decoration: none; }}
    .social-icon-link svg {{ fill: black; width: 20px; height: 20px; }}
    </style>
    """
    css_and_html_injection_method(fallback_css)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🧠 Our Model: Behind the Scenes 🧠</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Discover the journey of building our Salary Prediction Model, step by step.</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown('<div class="content-container">', unsafe_allow_html=True)
st.markdown('<h3 class="section-title">1. Data Collection & Initial Preprocessing</h3>', unsafe_allow_html=True)
st.markdown("""
    <p class="section-text">
        Our journey began with loading and preparing the Adult dataset. This crucial first step involved several processes:
        <ul>
            <li>Handling potential parsing errors during data loading.</li>
            <li>Explicitly converting numerical columns to ensure correct data types.</li>
            <li>Identifying and managing missing values, which are common in real-world datasets.</li>
            <li>Dropping the 'education' column as its numerical representation ('educational-num') was already present and more suitable for direct modeling.</li>
            <li>Finally, we split the data into training and testing sets, carefully preserving the original features to ensure consistency with our subsequent preprocessing pipeline.</li>
        </ul>
    </p>
""", unsafe_allow_html=True)

st.image("employee salary presentation slide 2.png", caption="Count of Missing Values per Column", use_column_width=True)

st.markdown('<h3 class="section-title">2. Data Preprocessing Pipeline</h3>', unsafe_allow_html=True)
st.markdown("""
    <p class="section-text">
        To maintain consistency and automate data transformations, we defined a robust preprocessing pipeline using Scikit-learn's <code>ColumnTransformer</code>. This pipeline automatically handles the one-hot encoding of our categorical features, converting them into a numerical format that machine learning models can understand. This automation is vital for consistent preprocessing when making predictions on new, unseen data, ensuring that the exact same transformations are applied as during training.
    </p>
""", unsafe_allow_html=True)

st.markdown('<h3 class="section-title">3. Initial Model Training & Evaluation</h3>', unsafe_allow_html=True)
st.markdown("""
    <p class="section-text">
        With our data prepared, we proceeded to train and evaluate several initial machine learning models. Each model was integrated within our preprocessing pipeline to ensure fair comparison and proper data handling. This step helped us gauge the baseline performance of different algorithms on our dataset.
    </p>
""", unsafe_allow_html=True)
st.image("employee salary presentation slide 3.png", caption="Initial Model F1-score Comparison", use_column_width=True)

st.markdown('<h3 class="section-title">4. Hyperparameter Tuning</h3>', unsafe_allow_html=True)
st.markdown("""
    <p class="section-text">
        To significantly improve model performance, we embarked on hyperparameter tuning. We focused on the Random Forest and Gradient Boosting models, utilizing techniques like <code>GridSearchCV</code> and <code>RandomizedSearchCV</code>. This process systematically explores different combinations of hyperparameters to find the optimal settings that yield the best performance metrics, preventing overfitting and enhancing generalization.
    </p>
""", unsafe_allow_html=True)

st.markdown('<h3 class="section-title">5. Ensemble Model & Final Evaluation</h3>', unsafe_allow_html=True)
st.markdown("""
    <p class="section-text">
        Our final step in model selection involved building and evaluating an Ensemble Model. This powerful approach combines the predictions of our best-tuned Random Forest and Gradient Boosting pipelines using a <code>Voting Classifier</code>. Ensembling often leads to more robust and accurate predictions by leveraging the strengths of individual models and mitigating their weaknesses.
    </p>
    <p class="section-text">
        Based on our comprehensive evaluation, particularly focusing on the F1-score (which balances Precision and Recall), the <b>Ensemble Model</b> demonstrated the best overall performance on the unseen test set. While our target accuracy was 90%, the Ensemble Model achieved approximately <b>87.69% Accuracy</b>, proving to be a strong predictive capability for income based on the available features.
    </p>
    <p class="section-text">
        Here are the key metrics for our best-performing Ensemble Model:
        <ul>
            <li><b>Accuracy:</b> 0.8769</li>
            <li><b>Precision:</b> 0.7777</li>
            <li><b>Recall:</b> 0.6646</li>
            <li><b>F1-score:</b> 0.7167</li>
        </ul>
    </p>
""", unsafe_allow_html=True)
st.image("employee salary presentation slide 6,7.png", caption="Comparison of Model Performance Metrics", use_column_width=True)
st.image("employee salary presentation slide 4.png", caption="Comparison of Model Performance (F1-score)", use_column_width=True)

st.markdown('<h3 class="section-title">6. Feature Importance</h3>', unsafe_allow_html=True)
st.markdown("""
    <p class="section-text">
        Understanding which features contribute most to the model's predictions is crucial. We analyzed the feature importances from our tuned Gradient Boosting model to identify the most influential attributes in predicting income. This insight helps in interpreting the model and can guide future data collection or feature engineering efforts.
    </p>
""", unsafe_allow_html=True)
st.image("employee salary presentation slide 5.png", caption="Top 20 Feature Importances from Tuned Gradient Boosting Model", use_column_width=True)

st.markdown('<h3 class="section-title">7. Model Deployment & Output Mechanism</h3>', unsafe_allow_html=True)
st.markdown("""
    <p class="section-text">
        For seamless deployment and usability, we saved the entire <b>Ensemble Model Pipeline</b> using Python's <code>pickle</code> module to <code>best_model_pipeline.pkl</code>. This pickled object encapsulates all the preprocessing steps and the trained model.
    </p>
    <p class="section-text">
        When a user enters new data into the predictor interface, the following happens:
        <ol>
            <li>The new input features are received.</li>
            <li>These raw features are passed directly into the loaded <code>best_model_pipeline.pkl</code>.</li>
            <li>The pipeline automatically applies all the necessary preprocessing steps (like one-hot encoding for categorical features) that were learned during training.</li>
            <li>Finally, the preprocessed data is fed into the trained Ensemble Model within the pipeline, which then makes a prediction: either <b>'>50K'</b> (indicating an annual income greater than 50,000 USD) or <b>'<=50K'</b> (indicating an annual income less than or equal to 50,000 USD).</li>
        </ol>
        This ensures that new data is transformed and predicted upon in exactly the same way as the training data, leading to consistent and reliable predictions.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col_back1, col_back2, col_back3 = st.columns([1,2,1])
with col_back2:
    if st.button("⬅️ Back to Predictor"):
        st.switch_page("app.py")

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
