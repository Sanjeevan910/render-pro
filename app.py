import streamlit as st
import pickle
import pandas as pd

with open('best_model_pipeline2.pkl', 'rb') as file:
    model = pickle.load(file)

st.title("Salary Predictor Model")
st.write("Enter some details and get the salary prediction")

age = st.slider("Age", min_value=17, max_value=75, step=1, value=17)
educational_num = st.slider("Educational-num", min_value=1, max_value=16, step=1, value=1)
workclass = st.selectbox(
    "workclass",
    options=["Private", "Self-emp-not-inc", "Local-gov", "NotListed", "State-gov", "Self-emp-inc", "Federal-gov"],
    index=0
)
occupation = st.selectbox(
    "occupation",
    options=[
        "Prof-specialty", "Craft-repair", "Exec-managerial", "Adm-clerical", "Sales",
        "Other-service", "Machine-op-inspct", "others", "Transport-moving", "Handlers-cleaners",
        "Farming-fishing", "Tech-support", "Protective-serv"
    ],
    index=0
)
gender = st.selectbox("gender", options=["Male", "Female"], index=0)
marital_status = st.selectbox(
    "marital-status",
    options=["Married-civ-spouse", "Never-married", "Divorced", "Separated", "Widowed", "Married-spouse-absent"],
    index=0
)
relationship = st.selectbox(
    "relationship",
    options=["Husband", "Not-in-family", "Own-child", "Unmarried", "Wife", "Other-relative"],
    index=0
)
race = st.selectbox(
    "race",
    options=["White", "Black", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other"],
    index=0
)
native_country = st.selectbox(
    "native-country",
    options=[
        "United-States", "Mexico", "others", "Philippines", "Germany", "Puerto-Rico", "Canada",
        "El-Salvador", "India", "Cuba", "England", "China", "South", "Jamaica", "Italy",
        "Dominican-Republic", "Japan", "Guatemala", "Poland", "Vietnam", "Columbia", "Haiti",
        "Portugal", "Taiwan", "Iran", "Greece", "Nicaragua", "Peru", "Ecuador", "France",
        "Ireland", "Hong", "Thailand", "Cambodia", "Trinadad&Tobago", "Laos", "Yugoslavia",
        "Outlying-US(Guam-USVI-etc)", "Scotland", "Honduras", "Hungary"
    ],
    index=0
)
hours_per_week = st.slider("hours-per-week", min_value=0, max_value=100, step=1, value=0)
capital_gain = st.number_input("capital-gain", step=1, value=0, format="%d")
capital_loss = st.number_input("capital-loss", step=1, value=0, format="%d")
fnlwgt = st.number_input("Fnlwgt", step=1, value=0, format="%d")

if fnlwgt < 0:
    st.error("Fnlwgt must be 0 or greater.")
    fnlwgt = 0
if capital_gain < 0:
    st.error("Capital gain must be 0 or greater.")
    capital_gain = 0 
if capital_loss < 0:
    st.error("Capital loss must be 0 or greater.")
    capital_loss = 0

if st.button("Salary Predictor Button"):
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
        'native-country': [native_country]
    })
    prediction = model.predict(features)[0]
    salary_label = ">50K" if prediction == 1 else "<=50K"
    st.write(f"Salary Prediction: **{salary_label}**")
