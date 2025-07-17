import streamlit as st
import pandas as pd

# Configure page settings
st.set_page_config(
    page_title="Risk Profile Assessment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling with better contrast
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .question-card {
        background: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        color: #111827;
    }
    
    .question-title {
        color: #1f2937;
        font-size: 1.4em;
        font-weight: 600;
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }
    
    .score-card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        color: #111827;
    }
    
    .stRadio > label {
        color: #111827 !important;
        font-weight: 600 !important;
        font-size: 1.1em !important;
    }
    
    .stRadio > div > div > div > label {
        color: #374151 !important;
        font-weight: 500 !important;
        padding: 0.75rem;
        margin: 0.3rem 0;
        border-radius: 6px;
        background-color: #f9fafb;
        border: 1px solid #d1d5db;
    }
    
    .stRadio > div > div > div > label:hover {
        background-color: #e5e7eb;
        border-color: #9ca3af;
    }
    
    .stProgress .st-bo {
        background-color: #1e3a8a;
    }
    
    .assessment-area {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
        color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# Rule-based scoring system (simplified without exposing weights)
risk_scoring_rules = {
    "Age": {
        "weight": 1.0,
        "scores": {
            "18–35 years": 1.0,
            "36–55 years": 0.5,
            "55 years and above": 0.2
        }
    },
    "Dependents": {
        "weight": 0.83,
        "scores": {
            "No one": 1.0,
            "Only spouse": 0.8,
            "Spouse and children": 0.6,
            "Only parents": 0.6,
            "Spouse, children, and parents": 0.1
        }
    },
    "Annual Income": {
        "weight": 0.83,
        "scores": {
            "Below INR 1 lakh": 0.2,
            "Between INR 1 lakh and INR 5 lakh": 0.4,
            "Between INR 5 lakh and INR 10 lakh": 0.6,
            "Between INR 10 lakh and INR 25 lakh": 0.8,
            "Above INR 25 lakh": 1.0
        }
    },
    "EMI % Income": {
        "weight": 0.65,
        "scores": {
            "None": 1.0,
            "Up to 20%": 0.8,
            "20–30%": 0.6,
            "30–40%": 0.4,
            "50% or above": 0.2
        }
    },
    "Income Stability": {
        "weight": 0.65,
        "scores": {
            "Very low stability": 0.1,
            "Low stability": 0.3,
            "Moderate stability": 0.6,
            "High stability": 1.0,
            "Very high stability": 1.0
        }
    },
    "Portfolio": {
        "weight": 0.5,
        "scores": {
            "Savings and fixed deposits": 0.4,
            "Bonds or debt": 0.6,
            "Mutual funds": 0.5,
            "Real estate or gold": 0.4,
            "Stock market": 0.8
        }
    },
    "Investment Objective": {
        "weight": 0.8,
        "scores": {
            "Retirement planning": 0.65,
            "Monthly income": 0.6,
            "Tax saving": 0.4,
            "Capital preservation": 0.5,
            "Wealth creation": 1.0
        }
    },
    "Investment Duration": {
        "weight": 0.8,
        "scores": {
            "Less than 1 year": 0.5,
            "1–3 years": 0.8,
            "3–5 years": 0.65,
            "5–10 years": 0.6,
            "More than 10 years": 0.7
        }
    },
    "Comfort with High Risk": {
        "weight": 0.7,
        "scores": {
            "Strongly agree": 1.0,
            "Agree": 0.9,
            "Neutral": 0.5,
            "Disagree": 0.2,
            "Strongly disagree": 0.1
        }
    },
    "Behavior on 20% Loss": {
        "weight": 0.65,
        "scores": {
            "Sell and preserve cash": 0.2,
            "Sell and move cash to fixed deposits or liquid fund": 0.3,
            "Wait till market recovers and then sell": 0.5,
            "Keep investments as they are": 0.8,
            "Invest more": 1.0
        }
    }
}

# Question templates (simplified without emojis in main content)
questions = [
    {
        "key": "Age",
        "title": "What is your age group?",
        "options": ["18–35 years", "36–55 years", "55 years and above"]
    },
    {
        "key": "Dependents",
        "title": "How many people depend on you financially?",
        "options": ["No one", "Only spouse", "Spouse and children", "Only parents", "Spouse, children, and parents"]
    },
    {
        "key": "Annual Income",
        "title": "What is your annual income range?",
        "options": ["Below INR 1 lakh", "Between INR 1 lakh and INR 5 lakh", "Between INR 5 lakh and INR 10 lakh",
                   "Between INR 10 lakh and INR 25 lakh", "Above INR 25 lakh"]
    },
    {
        "key": "EMI % Income",
        "title": "What percentage of your monthly income goes towards EMIs or loans?",
        "options": ["None", "Up to 20%", "20–30%", "30–40%", "50% or above"]
    },
    {
        "key": "Income Stability",
        "title": "How stable is your income?",
        "options": ["Very low stability", "Low stability", "Moderate stability", "High stability", "Very high stability"]
    },
    {
        "key": "Portfolio",
        "title": "Where is most of your current investment portfolio parked?",
        "options": ["Savings and fixed deposits", "Bonds or debt", "Mutual funds", "Real estate or gold", "Stock market"]
    },
    {
        "key": "Investment Objective",
        "title": "What is your primary investment objective?",
        "options": ["Retirement planning", "Monthly income", "Tax saving", "Capital preservation", "Wealth creation"]
    },
    {
        "key": "Investment Duration",
        "title": "For how long do you plan to stay invested?",
        "options": ["Less than 1 year", "1–3 years", "3–5 years", "5–10 years", "More than 10 years"]
    },
    {
        "key": "Comfort with High Risk",
        "title": "To achieve high returns, how comfortable are you with high-risk investments?",
        "options": ["Strongly agree", "Agree", "Neutral", "Disagree", "Strongly disagree"]
    },
    {
        "key": "Behavior on 20% Loss",
        "title": "If you lose 20% of your invested value one month after investment, what will you do?",
        "options": ["Sell and preserve cash", "Sell and move cash to fixed deposits or liquid fund",
                   "Wait till market recovers and then sell", "Keep investments as they are", "Invest more"]
    }
]

# Calculate total possible maximum score for normalization
max_possible_score = sum(rule["weight"] for rule in risk_scoring_rules.values())

def calculate_risk_score(answers):
    """Calculate weighted risk score based on user answers"""
    total_score = 0
    detailed_scores = {}
    
    for question, answer in answers.items():
        if question in risk_scoring_rules:
            rule = risk_scoring_rules[question]
            weight = rule["weight"]
            answer_score = rule["scores"].get(answer, 0)
            weighted_score = weight * answer_score
            total_score += weighted_score
            
            detailed_scores[question] = {
                "answer": answer,
                "base_score": answer_score,
                "weighted_score": weighted_score
            }
    
    # Normalize to 1-100 scale
    normalized_score = (total_score / max_possible_score) * 100
    
    return normalized_score, detailed_scores

def get_risk_category(score):
    """Categorize risk based on normalized score"""
    if score < 30:
        return "Conservative", "Low risk tolerance, prefers capital preservation", "#10b981"
    elif score < 45:
        return "Moderate Conservative", "Below average risk tolerance, prefers stable returns", "#f59e0b"
    elif score < 60:
        return "Balanced", "Moderate risk tolerance, balanced approach", "#3b82f6"
    elif score < 75:
        return "Moderate Aggressive", "Above average risk tolerance, growth-oriented", "#f97316"
    else:
        return "Aggressive", "High risk tolerance, seeks maximum growth potential", "#ef4444"

def initialize_session_state():
    """Initialize session state variables"""
    if 'stage' not in st.session_state:
        st.session_state.stage = 'welcome'
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

def show_welcome_page():
    """Display welcome page with introduction"""
    st.markdown("""
    <div class="main-header">
        <h1>Risk Profile Assessment</h1>
        <h3>Professional Investment Risk Evaluation</h3>
        <p>Complete a comprehensive questionnaire to understand your risk tolerance and investment profile</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Assessment Process")
        
        st.markdown("""
        **Step 1:** Review the assessment methodology  
        **Step 2:** Answer 10 comprehensive questions  
        **Step 3:** Receive your risk score and category  
        **Step 4:** Understand your investment profile
        """)
        
        st.markdown("### About This Assessment")
        st.info("This assessment uses a research-based methodology to evaluate your risk tolerance across multiple dimensions including demographics, financial status, and behavioral preferences.")
        
        if st.button("Start Assessment", type="primary", use_container_width=True):
            st.session_state.stage = 'methodology'
            st.rerun()

def show_methodology_page():
    """Display assessment methodology without exposing weights"""
    st.markdown("""
    <div class="main-header">
        <h2>Assessment Methodology</h2>
        <p>Understanding how your risk profile is evaluated</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### How We Calculate Your Score")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Scoring System:**
        - Each question evaluates different aspects of risk tolerance
        - Your answers receive scores based on risk implications
        - Final score is normalized to a 1-100 scale
        - Higher scores indicate higher risk tolerance
        """)
    
    with col2:
        st.markdown("""
        **Question Categories:**
        - Demographics and Life Stage
        - Financial Status and Stability
        - Investment Experience and Preferences
        - Risk Behavior and Psychology
        """)
    
    st.markdown("### Assessment Areas")
    
    # Display assessment areas without weights or detailed scoring
    assessment_areas = [
        ("Age and Life Stage", "Evaluates your investment time horizon and life stage considerations"),
        ("Financial Dependents", "Assesses your financial responsibilities and obligations"),
        ("Income Level", "Determines your financial capacity for risk-taking"),
        ("Debt Obligations", "Evaluates your current financial commitments"),
        ("Income Stability", "Assesses the predictability of your income"),
        ("Current Portfolio", "Reviews your existing investment experience"),
        ("Investment Goals", "Understands your primary investment objectives"),
        ("Time Horizon", "Evaluates your investment duration preferences"),
        ("Risk Comfort", "Assesses your psychological comfort with risk"),
        ("Loss Behavior", "Evaluates how you react to investment losses")
    ]
    
    for area, description in assessment_areas:
        st.markdown(f"""
        <div class="assessment-area">
            <h4>{area}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Begin Questions", type="primary", use_container_width=True):
            st.session_state.stage = 'questions'
            st.session_state.current_question = 0
            st.rerun()

def show_question_page():
    """Display individual questions professionally"""
    current_q = st.session_state.current_question
    total_questions = len(questions)
    
    # Progress tracking
    progress = (current_q + 1) / total_questions
    
    st.markdown(f"""
    <div class="main-header">
        <h2>Question {current_q + 1} of {total_questions}</h2>
        <p>Risk Profile Assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    st.markdown("### Progress")
    st.progress(progress)
    st.markdown(f"**{int(progress * 100)}% Complete** • {total_questions - current_q - 1} questions remaining")
    
    # Current question
    question = questions[current_q]
    
    st.markdown(f"""
    <div class="question-card">
        <div class="question-title">{question['title']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Answer options (without scores)
    selected_answer = st.radio(
        "Select your answer:",
        question["options"],
        key=f"q_{current_q}",
        label_visibility="collapsed"
    )
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if current_q > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col3:
        if selected_answer:
            if current_q < total_questions - 1:
                if st.button("Next →", type="primary", use_container_width=True):
                    st.session_state.answers[question["key"]] = selected_answer
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("Complete Assessment", type="primary", use_container_width=True):
                    st.session_state.answers[question["key"]] = selected_answer
                    st.session_state.stage = 'results'
                    st.rerun()

def show_results_page():
    """Display results with professional analysis"""
    # Calculate score
    risk_score, detailed_scores = calculate_risk_score(st.session_state.answers)
    risk_category, risk_description, color = get_risk_category(risk_score)
    
    # Main score display
    st.markdown(f"""
    <div class="score-card">
        <h1>{risk_category}</h1>
        <h2>Risk Score: {risk_score:.1f}/100</h2>
        <p style="font-size: 1.2em;">{risk_description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Score interpretation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Score</h3>
            <h2 style="color: {color};">{risk_score:.1f}/100</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Category</h3>
            <h3 style="color: {color};">{risk_category}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        approach = "Conservative Approach" if risk_score < 50 else "Growth-Oriented Approach"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Approach</h3>
            <h4 style="color: {color};">{approach}</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk scale visualization
    st.markdown("### Your Position on Risk Scale")
    progress_value = risk_score / 100
    st.progress(progress_value)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**0 - Conservative**")
    with col2:
        st.markdown("**50 - Balanced**")
    with col3:
        st.markdown("**100 - Aggressive**")
    
    # Simplified breakdown (without exposing weights)
    st.markdown("### Assessment Summary")
    
    breakdown_data = []
    for question, details in detailed_scores.items():
        breakdown_data.append({
            "Question Area": question,
            "Your Answer": details["answer"],
            "Risk Score": f"{details['base_score']:.2f}"
        })
    
    breakdown_df = pd.DataFrame(breakdown_data)
    st.dataframe(breakdown_df, use_container_width=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Take Assessment Again", use_container_width=True):
            # Reset session state
            st.session_state.stage = 'welcome'
            st.session_state.current_question = 0
            st.session_state.answers = {}
            st.rerun()
    
    st.info("*This assessment is for educational purposes only. Please consult a qualified financial advisor for personalized investment advice.*")

# Main application flow
def main():
    initialize_session_state()
    
    # Display appropriate page based on stage
    if st.session_state.stage == 'welcome':
        show_welcome_page()
    elif st.session_state.stage == 'methodology':
        show_methodology_page()
    elif st.session_state.stage == 'questions':
        show_question_page()
    elif st.session_state.stage == 'results':
        show_results_page()

if __name__ == "__main__":
    main()
