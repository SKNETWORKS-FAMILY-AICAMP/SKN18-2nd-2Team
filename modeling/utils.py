import numpy as np
import pandas as pd
import os
import json

import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance

def load_data(train_path, test_path):
    train_df = pd.read_csv(train_path)
    test_df  = pd.read_csv(test_path)
    return train_df, test_df

def get_config():
    with open("../config.json", encoding="UTF-8") as f:
        config = json.load(f)
    return config

def save_permutation_importance_original(pipe, model_name, X_val, y_val, out_png, top_k=30, random_state=42):
    """
    파이프라인 단위 permutation importance를 이용해
    '원본 컬럼' 기준의 중요도 그래프 저장.
    (인코더 이전의 DataFrame 컬럼을 한 번에 섞기 때문에 자동으로 그룹화 효과)
    """
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    try:
        perm = permutation_importance(
            pipe, X_val, y_val, n_repeats=10, random_state=random_state, n_jobs=-1
        )
        names = np.array(X_val.columns)
        imps = perm.importances_mean

        order = np.argsort(imps)[::-1][:top_k]
        names_top = names[order]
        imps_top = imps[order]

        if np.allclose(imps_top, 0):
            print(f"[INFO] {model_name}: (원본 기준) 중요도가 모두 0에 가까워 그래프 저장을 생략합니다.")
            return

        plt.figure(figsize=(10, max(4, 0.25 * len(names_top))))
        plt.barh(range(len(imps_top)), imps_top)
        plt.gca().invert_yaxis()
        plt.yticks(range(len(names_top)), names_top)
        plt.xlabel("Permutation Importance (mean decrease in score)")
        plt.title(f"Top Feature Importances (Original Columns) — {model_name}")
        plt.tight_layout()
        plt.savefig(out_png)
        plt.close()
    except Exception as e:
        print(f"[WARN] {model_name}: (원본 기준) permutation importance 실패: {e}")

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

