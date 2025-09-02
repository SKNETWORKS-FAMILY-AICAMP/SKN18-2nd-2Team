class DataProcessing():

    def __init__(self, train_csv, test_csv, seed = 42, test_size = 0.2):

        # 데이터셋 불러오기
        self.train_df, self.test_df = self.load_csv(train_csv, test_csv)
        # 머신러닝 분석에 필요없는 컬럼제거
        self.train_df, self.test_df = self.unnecessary_column_drop(self.train_df, self.test_df)
        # target과 나머지 features로 분류
        self.target, self.features = self.split_target_feature(self.train_df)
        # seed 설정
        self.SEED = seed
        # train_test_split 진행
        from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.features, self.target, test_size=test_size, random_state=self.SEED, stratify=self.target)
        # 인덱스 초기화
        self.X_train = self.X_train.reset_index(drop=True)
        self.X_test = self.X_test.reset_index(drop=True)
        self.y_train = self.y_train.reset_index(drop=True)
        self.y_test = self.y_test.reset_index(drop=True)
        # test_df에 대한 target, features 나누기
        self.test_df_y, self.test_df_X = self.split_target_feature(self.test_df)
        # 문자열 데이터를 인코딩(숫자로 변환)
        self.train_X_enc, self.test_X_enc, self.test_df_enc = self.do_encoding(self.X_train, self.X_test, self.test_df_X)
        # encoding 데이터와 수치형 데이터 병합
        self.train_merge, self.test_merge, self.test_df_merge = self.merge_data(self.X_train, self.train_enc, self.X_test, self.test_enc, self.test_df_X, self.test_df_enc)
        # train_merge, test_merge, test_df_merge에 StandardScaler적용
        from sklearn.preprocessing import StandardScaler
        import pandas as pd
        self.scaler = StandardScaler()
        self.train_merge = pd.DataFrame(self.scaler.fit_transform(self.train_merge), columns=self.train_merge.columns)
        self.test_merge = pd.DataFrame(self.scaler.transform(self.test_merge), columns=self.test_merge.columns)
        self.test_df_merge = pd.DataFrame(self.scaler.transform(self.test_df_merge), columns=self.test_df_merge.columns)


    def load_csv(self, train_csv, test_csv):
        # 데이터셋 불러오기
        import pandas as pd

        self.train_df = pd.read_csv(train_csv)
        self.test_df = pd.read_csv(test_csv)

        return self.train_df, self.test_df
    
    def unnecessary_column_drop(self, train_df, test_df):
        # 머신러닝 분석에 필요없는 컬럼제거
        self.train_df = train_df.drop(columns=['customer_id'], axis=1)
        self.test_df = test_df.drop(columns=['customer_id'], axis=1)

        return self.train_df, self.test_df
    
    def split_target_feature(self, df):
        # target과 나머지 features로 분류
        self.target = df['churned']
        self.features = df.drop(columns=['churned'], axis=1)

        return self.target, self.features
    
    def do_encoding(self, X_train, X_test, test_df_X):
        # 문자열 데이터를 인코딩(숫자로 변환)
        import pandas as pd
        from sklearn.preprocessing import OneHotEncoder

        self.categorical_features = X_train.select_dtypes(include=['object']).columns
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.X_train_encoded = self.encoder.fit_transform(X_train[self.categorical_features])
        self.X_test_encoded = self.encoder.transform(X_test[self.categorical_features])
        self.test_df_X_encoded = self.encoder.transform(test_df_X[self.categorical_features])
        # X_train, X_test, test_df_X에 one hot encoding 적용
        self.train_enc = pd.DataFrame(self.X_train_encoded.toarray(), columns=self.encoder.get_feature_names_out(self.categorical_features))
        self.test_enc = pd.DataFrame(self.X_test_encoded.toarray(), columns=self.encoder.get_feature_names_out(self.categorical_features))
        self.test_df_enc = pd.DataFrame(self.test_df_X_encoded.toarray(), columns=self.encoder.get_feature_names_out(self.categorical_features))

        return self.train_enc, self.test_enc, self.test_df_enc
    
    def merge_data(self, X_train, train_enc, X_test, test_enc, test_df_X, test_df_enc):
        # encoding 데이터와 수치형 데이터 병합
        self.train_merge = X_train.select_dtypes(include=['int64', 'float64']).join(train_enc)
        self.test_merge = X_test.select_dtypes(include=['int64', 'float64']).join(test_enc)
        self.test_df_merge = test_df_X.select_dtypes(include=['int64', 'float64']).join(test_df_enc)

        return self.train_merge, self.test_merge, self.test_df_merge
    
class CatBoost():

    def __init__(self):

        from catboost import CatBoostClassifier

        self.model = CatBoostClassifier(verbose=False, random_state=result.SEED)
        self.model.fit(result.train_merge, result.y_train)
        print(f'훈련용 평가지표: {self.model.score(result.train_merge, result.y_train)} / 테스트용 평가지표: {self.model.score(result.test_merge, result.y_test)}')

        # test.csv에 대한 성능평가
        print(f'test.csv 평가지표: {self.model.score(result.test_df_merge, result.test_df_y)}')

        # train.csv에 대한 roc_curve
        from sklearn.metrics import roc_curve, auc

        self.y_pred = self.model.predict_proba(result.test_merge)[:,1]
        self.y_predict = self.model.predict(result.test_merge)
        self.fpr, self.tpr, self.thresholds = roc_curve(result.y_test, self.y_predict)

        self.score_auc = auc(self.fpr, self.tpr)
        print(f"train.csv에 대한 로컬PC Score: {self.score_auc}")

        self.y_pred = self.model.predict_proba(result.test_df_merge)[:,1]
        self.y_predict = self.model.predict(result.test_df_merge)
        self.fpr, self.tpr, self.thresholds = roc_curve(result.test_df_y, self.y_predict)

        self.score_auc = auc(self.fpr, self.tpr)
        print(f"test.csv에 대한 로컬PC Score: {self.score_auc}")

        # train.csv에 대한 confusion matrix
        from sklearn.metrics import confusion_matrix

        self.pred_tree = self.model.predict(result.test_merge)
        self.conf_mx = confusion_matrix(result.y_test, self.pred_tree, normalize='true')
        print("=" * 30)
        print("train.csv confusion matrix")
        print(self.conf_mx)

        # test.csv에 대한 confusion matrix
        self.pred_tree = self.model.predict(result.test_df_merge)
        self.conf_mx = confusion_matrix(result.test_df_y, self.pred_tree, normalize='true')
        print("=" * 30)
        print("test.csv confusion matrix")
        print(self.conf_mx)

if __name__ == "__main__":
    result = DataProcessing("./data/train.csv", "./data/test.csv")
    model_result = CatBoost()