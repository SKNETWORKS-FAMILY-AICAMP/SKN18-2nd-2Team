from EDA import EDA
from utils import load_data, write_result
from preprocess import feature_engineering, remove_unique_cols, build_preprocessor, clean_data
from model import train_and_evaluate, load_models


def main():
    train_df, test_df = load_data("./data/train.csv", "./data/test.csv")

    EDA(train_df)

    # Data cleaning
    X_train, y_train, testset, test_target = clean_data(train_df, test_df)

    # 불필요한 컬럼 제거
    X_train, testset = remove_unique_cols(X_train, testset)

    # Feature extraction
    X_train = feature_engineering(X_train)
    testset = feature_engineering(testset)

    # 전처리
    pre = build_preprocessor(X_train)

    # 사용할 모델들 로드
    models = {k: v for k, v in load_models().items() if v is not None}

    # 결과저장
    results = []
    for name, model in models.items():
        try:
            result = train_and_evaluate(model, name, X_train, y_train, testset, test_target, pre)
            results.append(result)
        except Exception as e:
            print(f"[WARN] {name} 실패: {e}")

    write_result(results)

if __name__ == "__main__":
    main()
