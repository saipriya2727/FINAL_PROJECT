import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
import os
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

os.makedirs("models", exist_ok=True)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# =========================================================
# ===================== PCOS MODEL ========================
# =========================================================

print("\n================ PCOS MODEL COMPARISON =================\n")

pcos = pd.read_csv("data/pcos.csv")
pcos.columns = pcos.columns.str.strip()

features_pcos = [
    'BMI','Waist(inch)','Waist:Hip Ratio','Weight (Kg)',
    'BP _Systolic (mmHg)','BP _Diastolic (mmHg)',
    'RBS(mg/dl)','LH(mIU/mL)','FSH(mIU/mL)',
    'FSH/LH','AMH(ng/mL)','TSH (mIU/L)','PRL(ng/mL)'
]

target_pcos = 'PCOS (Y/N)'

data_pcos = pcos[features_pcos + [target_pcos]].copy()
data_pcos = data_pcos.apply(pd.to_numeric, errors='coerce')
data_pcos = data_pcos.dropna()

X_pcos = data_pcos[features_pcos]
y_pcos = data_pcos[target_pcos]

scaler_pcos = StandardScaler()
X_pcos_scaled = scaler_pcos.fit_transform(X_pcos)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "XGBoost": xgb.XGBClassifier(eval_metric='logloss', random_state=42)
}

for name, model in models.items():
    cv_scores = cross_val_score(model, X_pcos_scaled, y_pcos, cv=cv, scoring='accuracy')
    print(f"{name} - Mean CV Accuracy: {cv_scores.mean():.4f}")

# =========================================================
# ================= METS MODEL COMPARISON =================
# =========================================================

print("\n================ METS MODEL COMPARISON =================\n")

mets = pd.read_csv("data/mets.csv")
mets.columns = mets.columns.str.strip()

features_mets = [
    'WaistCirc','BMI','BloodGlucose',
    'Triglycerides','HDL','Age'
]

target_mets = 'MetabolicSyndrome'

data_mets = mets[features_mets + [target_mets]].copy()
data_mets = data_mets.apply(pd.to_numeric, errors='coerce')
data_mets = data_mets.dropna()

X_mets = data_mets[features_mets]
y_mets = data_mets[target_mets]

scaler_mets = StandardScaler()
X_mets_scaled = scaler_mets.fit_transform(X_mets)

for name, model in models.items():
    cv_scores = cross_val_score(model, X_mets_scaled, y_mets, cv=cv, scoring='accuracy')
    print(f"{name} - Mean CV Accuracy: {cv_scores.mean():.4f}")