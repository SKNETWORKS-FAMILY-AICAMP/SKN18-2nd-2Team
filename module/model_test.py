class Model_Evaluation():

    def __init__(self, result, call_model):
        self.call_model = call_model # 평가할 모델 호출
        print(f'훈련용 평가지표: {self.call_model.score(result.train_final, result.y_train)} / 테스트용 평가지표: {self.call_model.score(result.test_final, result.y_test)}')

        # test.csv에 대한 성능평가
        print(f'test.csv 평가지표: {self.call_model.score(result.test_df_final, result.test_df_y)}')
        # train.csv에 대한 roc_curve
        print(f"train.csv에 대한 로컬PC Score: {self.do_roc_curve(self.call_model, result.test_final, result.y_test)}")
        # test.csv에 대한 roc_curve
        print(f"test.csv에 대한 로컬PC Score: {self.do_roc_curve(self.call_model, result.test_df_final, result.test_df_y)}")

        # train.csv에 대한 confusion matrix
        print("=" * 30)
        print("train.csv confusion matrix")
        print(self.do_confusion_matrix(self.call_model, result.test_final, result.y_test))

        # test.csv에 대한 confusion matrix
        print("=" * 30)
        print("test.csv confusion matrix")
        print(self.do_confusion_matrix(self.call_model, result.test_df_final, result.test_df_y))

        # 훈련 데이터 f1 evaluation 결과
        self.val_acc, self.val_f1, self.val_report = self.get_f1_evaluation(self.call_model, result.test_final, result.y_test)
        print("=" * 30)
        print("train_data f1 evaluation")
        print("validation Accuracy:", self.val_acc)
        print("validation Macro-F1:", self.val_f1)
        print(self.val_report)

        # 테스트 데이터 f1 evaluation 결과
        self.val_acc, self.val_f1, self.val_report = self.get_f1_evaluation(self.call_model, result.test_df_final, result.test_df_y)
        print("=" * 30)
        print("test_data f1 evaluation")
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
    
class RandomForest():

    def CallRandomForest(result):
        from sklearn.ensemble import RandomForestClassifier

        model_rf = RandomForestClassifier(random_state=result.SEED)
        model_rf = model_rf.fit(result.train_final, result.y_train)

        return model_rf
    
class XGBoost():

    def CallXGBoost(result):
        from xgboost import XGBClassifier

        model_xgb = XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        random_state=result.SEED,
        n_jobs=-1
        )
        model_xgb = model_xgb.fit(result.train_final, result.y_train)

        return model_xgb
    
class LightGBM():

    def CallLightGBM(result):
        import lightgbm as lgb

        model_lgbm = lgb.LGBMClassifier(random_state=result.SEED)
        model_lgbm.fit(result.train_final, result.y_train)

        return model_lgbm

if __name__ == "__main__":
    from eda import DataProcessing
    
    result = DataProcessing("./data/train.csv", "./data/test.csv")
    # 테스트 모델명과 모델 호출 방식에 대한 dict타입 input
    model_call = {
        "catboost":Catboost.CallCatboost(result),
        "RandomForest":RandomForest.CallRandomForest(result),
        "XGBoost":XGBoost.CallXGBoost(result),
        "LightGBM":LightGBM.CallLightGBM(result)
    }
    # 모든 모델에 대한 테스트 결과 출력
    for i in model_call.keys():
        call_model = model_call[i]
        print(f"<{i}>의 성능결과")
        print("#" * 30)
        Model_Evaluation(result, call_model)
