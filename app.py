# 메인 파일

from utilities.model import get_model

def main():
    """
    자동으로 데이터를 로드하고 모델을 학습하는 메인 함수
    """
    print("모델 학습 시작!")
    print("=" * 50)
    
    # 자동으로 데이터를 로드하고 모델 학습
    final_models = get_model()
    
    print("=" * 50)
    print("작업 끝!")
    print(f"모델들이 './models/' 폴더에 저장되었습니다.")

if __name__ == "__main__":
    main()

