# Risk Profiling System - Professional Prototype

## Overview

A professional **rule-based risk profiling assessment tool** built with Streamlit. This application calculates a normalized risk tolerance score (1-100) through a comprehensive questionnaire designed for financial advisory and investment planning purposes.

## How to Run

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project**
```bash
git clone <repository-url>
cd risk-profili
```

2. **Install required dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Access the application**
- Open your web browser
- Navigate to `http://localhost:8501`
- The application will start automatically

### Alternative Installation (using virtual environment)
```bash
# Create virtual environment
python -m venv risk_env

# Activate virtual environment
# On Windows:
risk_env\Scripts\activate
# On macOS/Linux:
source risk_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## Assessment Questions

The system uses **10 comprehensive questions** covering all aspects of risk tolerance:

### 1. **Age Group**
- 18–35 years
- 36–55 years  
- 55 years and above

### 2. **Financial Dependents**
- No one
- Only spouse
- Spouse and children
- Only parents
- Spouse, children, and parents

### 3. **Annual Income Range**
- Below INR 1 lakh
- Between INR 1 lakh and INR 5 lakh
- Between INR 5 lakh and INR 10 lakh
- Between INR 10 lakh and INR 25 lakh
- Above INR 25 lakh

### 4. **EMI/Loan Percentage of Income**
- None
- Up to 20%
- 20–30%
- 30–40%
- 50% or above

### 5. **Income Stability**
- Very low stability
- Low stability
- Moderate stability
- High stability
- Very high stability

### 6. **Current Portfolio Allocation**
- Savings and fixed deposits
- Bonds or debt
- Mutual funds
- Real estate or gold
- Stock market

### 7. **Investment Objective**
- Retirement planning
- Monthly income
- Tax saving
- Capital preservation
- Wealth creation

### 8. **Investment Duration**
- Less than 1 year
- 1–3 years
- 3–5 years
- 5–10 years
- More than 10 years

### 9. **Comfort with High Risk**
- Strongly agree
- Agree
- Neutral
- Disagree
- Strongly disagree

### 10. **Behavior on 20% Loss**
- Sell and preserve cash
- Sell and move cash to fixed deposits or liquid fund
- Wait till market recovers and then sell
- Keep investments as they are
- Invest more

## Mathematical Calculation & Scoring

### Scoring Methodology

Each question has two components:
1. **Weight (W)**: Importance factor based on financial research
2. **Answer Score (S)**: Risk tolerance value for each answer option (0.1 to 1.0)

### Question Weights & Answer Scores

| Question | Weight | Low Risk Score | High Risk Score |
|----------|--------|----------------|-----------------|
| Age | 1.00 | 55+ years (0.2) | 18-35 years (1.0) |
| Dependents | 0.83 | Spouse+children+parents (0.1) | No one (1.0) |
| Annual Income | 0.83 | Below 1 lakh (0.2) | Above 25 lakh (1.0) |
| Investment Objective | 0.80 | Tax saving (0.4) | Wealth creation (1.0) |
| Investment Duration | 0.80 | Less than 1 year (0.5) | More than 10 years (0.7) |
| Comfort with High Risk | 0.70 | Strongly disagree (0.1) | Strongly agree (1.0) |
| EMI % Income | 0.65 | 50% or above (0.2) | None (1.0) |
| Income Stability | 0.65 | Very low (0.1) | Very high (1.0) |
| Behavior on 20% Loss | 0.65 | Sell and preserve (0.2) | Invest more (1.0) |
| Portfolio | 0.50 | Savings/FD (0.4) | Stock market (0.8) |

### Mathematical Formula

**Step 1: Calculate Weighted Score for Each Question**
```
Weighted Score = Weight × Answer Score
```

**Step 2: Calculate Total Raw Score**
```
Total Raw Score = Σ(Weight × Answer Score) for all 10 questions
```

**Step 3: Calculate Maximum Possible Score**
```
Max Possible Score = Σ(Weight × 1.0) for all questions = 7.41
```

**Step 4: Normalize to 1-100 Scale**
```
Final Score = (Total Raw Score / Max Possible Score) × 100
```

### Example Calculation

For a user with moderate risk profile:
- Age (36-55): 1.00 × 0.5 = 0.50
- Dependents (Spouse): 0.83 × 0.8 = 0.66
- Income (5-10 lakh): 0.83 × 0.6 = 0.50
- ... (continue for all questions)

Total Raw Score = 4.45
Final Score = (4.45 / 7.41) × 100 = 60.1

## Original Raw Score Categorization

### Understanding the Raw Score Scale

Before normalization to the 1-100 scale, the system works with **raw weighted scores** that provide the foundation for all categorization:

**Maximum Possible Raw Score**: 7.41 (sum of all weights)  
**Minimum Possible Raw Score**: 0.741 (all lowest answer scores × weights)

### Raw Score to Category Mapping

The normalized categories (0-100) are derived from these original raw score thresholds:

| Raw Score Range | Normalized Score | Risk Category |
|-----------------|------------------|---------------|
| 0.741 - 2.223 | 0-30 | Conservative |
| 2.223 - 3.335 | 30-45 | Moderate Conservative |
| 3.335 - 4.446 | 45-60 | Balanced |
| 4.446 - 5.558 | 60-75 | Moderate Aggressive |
| 5.558 - 7.41 | 75-100 | Aggressive |

### Raw Score Threshold Calculation

To convert normalized thresholds back to raw scores:
```
Raw Score Threshold = (Normalized Threshold / 100) × 7.41
```

**Key Thresholds:**
- **Conservative limit**: (30/100) × 7.41 = **2.223**
- **Balanced middle**: (60/100) × 7.41 = **4.446** 
- **Aggressive start**: (75/100) × 7.41 = **5.558**

### Investment Approach in Raw Scores

The 50-point normalized threshold equals **(50/100) × 7.41 = 3.705** raw score:

| Raw Score | Investment Approach |
|-----------|-------------------|
| **< 3.705** | Conservative Approach |
| **≥ 3.705** | Growth-Oriented Approach |

### Example with Raw Score Flow

**User Answers:**
- Age (36-55): 1.00 × 0.5 = **0.50**
- Dependents (Spouse): 0.83 × 0.8 = **0.66**
- Income (5-10 lakh): 0.83 × 0.6 = **0.50**
- (... other questions sum to 2.79)

**Total Raw Score**: 4.45

**Category Determination**: Since 4.45 falls in range 4.446-5.558 → **"Moderate Aggressive"**

**Approach Determination**: Since 4.45 > 3.705 → **"Growth-Oriented Approach"**

**Normalization**: (4.45 ÷ 7.41) × 100 = **60.1** (displayed to user)

This shows how the system processes raw weighted scores internally before presenting the user-friendly 1-100 scale.

## Risk Categories & Scale

The system categorizes users into **5 distinct risk profiles** based on their normalized score:

### 1. **Conservative (0-30 points)**
- **Profile**: Capital preservation focused
- **Characteristics**: 
  - Prefers guaranteed returns
  - Minimal risk tolerance
  - Short-term liquidity needs
  - Risk-averse behavior
- **Typical Investors**: Retirees, high dependents, low income
- **Investment Focus**: Fixed deposits, government bonds, liquid funds

### 2. **Moderate Conservative (30-45 points)**
- **Profile**: Stable returns preference
- **Characteristics**:
  - Below average risk tolerance
  - Prefers predictable income
  - Limited exposure to volatility
  - Cautious approach to markets
- **Typical Investors**: Pre-retirees, moderate income, some dependents
- **Investment Focus**: Debt funds, hybrid funds, some equity exposure

### 3. **Balanced (45-60 points)**
- **Profile**: Moderate risk tolerance
- **Characteristics**:
  - Balanced approach to risk and return
  - Willing to accept moderate volatility
  - Long-term perspective
  - Diversified investment approach
- **Typical Investors**: Middle-aged, stable income, moderate dependents
- **Investment Focus**: Balanced funds, diversified equity, debt mix

### 4. **Moderate Aggressive (60-75 points)**
- **Profile**: Growth-oriented approach
- **Characteristics**:
  - Above average risk tolerance
  - Growth-focused investment goals
  - Comfortable with market volatility
  - Long-term wealth creation focus
- **Typical Investors**: Young professionals, higher income, fewer dependents
- **Investment Focus**: Equity funds, growth stocks, emerging markets

### 5. **Aggressive (75-100 points)**
- **Profile**: Maximum growth potential
- **Characteristics**:
  - High risk tolerance
  - Maximum return expectations
  - Comfortable with high volatility
  - Very long-term investment horizon
- **Typical Investors**: Young, high income, no dependents, experienced
- **Investment Focus**: High-growth equity, small-cap, international markets

## Risk Scale Visualization

```
0    10    20    30    40    50    60    70    80    90    100
|----|----|----|----|----|----|----|----|----|----|----|----|
     Conservative    Mod-Cons   Balanced   Mod-Agg    Aggressive
     (Capital        (Stable    (Moderate  (Growth    (Maximum
     Preservation)   Returns)   Risk)      Oriented)  Growth)
```

## Technical Features

- **Framework**: Streamlit (Python web framework)
- **Scoring**: Weighted rule-based calculation
- **Normalization**: Mathematical scaling to 1-100 range
- **Design**: Professional CSS styling with high contrast
- **Compatibility**: Python 3.7+ required
- **Dependencies**: streamlit, pandas, numpy

## Project Structure

```
risk-profili/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies  
├── README.md          # Project documentation
└── .git/              # Version control
```

## Investment Approach Determination

The system determines the **Investment Approach** based on a simple binary classification using the 50-point threshold on the risk scale:

### Approach Logic

```python
approach = "Conservative Approach" if risk_score < 50 else "Growth-Oriented Approach"
```

### Scale Breakdown by Approach

| Score Range | Risk Category | Investment Approach | Reasoning |
|-------------|---------------|-------------------|-----------|
| 0-30 | Conservative | **Conservative Approach** | Capital preservation focus |
| 30-45 | Moderate Conservative | **Conservative Approach** | Stability over growth |
| 45-49.99 | Balanced (Lower) | **Conservative Approach** | Cautious balanced approach |
| 50-60 | Balanced (Upper) | **Growth-Oriented Approach** | Growth-focused balanced approach |
| 60-75 | Moderate Aggressive | **Growth-Oriented Approach** | Clear growth orientation |
| 75-100 | Aggressive | **Growth-Oriented Approach** | Maximum growth focus |

### Why the 50-Point Split?

The **50-point threshold** represents the mathematical midpoint of the risk scale and serves as the critical decision point between two fundamental investment philosophies:

#### Conservative Approach (Score < 50)
- **Philosophy**: "Preserve first, grow second"
- **Priority**: Capital protection over wealth maximization
- **Risk Tolerance**: Below average to moderate
- **Time Horizon**: Often shorter-term or income-focused
- **Typical Strategies**: 
  - Higher allocation to debt/fixed income
  - Lower equity exposure
  - Focus on dividend-paying stocks
  - Emphasis on guaranteed returns

#### Growth-Oriented Approach (Score ≥ 50)
- **Philosophy**: "Growth first, with acceptable risk"
- **Priority**: Wealth creation over capital protection
- **Risk Tolerance**: Moderate to high
- **Time Horizon**: Often longer-term
- **Typical Strategies**:
  - Higher allocation to equity
  - Growth stocks and emerging markets
  - Willing to accept volatility for returns
  - Focus on capital appreciation


## License

This project is for educational and prototype purposes.

## Support

For questions or issues, please refer to the project documentation or contact the development team.
