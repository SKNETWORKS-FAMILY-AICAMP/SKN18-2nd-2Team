import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def EDA(train_df: pd.DataFrame):
    """탐색적 데이터 분석 (EDA)"""
    
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False

    # 수치형 데이터에 대한 heatmap 상관관계 분석
    numeric_cols = train_df.select_dtypes(include=['float64', 'int64'])
    corr = numeric_cols.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('이탈률과 상관관계')
    plt.tight_layout()
    plt.savefig("../images/correlation_heatmap.png")
    plt.close()

    # 결측치 시각화
    missing_counts = train_df.isnull().sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=missing_counts.index, y=missing_counts.values, color="skyblue")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("결측치 개수")
    plt.title("컬럼별 결측치 개수")
    plt.tight_layout()
    plt.savefig("../images/train_data_missing_values.png")
    plt.close()

    # 타겟분포
    plt.figure(figsize=(6, 4))
    sns.countplot(x="churned", data=train_df)
    plt.title("타겟분포(Churned)")
    plt.xlabel("이탈 여부")
    plt.ylabel("개수")
    plt.tight_layout()
    plt.savefig("../images/target_distribution.png")
    plt.close()

    # 연령분포
    plt.figure(figsize=(6,4))
    sns.histplot(train_df["age"], bins=20, kde=True, color="skyblue")
    plt.title("연령분포(Age)")
    plt.xlabel("나이")
    plt.ylabel("개수")
    plt.tight_layout()
    plt.savefig("../images/age_distribution.png")
    plt.close()

    # churned 여부에 따른 나이 분포
    plt.figure(figsize=(6,4))
    sns.kdeplot(data=train_df, x="age", hue="churned", fill=True)
    plt.title("이탈 여부별 연령 분포")
    plt.xlabel("나이")
    plt.ylabel("밀도")
    plt.tight_layout()
    plt.savefig("../images/age_distribution_by_churned.png")
    plt.close()

    # 시청시간 분포 
    plt.figure(figsize=(6,4))
    sns.histplot(train_df["watch_hours"], bins=30, kde=True, color="orange")
    plt.title("시청 시간 분포 (watch_hours)")
    plt.xlabel("시청 시간 (시간)")
    plt.ylabel("빈도수")
    plt.tight_layout()
    plt.savefig("../images/watch_hours_distribution.png")
    plt.close()

    # 이탈여부별 시청시간 분포
    plt.figure(figsize=(6,4))
    sns.boxplot(x="churned", y="watch_hours", data=train_df, palette="Set2")
    plt.title("이탈 여부 vs 시청시간")
    plt.xlabel("Churned 여부")
    plt.ylabel("시청시간 (시간)")
    plt.tight_layout()
    plt.savefig("../images/watch_hours_distribution_by_churned.png")
    plt.close()

    # 월 요금 vs 이탈여부
    plt.figure(figsize=(6,4))
    sns.boxplot(x="churned", y="monthly_fee", data=train_df, palette="Set3")
    plt.title("월 요금 vs 이탈 여부")
    plt.xlabel("Churned 여부")
    plt.ylabel("월 요금 ($)")
    plt.tight_layout()
    plt.savefig("../images/monthly_fee_distribution_by_churned.png")
    plt.close()

    # 요금제 유형별 이탈률
    plt.figure(figsize=(6,4))
    sns.barplot(x="subscription_type", y="churned", data=train_df, estimator=lambda x: sum(x)/len(x))
    plt.title("요금제별 이탈률")
    plt.xlabel("구독 유형")
    plt.ylabel("이탈률")
    plt.tight_layout()
    plt.savefig("../images/subscription_type_churn_rate.png")
    plt.close()

    # 최근 로그인과 이탈여부
    plt.figure(figsize=(6,4))
    sns.boxplot(x="churned", y="last_login_days", data=train_df, palette="Set2")
    plt.title("이탈 여부 vs 최근 로그인 경과일")
    plt.xlabel("Churned 여부")
    plt.ylabel("최근 로그인 후 경과일 (일)")
    plt.tight_layout()
    plt.savefig("../images/last_login_days_distribution_by_churned.png")
    plt.close()