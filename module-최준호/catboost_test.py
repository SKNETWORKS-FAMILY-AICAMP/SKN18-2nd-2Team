from eda import DataProcessing

class CatBoost():

    def __init__(self):

        from catboost import CatBoostClassifier

        self.model = CatBoostClassifier(verbose=False, random_state=result.SEED)
        self.model.fit(result.train_final, result.y_train)
        print(f'훈련용 평가지표: {self.model.score(result.train_final, result.y_train)} / 테스트용 평가지표: {self.model.score(result.test_final, result.y_test)}')

        # test.csv에 대한 성능평가
        print(f'test.csv 평가지표: {self.model.score(result.test_df_final, result.test_df_y)}')

        # train.csv에 대한 roc_curve
        from sklearn.metrics import roc_curve, auc

        self.y_pred = self.model.predict_proba(result.test_final)[:,1]
        self.y_predict_train = self.model.predict(result.test_final)
        self.fpr, self.tpr, self.thresholds = roc_curve(result.y_test, self.y_predict_train)

        self.score_auc = auc(self.fpr, self.tpr)
        print(f"train.csv에 대한 로컬PC Score: {self.score_auc}")

        # test.csv에 대한 roc_curve

        self.y_pred = self.model.predict_proba(result.test_df_final)[:,1]
        self.y_predict_test = self.model.predict(result.test_df_final)
        self.fpr, self.tpr, self.thresholds = roc_curve(result.test_df_y, self.y_predict_test)

        self.score_auc = auc(self.fpr, self.tpr)
        print(f"test.csv에 대한 로컬PC Score: {self.score_auc}")

        # train.csv에 대한 confusion matrix
        from sklearn.metrics import confusion_matrix

        self.pred_tree = self.model.predict(result.test_final)
        self.conf_mx = confusion_matrix(result.y_test, self.pred_tree, normalize='true')
        print("=" * 30)
        print("train.csv confusion matrix")
        print(self.conf_mx)

        # test.csv에 대한 confusion matrix

        self.pred_tree = self.model.predict(result.test_df_final)
        self.conf_mx = confusion_matrix(result.test_df_y, self.pred_tree, normalize='true')
        print("=" * 30)
        print("test.csv confusion matrix")
        print(self.conf_mx)

if __name__ == "__main__":
    result = DataProcessing("./data/train.csv", "./data/test.csv")
    model_result = CatBoost()