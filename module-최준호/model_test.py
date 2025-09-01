class Model_Evaluation():

    def __init__(self, result):
        self.catboost_model = Catboost.CallCatboost(result) # 평가할 모델 호출
        print(f'훈련용 평가지표: {self.catboost_model.score(result.train_final, result.y_train)} / 테스트용 평가지표: {self.catboost_model.score(result.test_final, result.y_test)}')

        # test.csv에 대한 성능평가
        print(f'test.csv 평가지표: {self.catboost_model.score(result.test_df_final, result.test_df_y)}')
        # train.csv에 대한 roc_curve
        print(f"train.csv에 대한 로컬PC Score: {self.do_roc_curve(self.catboost_model, result.test_final, result.y_test)}")
        # test.csv에 대한 roc_curve
        print(f"test.csv에 대한 로컬PC Score: {self.do_roc_curve(self.catboost_model, result.test_df_final, result.test_df_y)}")

        # train.csv에 대한 confusion matrix
        print("=" * 30)
        print("train.csv confusion matrix")
        print(self.do_confusion_matrix(self.catboost_model, result.test_final, result.y_test))

        # test.csv에 대한 confusion matrix
        print("=" * 30)
        print("test.csv confusion matrix")
        print(self.do_confusion_matrix(self.catboost_model, result.test_df_final, result.test_df_y))

        # 훈련 데이터 f1 evaluation 결과
        self.val_acc, self.val_f1, self.val_report = self.get_f1_evaluation(self.catboost_model, result.test_final, result.y_test)
        print("=" * 30)
        print("validation Accuracy:", self.val_acc)
        print("validation Macro-F1:", self.val_f1)
        print(self.val_report)

        # 테스트 데이터 f1 evaluation 결과
        self.val_acc, self.val_f1, self.val_report = self.get_f1_evaluation(self.catboost_model, result.test_df_final, result.test_df_y)
        print("=" * 30)
        print("validation Accuracy:", self.val_acc)
        print("validation Macro-F1:", self.val_f1)
        print(self.val_report)
    
    # train.csv에 대한 roc_curve
    def do_roc_curve(self, model, test, predict):
        from sklearn.metrics import roc_curve, auc

        self.y_predict = model.predict(test)
        self.fpr, self.tpr, self.thresholds = roc_curve(predict, self.y_predict)

        self.score_auc = auc(self.fpr, self.tpr)

        return self.score_auc
    
    # confusion matrix
    def do_confusion_matrix(self, model, test_final, y_test):
        from sklearn.metrics import confusion_matrix
        self.pred_tree = model.predict(test_final)
        self.conf_mx = confusion_matrix(y_test, self.pred_tree, normalize='true')

        return self.conf_mx
    
    # f1-score 지수 평가
    def get_f1_evaluation(self, model, df_final, y_final):
        from sklearn.metrics import accuracy_score, f1_score, classification_report

        # 훈련 데이터 평가
        self.y_pred = model.predict(df_final)
        self.val_acc = accuracy_score(y_final, self.y_pred)
        self.val_f1 = f1_score(y_final, self.y_pred, average="macro")
        self.val_report = classification_report(y_final, self.y_pred)

        return self.val_acc, self.val_f1, self.val_report

class Catboost():

    def CallCatboost(result):
        from catboost import CatBoostClassifier

        model = CatBoostClassifier(verbose=False, random_state=result.SEED)
        model.fit(result.train_final, result.y_train)

        return model

if __name__ == "__main__":
    from eda import DataProcessing
    
    result = DataProcessing("./data/train.csv", "./data/test.csv")
    call_model = Catboost() # 평가할 모델 설정
    model_test = Model_Evaluation(result)