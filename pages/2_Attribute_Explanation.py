import streamlit as st
import base64

st.set_page_config(
    page_title="Attribute Explanation",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

.explanation-container {{
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
    border: 1px solid rgba(255, 255, 255, 0.3);
}}

.attribute-item {{
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px dashed rgba(255, 255, 255, 0.2);
}}

.attribute-item:last-child {{
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}}

.attribute-name {{
    font-weight: bold;
    color: #FFD700;
    font-size: 1.1em;
}}

.attribute-description {{
    color: white;
    font-size: 0.95em;
    line-height: 1.4;
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
    body, p, .stMarkdown, .stText, .stButton > button, label, h1, h3, h4, h5, h6 {{ color: white !important; }}
    h2 {{ color: white !important; font-weight: bold !important; text-shadow: 1px 1px 4px rgba(0,0,0,0.7); }}
    label[data-testid*="stWidgetLabel"] p {{ color: #FFD700 !important; font-weight: bold !important; font-size: 1.1em !important; }}
    .explanation-container {{ background-color: rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 20px; margin-top: 20px; border: 1px solid rgba(255, 255, 255, 0.3); }}
    .attribute-item {{ margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px dashed rgba(255, 255, 255, 0.2); }}
    .attribute-item:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
    .attribute-name {{ font-weight: bold; color: #FFD700; font-size: 1.1em; }}
    .attribute-description {{ color: white; font-size: 0.95em; line-height: 1.4; }}
    .stButton>button {{ background-color: #FFD700; color: black !important; }}
    .stButton>button:hover {{ background-color: #FFC000; }}
    .footer {{ position: relative; width: 100%; background-color: rgba(0,0,0,0.5); color: white; text-align: center; padding: 15px 0; margin-top: 50px; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    .social-icons {{ margin-top: 10px; display: flex; gap: 15px; }}
    .social-icon-link {{ display: inline-flex; align-items: center; justify-content: center; width: 35px; height: 35px; border-radius: 50%; background-color: #FFD700; text-decoration: none; }}
    .social-icon-link svg {{ fill: black; width: 20px; height: 20px; }}
    </style>
    """
    css_and_html_injection_method(fallback_css)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>📚 Attribute Explanations 📚</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>Understand the meaning of each input attribute used in the salary prediction model.</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div class="explanation-container">
    <div class="attribute-item">
        <p class="attribute-name">Age:</p>
        <p class="attribute-description">The age of the individual. Generally, experience and career progression correlate with age, which can impact salary.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Workclass:</p>
        <p class="attribute-description">The type of employer or working arrangement. Examples include Private, Self-emp-not-inc (self-employed not incorporated), Local-gov, Federal-gov, etc. This often indicates the stability and pay structure.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Fnlwgt (Final Weight):</p>
        <p class="attribute-description">This is the 'final weight' from the Census data. It represents the number of people the data entry is supposed to represent. While not a direct predictor of individual salary, it's used in demographic studies to give a proportional representation of the population. In this model, it's included as a feature due to its presence in the original dataset and potential subtle correlations.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Educational Years (Educational-num):</p>
        <p class="attribute-description">The number of years of education completed. This is a numerical representation of the education level (e.g., Bachelor's degree might be 13 years, High School grad 9 years). Higher education levels are generally associated with higher earning potential.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Marital Status:</p>
        <p class="attribute-description">The marital status of the individual. Categories include Married-civ-spouse, Never-married, Divorced, Separated, Widowed. This attribute can sometimes correlate with financial stability or household income patterns.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Occupation:</p>
        <p class="attribute-description">The specific type of occupation or job role. Different occupations have vastly different salary ranges. Examples include Prof-specialty (Professional Specialty), Exec-managerial (Executive, Managerial), Craft-repair, etc.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Relationship:</p>
        <p class="attribute-description">The individual's relationship status within a household. This can be Husband, Wife, Own-child, Not-in-family, Unmarried, Other-relative. This attribute often correlates strongly with gender and marital status and can indirectly relate to financial roles within a household.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Race:</p>
        <p class="attribute-description">The racial background of the individual. This is a demographic attribute.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Gender:</p>
        <p class="attribute-description">The sex of the individual (Male or Female). Historically, gender can be a factor in salary prediction, reflecting societal trends and disparities.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Capital Gain:</p>
        <p class="attribute-description">Income from investments or the sale of assets (e.g., stocks, property). This directly contributes to total income.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Capital Loss:</p>
        <p class="attribute-description">Losses from investments or the sale of assets. This reduces total income.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Hours per Week:</p>
        <p class="attribute-description">The number of hours the individual works per week. More hours typically correlate with higher gross pay, though this can vary by occupation and pay structure.</p>
    </div>
    <div class="attribute-item">
        <p class="attribute-name">Native Country:</p>
        <p class="attribute-description">The country of origin of the individual. This is a demographic attribute.</p>
    </div>
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
