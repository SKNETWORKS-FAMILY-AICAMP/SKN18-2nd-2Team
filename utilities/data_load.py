# 데이터 불러오기

import pandas as pd
import numpy as np
import os
import easydict

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

#필요없는 컬럼(user_id) 제거 및 인덱스 설정

def prepare_data(train_data, test_data):
    train_porcessed = train_data.drop(columns=["user_id"])
    test_processed = test_data.set_index("user_id")
    return train_porcessed, test_processed

