import pickle
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu

# ==============================
# 1. PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="MediGuard | AI Health Assistant",
    layout="wide",
    page_icon="🩺",
    initial_sidebar_state="expanded"
)

# ==============================
# 2. GLOBAL STYLING (ADVANCED UI)
# ==============================
st.markdown(
    """
    <style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top left, #e0f2ff 0, #f9fafb 35%, #ffffff 100%);
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f3f6fb 40%, #e8f0ff 100%);
        border-right: 1px solid #e0e7ff;
        box-shadow: 4px 0 18px rgba(15, 23, 42, 0.08);
    }

    [data-testid="stSidebar"] .css-1d391kg, /* older versions */
    [data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    /* TOP HERO AREA */
    .hero-card {
        background: linear-gradient(120deg, #2563eb 0%, #38bdf8 40%, #22c55e 100%);
        border-radius: 24px;
        padding: 22px 26px;
        color: white;
        box-shadow: 0 22px 45px rgba(15, 23, 42, 0.35);
        position: relative;
        overflow: hidden;
    }
    .hero-title {
        font-size: 2.0rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        margin-bottom: 0.4rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        opacity: 0.95;
        max-width: 600px;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 0.8rem;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.15);
        font-size: 0.8rem;
    }
    .hero-pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 0.6rem;
        font-size: 0.78rem;
    }
    .hero-pill {
        padding: 4px 10px;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.16);
        border: 1px solid rgba(15, 23, 42, 0.16);
    }
    .hero-fade-circle {
        position: absolute;
        width: 260px;
        height: 260px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(255,255,255,0.35), transparent 60%);
        right: -60px;
        top: -40px;
        filter: blur(1px);
        opacity: 0.9;
    }
    .hero-fade-circle-small {
        position: absolute;
        width: 170px;
        height: 170px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(15,23,42,0.2), transparent 65%);
        right: 60px;
        bottom: -50px;
        opacity: 0.8;
    }

    /* INPUT CARDS */
    .section-card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 18px 18px 8px 18px;
        border: 1px solid rgba(148, 163, 184, 0.35);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
        backdrop-filter: blur(12px);
        margin-top: 18px;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }
    .section-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.10);
        border-color: rgba(59, 130, 246, 0.65);
    }
    .section-header {
        font-size: 0.9rem;
        font-weight: 600;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 0.4rem;
    }
    .section-subtext {
        font-size: 0.78rem;
        color: #6b7280;
        margin-bottom: 0.7rem;
    }

    /* STREAMLIT INPUT TWEAKS */
    label {
        font-size: 0.83rem !important;
        font-weight: 500 !important;
        color: #0f172a !important;
    }

    input[type="number"], input[type="text"] {
        border-radius: 11px !important;
        border: 1px solid #d1d5db !important;
        padding: 7px 10px !important;
        font-size: 0.86rem !important;
    }

    .stSelectbox > div > div {
        border-radius: 11px !important;
        border: 1px solid #d1d5db !important;
        font-size: 0.86rem !important;
    }

    .stSlider > div > div > div {
        color: #2563eb !important;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(120deg, #2563eb, #1d4ed8, #22c55e);
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.6rem 1.6rem;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        width: 100%;
        box-shadow: 0 16px 35px rgba(37, 99, 235, 0.45);
        transition: all 0.18s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-1.5px) scale(1.01);
        box-shadow: 0 20px 50px rgba(37, 99, 235, 0.60);
    }

    /* RESULT CARDS */
    .result-wrapper {
        margin-top: 20px;
    }
    .result-card {
        border-radius: 20px;
        padding: 18px 18px 14px 18px;
        display: flex;
        gap: 14px;
        align-items: flex-start;
        border: 1px solid;
        box-shadow: 0 16px 32px rgba(15,23,42,0.16);
    }
    .result-card.risk {
        background: radial-gradient(circle at top left, #fef2f2, #fee2e2);
        border-color: #f97373;
    }
    .result-card.safe {
        background: radial-gradient(circle at top left, #ecfdf5, #dcfce7);
        border-color: #22c55e;
    }
    .result-icon {
        font-size: 1.65rem;
        margin-top: 4px;
    }
    .result-content-title {
        font-size: 1.0rem;
        font-weight: 600;
        margin-bottom: 2px;
    }
    .result-content-body {
        font-size: 0.86rem;
        color: #4b5563;
    }
    .result-caption {
        font-size: 0.78rem;
        margin-top: 6px;
        color: #6b7280;
    }

    /* SMALL METRIC TAGS */
    .metric-row {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-top: 0.4rem;
        font-size: 0.78rem;
    }
    .metric-pill {
        padding: 3px 10px;
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.14);
        border: 1px solid rgba(148, 163, 184, 0.5);
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    /* DISCLAIMER BOX */
    .disclaimer-box {
        font-size: 0.75rem;
        border-radius: 16px;
        padding: 10px 12px;
        border: 1px dashed rgba(148, 163, 184, 0.7);
        background: rgba(248, 250, 252, 0.9);
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# 3. MODEL LOADING
# ==============================
working_dir = Path(__file__).resolve().parent


@st.cache_resource
def load_model(filename: str):
    path = working_dir / "saved_models" / filename
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return None


diabetes_model = load_model("diabetes_model.sav")
heart_disease_model = load_model("heart_disease_model.sav")
parkinsons_model = load_model("parkinsons_model.sav")

# ==============================
# 4. SIDEBAR NAVIGATION
# ==============================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=80)
    st.markdown("### MediGuard")
    st.caption("AI-Powered Multi-Disease Screening")

    selected = option_menu(
        menu_title=None,
        options=["Diabetes", "Heart Disease", "Parkinson's"],
        icons=["droplet-half", "heart-pulse", "activity"],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "rgba(255,255,255,0)",
            },
            "icon": {"color": "#2563eb", "font-size": "16px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px 0",
                "border-radius": "999px",
                "padding": "6px 14px",
                "border": "1px solid rgba(148,163,184,0.35)",
            },
            "nav-link-selected": {
                "background-color": "#2563eb",
            },
        },
    )

    st.markdown(
        """
        <div class="disclaimer-box">
        <b>Disclaimer</b>: This assistant provides risk estimation based on model patterns only.  
        It is not a substitute for clinical diagnosis, lab tests, or professional medical advice.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================
# 5. RESULT DISPLAY HELPER
# ==============================
def display_result(prediction, positive_class, positive_msg, negative_msg):
    st.markdown("<div class='result-wrapper'>", unsafe_allow_html=True)
    if prediction[0] == positive_class:
        st.markdown(
            f"""
            <div class="result-card risk">
                <div class="result-icon">⚠️</div>
                <div>
                    <div class="result-content-title">{positive_msg}</div>
                    <div class="result-content-body">
                        The model detected a pattern consistent with elevated risk.  
                        Use this result as an early alert and discuss it with a qualified healthcare professional.
                    </div>
                    <div class="result-caption">
                        Recommended: Schedule a consultation, review lifestyle factors, and consider further diagnostic tests.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="result-card safe">
                <div class="result-icon">✅</div>
                <div>
                    <div class="result-content-title">{negative_msg}</div>
                    <div class="result-content-body">
                        Based on the information provided, the model did not detect strong indicators of this condition.
                    </div>
                    <div class="result-caption">
                        This is not a medical clearance. Continue regular check-ups and maintain a healthy lifestyle.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


# ==============================
# 6. PAGE-SPECIFIC UIs
# ==============================

# ---- HEADER (CHANGES BY PAGE) ----
def render_header(title_icon: str, title_text: str, subtitle: str, tags: list[str]):
    c1, c2 = st.columns([2.5, 1.2], gap="large")
    with c1:
        st.markdown(
            f"""
            <div class="hero-card">
                <div class="hero-fade-circle"></div>
                <div class="hero-fade-circle-small"></div>
                <div class="hero-title">{title_icon} {title_text}</div>
                <div class="hero-subtitle">{subtitle}</div>
                <div class="hero-badge">
                    🧠 AI Risk Engine • Real-time Screening
                </div>
                <div class="hero-pill-row">
                    {''.join([f'<span class="hero-pill">{t}</span>' for t in tags])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="section-card" style="margin-top:0;">
                <div class="section-header">
                    🔍 How to use
                </div>
                <div class="section-subtext">
                    • Enter values from recent clinical reports, not guesses. <br>
                    • Fill as many fields as accurately as possible. <br>
                    • Use the result as a risk signal, not a diagnosis.
                </div>
                <div class="metric-row">
                    <div class="metric-pill">⚙️ Model-based scoring</div>
                    <div class="metric-pill">⏱️ Instant feedback</div>
                    <div class="metric-pill">🔒 No login required</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# === DIABETES PAGE ===
if selected == "Diabetes":
    render_header(
        "🩸",
        "Diabetes Risk Assessment",
        "Screen type-2 diabetes risk using routinely collected clinical parameters.",
        ["Fasting glucose", "Blood pressure", "BMI", "Family history proxy"],
    )

    if diabetes_model is None:
        st.warning("Model file not found. Ensure 'diabetes_model.sav' exists in 'saved_models/'.")
    else:
        with st.form("diabetes_form"):
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-header">Patient Profile</div>
                    <div class="section-subtext">
                        Basic demographic and metabolic details.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col1, col2, col3 = st.columns(3)

            with col1:
                Pregnancies = st.number_input(
                    "Pregnancies",
                    min_value=0,
                    max_value=20,
                    step=1,
                    help="Number of times pregnant (0 if not applicable).",
                )
                SkinThickness = st.number_input(
                    "Skin Thickness (mm)",
                    min_value=0,
                    max_value=100,
                    value=20,
                    help="Triceps skinfold thickness.",
                )
                DiabetesPedigreeFunction = st.number_input(
                    "Diabetes Pedigree Function",
                    min_value=0.0,
                    max_value=2.5,
                    value=0.47,
                    format="%.3f",
                    help="Proxy for genetic predisposition based on family history.",
                )

            with col2:
                Glucose = st.number_input(
                    "Glucose Level (mg/dL)",
                    min_value=0,
                    max_value=500,
                    value=100,
                    help="Plasma glucose concentration.",
                )
                Insulin = st.number_input(
                    "Insulin Level (µU/mL)",
                    min_value=0,
                    max_value=900,
                    value=80,
                    help="2-hour serum insulin.",
                )
                Age = st.number_input(
                    "Age (years)",
                    min_value=0,
                    max_value=120,
                    value=30,
                )

            with col3:
                BloodPressure = st.number_input(
                    "Blood Pressure (mm Hg)",
                    min_value=0,
                    max_value=200,
                    value=70,
                )
                BMI = st.number_input(
                    "Body Mass Index (BMI)",
                    min_value=0.0,
                    max_value=70.0,
                    value=25.0,
                    format="%.1f",
                )

            st.markdown("")  # small spacing
            submitted = st.form_submit_button("Run Diabetes Risk Analysis")

            if submitted:
                user_input = [
                    Pregnancies,
                    Glucose,
                    BloodPressure,
                    SkinThickness,
                    Insulin,
                    BMI,
                    DiabetesPedigreeFunction,
                    Age,
                ]
                prediction = diabetes_model.predict([user_input])
                display_result(
                    prediction,
                    positive_class=1,
                    positive_msg="High Risk: Likely Diabetic Pattern Detected",
                    negative_msg="Low Risk: No Strong Diabetic Pattern Detected",
                )

# === HEART DISEASE PAGE ===
if selected == "Heart Disease":
    render_header(
        "❤️",
        "Cardiovascular Risk Evaluation",
        "Estimate the presence of heart disease using classic cardiology parameters.",
        ["Chest pain profile", "Cholesterol", "Stress test", "ECG pattern"],
    )

    if heart_disease_model is None:
        st.warning("Model file not found. Ensure 'heart_disease_model.sav' exists in 'saved_models/'.")
    else:
        with st.form("heart_form"):
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-header">Clinical Profile</div>
                    <div class="section-subtext">
                        Core cardiovascular risk markers and functional test results.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                age = st.number_input("Age (years)", min_value=1, max_value=120, value=50)
                trestbps = st.number_input(
                    "Resting Blood Pressure (mm Hg)",
                    min_value=50,
                    max_value=250,
                    value=120,
                )
                restecg = st.selectbox(
                    "Resting ECG Result",
                    options=[0, 1, 2],
                    format_func=lambda x: ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"][x],
                )
                oldpeak = st.number_input(
                    "ST Depression (Oldpeak)",
                    min_value=0.0,
                    max_value=10.0,
                    value=1.0,
                    step=0.1,
                    help="ST depression induced by exercise relative to rest.",
                )

            with col2:
                sex_opt = st.selectbox("Sex", options=["Male", "Female"])
                sex = 1 if sex_opt == "Male" else 0

                chol = st.number_input(
                    "Serum Cholesterol (mg/dL)",
                    min_value=100,
                    max_value=600,
                    value=200,
                )
                thalach = st.number_input(
                    "Max Heart Rate Achieved (bpm)",
                    min_value=60,
                    max_value=220,
                    value=150,
                )
                slope = st.selectbox(
                    "Slope of Peak Exercise ST Segment",
                    options=[0, 1, 2],
                    format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x],
                )

            with col3:
                cp_opt = st.selectbox(
                    "Chest Pain Type",
                    options=["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"],
                )
                cp_mapping = {
                    "Typical Angina": 0,
                    "Atypical Angina": 1,
                    "Non-anginal Pain": 2,
                    "Asymptomatic": 3,
                }
                cp = cp_mapping[cp_opt]

                fbs_opt = st.selectbox("Fasting Blood Sugar > 120 mg/dL?", options=["No", "Yes"])
                fbs = 1 if fbs_opt == "Yes" else 0

                exang_opt = st.selectbox("Exercise-Induced Angina?", options=["No", "Yes"])
                exang = 1 if exang_opt == "Yes" else 0

                ca = st.slider("Number of Major Vessels (0–3) seen in Fluoroscopy", 0, 3, 0)
                thal = st.selectbox(
                    "Thalassemia (Thal)",
                    options=[0, 1, 2, 3],
                    format_func=lambda x: ["Unknown", "Normal", "Fixed Defect", "Reversible Defect"][x],
                )

            st.markdown("")
            submitted = st.form_submit_button("Run Cardiac Risk Evaluation")

            if submitted:
                user_input = [
                    age,
                    sex,
                    cp,
                    trestbps,
                    chol,
                    fbs,
                    restecg,
                    thalach,
                    exang,
                    oldpeak,
                    slope,
                    ca,
                    thal,
                ]
                prediction = heart_disease_model.predict([user_input])
                display_result(
                    prediction,
                    positive_class=1,
                    positive_msg="Alert: Model Suggests Cardiac Disease Pattern",
                    negative_msg="Reassuring: No Strong Cardiac Disease Pattern Detected",
                )

# === PARKINSON'S PAGE ===
if selected == "Parkinson's":
    render_header(
        "🧠",
        "Parkinson’s Voice-Based Screening",
        "Leverage advanced acoustic biomarkers from sustained phonation recordings.",
        ["Jitter / Shimmer", "HNR", "Non-linear dynamics", "Frequency spread"],
    )

    if parkinsons_model is None:
        st.warning("Model file not found. Ensure 'parkinsons_model.sav' exists in 'saved_models/'.")
    else:
        with st.form("parkinsons_form"):
            # Voice frequency parameters
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-header">Voice Frequency Parameters</div>
                    <div class="section-subtext">
                        Baseline fundamental frequency statistics from sustained phonation.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            c1, c2, c3 = st.columns(3)
            fo = c1.number_input("MDVP:Fo(Hz) – Avg Vocal Fundamental Frequency", value=119.99)
            fhi = c2.number_input("MDVP:Fhi(Hz) – Max Vocal Fundamental Frequency", value=157.30)
            flo = c3.number_input("MDVP:Flo(Hz) – Min Vocal Fundamental Frequency", value=74.99)

            # Jitter metrics
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-header">Jitter Metrics (Cycle-to-cycle Frequency Variation)</div>
                    <div class="section-subtext">
                        Fine-grained frequency instability features derived from the speech signal.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            c1, c2, c3, c4, c5 = st.columns(5)
            jitter_percent = c1.number_input("MDVP:Jitter(%)", value=0.00784, format="%.5f")
            jitter_abs = c2.number_input("MDVP:Jitter(Abs)", value=0.00007, format="%.5f")
            rap = c3.number_input("MDVP:RAP", value=0.00370, format="%.5f")
            ppq = c4.number_input("MDVP:PPQ", value=0.00554, format="%.5f")
            ddp = c5.number_input("Jitter:DDP", value=0.01109, format="%.5f")

            # Shimmer metrics
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-header">Shimmer Metrics (Cycle-to-cycle Amplitude Variation)</div>
                    <div class="section-subtext">
                        Amplitude perturbation features indicating vocal intensity irregularity.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            shimmer = c1.number_input("MDVP:Shimmer", value=0.04374, format="%.5f")
            shimmer_db = c2.number_input("MDVP:Shimmer(dB)", value=0.426, format="%.3f")
            apq3 = c3.number_input("Shimmer:APQ3", value=0.02182, format="%.5f")
            apq5 = c4.number_input("Shimmer:APQ5", value=0.03130, format="%.5f")
            apq = c5.number_input("MDVP:APQ", value=0.02971, format="%.5f")
            dda = c6.number_input("Shimmer:DDA", value=0.06545, format="%.5f")

            # Harmonic & non-linear metrics
            st.markdown(
                """
                <div class="section-card">
                    <div class="section-header">Harmonicity & Non-Linear Dynamics</div>
                    <div class="section-subtext">
                        Markers capturing noise-to-harmonics ratio, fractal scaling, and signal complexity.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            c1, c2, c3, c4 = st.columns(4)
            nhr = c1.number_input("NHR", value=0.02211, format="%.5f")
            hnr = c2.number_input("HNR", value=21.033)
            rpde = c3.number_input("RPDE", value=0.414783, format="%.6f")
            dfa = c4.number_input("DFA", value=0.815285, format="%.6f")

            c5, c6, c7, c8 = st.columns(4)
            spread1 = c5.number_input("spread1", value=-4.813031, format="%.6f")
            spread2 = c6.number_input("spread2", value=0.266482, format="%.6f")
            d2 = c7.number_input("D2", value=2.301442, format="%.6f")
            ppe = c8.number_input("PPE", value=0.284654, format="%.6f")

            st.markdown("")
            submitted = st.form_submit_button("Run Parkinson’s Voice Analysis")

            if submitted:
                user_input = [
                    fo,
                    fhi,
                    flo,
                    jitter_percent,
                    jitter_abs,
                    rap,
                    ppq,
                    ddp,
                    shimmer,
                    shimmer_db,
                    apq3,
                    apq5,
                    apq,
                    dda,
                    nhr,
                    hnr,
                    rpde,
                    dfa,
                    spread1,
                    spread2,
                    d2,
                    ppe,
                ]
                prediction = parkinsons_model.predict([user_input])
                display_result(
                    prediction,
                    positive_class=1,
                    positive_msg="Positive Screen: Parkinson-like Voice Pattern Detected",
                    negative_msg="Negative Screen: No Strong Parkinson-like Voice Pattern Detected",
                )
