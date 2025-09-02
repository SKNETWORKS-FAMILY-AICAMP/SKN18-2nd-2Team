import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from utils import save_feature_importances_from_pipeline
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    AdaBoostClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
)
from sklearn.svm import SVC
from xgboost import XGBClassifier
import lightgbm as lgb
from catboost import CatBoostClassifier

RANDOM_STATE = 42

def load_models():
    return {
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "RandomForest": RandomForestClassifier(random_state=RANDOM_STATE),
        "XGBoost": XGBClassifier(random_state=RANDOM_STATE, eval_metric="logloss"),
        "LightGBM": lgb.LGBMClassifier(random_state=RANDOM_STATE, verbose=-1),
        "CatBoost": CatBoostClassifier(random_state=RANDOM_STATE, verbose=0),
        "SVC": SVC(probability=True, random_state=RANDOM_STATE),
        "ExtraTrees": ExtraTreesClassifier(random_state=RANDOM_STATE),
        "AdaBoost": AdaBoostClassifier(random_state=RANDOM_STATE),
        "HistGradientBoosting": HistGradientBoostingClassifier(random_state=RANDOM_STATE),
        "GradientBoosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
        "KNeighbors": KNeighborsClassifier(),
        "RidgeClassifier": RidgeClassifier(random_state=RANDOM_STATE),
        "MLPClassifier": MLPClassifier(random_state=RANDOM_STATE, max_iter=1000),
    }

def train_and_evaluate(model, model_name, X, y, testset, test_target, pre):
    pipe = ImbPipeline([
        ("pre", pre),
        ("smote", SMOTE(random_state=RANDOM_STATE)),
        ("model", model),
    ])

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    pipe.fit(X_train, y_train)

    # 피처 중요도 저장 (Validation set 기준)
    out_dir = "./images/feature_importances"
    out_png = os.path.join(out_dir, f"{model_name}_feature_importances.png")
    
    save_feature_importances_from_pipeline(pipe, model_name, X_val, y_val, out_png, top_k=30, random_state=RANDOM_STATE)
    
    # validation
    y_val_pred  = pipe.predict(X_val)
    val_acc     = accuracy_score(y_val, y_val_pred)
    val_f1      = f1_score(y_val, y_val_pred, average="macro")
    
    # test
    test_pred = pipe.predict(testset)
    test_acc  = accuracy_score(test_target, test_pred)
    test_f1   = f1_score(test_target, test_pred, average="macro")

    return {
        "model": model_name,
        "val_acc": val_acc,
        "val_f1": val_f1,
        "test_acc": test_acc,
        "test_f1": test_f1,
    }