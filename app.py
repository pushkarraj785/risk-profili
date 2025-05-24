import streamlit as st
import pandas as pd
import xgboost as xgb
import shap

# 1. Feature mapping for user input to model encoding (as in training)
encoding = {
    "Age": {
        "18–35 years": 0,
        "36–55 years": 1,
        "55 years and above": 2
    },
    "Dependents": {
        "No one": 0,
        "Only spouse": 1,
        "Spouse and children": 2,
        "Only parents": 3,
        "Spouse, children, and parents": 4
    },
    "Annual Income": {
        "Below INR 1 lakh": 0,
        "Between INR 1 lakh and INR 5 lakh": 1,
        "Between INR 5 lakh and INR 10 lakh": 2,
        "Between INR 10 lakh and INR 25 lakh": 3,
        "Above INR 25 lakh": 4
    },
    "EMI % Income": {
        "None": 0,
        "Up to 20%": 1,
        "20–30%": 2,
        "30–40%": 3,
        "50% or above": 4
    },
    "Income Stability": {
        "Very low stability": 0,
        "Low stability": 1,
        "Moderate stability": 2,
        "High stability": 3,
        "Very high stability": 4
    },
    "Portfolio": {
        "Savings and fixed deposits": 0,
        "Bonds or debt": 1,
        "Mutual funds": 2,
        "Real estate or gold": 3,
        "Stock market": 4
    },
    "Investment Objective": {
        "Retirement planning": 0,
        "Monthly income": 1,
        "Tax saving": 2,
        "Capital preservation": 3,
        "Wealth creation": 4
    },
    "Investment Duration": {
        "Less than 1 year": 0,
        "1–3 years": 1,
        "3–5 years": 2,
        "5–10 years": 3,
        "More than 10 years": 4
    },
    "Comfort with High Risk": {
        "Strongly agree": 0,
        "Agree": 1,
        "Neutral": 2,
        "Disagree": 3,
        "Strongly disagree": 4
    },
    "Behavior on 20% Loss": {
        "Sell and preserve cash": 0,
        "Sell and move cash to fixed deposits or liquid fund": 1,
        "Wait till market recovers and then sell": 2,
        "Keep investments as they are": 3,
        "Invest more": 4
    }
}

feature_names = [
    "Age", "Dependents", "Annual Income", "EMI % Income", "Income Stability",
    "Portfolio", "Investment Objective", "Investment Duration",
    "Comfort with High Risk", "Behavior on 20% Loss"
]

# 2. Load trained model
@st.cache_resource
def load_model():
    model = xgb.XGBClassifier()
    model.load_model('model/risk_model.json')
    return model

model = load_model()

st.title("🧠 Risk Profiling Robo-Advisor (Research Paper-based)")
st.write("Answer all the questions below to know your risk profile and understand the key reasons for your score:")

# 3. User-friendly question blocks
q1 = st.selectbox(
    "1. What is your age group?",
    ["18–35 years", "36–55 years", "55 years and above"]
)
q2 = st.selectbox(
    "2. How many people depend on you financially?",
    ["No one", "Only spouse", "Spouse and children", "Only parents", "Spouse, children, and parents"]
)
q3 = st.selectbox(
    "3. What is your annual income range?",
    ["Below INR 1 lakh", "Between INR 1 lakh and INR 5 lakh", "Between INR 5 lakh and INR 10 lakh",
     "Between INR 10 lakh and INR 25 lakh", "Above INR 25 lakh"]
)
q4 = st.selectbox(
    "4. What percentage of your monthly income goes towards EMIs or loans?",
    ["None", "Up to 20%", "20–30%", "30–40%", "50% or above"]
)
q5 = st.selectbox(
    "5. How stable is your income?",
    ["Very low stability", "Low stability", "Moderate stability", "High stability", "Very high stability"]
)
q6 = st.selectbox(
    "6. Where is most of your current investment portfolio parked?",
    ["Savings and fixed deposits", "Bonds or debt", "Mutual funds", "Real estate or gold", "Stock market"]
)
q7 = st.selectbox(
    "7. What is your primary investment objective?",
    ["Retirement planning", "Monthly income", "Tax saving", "Capital preservation", "Wealth creation"]
)
q8 = st.selectbox(
    "8. For how long do you plan to stay invested?",
    ["Less than 1 year", "1–3 years", "3–5 years", "5–10 years", "More than 10 years"]
)
q9 = st.selectbox(
    "9. To achieve high returns, how comfortable are you with high-risk investments?",
    ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]
)
q10 = st.selectbox(
    "10. If you lose 20% of your invested value one month after investment, what will you do?",
    ["Sell and preserve cash", "Sell and move cash to fixed deposits or liquid fund",
     "Wait till market recovers and then sell", "Keep investments as they are", "Invest more"]
)

if st.button("Get My Risk Profile"):
    # 4. Encode user answers
    input_dict = {
        "Age": encoding["Age"][q1],
        "Dependents": encoding["Dependents"][q2],
        "Annual Income": encoding["Annual Income"][q3],
        "EMI % Income": encoding["EMI % Income"][q4],
        "Income Stability": encoding["Income Stability"][q5],
        "Portfolio": encoding["Portfolio"][q6],
        "Investment Objective": encoding["Investment Objective"][q7],
        "Investment Duration": encoding["Investment Duration"][q8],
        "Comfort with High Risk": encoding["Comfort with High Risk"][q9],
        "Behavior on 20% Loss": encoding["Behavior on 20% Loss"][q10]
    }
    input_df = pd.DataFrame([input_dict])

    # 5. Predict
    pred = model.predict(input_df)[0]
    risk_map = {
        0: "No Risk",
        1: "Low Risk",
        2: "Moderate Risk",
        3: "Likes Risk",
        4: "High Risk"
    }
    st.success(f"### Your Risk Profile: {risk_map.get(pred, 'Unknown')}")

    # # 6. Explainability with SHAP
    # st.subheader("Why this result?")
    # explainer = shap.TreeExplainer(model)
    # shap_values = explainer.shap_values(input_df)
    # shap.initjs()
    # st.pyplot(shap.force_plot(
    #     explainer.expected_value, shap_values, input_df, matplotlib=True, show=False
    # ))

    st.info("*Model and explanations are for demonstration and educational purposes only. For professional advice, consult a SEBI-registered advisor.*")
