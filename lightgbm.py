# 1. 라이브러리 import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# 2. 데이터 불러오기
df = pd.read_csv('C:\\dev\\SKN18-2nd-2Team\\data\\netflix_customer_churn.csv')

# 3. EDA
print(df.info())
print(df.describe())
print(df.isnull().sum())
print(df['churned'].value_counts())

# 4. 시각화 예시
sns.countplot(x='churned', data=df)
plt.title('Churn Distribution')
plt.show()

# 5. 전처리 (customer_id 컬럼 삭제)
if 'customer_id' in df.columns:
    df = df.drop('customer_id', axis=1)

# 6. 범주형 변수 인코딩
cat_cols = df.select_dtypes(include='object').columns
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

# 7. 학습/테스트 데이터 분리
X = df.drop('churned', axis=1)
y = df['churned']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 8. LightGBM 모델 학습
lgbm = lgb.LGBMClassifier(random_state=42)
lgbm.fit(X_train, y_train)

# 9. 예측 및 평가
y_pred = lgbm.predict(X_test)
y_proba = lgbm.predict_proba(X_test)[:,1]

print(classification_report(y_test, y_pred))
print('ROC AUC:', roc_auc_score(y_test, y_proba))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d')
plt.title('Confusion Matrix')
plt.show()