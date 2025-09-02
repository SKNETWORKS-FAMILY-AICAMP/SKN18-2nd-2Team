import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report

from xgboost import XGBClassifier
from sklearn.svm import SVC

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 행동 기반 파생 변수
    if "watch_hours" in df and "last_login_days" in df:
        df["watch_per_login"] = df["watch_hours"] / (df["last_login_days"] + 1)
    if "monthly_fee" in df and "number_of_profiles" in df:
        df["fee_per_profile"] = df["monthly_fee"] / (df["number_of_profiles"] + 1e-3)
    if "avg_watch_time_per_day" in df and "monthly_fee" in df:
        df["efficiency"] = df["avg_watch_time_per_day"] / (df["monthly_fee"] + 1e-3)

    # 로그 변환
    if "watch_hours" in df:
        df["log_watch_hours"] = np.log1p(df["watch_hours"])
    if "avg_watch_time_per_day" in df:
        df["log_avg_watch"] = np.log1p(df["avg_watch_time_per_day"])

    # 나이 / 로그인 구간화
    if "age" in df:
        df["age_group"] = pd.cut(df["age"], bins=[17,30,50,70], labels=["18-30","31-50","51-70"])
    if "last_login_days" in df:
        df["login_bin"] = pd.cut(df["last_login_days"], bins=[-1,7,30,60],
                                 labels=["0-7","8-30","31-60"])

    # 범주형 교차
    if "subscription_type" in df and "device" in df:
        df["subscription_device"] = df["subscription_type"].astype(str) + "_" + df["device"].astype(str)

    return df

def find_unique_columns(df: pd.DataFrame):
    """행 수와 동일한 고유값을 가지는 ID 성 컬럼 찾기"""
    n = len(df)
    return [c for c in df.columns if df[c].nunique(dropna=False) == n]


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """범주형 → 원-핫 인코딩, 수치형 → 패스스루"""
    cat_cols = [c for c in X.columns if X[c].dtype == 'object' or pd.api.types.is_categorical_dtype(X[c])]
    num_cols = [c for c in X.columns if c not in cat_cols]

    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=True), cat_cols),
        ("num", "passthrough", num_cols),
    ])
    return pre

def EDA(train_df: pd.DataFrame):
    """탐색적 데이터 분석 (EDA)"""

    # 결측치 시각화
    plt.figure(figsize=(12, 6))
    sns.heatmap(train_df.isnull(), cbar=False, cmap="viridis")
    plt.title("Train Data Missing Values")
    plt.tight_layout()
    plt.savefig("./images/train_data_missing_values.png")
    plt.close()

    # 타겟분포
    plt.figure(figsize=(6, 4))
    sns.countplot(x="churned", data=train_df)
    plt.title("타겟분포(Churned)")
    plt.xlabel("이탈 여부")
    plt.ylabel("개수")
    plt.tight_layout()
    plt.savefig("./images/target_distribution.png")
    plt.close()

    # 연령분포
    plt.figure(figsize=(6,4))
    sns.histplot(train_df["age"], bins=20, kde=True, color="skyblue")
    plt.title("연령분포(Age)")
    plt.xlabel("나이")
    plt.ylabel("개수")
    plt.tight_layout()
    plt.savefig("./images/age_distribution.png")
    plt.close()

    # churned 여부에 따른 나이 분포
    plt.figure(figsize=(6,4))
    sns.kdeplot(data=train_df, x="age", hue="churned", fill=True)
    plt.title("이탈 여부별 연령 분포")
    plt.xlabel("나이")
    plt.ylabel("밀도")
    plt.tight_layout()
    plt.savefig("./images/age_distribution_by_churned.png")
    plt.close()

    # 시청시간 분포 
    plt.figure(figsize=(6,4))
    sns.histplot(train_df["watch_hours"], bins=30, kde=True, color="orange")
    plt.title("시청 시간 분포 (watch_hours)")
    plt.xlabel("시청 시간 (시간)")
    plt.ylabel("빈도수")
    plt.tight_layout()
    plt.savefig("./images/watch_hours_distribution.png")
    plt.close()

    # 이탈여부별 시청시간 분포
    plt.figure(figsize=(6,4))
    sns.boxplot(x="churned", y="watch_hours", data=train_df, palette="Set2")
    plt.title("이탈 여부 vs 시청시간")
    plt.xlabel("Churned 여부")
    plt.ylabel("시청시간 (시간)")
    plt.tight_layout()
    plt.savefig("./images/watch_hours_distribution_by_churned.png")
    plt.close()

    # 월 요금 vs 이탈여부
    plt.figure(figsize=(6,4))
    sns.boxplot(x="churned", y="monthly_fee", data=train_df, palette="Set3")
    plt.title("월 요금 vs 이탈 여부")
    plt.xlabel("Churned 여부")
    plt.ylabel("월 요금 ($)")
    plt.tight_layout()
    plt.savefig("./images/monthly_fee_distribution_by_churned.png")
    plt.close()

    # 요금제 유형별 이탈률
    plt.figure(figsize=(6,4))
    sns.barplot(x="subscription_type", y="churned", data=train_df, estimator=lambda x: sum(x)/len(x))
    plt.title("요금제별 이탈률")
    plt.xlabel("구독 유형")
    plt.ylabel("이탈률")
    plt.tight_layout()
    plt.savefig("./images/subscription_type_churn_rate.png")
    plt.close()

    # 최근 로그인과 이탈여부
    plt.figure(figsize=(6,4))
    sns.boxplot(x="churned", y="last_login_days", data=train_df, palette="Set2")
    plt.title("이탈 여부 vs 최근 로그인 경과일")
    plt.xlabel("Churned 여부")
    plt.ylabel("최근 로그인 후 경과일 (일)")
    plt.tight_layout()
    plt.savefig("./images/last_login_days_distribution_by_churned.png")
    plt.close()

def plot_feature_importances(model, feature_names, out_png="./images/feature_importances.png", top_k=30):
    """XGBoost 중요 피처 시각화"""
    fmap = model.get_booster().get_score(importance_type="gain")
    items = []
    for k, v in fmap.items():
        try:
            idx = int(k[1:])
            name = feature_names[idx] if idx < len(feature_names) else k
        except Exception:
            name = k
        items.append((name, v))

    items.sort(key=lambda x: x[1], reverse=True)
    top = items[:top_k]

    if not top:
        return

    labels, values = zip(*top)
    plt.figure(figsize=(10, max(4, 0.25 * len(labels))))
    plt.barh(range(len(values)), values)
    plt.gca().invert_yaxis()
    plt.yticks(range(len(labels)), labels)
    plt.xlabel("Gain")
    plt.title("Top Feature Importances (XGBClassifier)")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def train_and_evaluate(model, model_name, X, y, testset, test_target, pre):
    """모델 학습 & 평가 공통 함수"""
    pipe = Pipeline([
        ("pre", pre),
        ("model", model),
    ])

    # Train/Test split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe.fit(X_train, y_train)

    # 내부 검증 성능
    y_val_pred = pipe.predict(X_val)
    val_acc = accuracy_score(y_val, y_val_pred)
    val_f1 = f1_score(y_val, y_val_pred, average="macro")

    print(f"\n=== {model_name} Validation Results ===")
    print("Validation Accuracy:", val_acc)
    print("Validation Macro-F1:", val_f1)
    print(classification_report(y_val, y_val_pred))

    # 외부 테스트 성능
    test_pred = pipe.predict(testset)
    test_acc = accuracy_score(test_target, test_pred)
    test_f1 = f1_score(test_target, test_pred, average="macro")

    print(f"\n=== {model_name} Test Results ===")
    print("Test Accuracy:", test_acc)
    print("Test Macro-F1:", test_f1)
    print(classification_report(test_target, test_pred))

    return {
        "model": model_name,
        "val_acc": val_acc,
        "val_f1": val_f1,
        "test_acc": test_acc,
        "test_f1": test_f1,
    }


def main():
    # 데이터 불러오기
    train_dataset = "./data/train.csv"
    train_df = pd.read_csv(train_dataset)

    test_dataset = "./data/test.csv"
    test_df = pd.read_csv(test_dataset)
    
    # EDA
    # EDA(train_df)

    # 타깃 컬럼
    target = "churned"
    y = train_df[target]
    X = train_df.drop(columns=[target])
    testset = test_df.drop(columns=[target])
    test_target = test_df[target]

    # 유니크 컬럼 제거
    unique_cols = find_unique_columns(X)
    if unique_cols:
        X.drop(columns=unique_cols, inplace=True)
        testset.drop(columns=unique_cols, inplace=True)

    # feature engineering
    # X = feature_engineering(X)
    # testset = feature_engineering(testset)

    # 결측치 제거
    data = pd.concat([X, y], axis=1).dropna()
    X, y = data.drop(columns=[target]), data[target]
    testset = testset.dropna()

    # 전처리기 & 모델
    pre = build_preprocessor(X)
    xgb_model = XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        random_state=42,
        n_jobs=-1
    )

    svc_model = SVC(
        kernel="rbf",
        C=1.0,
        probability=True,  # 필요시 ROC/AUC 등 확률 기반 평가 가능
        random_state=42
    )

    # 결과 비교
    results = []
    results.append(train_and_evaluate(xgb_model, "XGBoost", X, y, testset, test_target, pre))
    results.append(train_and_evaluate(svc_model, "SVC", X, y, testset, test_target, pre))

    print("\n=== 최종 비교 결과 ===")
    with open("./images/training_report.txt", "w", encoding="utf-8") as f:
        for r in results:
            print(f"{r['model']}: "
                f"ValAcc={r['val_acc']:.4f}, ValF1={r['val_f1']:.4f}, "
                f"TestAcc={r['test_acc']:.4f}, TestF1={r['test_f1']:.4f}")
            f.write(f"{r['model']}\n")
            f.write(f"Validation Accuracy: {r['val_acc']:.4f}\n")
            f.write(f"Validation Macro-F1: {r['val_f1']:.4f}\n\n")
            f.write("\n\n")
            f.write(f"Test Accuracy: {r['test_acc']:.4f}\n")
            f.write(f"Test Macro-F1: {r['test_f1']:.4f}\n\n")
            f.write("\n\n")

if __name__ == "__main__":
    main()

