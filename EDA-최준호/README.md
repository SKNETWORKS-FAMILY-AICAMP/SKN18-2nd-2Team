# 기본 EDA 방안(별도 featuring 없음)
- customer_id 삭제
- target: churned, features: churned, customer_id를 제외한 모든 column
- target의 0과 1의 개수 => 0: 2485, 1: 2515
- customer_id를 제외한 문자열 데이터(gender, subscription_type, region, device, payment_method, favorite_genre)은 One hot encoding으로 이용하여 숫자로 변환
- 숫자 데이터(age, watch_hours, last_login_days, monthly_fee, number_of_profiles, avg_watch_time_per_day) => StandardScaler 이용

# 기본 EDA에 모델 적용 결과(catboost)
- train/test score  => (훈련용 평가지표: 1.0 / 테스트용 평가지표: 0.998)
- roc_curve auc: 0.9999839994239792
- confusion_matrix(precision, recall) => [1.        , 0.        ],
                                        [0.00397614, 0.99602386]