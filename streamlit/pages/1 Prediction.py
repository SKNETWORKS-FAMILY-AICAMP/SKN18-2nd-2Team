import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from utils import get_config
from model import load_saved_model
from preprocess import feature_engineering
from database import Database

import streamlit as st
from sidebar_utils import setup_shared_sidebar


#####################################
# 고객 이탈 확률 예측 페이지 만들기 #
#####################################

# 1. 고객 데이터를 입력하는 폼 만들기
# 2. 고객 선택
# 3. 이탈 확률을 예측하기
#     - 입력된 고객데이터를 통해 모델 예측 결과를 표시하기
# 4. 고객 정보 및 시각화
#     - 고객 정보와 모델예측 결과를 표시
# 5. 이탈 사유 표시
#     - 예측 결과에 따른 주요 이탈 행동요인을 텍스트 혹은 그래프로 표시
# 기본 sidebar 없애기

<<<<<<< HEAD
=======
# --- 페이지 진입 시 세션 리셋: 다른 페이지에서 들어왔을 때만 ---
prev_page = st.session_state.get("current_page")
st.session_state["current_page"] = "prediction"

if prev_page != "prediction":
    for key in ("sample_id_selected", "list_customer_selected",
                "selected_customer_id", "search_executed"):
        st.session_state.pop(key, None)


>>>>>>> dev
def show_prediction_prob(user_info):
    # --------------------------
    # 예측 결과 출력 (모델 사용)
    # --------------------------
    if not user_info.empty:
        customer = user_info.iloc[0]
        st.subheader("예측 결과")
        try:
            # 1) 고객 데이터 준비
            try:
                X_customer = user_info.copy().drop(columns=["churned"])
            except:
                X_customer = feature_engineering(user_info)
            else:
                X_customer = feature_engineering(X_customer)
    
            # 2) 선택된 모델 불러오기
            pipe = load_saved_model(model_name)

            # 3) 예측 확률 얻기
            churn_proba = pipe.predict_proba(X_customer)[0][1] * 100
            retention_proba = 100 - churn_proba
        except Exception as e:
            st.error(f"모델 예측 실패: {e}")
    return customer, churn_proba, retention_proba

def show_prediction_bar(churn_proba, retention_proba):
    # 위험도에 따른 동적 색상 설정
    if churn_proba >= 70:
        churn_color = "#DC143C"  # 진한 빨간색 (매우 위험)
        risk_emoji = "🔴"
    elif churn_proba >= 50:
        churn_color = "#FF4500"  # 주황빨간색 (높은 위험)
        risk_emoji = "🟠"
    elif churn_proba >= 30:
        churn_color = "#FF6347"  # 토마토색 (보통 위험)
        risk_emoji = "🟡"
    else:
        churn_color = "#32CD32"  # 라임그린 (낮은 위험)
        risk_emoji = "🟢"
    
    # 색상으로 구분된 차트 (CSS 스타일 사용)
    st.markdown(f"""
    <style>
    .churn-bar {{
        background-color: {churn_color};
        color: white;
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    .retention-bar {{
        background-color: #1f77b4;
        color: white;
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .probability-container {{
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }}
    </style>
    """, unsafe_allow_html=True)
    
<<<<<<< HEAD
    # 확률 표시 컨테이너
    # st.markdown('<div class="probability-container">', unsafe_allow_html=True)
    
=======
>>>>>>> dev
    # 이탈 확률 바 (동적 크기)
    churn_width = max(80, int(churn_proba * 4))  # 최소 80px, 최대 380px
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 15px 0;">
        <div style="width: 100px; font-weight: bold; font-size: 16px;">{risk_emoji} 이탈:</div>
        <div class="churn-bar" style="width: {churn_width}px; min-width: 100px;">
            {churn_proba:.4f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 유지 확률 바 (동적 크기)
    retention_width = max(80, int(retention_proba * 4))  # 최소 80px, 최대 380px
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin: 15px 0;">
        <div style="width: 100px; font-weight: bold; font-size: 16px;">✅ 유지:</div>
        <div class="retention-bar" style="width: {retention_width}px; min-width: 100px;">
            {retention_proba:.4f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def filter_customer():
    st.write("**고객 목록에서 선택하세요:**")
    st.write("")

    # 필터링 옵션
    col1, col2, col3 = st.columns(3)
    with col1:
        region_filter = st.selectbox("지역", ["전체"] + sorted(df['region'].unique().tolist()))
    with col2:
        subscription_filter = st.selectbox("구독 타입", ["전체"] + sorted(df['subscription_type'].unique().tolist()))
    with col3:
        gender_filter = st.selectbox("성별", ["전체"] + sorted(df['gender'].unique().tolist()))

    col4, col5, col6 = st.columns(3)
    with col4:
        device_filter = st.selectbox("디바이스", ["전체"] + sorted(df['device'].unique().tolist()))
    with col5:
        payment_filter = st.selectbox("결제 방법", ["전체"] + sorted(df['payment_method'].unique().tolist()))
    with col6:
        genre_filter = st.selectbox("선호 장르", ["전체"] + sorted(df['favorite_genre'].unique().tolist()))


    # 필터 적용
    filtered_df = df.copy()

    if region_filter != "전체":
        filtered_df = filtered_df[filtered_df['region'] == region_filter]

    if subscription_filter != "전체":
        filtered_df = filtered_df[filtered_df['subscription_type'] == subscription_filter]

    if gender_filter != "전체":
        filtered_df = filtered_df[filtered_df['gender'] == gender_filter]

    if device_filter != "전체":
        filtered_df = filtered_df[filtered_df['device'] == device_filter]

    if payment_filter != "전체":
        filtered_df = filtered_df[filtered_df['payment_method'] == payment_filter]

    if genre_filter != "전체":
        filtered_df = filtered_df[filtered_df['favorite_genre'] == genre_filter]


    # 고객 정보를 보기 좋게 표시하기 위한 포맷팅
    customer_options = []
    customer_mapping = {}

    # 최대 100명까지 표시
    display_df = filtered_df.head(100)

    if len(display_df) == 0:
        st.warning("선택한 조건에 맞는 고객이 없습니다.")
    else:
        st.info(f"조건에 맞는 고객 {len(filtered_df)}명 중 {len(display_df)}명을 표시합니다.")
        
        for idx, row in display_df.iterrows():
            display_text = f"{row['customer_id'][:8]}... | {row['age']}세 {row['gender']} | {row['subscription_type']} | {row['region']} | {row['device']} | {row['payment_method']} | {row['favorite_genre']}"
            customer_options.append(display_text)
            customer_mapping[display_text] = row['customer_id']
        
        selected_customer_display = st.selectbox(
            "고객 선택",
            options=["선택하세요..."] + customer_options,
            key="customer_selectbox"
        )

        if selected_customer_display != "선택하세요...":
            # 이전에 선택된 고객과 다른 경우에만 상태 업데이트
            selected_id = customer_mapping[selected_customer_display]
            if st.session_state.list_customer_selected != selected_id:
                st.session_state.list_customer_selected = selected_id
                st.session_state.selected_customer_id = ""
                st.session_state.search_executed = False
                # 목록에서 선택했을 때는 샘플 ID도 초기화하여 새로운 선택이 위에 반영되도록 함
                st.session_state.sample_id_selected = ""

    # 직접 입력, 샘플 ID 선택, 또는 고객 목록 선택 결과 처리
    if st.session_state.search_executed and st.session_state.selected_customer_id:
        customer_id_input = st.session_state.selected_customer_id
    elif st.session_state.sample_id_selected:
        customer_id_input = st.session_state.sample_id_selected  # 샘플 ID도 아래에 상세 표시
    elif st.session_state.list_customer_selected:
        customer_id_input = st.session_state.list_customer_selected
    else:
        customer_id_input = ""
    return filtered_df[filtered_df['customer_id']==customer_id_input]

def analize_churn_customer(customer, churn_rate):
    # 이탈 위험 요소 분석
    st.subheader("🚨 주요 위험 요소 분석")
    
    risk_factors = []
    protection_factors = []
    
    # 위험 요소 분석
    if customer['payment_method'] == 'Gift Card':
        risk_factors.append("기프트카드 결제 (만료 위험)")
    if customer['last_login_days'] > 30:
        risk_factors.append("30일 이상 미접속 (매우 높은 위험)")
    elif customer['last_login_days'] > 14:
        risk_factors.append("14일 이상 미접속 (높은 위험)")
    if customer['watch_hours'] < 5:
        risk_factors.append("낮은 시청 시간 (월 5시간 미만)")
    if customer['age'] < 25:
        risk_factors.append("젊은 연령층 (변동성 높음)")
    elif customer['age'] > 60:
        risk_factors.append("고령층 (기술 적응 어려움)")
    if customer['subscription_type'] == 'Basic':
        risk_factors.append("기본 요금제 (기능 제한)")
    if customer['monthly_fee'] < 5:
        risk_factors.append("낮은 구독료 (가치 인식 부족)")
    if customer['device'] == 'Tablet':
        risk_factors.append("태블릿 사용 (불편한 시청 환경)")
    if customer['number_of_profiles'] == 1:
        risk_factors.append("단일 프로필 (가족 공유 미활용)")
    
    # 보호 요소 분석
    if customer['subscription_type'] == 'Premium':
        protection_factors.append("프리미엄 구독 (높은 만족도)")
    if customer['watch_hours'] > 20:
        protection_factors.append("높은 시청 시간 (적극적 이용)")
    elif customer['watch_hours'] > 10:
        protection_factors.append("적정 시청 시간 (안정적 이용)")
    if customer['last_login_days'] < 3:
        protection_factors.append("최근 접속 (활발한 이용)")
    if customer['payment_method'] == 'Credit Card':
        protection_factors.append("신용카드 결제 (안정적 결제)")
    if 25 <= customer['age'] <= 40:
        protection_factors.append("핵심 연령층 (안정적 이용 패턴)")
    if customer['device'] == 'Smart TV':
        protection_factors.append("스마트 TV 이용 (편리한 시청 환경)")
    if customer['number_of_profiles'] >= 4:
        protection_factors.append("다중 프로필 (가족 공유 활용)")
    if customer['monthly_fee'] > 15:
        protection_factors.append("높은 구독료 (서비스 가치 인정)")
    
    # 위험 요소 표시
    if risk_factors:
        st.error("🚨 **위험 요소**")
        for factor in risk_factors:
            st.write(f"• {factor}")
    
    # 보호 요소 표시
    if protection_factors:
        st.success("✅ **보호 요소**")
        for factor in protection_factors:
            st.write(f"• {factor}")
    
    # 종합 위험도 평가
    risk_level = ""
    if churn_rate >= 70:
        risk_level = "🔴 **매우 높음** - 즉시 대응 필요"
    elif churn_rate >= 50:
        risk_level = "🟠 **높음** - 적극적 관리 필요"
    elif churn_rate >= 30:
        risk_level = "🟡 **보통** - 주기적 모니터링 필요"
    else:
        risk_level = "🟢 **낮음** - 안정적 고객"
    
    st.info(f"**종합 위험도:** {risk_level}")
    


def show_customer_info(customer):
    # --------------------------
    # 상세 고객 정보
    # --------------------------
    with st.expander("상세 고객 정보 보기"):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**고객 ID:** {customer['customer_id']}")
            st.write(f"**나이:** {customer['age']}세")
            st.write(f"**성별:** {customer['gender']}")
            st.write(f"**구독 타입:** {customer['subscription_type']}")
            st.write(f"**지역:** {customer['region']}")
            st.write(f"**디바이스:** {customer['device']}")
        with col2:
            st.write(f"**월 시청 시간:** {customer['watch_hours']:.1f}시간")
            st.write(f"**마지막 로그인:** {customer['last_login_days']}일 전")
            st.write(f"**월 구독료:** ${customer['monthly_fee']}")
            st.write(f"**결제 방법:** {customer['payment_method']}")
            st.write(f"**프로필 수:** {customer['number_of_profiles']}")
            st.write(f"**선호 장르:** {customer['favorite_genre']}")

def render_customer_block(customer_id: str):
    """customer_id로 예측/분석/상세정보를 한 번에 렌더링"""
    if not customer_id:
        return
    customer_df = df[df['customer_id'] == int(customer_id)]
    if customer_df.empty:
        st.error("고객을 찾을 수 없습니다.")
        return
<<<<<<< HEAD
    print(customer_df)
=======
>>>>>>> dev
    customer, churn_proba, retention_proba = show_prediction_prob(customer_df)
    show_prediction_bar(churn_proba, retention_proba)
    analize_churn_customer(customer, churn_proba)
    show_customer_info(customer)

<<<<<<< HEAD
=======
def _set_current_customer(cid: str, source: str):
    # 선택 출처는 참고용(디버깅/UX)
    st.session_state["current_customer_id"] = cid
    st.session_state["current_customer_source"] = source
    # 서로 충돌 안 나게 나머지 키는 정리
    st.session_state["selected_customer_id"] = cid if source == "manual" else ""
    st.session_state["sample_id_selected"] = cid if source == "sample" else ""
    st.session_state["list_customer_selected"] = cid if source == "list" else ""
    st.session_state["search_executed"] = (source == "manual")

>>>>>>> dev
st.markdown("""
    <style>
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

config = get_config()
db_instance = Database(**config["database"])
db_instance.connect()
rows, cols = db_instance.read_all_data()

df = pd.DataFrame(rows, columns=cols)

st.title("🔎고객 이탈 확률 예측🔎")

all_models = [
    "LogisticRegression", "RandomForest", "XGBoost", "LightGBM", "CatBoost",
    "SVC", "ExtraTrees", "AdaBoost", "HistGradientBoosting", "GradientBoosting",
    "KNeighbors", "RidgeClassifier", "MLPClassifier"
]

st.subheader("🔧 모델 선택")
pad_l, main, pad_r = st.columns([1.5, 1, 1])
with pad_l:
    model_name = st.selectbox("예측 모델을 선택하세요", all_models)

# 고객 선택 방법 탭
tab1, tab2 = st.tabs(["고객 ID 직접 입력", "사용자 이탈 예측"])

# 세션 상태 초기화
if 'selected_customer_id' not in st.session_state:
    st.session_state.selected_customer_id = ""
if 'search_executed' not in st.session_state:
    st.session_state.search_executed = False
if 'sample_id_selected' not in st.session_state:
    st.session_state.sample_id_selected = ""
if 'list_customer_selected' not in st.session_state:
    st.session_state.list_customer_selected = ""

with tab1:
    # 고객 ID 입력 & 버튼
    st.subheader("고객 조회")
    pad_l, main, pad_r = st.columns([1.5, 1, 1])
    with pad_l:
        input_customer_id = st.text_input(
            "CustomerID",
            placeholder="고객 ID를 입력하세요"
        )
    search_clicked = st.button("고객 정보 조회", type="primary", key="search_button")

    # 1) 직접 입력 후 조회 버튼 클릭 시
    if search_clicked:
        if input_customer_id:
<<<<<<< HEAD
            st.session_state.selected_customer_id = input_customer_id
            st.session_state.search_executed = True
            render_customer_block(input_customer_id)
=======
             _set_current_customer(input_customer_id, "manual")
>>>>>>> dev
        else:
            st.error("고객 ID를 입력해주세요.")

    # 2) 자동 렌더링: 샘플ID / 목록선택 / 최근 직접조회 순으로 우선 적용
    elif st.session_state.get("sample_id_selected"):
<<<<<<< HEAD
        render_customer_block(st.session_state.sample_id_selected)
    elif st.session_state.get("list_customer_selected"):
        render_customer_block(st.session_state.list_customer_selected)
    elif st.session_state.get("search_executed") and st.session_state.get("selected_customer_id"):
        render_customer_block(st.session_state.selected_customer_id)

=======
        _set_current_customer(st.session_state.sample_id_selected,"manual")
    elif st.session_state.get("list_customer_selected","manual"):
        _set_current_customer(st.session_state.list_customer_selected,"manual")
    elif st.session_state.get("search_executed") and st.session_state.get("selected_customer_id"):
        _set_current_customer(st.session_state.selected_customer_id,"manual")

current_id = st.session_state.get("current_customer_id", "")
if current_id:
    render_customer_block(current_id)
>>>>>>> dev
with tab2:
    st.write("**직접/선택 입력으로 사용자의 특성을 넣고 이탈 확률을 예측합니다.**")

    # 1) 입력 컬럼 정의
    FREE_INPUT_COLS = {
        "watch_hours",
        "last_login_days",
        "number_of_profiles",
        "avg_watch_time_per_day",
    }
    EXCLUDE_COLS = {"customer_id", "churned"}
    feature_cols = [c for c in df.columns if c not in EXCLUDE_COLS]

    # 2) 유틸
    def _is_integer_col(s: pd.Series) -> bool:
        return pd.api.types.is_integer_dtype(s)

    def _num_defaults(series: pd.Series):
        s = pd.to_numeric(series, errors="coerce").dropna()
        if len(s) == 0:
            return 0.0, None, None, 1.0
        median = float(s.median())
        min_v = float(s.min())
        max_v = float(s.max())
        step = 1.0 if _is_integer_col(series) else max((max_v - min_v) / 100, 0.1)
        return median, min_v, max_v, step

    def _select_options(series: pd.Series):
        # NaN 제거, 고유값 추출 (원래 dtype 유지)
        vals = series.dropna().unique().tolist()
        # 보기 좋게 정렬: 숫자형은 숫자 기준, 그 외는 문자열 기준
        if pd.api.types.is_numeric_dtype(series):
            vals = sorted(vals)
        else:
            vals = sorted(map(lambda x: str(x), vals))
        return vals

    # 3) 폼
    with st.form("manual_input_form", clear_on_submit=False):
        user_inputs = {}
        submit = False
        col_l, col_r = st.columns(2)
        left = True

        for col in feature_cols:
            host = col_l if left else col_r
            left = not left
            s = df[col]

            if col in FREE_INPUT_COLS:
                # 자유 입력 4개만 number_input 제공
                default, min_v, max_v, step = _num_defaults(s)
                if _is_integer_col(s):
                    user_inputs[col] = host.number_input(
                        f"{col}",
                        value=int(default) if default is not None else 0,
                        min_value=int(min_v) if min_v is not None else None,
                        max_value=int(max_v) if max_v is not None else None,
                        step=1
                    )
                else:
                    user_inputs[col] = host.number_input(
                        f"{col}",
                        value=float(default) if default is not None else 0.0,
                        min_value=min_v if min_v is not None else None,
                        max_value=max_v if max_v is not None else None,
                        step=step
                    )
            else:
                # 나머지는 전부 선택형 selectbox (직접입력 없음)
                opts = _select_options(s)
                if len(opts) == 0:
                    host.warning(f"`{col}`에 선택할 값이 없어요. 데이터에 고유값이 없습니다.")
                    continue

                # 불리언 컬럼은 True/False를 명시적으로
                if pd.api.types.is_bool_dtype(s):
                    # 가장 흔한 값을 기본 선택
                    true_cnt = int((s == True).sum())
                    false_cnt = int((s == False).sum())
                    default_idx = 0 if true_cnt >= false_cnt else 1
                    user_inputs[col] = host.selectbox(f"{col}", options=[True, False], index=default_idx)
                else:
                    # 숫자형/문자형 모두 selectbox. 숫자형은 숫자 그대로, 문자형은 str
                    # 기본값: 최빈값(없으면 첫 번째)
                    try:
                        mode_val = s.mode(dropna=True)[0]
                    except Exception:
                        mode_val = opts[0]
                    # 문자형으로 바꿨으면 index 재계산 필요
                    if not pd.api.types.is_numeric_dtype(s):
                        mode_val = str(mode_val)
                    default_idx = opts.index(mode_val) if mode_val in opts else 0
                    user_inputs[col] = host.selectbox(f"{col}", options=opts, index=default_idx)

        st.divider()
        submit = st.form_submit_button("예측", type="primary")
    if submit:
        X_user = pd.DataFrame([user_inputs])
        db_instance.insert(user_inputs)
        customer, churn_proba, retention_proba = show_prediction_prob(X_user)
        show_prediction_bar(churn_proba, retention_proba)
        analize_churn_customer(customer, churn_proba)


# 사용 가능한 고객 ID 샘플 표시
with st.expander("사용 가능한 고객 ID 샘플 보기"):
    st.write("**샘플 고객 ID들:**")
    
    # 전체 고객 ID 목록
    all_customer_ids = df['customer_id'].tolist()
    total_customers = len(all_customer_ids)
    
    # 페이지네이션 설정 (50개씩)
    items_per_page = 50
    total_pages = (total_customers - 1) // items_per_page + 1
    
    # 페이지 선택
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        current_page = st.selectbox(
            f"페이지 선택 (총 {total_pages}페이지, {total_customers}개 고객 ID)",
            range(1, total_pages + 1),
            key="id_page_selector"
        )
    
    # 현재 페이지의 고객 ID 계산
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_customers)
    page_customer_ids = all_customer_ids[start_idx:end_idx]
    
    st.write(f"**{current_page}페이지 ({start_idx + 1}-{end_idx}번째 고객 ID)**")
    
    # 10개씩 한 줄에 표시
    for i in range(0, len(page_customer_ids), 10):
        cols = st.columns(10)
        for j, customer_id in enumerate(page_customer_ids[i:i+10]):
            with cols[j]:
                # 고객 ID를 클릭 가능한 버튼으로 만들기
                button_key = f"id_button_{customer_id}"
                customer_id_str = str(customer_id)+" 고객"
                if st.button(customer_id_str, key=button_key, help=customer_id_str):
<<<<<<< HEAD
                    # 클릭하면 해당 고객 ID로 예측 실행 (샘플 ID 클릭)
                    if st.session_state.sample_id_selected != customer_id:
                        st.session_state.sample_id_selected = customer_id
                        st.session_state.selected_customer_id = ""
                        st.session_state.list_customer_selected = ""
                        st.session_state.search_executed = False
                        st.rerun()  # 페이지 새로고침하여 예측 결과 표시
=======
                    _set_current_customer(str(customer_id), "sample")
                    st.rerun()
>>>>>>> dev



# 기본 배경색상을 검정으로 설정하기
st.markdown("""
<style>
/* 사이드바 배경색 설정 */
[data-testid="stSidebar"] {
    background-color: #0E1117;
}
<<<<<<< HEAD

/* 메인 바탕화면 배경색 설정 */
.main {
    background-color: #0E1117;
}
=======
>>>>>>> dev
</style>
""", unsafe_allow_html=True)


setup_shared_sidebar()