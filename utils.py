import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance

def load_data(train_path, test_path):
    train_df = pd.read_csv(train_path)
    test_df  = pd.read_csv(test_path)
    return train_df, test_df


def _get_feature_names_from_pre(pre, input_cols):
    """
    ColumnTransformer(=pre)가 fit된 뒤, 변환 후 피처 이름 반환.
    OneHotEncoder가 있으면 'cat__col_category' 형식으로 풀려서 나옴.
    """
    try:
        return pre.get_feature_names_out(input_cols)
    except Exception:
        # 구버전 호환 or 실패 시 기본 f0,f1,... 반환
        n_out = pre.transform(pd.DataFrame(columns=input_cols)).shape[1]
        return np.array([f"f{i}" for i in range(n_out)])

def _extract_importances_from_estimator(estimator, feat_names):
    """
    모델에서 중요도(또는 계수)를 추출해 (names, importances)로 반환.
    사용 가능 순서:
      1) XGBoost: booster.get_score('gain') → f{idx} 매핑
      2) feature_importances_ (트리, LGBM, CatBoost 등)
      3) coef_ (선형/다중클래스 → 절댓값 평균)
      4) 실패 시 None
    """
    # XGBoost (booster gain, f{index} → 이름 매핑 필요)
    try:
        from xgboost import XGBClassifier as _XGB
        if isinstance(estimator, _XGB):
            fmap = estimator.get_booster().get_score(importance_type="gain")
            items = []
            for k, v in fmap.items():
                # k like 'f123'
                try:
                    idx = int(k[1:])
                    name = feat_names[idx] if idx < len(feat_names) else k
                except Exception:
                    name = k
                items.append((name, float(v)))
            if items:
                items.sort(key=lambda x: x[1], reverse=True)
                names, imps = zip(*items)
                return np.array(names), np.array(imps, dtype=float)
    except Exception:
        pass

    # feature_importances_ (Tree 계열 / LGBM / CatBoost 등)
    if hasattr(estimator, "feature_importances_"):
        imps = np.asarray(estimator.feature_importances_, dtype=float)
        # 길이 맞추기
        if len(imps) == len(feat_names):
            return np.array(feat_names), imps

    # coef_ (선형 모델 / Linear SVM 등)
    if hasattr(estimator, "coef_"):
        co = np.asarray(estimator.coef_, dtype=float)
        # 다중 클래스 → 클래스축 평균(절댓값)
        if co.ndim == 2:
            imps = np.mean(np.abs(co), axis=0)
        else:
            imps = np.abs(co)
        if len(imps) == len(feat_names):
            return np.array(feat_names), imps

    return None, None

def save_feature_importances_from_pipeline(pipe, model_name, X_val, y_val, out_png, top_k=30, random_state=42):
    """
    학습된 imblearn.Pipeline(pipe)에서 피처 중요도 그래프 저장.
    1) 전처리 스텝에서 피처 이름 추출
    2) 최종 모델에서 중요도/계수 추출 시도
    3) 안되면 permutation importance(Validation set, n_repeats=5)
    """
    os.makedirs(os.path.dirname(out_png), exist_ok=True)

    # 1) 피처 이름
    pre = pipe.named_steps.get("pre") or pipe.named_steps.get("pre_after") or pipe.named_steps.get("pre_for_smote")
    if pre is None:
        print(f"[WARN] {model_name}: 전처리 스텝을 찾지 못해 피처 이름을 만들 수 없습니다.")
        return

    # X_val는 DataFrame이어야 이름 매칭이 정확함
    feat_names = _get_feature_names_from_pre(pre, list(X_val.columns))

    # 2) 모델에서 직접 추출
    estimator = pipe.named_steps["model"]
    names, imps = _extract_importances_from_estimator(estimator, feat_names)

    # 3) 실패 시 permutation importance
    if names is None or imps is None:
        try:
            perm = permutation_importance(pipe, X_val, y_val, n_repeats=5, random_state=random_state, n_jobs=-1)
            imps = perm.importances_mean
            names = feat_names
        except Exception as e:
            print(f"[WARN] {model_name}: permutation importance 실패: {e}")
            return

    # 상위 top_k 선택
    order = np.argsort(imps)[::-1][:top_k]
    names_top = np.array(names)[order]
    imps_top = np.array(imps)[order]

    # 0만 있는 경우 대비
    if np.allclose(imps_top, 0):
        print(f"[INFO] {model_name}: 중요도가 모두 0에 가까워 그래프 저장을 생략합니다.")
        return

    # 플롯
    plt.figure(figsize=(10, max(4, 0.25 * len(names_top))))
    plt.barh(range(len(imps_top)), imps_top)
    plt.gca().invert_yaxis()
    plt.yticks(range(len(names_top)), names_top)
    plt.xlabel("Importance")
    plt.title(f"Top Feature Importances — {model_name}")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def write_result(results):
    os.makedirs("./images", exist_ok=True)
    with open("./images/training_report.txt", "w", encoding="utf-8") as f:
        for r in results:
            f.write(
                f"{r['model']}\n"
                f"Validation Accuracy: {r['val_acc']:.4f}\n"
                f"Validation Macro-F1: {r['val_f1']:.4f}\n\n"
                f"Test Accuracy: {r['test_acc']:.4f}\n"
                f"Test Macro-F1: {r['test_f1']:.4f}\n\n"
            )

def save_results_plot(results, out_path="./images/model_performance.png"):
    """
    모델별 성능(Accuracy)을 비교하는 그래프 저장
    """
    models = [r["model"] for r in results]
    test_acc = [r["test_acc"] for r in results]

    x = range(len(models))
    bar_width = 0.2

    plt.figure(figsize=(12, 6))
    
    # Accuracy
    accuracy_bar = plt.bar([i - bar_width*0.5 for i in x], test_acc, width=bar_width, label="Test Accuracy")


    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width()/2, height + 0.01,  # 위치
                f"{height:.4f}", ha="center", va="bottom", fontsize=8
            )
    add_labels(accuracy_bar)

    plt.xticks(x, models, rotation=45, ha="right")
    plt.ylabel("Score")
    plt.title("모델 정확도 비교")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

