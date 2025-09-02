# 데이터 전처리 함수들

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')
from utilities.utils import prepare_data

def preprocess_data(train_data, test_data, validation_data):
    """
    전체 데이터 전처리 파이프라인
    
    Parameters:
    train_data: 학습 데이터
    test_data: 테스트 데이터
    
    Returns:
    X_train_processed: 전처리된 학습 피처
    X_test_processed: 전처리된 테스트 피처
    y_train: 학습 타겟
    """
    
    print("데이터 전처리 시작...")
    
    # 1. 데이터 타입 확인 및 변환
    train_processed = convert_data_types(train_data)
    test_processed = convert_data_types(test_data)
    validation_processed = convert_data_types(validation_data)
    
    # 2. 범주형 변수 인코딩
    train_encoded, test_encoded, validation_encoded = encode_categorical_variables(train_processed, test_processed, validation_processed)
    
    # 3. 피처와 타겟 분리
    X_train, y_train, X_test, X_validation, y_validation = prepare_data(train_encoded, test_encoded, validation_encoded)
    
    # 4. 수치형 변수 스케일링
    X_train_scaled, X_test_scaled, X_validation_scaled = scale_numerical_features(X_train, X_test, X_validation)
    
    # 5. SMOTE를 사용한 불균형 데이터 처리
    X_train_smote, y_train_smote = apply_smote(X_train_scaled, y_train)
    
    print("데이터 전처리 완료!")
    print(f"전처리 후 학습 데이터 형태: {X_train_smote.shape}")
    print(f"전처리 후 테스트 데이터 형태: {X_test_scaled.shape}")
    print(f"전처리 후 검증 데이터 형태: {X_validation_scaled.shape}")
    
    return X_train_smote, X_test_scaled, y_train_smote, X_validation_scaled, y_validation

def convert_data_types(data):
    """
    데이터 타입을 적절하게 변환
    """
    data_processed = data.copy()
    
    # customer_id는 문자열로 유지 (나중에 제거)
    
    # 수치형 변수들
    numeric_columns = ['age', 'watch_hours', 'last_login_days', 'monthly_fee', 
                       'number_of_profiles', 'avg_watch_time_per_day']
    
    for col in numeric_columns:
        if col in data_processed.columns:
            data_processed[col] = pd.to_numeric(data_processed[col], errors='coerce')
    
    # 범주형 변수들
    categorical_columns = ['gender', 'subscription_type', 'region', 'device', 
                          'payment_method', 'favorite_genre']
    
    for col in categorical_columns:
        if col in data_processed.columns:
            data_processed[col] = data_processed[col].astype('category')
    
    return data_processed

def encode_categorical_variables(train_data, test_data, validation_data):
    """
    범주형 변수를 숫자로 인코딩
    """
    train_encoded = train_data.copy()
    test_encoded = test_data.copy()
    validation_encoded = validation_data.copy()
    
    # LabelEncoder를 사용하여 범주형 변수 인코딩
    categorical_columns = ['gender', 'subscription_type', 'region', 'device', 
                          'payment_method', 'favorite_genre']
    
    label_encoders = {}
    
    for col in categorical_columns:
        if col in train_encoded.columns:
            le = LabelEncoder()
            
            # 학습 데이터와 테스트 데이터의 모든 고유값을 고려하여 fit
            all_values = pd.concat([train_encoded[col], test_encoded[col]]).unique()
            le.fit(all_values)
            
            # 인코딩 적용
            train_encoded[col] = le.transform(train_encoded[col])
            test_encoded[col] = le.transform(test_encoded[col])
            validation_encoded[col] = le.transform(validation_encoded[col])
            
            label_encoders[col] = le
    
    return train_encoded, test_encoded, validation_encoded

def separate_features_target(data):
    """
    피처와 타겟 변수 분리
    """
    # 타겟 변수
    target = 'churned'
    
    # 피처 변수 (customer_id와 churned 제외)
    feature_columns = [col for col in data.columns if col not in ['customer_id', target]]
    
    X = data[feature_columns]
    y = data[target]
    
    return X, y

def scale_numerical_features(X_train, X_test, X_validation):
    """
    수치형 변수 스케일링
    """
    # 수치형 변수 식별
    numeric_columns = X_train.select_dtypes(include=[np.number]).columns
    
    if len(numeric_columns) > 0:
        scaler = StandardScaler()
        
        # 학습 데이터로 fit하고 transform
        X_train_scaled = X_train.copy()
        X_test_scaled = X_test.copy()
        X_validation_scaled = X_validation.copy()
        
        X_train_scaled[numeric_columns] = scaler.fit_transform(X_train[numeric_columns])
        X_test_scaled[numeric_columns] = scaler.transform(X_test[numeric_columns])
        X_validation_scaled[numeric_columns] = scaler.transform(X_validation[numeric_columns])
        
        return X_train_scaled, X_test_scaled, X_validation_scaled
    else:
        return X_train, X_test, X_validation

def apply_smote(X, y):
    """
    SMOTE를 사용하여 불균형 데이터 처리
    """
    try:
        smote = SMOTE(random_state=42)
        X_smote, y_smote = smote.fit_resample(X, y)
        
        print(f"SMOTE 적용 전: {y.value_counts().to_dict()}")
        print(f"SMOTE 적용 후: {pd.Series(y_smote).value_counts().to_dict()}")
        
        return X_smote, y_smote
    except Exception as e:
        print(f"SMOTE 적용 중 오류 발생: {e}")
        print("원본 데이터 반환")
        return X, y

def get_preprocessed_data():
    """
    전처리된 데이터를 반환하는 메인 함수
    """
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from utilities.data_load import data_load
    from utilities.data_load import data_split
    
    # 데이터 로드
    train_data, test_data = data_load()
    
    # train 데이터를 train과 validation으로 분할
    train_split, validation_split = data_split(train_data)
    
    # 전처리 수행
    X_train_processed, X_test_processed, y_train_processed, X_validation_processed, y_validation_processed = preprocess_data(
        train_split, test_data, validation_split
    )
    
    return X_train_processed, X_test_processed, y_train_processed, X_validation_processed, y_validation_processed

if __name__ == "__main__":
    # 테스트 실행
    X_train, X_test, y_train, X_validation, y_validation = get_preprocessed_data()
    print("전처리 테스트 완료!")
