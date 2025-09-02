# 데이터 불러오기

import pandas as pd
import os
import easydict
from sklearn.model_selection import train_test_split

# 프로젝트 설정 및 경로 정보 반환
def get_args():

    args = easydict.EasyDict()

    # 데이터 경로 설정
    args.data_path = "./data/"
    args.train_data = os.path.join(args.data_path,"train.csv")
    args.test_data = os.path.join(args.data_path,"test.csv")
    # 결과 저장 경로
    args.save_results = 'results/results.csv'
    args.results = []

    return args

# 데이터 로드 함수

def data_load():
    args = get_args()   

    # 데이터 로드 함수 호출 
    train_data = pd.read_csv(args.train_data)
    test_data = pd.read_csv(args.test_data)
    
    print(f"데이터 로드 완료")
    print(f"test_data: {test_data.shape}")
    print(f"train_data: {train_data.shape}")

    return train_data, test_data

def data_split(train_data, test_size=0.2):
    train_split, validation_split = train_test_split(
    train_data, 
    test_size=test_size, 
    stratify=train_data['churned']  # 타겟 변수 기준으로 계층적 분할
    )
    return train_split, validation_split
