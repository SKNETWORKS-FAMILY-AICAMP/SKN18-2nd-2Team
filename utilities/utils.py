# 유틸리티 함수

import random
import os
import numpy as np
import torch
from functools import wraps
from sklearn.model_selection import train_test_split

# reset_seeds

def reset_seeds(func, seed=42):
    @wraps(func)
    def wrapper(*args, **kwargs):
        random.seed(seed)
        os.environ["PYTHONHASHSEED"] = str(seed)  # 파이썬 환경변수 시드 고정
        np.random.seed(seed)
        torch.manual_seed(seed)  # cpu 연산 무작위 고정
        torch.cuda.manual_seed(seed)  # gpu 연산 무작위 고정
        torch.backends.cudnn.deterministic = True  # (예측에 대한 불확실성 제거 )
        return func(*args, **kwargs)
    return wrapper

def EDA(train_data,test_data):

    # target
    target = "churned"
    x = train_data.drop(columns=[target])
    y = train_data[target]
    test_set = test_data.drop(columns=[target])
    test_target = test_data[target]

    #필요없는 컬럼(user_id) 제거 및 인덱스 설정

def prepare_data(train_data, test_data, validation_data):
    # 피처와 타겟 분리
    X_train, y_train = separate_features_target(train_data)
    X_test = test_data.drop(columns=['customer_id'])  # customer_id는 제거
    X_validation, y_validation = separate_features_target(validation_data)
    
    return X_train, y_train, X_test, X_validation, y_validation

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
