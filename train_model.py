import pandas as pd
import numpy as np
import random
import xgboost as xgb
from sklearn.model_selection import train_test_split
import os

# Define features and their weights/scores from the paper (Appendix 2)
feature_configs = [
    # (feature, weight, [(option, score), ...])
    ("Age", 1, [("18-35", 1), ("36-55", 0.5), ("55+", 0.2)]),
    ("Dependents", 0.83, [("No one", 1), ("Spouse only", 0.8), ("Spouse and children", 0.6), ("Parents only", 0.6), ("Spouse, children and parents", 0.1)]),
    ("Annual Income", 0.83, [("Below INR 1 lac", 0.2), ("1-5 lac", 0.4), ("5-10 lac", 0.6), ("10-25 lac", 0.8), ("Above 25 lac", 1)]),
    ("EMI % Income", 0.65, [("None", 1), ("Up to 20%", 0.8), ("20-30%", 0.6), ("30-40%", 0.4), ("50% or above", 0.2)]),
    ("Income Stability", 0.65, [("Very low", 0.1), ("Low", 0.3), ("Moderate", 0.6), ("High", 1), ("Very high", 1)]),
    ("Portfolio", 0.5, [("Savings/FD", 0.4), ("Bonds/debt", 0.6), ("Mutual Funds", 0.5), ("Real Estate/Gold", 0.4), ("Stock Market", 0.8)]),
    ("Investment Objective", 0.8, [("Retirement planning", 0.65), ("Monthly Income", 0.6), ("Tax Saving", 0.4), ("Capital Preservation", 0.5), ("Wealth Creation", 1)]),
    ("Investment Duration", 0.8, [("Less than 1 year", 0.5), ("1 to 3 years", 0.8), ("3 to 5 years", 0.65), ("5 to 10 years", 0.6), ("More than 10 years", 0.7)]),
    ("Comfort with High Risk", 0.7, [("Strongly agree", 1), ("Agree", 0.9), ("Neutral", 0.5), ("Disagree", 0.2), ("Strongly disagree", 0.1)]),
    ("Behavior on 20% Loss", 0.65, [("Sell & preserve cash", 0.2), ("Sell & move to safe", 0.3), ("Wait & sell later", 0.5), ("Keep investments", 0.8), ("Invest more", 1)])
]

feature_names = [f[0] for f in feature_configs]

# Risk class boundaries as per paper
# (Linear model boundary): 3, 4, 4.9, 5.8
def score_to_risk_category(score):
    if score < 3:
        return 0  # No risk
    elif score < 4:
        return 1  # Low risk
    elif score < 4.9:
        return 2  # Moderate risk
    elif score < 5.8:
        return 3  # Likes risk
    else:
        return 4  # High risk

# Generate synthetic data
num_samples = 50000
data_rows = []
for _ in range(num_samples):
    row = {}
    total_score = 0
    for feature, weight, options in feature_configs:
        option, option_score = random.choice(options)
        row[feature] = option
        total_score += weight * option_score
    row["risk_category"] = score_to_risk_category(total_score)
    data_rows.append(row)

df = pd.DataFrame(data_rows)
os.makedirs("data", exist_ok=True)
df.to_csv("data/sample_data.csv", index=False)

# Encode features numerically for model
encodings = {}
for feature, weight, options in feature_configs:
    encodings[feature] = {option: i for i, (option, _) in enumerate(options)}
    df[feature] = df[feature].map(encodings[feature])

X = df[feature_names]
y = df["risk_category"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    use_label_encoder=False,
    eval_metric='mlogloss'
)
model.fit(X_train, y_train)
os.makedirs("model", exist_ok=True)
model.save_model("model/risk_model.json")
print("Synthetic data and trained model created!")
