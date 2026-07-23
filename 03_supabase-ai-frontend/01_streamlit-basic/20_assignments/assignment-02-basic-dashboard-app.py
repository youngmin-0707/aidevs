import streamlit as st  # 웹 화면을 만드는 Streamlit을 st라는 짧은 이름으로 가져옵니다.


st.set_page_config(  # 브라우저 탭과 앱 화면의 기본 설정을 지정합니다.
    page_title="학습 현황 대시보드",  # 브라우저 탭에 표시할 제목입니다.
    page_icon="📊",  # 브라우저 탭 제목 옆에 표시할 아이콘입니다.
    layout="wide",  # 메인 화면을 좌우로 넓게 사용하도록 설정합니다.
)

st.title("📊 학습 현황 대시보드")  # 메인 화면의 가장 큰 제목을 표시합니다.
st.write("사이드바에 정보를 입력하면 나의 학습 현황을 확인할 수 있습니다.")  # 앱 사용 방법을 설명합니다.



st.sidebar.header("사용자 설정")  # 사이드바에 설정 영역의 제목을 표시합니다.

user_name = st.sidebar.text_input(  # 사이드바에 이름을 입력하는 입력창을 만듭니다.
    "이름을 입력하세요",  # 이름 입력창 위에 표시할 안내 문구입니다.
    placeholder="예: 홍길동",  # 사용자가 입력하기 전에 보여 줄 예시입니다.
)

study_field = st.sidebar.selectbox(  # 사이드바에서 학습 분야를 선택하도록 만듭니다.
    "학습 분야를 선택하세요",  # 선택창 위에 표시할 안내 문구입니다.
    ["Python", "Streamlit", "FastAPI", "Supabase"],  # 사용자가 선택할 수 있는 학습 분야입니다.
)

study_hours = st.sidebar.slider(  # 사이드바에서 오늘의 학습 시간을 선택하도록 만듭니다.
    "오늘 학습 시간",  # 슬라이더 위에 표시할 이름입니다.
    min_value=0,  # 슬라이더에서 선택할 수 있는 가장 작은 값입니다.
    max_value=12,  # 슬라이더에서 선택할 수 있는 가장 큰 값입니다.
    value=0,  # 앱을 처음 실행했을 때 선택되어 있는 기본값입니다.
    format="%d시간",  # 선택한 숫자 뒤에 시간 단위를 붙여 표시합니다.
)


progress_value = study_hours / 12  # 최대 10시간을 기준으로 0부터 1 사이의 진행률을 계산합니다.
progress_percent = study_hours * 12  # 화면에 표시하기 위해 진행률을 백분율 숫자로 계산합니다.


st.subheader("오늘의 주요 지표")  # 지표 영역의 작은 제목을 표시합니다.

left_column, right_column = st.columns(2)  # 화면을 같은 너비의 두 열로 나눕니다.

with left_column:  # 왼쪽 열 안에 표시할 내용을 시작합니다.
    st.metric("오늘 학습 시간", f"{study_hours}시간")  # 오늘 선택한 학습 시간을 지표로 표시합니다.

with right_column:  # 오른쪽 열 안에 표시할 내용을 시작합니다.
    st.metric("목표 달성률", f"{progress_percent}%")  # 계산한 학습 진행률을 지표로 표시합니다.


overview_tab, detail_tab = st.tabs(["개요", "상세 내용"])  # 화면 내용을 개요와 상세 내용 탭으로 나눕니다.

with overview_tab:  # 사용자가 개요 탭을 열었을 때 보여 줄 영역입니다.
    st.subheader("학습 개요")  # 개요 탭의 작은 제목을 표시합니다.

    if not user_name:  # 이름이 빈 문자열인지 확인합니다.
        st.warning("사이드바에서 이름을 입력해 주세요.")  # 이름이 없을 때 경고 메시지를 표시합니다.
    elif study_hours == 0:  # 이름은 있지만 학습 시간이 0시간인지 확인합니다.
        st.info(f"{user_name}님, 오늘의 학습 시간을 설정해 주세요.")  # 학습 시간 설정을 안내합니다.
    elif study_hours >= 7:  # 오늘의 학습 시간이 7시간 이상인지 확인합니다.
        st.success(f"{user_name}님, 오늘 학습 목표를 충분히 달성했습니다!")  # 목표를 달성했다는 메시지를 표시합니다.
    else:  # 이름을 입력했고 학습 시간이 1시간 이상 7시간 미만일 때 실행합니다.
        st.info(f"{user_name}님, {study_field} 학습을 꾸준히 이어가고 있습니다.")  # 현재 학습 상태를 안내합니다.

    st.progress(progress_value)  # 계산한 진행률을 가로 막대 모양으로 표시합니다.

with detail_tab:  # 사용자가 상세 내용 탭을 열었을 때 보여 줄 영역입니다.
    st.subheader("상세 학습 정보")  # 상세 탭의 작은 제목을 표시합니다.
    st.write(f"사용자 이름: {user_name if user_name else '입력되지 않음'}")  # 입력한 이름 또는 미입력 상태를 표시합니다.
    st.write(f"선택한 학습 분야: {study_field}")  # 사이드바에서 선택한 학습 분야를 표시합니다.
    st.write(f"오늘 학습 시간: {study_hours}시간")  # 사이드바에서 선택한 학습 시간을 표시합니다.
    st.write(f"현재 목표 달성률: {progress_percent}%")  # 계산한 목표 달성률을 표시합니다.
