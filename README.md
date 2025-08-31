# SKN18-2nd-2Team

# Netflix Customer Churn Prediction

Netflix 고객 이탈(Churn) 데이터를 활용하여 EDA(탐색적 데이터 분석)와 LightGBM 분류 모델을 통한 이탈 예측

## 프로젝트 구조

- `EDA.ipynb` : 데이터 분석, 전처리, 모델 학습 및 평가 전체 워크플로우가 담긴 노트북
- `data/netflix_customer_churn.csv` : 원본 데이터 파일

## 주요 단계

1. 데이터 로드 및 EDA
    - pandas를 사용해 데이터를 불러오고, 결측치, 데이터 타입, 기본 통계량을 확인
    - seaborn, matplotlib을 활용해 주요 변수의 분포와 상관관계를 시각화

2. 데이터 전처리
    - 불필요한 컬럼(`customer_id`) 제거
    - 범주형 변수는 원-핫 인코딩 처리

3. 학습/테스트 데이터 분리
    - 8:2 비율로 데이터 분할

4. LightGBM 모델 학습
    - LightGBM 분류기를 학습 데이터에 적합
    - 테스트 데이터로 예측 및 평가 수행

5. 모델 평가
    - 분류 리포트, ROC AUC, 혼동 행렬 등 다양한 지표로 모델 성능 평가


### 결과
정확도(accuracy): 0.87 (87%)
이탈 고객(1) 정밀도(precision): 0.78
이탈 고객(1) 재현율(recall): 0.68
이탈 고객(1) F1-score: 0.73
ROC AUC: 0.91


