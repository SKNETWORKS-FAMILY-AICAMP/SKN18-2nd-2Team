# 모델별 성능 확인 및 최적화

import lightgbm as lgb
import optuna
from catboost import CatBoostClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.model_selection import GridSearchCV, KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import xgboost
from utilities.utils import reset_seeds
from xgboost import XGBClassifier

import pickle

# 베이스 모델 생성

MODELS = {
    "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
    "RandomForest": RandomForestClassifier(random_state=42),
    "XGBoost": xgboost.XGBClassifier(
        random_state=42, eval_metric="logloss"
    ),
    "LightGBM": lgb.LGBMClassifier(random_state=42),
    "CatBoost": CatBoostClassifier(random_state=42, verbose=0),
    "SVC": SVC(probability=True, random_state=42),
    "ExtraTrees": ExtraTreesClassifier(random_state=42),
    "AdaBoost": AdaBoostClassifier(random_state=42),
    "HistGradientBoosting": HistGradientBoostingClassifier(random_state=42),
    "GradientBoosting": GradientBoostingClassifier(random_state=42),
    "KNeighbors": KNeighborsClassifier(),
    "RidgeClassifier": RidgeClassifier(random_state=42),
    "MLPClassifier": MLPClassifier(random_state=42, max_iter=1000),
}

# 하이퍼파라미터 범위지정
def __pre_hpo(trial, model_name, X, y):
    model = MODELS[model_name]
    # 주의 진짜 매우 아주 오래 걸림
    # 모델에 따라 하이퍼파라미터 범위 설정
    if model_name == "XGBoost":
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 40, 200),
            "max_depth": trial.suggest_int("max_depth", 2, 6),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "gamma": trial.suggest_float("gamma", 0.1, 5.0),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
        }
        model.set_params(**params)

    elif model_name in ["RandomForest", "ExtraTrees"]:
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 100, 500),
            "max_depth": trial.suggest_int("max_depth", 5, 20),
            "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
            "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 4),
        }
        model.set_params(**params)

    elif model_name == "LightGBM":
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "num_leaves": trial.suggest_int("num_leaves", 20, 150),
        }
        model.set_params(**params)

    elif model_name == "CatBoost":
        params = {
            "iterations": trial.suggest_int(
                "iterations", 50, 300
            ),  # 더 적은 범위로 줄임
            "learning_rate": trial.suggest_float(
                "learning_rate", 0.01, 0.3
            ),  # learning_rate 범위 조정
        }
        model.set_params(**params)

    elif model_name == "LogisticRegression":
        params = {"C": trial.suggest_float("C", 0.001, 10)}
        model.set_params(**params)

    elif model_name == "SVC":
        params = {
            "C": trial.suggest_float("C", 0.1, 10),
            "gamma": trial.suggest_float("gamma", 0.001, 1.0),
        }
        model.set_params(**params)

    elif model_name == "AdaBoost":
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 50, 500),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 1.0),
        }
        model.set_params(**params)

    elif model_name == "HistGradientBoosting":
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "max_depth": trial.suggest_int("max_depth", 3, 15),
        }
        model.set_params(**params)

    elif model_name == "GradientBoosting":
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 100, 500),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
            "max_depth": trial.suggest_int("max_depth", 3, 5),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        }
        model.set_params(**params)

    elif model_name == "KNeighbors":
        params = {
            "n_neighbors": trial.suggest_int("n_neighbors", 3, 15),
        }
        model.set_params(**params)

    elif model_name == "RidgeClassifier":
        params = {"alpha": trial.suggest_float("alpha", 0.1, 10.0)}
        model.set_params(**params)

    elif model_name == "MLPClassifier":
        params = {
            "alpha": trial.suggest_float("alpha", 0.0001, 0.01),
        }
        model.set_params(**params)

    pipeline = Pipeline(steps=[("model", model)])

    # 교차 검증을 통한 모델 성능 평가
    cv = KFold(n_splits=10, shuffle=True, random_state=42)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring="accuracy", n_jobs=-1)

    return scores.mean()

# 하이퍼 파라미터 최적화
def __run_prehpo(X_train_selected, y_train_smote):
    # 하이퍼파라미터 최적화 수행
    best_params = {}
    for model_name in MODELS.keys():
        try:
            study = optuna.create_study(direction="maximize")
            study.optimize(
                lambda trial: __pre_hpo(trial, model_name, X_train_selected, y_train_smote),
                n_trials=50,
                n_jobs=-1,
            )  # n_trials로 조절
            best_params[model_name] = study.best_params
            print(f"Best params for {model_name}: {best_params[model_name]}")
        except Exception as e:
            print(f"⚠️  Error optimizing {model_name}: {e}")
            best_params[model_name] = None
    
    return best_params

# gridsearchcv로 정밀하게 최적화
def __run_hpo(best_params, X_selected, y_smote):
    """
    주어진 모델들에 대해 GridSearchCV를 사용하여 최적의 하이퍼파라미터를 찾는 함수.

    Parameters:
    models (dict): 모델 이름과 모델 객체로 구성된 딕셔너리.
    best_params (dict): 각 모델에 대한 Optuna로 찾은 최적 파라미터.
    X_selected (DataFrame): 학습용 피처 데이터.
    y_smote (Series): 학습용 타겟 데이터.

    Returns:
    final_models (dict): 각 모델의 최적 하이퍼파라미터로 학습된 모델.
    """
    final_models = {}
    
    # best_params가 None인 경우 처리
    if best_params is None:
        print("⚠️  best_params가 None입니다. GridSearchCV를 건너뜁니다.")
        return final_models

    for model_name in MODELS.keys():
        # best_params에 해당 모델이 없거나 None인 경우 건너뛰기
        if model_name not in best_params or best_params[model_name] is None:
            print(f"⚠️  Skipping {model_name} - no best parameters found")
            continue
            
        print(f"\n🔧 GridSearchCV로 {model_name} 정밀 최적화 시작...")
        model = MODELS[model_name]

        # 각 모델에 따른 파라미터 그리드 설정
        if model_name in ["RandomForest", "ExtraTrees"]:
            param_grid = {
                "max_depth": [
                    max(1, best_params[model_name]["max_depth"] - 2),
                    best_params[model_name]["max_depth"],
                    best_params[model_name]["max_depth"] + 2,
                ],
                "min_samples_split": [
                    max(2, best_params[model_name]["min_samples_split"] - 1),
                    best_params[model_name]["min_samples_split"],
                    best_params[model_name]["min_samples_split"] + 1,
                ],
                "min_samples_leaf": [
                    best_params[model_name]["min_samples_leaf"] - 1,
                    best_params[model_name]["min_samples_leaf"],
                    best_params[model_name]["min_samples_leaf"] + 1,
                ],
            }

        elif model_name == "XGBoost":
            param_grid = {
                "subsample": [
                    best_params[model_name]["subsample"] * 0.8,
                    best_params[model_name]["subsample"],
                    best_params[model_name]["subsample"] * 1.2,
                ]
            }

        elif model_name == "LightGBM":
            param_grid = {
                "num_leaves": [
                    max(10, best_params[model_name]["num_leaves"] - 10),
                    best_params[model_name]["num_leaves"],
                    best_params[model_name]["num_leaves"] + 10,
                ]
            }

        elif model_name == "CatBoost":
            param_grid = {
                "learning_rate": [
                    best_params[model_name]["learning_rate"] * 0.8,
                    best_params[model_name]["learning_rate"],
                    best_params[model_name]["learning_rate"] * 1.2,
                ]
            }

        elif model_name == "LogisticRegression":
            param_grid = {
                "C": [
                    best_params[model_name]["C"] * 0.8,
                    best_params[model_name]["C"],
                    best_params[model_name]["C"] * 1.2,
                ]
            }

        elif model_name == "SVC":
            param_grid = {
                "C": [
                    best_params[model_name]["C"] * 0.8,
                    best_params[model_name]["C"],
                    best_params[model_name]["C"] * 1.2,
                ]
            }

        elif model_name == "AdaBoost":
            param_grid = {
                "learning_rate": [
                    best_params[model_name]["learning_rate"] * 0.8,
                    best_params[model_name]["learning_rate"],
                    best_params[model_name]["learning_rate"] * 1.2,
                ]
            }

        elif model_name == "HistGradientBoosting":
            param_grid = {
                "max_depth": [
                    max(1, best_params[model_name]["max_depth"] - 2),
                    best_params[model_name]["max_depth"],
                    best_params[model_name]["max_depth"] + 2,
                ]
            }

        elif model_name == "GradientBoosting":
            param_grid = {
                "max_depth": [
                    max(1, best_params[model_name]["max_depth"] - 2),
                    best_params[model_name]["max_depth"],
                    best_params[model_name]["max_depth"] + 2,
                ]
            }

        elif model_name == "KNeighbors":
            param_grid = {
                "n_neighbors": [
                    max(1, best_params[model_name]["n_neighbors"] - 1),
                    best_params[model_name]["n_neighbors"],
                    best_params[model_name]["n_neighbors"] + 1,
                ]
            }

        elif model_name == "RidgeClassifier":
            param_grid = {
                "alpha": [
                    best_params[model_name]["alpha"] * 0.8,
                    best_params[model_name]["alpha"],
                    best_params[model_name]["alpha"] * 1.2,
                ]
            }

        elif model_name == "MLPClassifier":
            param_grid = {
                "alpha": [
                    best_params[model_name]["alpha"] * 0.8,
                    best_params[model_name]["alpha"],
                    best_params[model_name]["alpha"] * 1.2,
                ]
            }

        # GridSearchCV 실행
        try:
            grid_search = GridSearchCV(
                estimator=model, param_grid=param_grid, cv=10, scoring="accuracy", n_jobs=-1
            )
            grid_search.fit(X_selected, y_smote)
            final_models[model_name] = grid_search.best_estimator_

            # 최적 하이퍼파라미터 및 교차 검증 정확도 출력
            print(f" {model_name} GridSearchCV 완료!")
            print(f" Best params for {model_name} after GridSearchCV: {grid_search.best_params_}")
            print(f" Best CV Accuracy for {model_name}: {grid_search.best_score_:.4f}")
        except Exception as e:
            print(f"  Error in GridSearchCV for {model_name}: {e}")
            continue

    return final_models

def __evaluate_validation_performance(final_models, X_validation, y_validation):
    """
    validation 데이터로 모델 성능을 평가하는 함수
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
    
    print("=" * 60)
    print("검증 데이터 성능 평가 결과")
    print("=" * 60)
    
    validation_results = []
    
    for model_name, model in final_models.items():
        try:
            # 예측 수행
            y_validation_pred = model.predict(X_validation)
            y_validation_proba = model.predict_proba(X_validation)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # 메트릭 계산
            accuracy = accuracy_score(y_validation, y_validation_pred)
            precision = precision_score(y_validation, y_validation_pred, average='weighted')
            recall = recall_score(y_validation, y_validation_pred, average='weighted')
            f1 = f1_score(y_validation, y_validation_pred, average='weighted')
            auc = roc_auc_score(y_validation, y_validation_proba) if y_validation_proba is not None else 0
            
            validation_results.append({
                'Model': model_name,
                'Validation_Accuracy': accuracy,
                'Validation_Precision': precision,
                'Validation_Recall': recall,
                'Validation_F1': f1,
                'Validation_AUC': auc
            })
            
            print(f"{model_name:<20} | Accuracy: {accuracy:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")
            
        except Exception as e:
            print(f"{model_name:<20} | 평가 실패: {e}")
    
    # 최고 성능 모델 찾기
    if validation_results:
        best_model = max(validation_results, key=lambda x: x['Validation_Accuracy'])
        print("=" * 60)
        print(f"최고 성능 모델 (검증 데이터 기준): {best_model['Model']}")
        print(f"검증 정확도: {best_model['Validation_Accuracy']:.4f}")
        print(f"검증 F1 점수: {best_model['Validation_F1']:.4f}")
        print(f"검증 AUC: {best_model['Validation_AUC']:.4f}")
        print("=" * 60)
    
    return validation_results

    # 베이스 모델 저장
def __save_models(final_models):
    # 모델들을 저장할 디렉토리 설정
    model_save_path = "./models/"
    
    # 디렉토리가 없으면 생성
    import os
    os.makedirs(model_save_path, exist_ok=True)

    # 모델 저장
    for model_name, model in final_models.items():
        try:
            file_path = f"{model_save_path}{model_name}.pkl"
            with open(file_path, "wb") as file:
                pickle.dump(model, file)
            print(f"Model {model_name} saved to {file_path}")
        except Exception as e:
            print(f" Error saving {model_name}: {e}")


@reset_seeds
def get_model(X_train=None, y_train=None, X_test=None, y_test=None, X_validation=None, y_validation=None, auto_load=True):
    """
    자동으로 데이터를 인식하고 모델을 학습하는 함수
    
    Parameters:
    X_train: 학습 피처 데이터 (DataFrame)
    y_train: 학습 타겟 데이터 (Series)
    X_test: 테스트 피처 데이터 (DataFrame, 선택사항)
    y_test: 테스트 타겟 데이터 (Series, 선택사항)
    X_validation: 검증 피처 데이터 (DataFrame, 선택사항)
    y_validation: 검증 타겟 데이터 (Series, 선택사항)
    auto_load: 데이터가 없을 때 자동 로드 여부 (기본값: True)
    
    Returns:
    final_models: 학습된 모델들의 딕셔너리
    """
    # 데이터가 제공되지 않은 경우 자동으로 로드
    if (X_train is None or y_train is None) and auto_load:
        print(" 데이터를 자동으로 로드합니다...")
        try:
            from utilities.preprocess import get_preprocessed_data
            X_train, X_test, y_train, X_validation, y_validation = get_preprocessed_data()
            print(f" 데이터 로드 완료: X_train shape={X_train.shape}, y_train shape={y_train.shape}")
            if X_validation is not None:
                print(f" 검증 데이터: X_validation shape={X_validation.shape}, y_validation shape={y_validation.shape}")
        except Exception as e:
            print(f"데이터 로드 실패: {e}")
            print("직접 데이터를 전달해주세요.")
            return {}
    elif X_train is None or y_train is None:
        print("데이터가 제공되지 않았습니다.")
        print(" X_train과 y_train을 직접 전달하거나 auto_load=True로 설정하세요.")
        return {}
    
    # 데이터 검증
    if X_train.shape[0] != y_train.shape[0]:
        raise ValueError(f"X_train과 y_train의 샘플 수가 일치하지 않습니다: X_train={X_train.shape[0]}, y_train={y_train.shape[0]}")
    
    if X_validation is not None and y_validation is not None:
        if X_validation.shape[0] != y_validation.shape[0]:
            raise ValueError(f"X_validation과 y_validation의 샘플 수가 일치하지 않습니다: X_validation={X_validation.shape[0]}, y_validation={y_validation.shape[0]}")
    
    print(f"모델 학습 시작...")
    print(f"학습 데이터 형태: {X_train.shape}")
    print(f"타겟 데이터 형태: {y_train.shape}")
    if X_validation is not None:
        print(f"검증 데이터 형태: {X_validation.shape}")
    
    # 하이퍼파라미터 최적화 및 모델 학습
    best_params = __run_prehpo(X_train, y_train)
    final_models = __run_hpo(best_params, X_train, y_train)
    
    # validation 데이터가 있는 경우 validation 성능 평가
    if X_validation is not None and y_validation is not None:
        print("\n검증 데이터로 모델 성능 평가 중...")
        __evaluate_validation_performance(final_models, X_validation, y_validation)
    
    __save_models(final_models)
    
    print(f" 모델 학습 완료! {len(final_models)}개의 모델이 저장되었습니다.")
    return final_models