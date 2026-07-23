r"""Streamlit 테마 설정 확인 예제입니다.

이 예제는 같은 폴더 안의 `.streamlit/config.toml` 파일을 읽어 화면 테마를 적용합니다.

실행 위치가 중요합니다.
반드시 `04_theme-and-config` 폴더로 이동한 뒤 실행합니다.

실행:
    cd C:\aidev\03_supabase-ai-frontend\01_streamlit-basic\04_theme-and-config
    ..\..\.venv\Scripts\Activate.ps1
    streamlit run .\01_theme-preview.py

확인:
    - 전체 배경이 흰색인지 확인합니다.
    - 기본 글자가 검정색인지 확인합니다.
    - 버튼과 선택 강조 색상이 config.toml의 primaryColor를 따르는지 확인합니다.
"""

import streamlit as st  # 웹 화면을 만드는 Streamlit을 st라는 짧은 이름으로 가져옵니다.


# set_page_config()는 브라우저 탭과 화면 배치 등 페이지의 기본 설정을 지정합니다.
# 이 함수는 다른 Streamlit 화면 요소보다 먼저 실행하는 것이 좋습니다.
st.set_page_config(
    page_title="Streamlit Theme Preview",  # 브라우저 탭에 표시할 제목입니다.
    page_icon="🎨",  # 브라우저 탭 제목 옆에 표시할 아이콘입니다.
    layout="centered",  # 화면 내용을 가운데 영역에 모아서 표시합니다.
)

# title()은 화면의 가장 큰 제목을 표시합니다.
st.title("Streamlit 테마 설정 확인")

# write()는 문자열, 숫자, 변수 등 다양한 내용을 화면에 출력합니다.
st.write(
    "이 화면은 `04_theme-and-config/.streamlit/config.toml` 파일의 테마 설정을 기준으로 표시됩니다."
)

# info()는 사용자가 알아야 할 정보를 파란색 안내창으로 표시합니다.
st.info(
    "테마는 Python 코드가 아니라 `.streamlit/config.toml` 파일에서 설정합니다. "
    "테마를 수정한 뒤에는 Streamlit 앱을 종료하고 다시 실행하는 것이 가장 확실합니다."
)

# subheader()는 큰 제목 아래에서 영역을 구분하는 작은 제목을 표시합니다.
st.subheader("입력 위젯 색상 확인")

# selectbox()는 목록에서 항목 하나를 선택할 수 있는 입력창을 만듭니다.
# 사용자가 선택한 값은 topic 변수에 저장됩니다.
topic = st.selectbox(
    "확인할 항목을 선택하세요",  # 입력창 위에 표시할 안내 문구입니다.
    ["배경색", "글자색", "강조색", "입력 영역"],  # 선택 가능한 항목 목록입니다.
)

# radio()는 여러 항목 중 하나를 라디오 버튼으로 선택하게 합니다.
# 사용자가 선택한 값은 mode 변수에 저장됩니다.
mode = st.radio(
    "화면 모드",  # 라디오 버튼 위에 표시할 안내 문구입니다.
    ["기본", "연습", "프로젝트"],  # 선택 가능한 화면 모드 목록입니다.
    horizontal=True,  # 버튼을 위아래가 아닌 왼쪽에서 오른쪽으로 배치합니다.
)

# text_area()는 여러 줄의 글을 입력할 수 있는 입력창을 만듭니다.
# 사용자가 입력한 글은 memo 변수에 저장됩니다.
memo = st.text_area(
    "테마 확인 메모",  # 입력창 위에 표시할 이름입니다.
    placeholder="예: 배경은 흰색이고 글자는 검정색으로 보입니다.",  # 입력 전 보여 줄 예시입니다.
)

# button()은 클릭했을 때 True가 되므로, 버튼을 누른 순간에만 아래 코드를 실행합니다.
if st.button("선택 내용 확인"):
    # success()는 선택한 내용을 초록색 성공 안내창으로 표시합니다.
    st.success(f"선택 항목: {topic} / 화면 모드: {mode}")

    # strip()은 문자열 앞뒤의 공백을 제거합니다.
    # 공백을 제거한 메모가 남아 있다면 사용자가 실제 내용을 입력한 것입니다.
    if memo.strip():
        st.write("메모:", memo)
    else:
        # 메모가 비어 있거나 공백뿐이면 노란색 경고 안내창을 표시합니다.
        st.warning("메모를 입력하지 않았습니다.")

# 두 번째 화면 영역의 작은 제목을 표시합니다.
st.subheader("테마 설정 파일 예시")

# code()는 문자열을 코드 블록 모양으로 화면에 출력합니다.
st.code(
    """
[theme]
base = "light"
primaryColor = "#2563eb"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f5f5f5"
textColor = "#000000"
font = "sans serif"
    """.strip(),  # 여러 줄 문자열의 처음과 끝에 생긴 불필요한 공백을 제거합니다.
    language="toml",  # TOML 문법에 맞게 코드 색상을 표시합니다.
)

# caption()은 화면 아래에 부가 설명을 작은 글씨로 표시합니다.
st.caption(
    "이 예제의 테마는 이 폴더 안의 `.streamlit/config.toml`에만 들어 있습니다. "
    "다른 예제 전체에 자동 적용하지 않기 위해 과정 최상위가 아니라 실습 폴더 안에 둡니다."
)
