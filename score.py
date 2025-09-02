# 시각화 파일

import pickle
import os
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns
from utilities.preprocess import get_preprocessed_data

def load_models():
    """
    models 폴더에서 저장된 모델들을 로드합니다.
    """
    models = {}
    model_path = "./models/"
    
    if not os.path.exists(model_path):
        print("models 폴더가 존재하지 않습니다.")
        return models
    
    # .pkl 파일들을 찾아서 로드
    for file in os.listdir(model_path):
        if file.endswith('.pkl'):
            model_name = file.replace('.pkl', '')
            try:
                with open(os.path.join(model_path, file), 'rb') as f:
                    models[model_name] = pickle.load(f)
                print(f" {model_name} 모델 로드 완료")
            except Exception as e:
                print(f" {model_name} 모델 로드 실패: {e}")
    
    return models

def evaluate_models(models, X_train, y_train, X_test=None, y_test=None):
    """
    모델들의 성능을 평가합니다.
    """
    results = []
    
    print("모델 성능 평가 시작...")
    print("=" * 80)
    
    for model_name, model in models.items():
        print(f"\n {model_name} 평가 중...")
        
        # 교차 검증 점수
        try:
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
        except Exception as e:
            print(f" 교차 검증 실패: {e}")
            cv_mean, cv_std = 0, 0
        
        # 학습 데이터에 대한 예측
        try:
            y_train_pred = model.predict(X_train)
            y_train_proba = model.predict_proba(X_train)[:, 1] if hasattr(model, 'predict_proba') else None
            
            # 메트릭 계산
            train_accuracy = accuracy_score(y_train, y_train_pred)
            train_precision = precision_score(y_train, y_train_pred, average='weighted')
            train_recall = recall_score(y_train, y_train_pred, average='weighted')
            train_f1 = f1_score(y_train, y_train_pred, average='weighted')
            train_auc = roc_auc_score(y_train, y_train_proba) if y_train_proba is not None else 0
            
        except Exception as e:
            print(f"학습 데이터 예측 실패: {e}")
            train_accuracy = train_precision = train_recall = train_f1 = train_auc = 0
        
        # 테스트 데이터가 있는 경우 테스트 성능도 평가
        test_accuracy = test_precision = test_recall = test_f1 = test_auc = 0
        if X_test is not None and y_test is not None:
            try:
                y_test_pred = model.predict(X_test)
                y_test_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
                
                test_accuracy = accuracy_score(y_test, y_test_pred)
                test_precision = precision_score(y_test, y_test_pred, average='weighted')
                test_recall = recall_score(y_test, y_test_pred, average='weighted')
                test_f1 = f1_score(y_test, y_test_pred, average='weighted')
                test_auc = roc_auc_score(y_test, y_test_proba) if y_test_proba is not None else 0
                
            except Exception as e:
                print(f"테스트 데이터 예측 실패: {e}")
        
        # 결과 저장
        result = {
            'Model': model_name,
            'CV_Accuracy_Mean': cv_mean,
            'CV_Accuracy_Std': cv_std,
            'Train_Accuracy': train_accuracy,
            'Train_Precision': train_precision,
            'Train_Recall': train_recall,
            'Train_F1': train_f1,
            'Train_AUC': train_auc,
            'Test_Accuracy': test_accuracy,
            'Test_Precision': test_precision,
            'Test_Recall': test_recall,
            'Test_F1': test_f1,
            'Test_AUC': test_auc
        }
        
        results.append(result)
        
        # 개별 모델 결과 출력
        print(f"   교차 검증 정확도: {cv_mean:.4f} (±{cv_std:.4f})")
        print(f"   학습 정확도: {train_accuracy:.4f}")
        print(f"   학습 F1 점수: {train_f1:.4f}")
        print(f"   학습 AUC: {train_auc:.4f}")
        if X_test is not None:
            print(f"   테스트 정확도: {test_accuracy:.4f}")
            print(f"   테스트 F1 점수: {test_f1:.4f}")
            print(f"   테스트 AUC: {test_auc:.4f}")
    
    return pd.DataFrame(results)

def create_visualizations(results_df):
    """
    결과를 시각화합니다.
    """
    print("\n시각화 생성 중...")
    
    # 결과 폴더 생성
    os.makedirs('./result', exist_ok=True)
    
    # 모델 이름을 짧게 줄이기
    model_short_names = {
        'AdaBoost': 'Ada',
        'CatBoost': 'Cat',
        'ExtraTrees': 'ET',
        'GradientBoosting': 'GB',
        'HistGradientBoosting': 'HGB',
        'KNeighbors': 'KNN',
        'LightGBM': 'LGB',
        'LogisticRegression': 'LR',
        'MLPClassifier': 'MLP',
        'RandomForest': 'RF',
        'RidgeClassifier': 'Ridge',
        'SVC': 'SVC',
        'XGBoost': 'XGB'
    }
    
    # 짧은 이름으로 변경
    results_df['Model_Short'] = results_df['Model'].map(model_short_names)
    
    # 색상 팔레트 설정 (더 명확한 색상)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
              '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
              '#F8C471', '#82E0AA', '#F1948A']
    
    # 1. CV 정확도 막대 차트 (수평으로 배치하여 글자 겹침 방지)
    plt.figure(figsize=(16, 10))
    
    # 성능 순으로 정렬
    ranked_df = results_df.sort_values('CV_Accuracy_Mean', ascending=True)
    
    # 수평 막대 차트
    bars = plt.barh(ranked_df['Model_Short'], ranked_df['CV_Accuracy_Mean'], color=colors)
    plt.title('Cross-Validation Accuracy Ranking', fontsize=20, fontweight='bold', pad=20)
    plt.xlabel('CV Accuracy', fontsize=14, fontweight='bold')
    plt.ylabel('Models', fontsize=14, fontweight='bold')
    
    # Y축 범위 설정 (전체 범위 사용)
    plt.xlim(0.8, 1.0)
    
    # 값 표시 (큰 폰트)
    for bar, value, std in zip(bars, ranked_df['CV_Accuracy_Mean'], ranked_df['CV_Accuracy_Std']):
        plt.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2, 
                f'{value:.4f} (±{std:.4f})', ha='left', va='center', 
                fontsize=12, fontweight='bold')
    
    # 격자 추가
    plt.grid(True, alpha=0.3, axis='x')
    
    # 최고 성능 모델 강조
    best_model = ranked_df.iloc[-1]
    best_bar = bars[-1]
    best_bar.set_color('#FF6B6B')  # 빨간색으로 강조
    best_bar.set_edgecolor('black')
    best_bar.set_linewidth(2)
    
    # 최고 성능 표시
    plt.text(best_bar.get_width() + 0.001, best_bar.get_y() + best_bar.get_height()/2, 
            f' BEST: {best_model["CV_Accuracy_Mean"]:.4f}', ha='left', va='center', 
            fontsize=14, fontweight='bold', color='red')
    
    plt.tight_layout()
    plt.savefig('./result/cv_accuracy_ranking.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 2. 성능 차이 시각화 (최고 성능 대비)
    plt.figure(figsize=(16, 10))
    
    max_accuracy = results_df['CV_Accuracy_Mean'].max()
    performance_diff = (results_df['CV_Accuracy_Mean'] - max_accuracy) * 10000  # 차이를 10000배 확대
    
    # 성능 차이로 정렬
    diff_df = results_df.copy()
    diff_df['Performance_Diff'] = performance_diff
    diff_df = diff_df.sort_values('Performance_Diff', ascending=True)
    
    # 색상 설정 (차이가 클수록 빨간색)
    colors_diff = ['red' if diff < 0 else 'lightblue' for diff in diff_df['Performance_Diff']]
    
    bars = plt.barh(diff_df['Model_Short'], diff_df['Performance_Diff'], color=colors_diff)
    plt.title('Performance Difference from Best Model (×10000)', fontsize=20, fontweight='bold', pad=20)
    plt.xlabel('Difference from Best', fontsize=14, fontweight='bold')
    plt.ylabel('Models', fontsize=14, fontweight='bold')
    
    # 0선 추가
    plt.axvline(x=0, color='black', linestyle='--', linewidth=2, alpha=0.7)
    
    # 값 표시
    for bar, value, acc in zip(bars, diff_df['Performance_Diff'], diff_df['CV_Accuracy_Mean']):
        if value == 0:
            plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, 
                    f'BEST: {acc:.4f}', ha='left', va='center', 
                    fontsize=12, fontweight='bold', color='red')
        else:
            plt.text(bar.get_width() + (5 if value > 0 else -5), bar.get_y() + bar.get_height()/2, 
                    f'{value:.0f}', ha='left' if value > 0 else 'right', va='center', 
                    fontsize=11, fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('./result/performance_difference.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # 추가: 성능 차이 분석
    print("\n 성능 차이 분석")
    print("=" * 60)
    max_acc = results_df['CV_Accuracy_Mean'].max()
    min_acc = results_df['CV_Accuracy_Mean'].min()
    print(f"최고 성능: {max_acc:.4f}")
    print(f"최저 성능: {min_acc:.4f}")
    print(f"성능 차이: {(max_acc - min_acc) * 100:.2f}%")
    print(f"표준편차: {results_df['CV_Accuracy_Mean'].std():.4f}")
    
    # 상위 모델 순위표
    print("\n모델 순위 (교차 검증 정확도 기준)")
    print("=" * 60)
    ranked_models = results_df.sort_values('CV_Accuracy_Mean', ascending=False)
    for i, (_, row) in enumerate(ranked_models.iterrows(), 1):
        diff_from_best = (max_acc - row['CV_Accuracy_Mean']) * 10000
        print(f"{i:2d}. {row['Model']:<20} CV_Acc: {row['CV_Accuracy_Mean']:.4f} (±{row['CV_Accuracy_Std']:.4f}) [차이: {diff_from_best:.0f}]")

def save_results(results_df):
    """
    결과를 CSV 파일로 저장합니다.
    """
    # 결과 폴더 생성
    os.makedirs('./result', exist_ok=True)
    
    # CSV로 저장
    csv_path = './result/model_evaluation_results.csv'
    results_df.to_csv(csv_path, index=False)
    print(f"\n 결과가 {csv_path}에 저장되었습니다.")
    
    # 요약 통계
    summary_path = './result/model_summary.txt'
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("Netflix 고객 이탈 예측 모델 성능 평가 결과\n")
        f.write("=" * 50 + "\n\n")
        
        # 최고 성능 모델
        best_cv = results_df.loc[results_df['CV_Accuracy_Mean'].idxmax()]
        f.write(f" 최고 성능 모델 (교차 검증 기준): {best_cv['Model']}\n")
        f.write(f"   교차 검증 정확도: {best_cv['CV_Accuracy_Mean']:.4f} (±{best_cv['CV_Accuracy_Std']:.4f})\n")
        f.write(f"   학습 정확도: {best_cv['Train_Accuracy']:.4f}\n")
        f.write(f"   학습 F1 점수: {best_cv['Train_F1']:.4f}\n")
        f.write(f"   학습 AUC: {best_cv['Train_AUC']:.4f}\n\n")
        
        # 전체 통계
        f.write(" 전체 모델 통계:\n")
        f.write(f"   평균 교차 검증 정확도: {results_df['CV_Accuracy_Mean'].mean():.4f}\n")
        f.write(f"   최고 교차 검증 정확도: {results_df['CV_Accuracy_Mean'].max():.4f}\n")
        f.write(f"   최저 교차 검증 정확도: {results_df['CV_Accuracy_Mean'].min():.4f}\n")
        f.write(f"   표준편차: {results_df['CV_Accuracy_Mean'].std():.4f}\n\n")
        
        # 상위 3개 모델
        f.write(" 상위 3개 모델:\n")
        top_3 = results_df.nlargest(3, 'CV_Accuracy_Mean')
        for i, (_, row) in enumerate(top_3.iterrows(), 1):
            f.write(f"   {i}. {row['Model']}: {row['CV_Accuracy_Mean']:.4f}\n")
    
    print(f" 요약이 {summary_path}에 저장되었습니다.")

def main():
    """
    메인 함수
    """
    print(" Netflix 고객 이탈 예측 모델 성능 평가 시작!")
    print("=" * 60)
    
    # 1. 모델 로드
    print(" 저장된 모델들을 로드합니다...")
    models = load_models()
    
    if not models:
        print(" 로드할 모델이 없습니다. 먼저 모델을 학습해주세요.")
        return
    
    print(f" {len(models)}개의 모델이 로드되었습니다.")
    
    # 2. 데이터 로드
    print("\n 데이터를 로드합니다...")
    try:
        X_train, X_test, y_train = get_preprocessed_data()
        print(f"데이터 로드 완료: X_train shape={X_train.shape}")
    except Exception as e:
        print(f" 데이터 로드 실패: {e}")
        return
    
    # 3. 모델 평가
    results_df = evaluate_models(models, X_train, y_train, X_test, y_train)  # 테스트 데이터는 학습 데이터로 대체
    
    # 4. 결과 저장
    save_results(results_df)
    
    # 5. 시각화
    create_visualizations(results_df)
    
    print("\n 모델 성능 평가가 완료되었습니다!")
    print(" 결과 파일들이 './result/' 폴더에 저장되었습니다.")

if __name__ == "__main__":
    main()
