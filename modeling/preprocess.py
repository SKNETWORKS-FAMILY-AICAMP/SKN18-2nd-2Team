import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "watch_hours" in df and "last_login_days" in df:
        df["watch_per_login"] = df["watch_hours"] / (df["last_login_days"] + 1)
    if "monthly_fee" in df and "number_of_profiles" in df:
        df["fee_per_profile"] = df["monthly_fee"] / (df["number_of_profiles"] + 1e-3)
    if "avg_watch_time_per_day" in df and "monthly_fee" in df:
        df["efficiency"] = df["avg_watch_time_per_day"] / (df["monthly_fee"] + 1e-3)

    if "watch_hours" in df:
        df["log_watch_hours"] = np.log1p(df["watch_hours"])
    if "avg_watch_time_per_day" in df:
        df["log_avg_watch"] = np.log1p(df["avg_watch_time_per_day"])

    if "age" in df:
        df["age_group"] = pd.cut(df["age"], bins=[17,30,50,70], labels=["18-30","31-50","51-70"])
    if "last_login_days" in df:
        df["login_bin"] = pd.cut(df["last_login_days"], bins=[-1,7,30,60],
                                 labels=["0-7","8-30","31-60"])

    if "subscription_type" in df and "device" in df:
        df["subscription_device"] = df["subscription_type"].astype(str) + "_" + df["device"].astype(str)
    return df

def find_unique_columns(df: pd.DataFrame):
    """Unique 컬럼 제거"""
    n = len(df)
    return [c for c in df.columns if df[c].nunique(dropna=False) == n]

def remove_unique_cols(X_train: pd.DataFrame, X_test: pd.DataFrame):
    unique_cols = find_unique_columns(X_train)
    if unique_cols:
        X_train.drop(columns=unique_cols, inplace=True)
        X_test.drop(columns=unique_cols, inplace=True)
    return X_train, X_test
    
def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """범주형 → OHE(dense), 수치형 → StandardScaler"""
    cat_cols = [c for c in X.columns if X[c].dtype == 'object' or pd.api.types.is_categorical_dtype(X[c])]
    num_cols = [c for c in X.columns if c not in cat_cols]

    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
        ("num", StandardScaler(), num_cols),
    ])
    return pre

def clean_data(train_df, test_df):
    # 타켓컬럼 분리
    target = "churned"
    y = train_df[target]
    X = train_df.drop(columns=[target])
    testset = test_df.drop(columns=[target])
    test_target = test_df[target]
    
    # 결측치 제거
    data = pd.concat([X, y], axis=1).dropna()
    X, y = data.drop(columns=[target]), data[target]
    testset = testset.dropna()
    return X, y, testset, test_target