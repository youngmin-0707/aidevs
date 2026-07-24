import streamlit as st  # 웹 화면을 만들기 위해 Streamlit을 st라는 이름으로 가져옵니다.


# 설문 제출 여부를 저장할 공간이 없으면 False로 초기화합니다.
# session_state에 저장한 값은 Streamlit 코드가 다시 실행되어도 유지됩니다.
if "survey_submitted" not in st.session_state:
    st.session_state.survey_submitted = False

# 설문 결과를 저장할 공간이 없으면 빈 딕셔너리로 초기화합니다.
if "survey_result" not in st.session_state:
    st.session_state.survey_result = {}


# 설문이 제출된 상태라면 입력 폼 대신 결과 화면을 표시합니다.
if st.session_state.survey_submitted:
    # session_state에 저장된 설문 결과를 result라는 변수에 담습니다.
    result = st.session_state.survey_result

    # 결과 화면의 제목과 제출 완료 메시지를 표시합니다.
    st.title("설문 결과")
    st.success("설문이 정상적으로 제출되었습니다.")

    # 저장된 설문 응답을 항목별로 표시합니다.
    st.write(f"이름 또는 닉네임: {result['name']}")
    st.write(f"나이: {result['age']}세")
    st.write(f"관심 주제: {result['topic']}")
    st.write(
        f"배우고 싶은 기술: "
        f"{', '.join(result['technologies']) if result['technologies'] else '선택하지 않음'}"
    )
    st.write(f"프로그래밍 경험: {result['experience']}년")
    st.write(
        f"수업에서 기대하는 점: "
        f"{result['opinion'] if result['opinion'] else '작성하지 않음'}"
    )
    st.write(
        f"수업 정보 수신: "
        f"{'동의' if result['receive_news'] else '동의하지 않음'}"
    )

    # 버튼을 누르면 제출 상태와 저장된 결과를 초기화합니다.
    if st.button("새 설문 작성"):
        st.session_state.survey_submitted = False
        st.session_state.survey_result = {}

        # 초기화된 상태를 바로 반영하기 위해 코드를 처음부터 다시 실행합니다.
        st.rerun()

# 아직 설문을 제출하지 않았다면 설문 작성 화면을 표시합니다.
else:
    # 설문 화면의 가장 큰 제목과 간단한 설명을 표시합니다.
    st.title("간단한 개발 학습 설문")
    st.write("아래 항목을 입력한 뒤 제출 버튼을 눌러 주세요.")

    # form 안에 있는 입력값은 제출 버튼을 눌렀을 때 한 번에 처리됩니다.
    with st.form("survey_form"):
        # text_input은 한 줄의 짧은 글을 입력받습니다.
        name = st.text_input(
            "이름 또는 닉네임",
            placeholder="예: 코딩초보",
        )

        # number_input은 숫자를 입력받습니다.
        age = st.number_input(
            "나이",
            min_value=1,
            max_value=100,
            value=20,
        )

        # selectbox는 여러 항목 중 한 가지를 선택받습니다.
        topic = st.selectbox(
            "가장 관심 있는 주제",
            ["Python", "Streamlit", "FastAPI", "Supabase"],
            index=None,  # 처음에는 아무 항목도 선택되지 않게 합니다.
            placeholder="관심 주제를 선택하세요",
        )

        # multiselect는 여러 항목을 동시에 선택받습니다.
        technologies = st.multiselect(
            "배우고 싶은 기술",
            ["웹 개발", "데이터 분석", "인공지능", "데이터베이스"],
        )

        # slider는 막대를 움직여 범위 안의 숫자를 선택받습니다.
        experience = st.slider(
            "프로그래밍 경험",
            min_value=0,
            max_value=10,
            value=0,
            format="%d년",
        )

        # text_area는 여러 줄의 긴 글을 입력받습니다.
        opinion = st.text_area(
            "수업에서 기대하는 점",
            placeholder="배우고 싶은 내용을 자유롭게 작성해 주세요.",
        )

        # checkbox는 항목의 동의 여부를 True 또는 False로 저장합니다.
        receive_news = st.checkbox("새로운 수업 정보를 받겠습니다.")

        # form_submit_button을 누르면 폼의 모든 입력값이 한 번에 제출됩니다.
        submitted = st.form_submit_button("설문 제출")

    # 제출 버튼을 누른 경우에만 입력값을 검사하고 처리합니다.
    if submitted:
        # 이름이나 관심 주제가 비어 있으면 안내 메시지를 표시합니다.
        if not name or not topic:
            st.warning("이름과 관심 주제를 모두 입력해 주세요.")
        else:
            # 입력한 설문 내용을 딕셔너리로 묶어 session_state에 저장합니다.
            st.session_state.survey_result = {
                "name": name,
                "age": age,
                "topic": topic,
                "technologies": technologies,
                "experience": experience,
                "opinion": opinion,
                "receive_news": receive_news,
            }

            # 제출 상태를 True로 변경하여 다음 실행에서 결과 화면을 표시합니다.
            st.session_state.survey_submitted = True

            # 입력 폼을 없애고 결과 화면으로 즉시 전환하기 위해 다시 실행합니다.
            st.rerun()
