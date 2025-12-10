import os
import pickle
from pathlib import Path

import streamlit as st
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(
    page_title="Health Assistant",
    layout="wide",
    page_icon="🧑‍⚕️",
)

# Get working directory of this file
working_dir = Path(__file__).resolve().parent

# Helper to load a model safely
@st.cache_resource
def load_model(path: Path):
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        st.error(f"Model file not found: {path}")
        return None
    except Exception as e:
        st.error(f"Error loading model from {path} -> {e}")
        return None

# Load models
diabetes_model_path = working_dir / "saved_models" / "diabetes_model.sav"
heart_model_path = working_dir / "saved_models" / "heart_disease_model.sav"
parkinsons_model_path = working_dir / "saved_models" / "parkinsons_model.sav"

diabetes_model = load_model(diabetes_model_path)
heart_disease_model = load_model(heart_model_path)
parkinsons_model = load_model(parkinsons_model_path)

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        "Multiple Disease Prediction System",
        ["Diabetes Prediction", "Heart Disease Prediction", "Parkinsons Prediction"],
        menu_icon="hospital-fill",
        icons=["activity", "heart", "person"],
        default_index=0,
    )

# Utility: validate and convert to float
def to_float_list(values, field_names):
    """
    values: list of strings from text_input
    field_names: list of field labels for error messages
    """
    converted = []
    for v, name in zip(values, field_names):
        if v is None or v.strip() == "":
            st.error(f"Please enter a value for '{name}'.")
            return None
        try:
            converted.append(float(v))
        except ValueError:
            st.error(f"'{name}' must be a numeric value. Got: {v}")
            return None
    return converted

# Diabetes Prediction Page
if selected == "Diabetes Prediction":

    st.title("Diabetes Prediction using ML")

    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input("Number of Pregnancies")
    with col2:
        Glucose = st.text_input("Glucose Level")
    with col3:
        BloodPressure = st.text_input("Blood Pressure value")

    with col1:
        SkinThickness = st.text_input("Skin Thickness value")
    with col2:
        Insulin = st.text_input("Insulin Level")
    with col3:
        BMI = st.text_input("BMI value")

    with col1:
        DiabetesPedigreeFunction = st.text_input("Diabetes Pedigree Function value")
    with col2:
        Age = st.text_input("Age of the Person")

    diab_diagnosis = ""

    if st.button("Diabetes Test Result"):
        if diabetes_model is None:
            st.error("Diabetes model is not loaded.")
        else:
            fields = [
                "Number of Pregnancies",
                "Glucose Level",
                "Blood Pressure value",
                "Skin Thickness value",
                "Insulin Level",
                "BMI value",
                "Diabetes Pedigree Function value",
                "Age of the Person",
            ]
            raw_values = [
                Pregnancies, Glucose, BloodPressure, SkinThickness,
                Insulin, BMI, DiabetesPedigreeFunction, Age,
            ]
            user_input = to_float_list(raw_values, fields)

            if user_input is not None:
                diab_prediction = diabetes_model.predict([user_input])
                if diab_prediction[0] == 1:
                    diab_diagnosis = "The person is diabetic"
                else:
                    diab_diagnosis = "The person is not diabetic"

    if diab_diagnosis:
        st.success(diab_diagnosis)

# Heart Disease Prediction Page
if selected == "Heart Disease Prediction":

    st.title("Heart Disease Prediction using ML")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input("Age")
    with col2:
        sex = st.text_input("Sex")
    with col3:
        cp = st.text_input("Chest Pain types")

    with col1:
        trestbps = st.text_input("Resting Blood Pressure")
    with col2:
        chol = st.text_input("Serum Cholesterol in mg/dl")
    with col3:
        fbs = st.text_input("Fasting Blood Sugar > 120 mg/dl (1 = yes, 0 = no)")

    with col1:
        restecg = st.text_input("Resting Electrocardiographic results")
    with col2:
        thalach = st.text_input("Maximum Heart Rate achieved")
    with col3:
        exang = st.text_input("Exercise Induced Angina (1 = yes, 0 = no)")

    with col1:
        oldpeak = st.text_input("ST depression induced by exercise")
    with col2:
        slope = st.text_input("Slope of the peak exercise ST segment")
    with col3:
        ca = st.text_input("Major vessels colored by flourosopy")

    with col1:
        thal = st.text_input("thal: 0 = normal; 1 = fixed defect; 2 = reversable defect")

    heart_diagnosis = ""

    if st.button("Heart Disease Test Result"):
        if heart_disease_model is None:
            st.error("Heart disease model is not loaded.")
        else:
            fields = [
                "Age", "Sex", "Chest Pain types", "Resting Blood Pressure",
                "Serum Cholesterol", "Fasting Blood Sugar",
                "Resting ECG", "Maximum Heart Rate achieved",
                "Exercise Induced Angina", "ST depression induced by exercise",
                "Slope of ST segment", "Number of major vessels", "Thal",
            ]
            raw_values = [
                age, sex, cp, trestbps, chol, fbs, restecg,
                thalach, exang, oldpeak, slope, ca, thal,
            ]
            user_input = to_float_list(raw_values, fields)

            if user_input is not None:
                heart_prediction = heart_disease_model.predict([user_input])
                if heart_prediction[0] == 1:
                    heart_diagnosis = "The person is having heart disease"
                else:
                    heart_diagnosis = "The person does not have any heart disease"

    if heart_diagnosis:
        st.success(heart_diagnosis)

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":

    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input("MDVP:Fo(Hz)")
    with col2:
        fhi = st.text_input("MDVP:Fhi(Hz)")
    with col3:
        flo = st.text_input("MDVP:Flo(Hz)")
    with col4:
        Jitter_percent = st.text_input("MDVP:Jitter(%)")
    with col5:
        Jitter_Abs = st.text_input("MDVP:Jitter(Abs)")

    with col1:
        RAP = st.text_input("MDVP:RAP")
    with col2:
        PPQ = st.text_input("MDVP:PPQ")
    with col3:
        DDP = st.text_input("Jitter:DDP")
    with col4:
        Shimmer = st.text_input("MDVP:Shimmer")
    with col5:
        Shimmer_dB = st.text_input("MDVP:Shimmer(dB)")

    with col1:
        APQ3 = st.text_input("Shimmer:APQ3")
    with col2:
        APQ5 = st.text_input("Shimmer:APQ5")
    with col3:
        APQ = st.text_input("MDVP:APQ")
    with col4:
        DDA = st.text_input("Shimmer:DDA")
    with col5:
        NHR = st.text_input("NHR")

    with col1:
        HNR = st.text_input("HNR")
    with col2:
        RPDE = st.text_input("RPDE")
    with col3:
        DFA = st.text_input("DFA")
    with col4:
        spread1 = st.text_input("spread1")
    with col5:
        spread2 = st.text_input("spread2")

    with col1:
        D2 = st.text_input("D2")
    with col2:
        PPE = st.text_input("PPE")

    parkinsons_diagnosis = ""

    if st.button("Parkinson's Test Result"):
        if parkinsons_model is None:
            st.error("Parkinson's model is not loaded.")
        else:
            fields = [
                "MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)",
                "MDVP:Jitter(Abs)", "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP",
                "MDVP:Shimmer", "MDVP:Shimmer(dB)", "Shimmer:APQ3",
                "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR",
                "RPDE", "DFA", "spread1", "spread2", "D2", "PPE",
            ]

            raw_values = [
                fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP,
                Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR,
                RPDE, DFA, spread1, spread2, D2, PPE,
            ]

            user_input = to_float_list(raw_values, fields)

            if user_input is not None:
                parkinsons_prediction = parkinsons_model.predict([user_input])
                if parkinsons_prediction[0] == 1:
                    parkinsons_diagnosis = "The person has Parkinson's disease"
                else:
                    parkinsons_diagnosis = "The person does not have Parkinson's disease"

    if parkinsons_diagnosis:
        st.success(parkinsons_diagnosis)
