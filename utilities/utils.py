# 유틸리티 함수

import random
import os
import numpy as np
import torch
from functools import wraps

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