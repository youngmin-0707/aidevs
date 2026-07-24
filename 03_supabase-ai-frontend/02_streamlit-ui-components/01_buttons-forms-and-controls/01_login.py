# 01_login.py
# Streamlit 라이브러리를 st라는 짧은 이름으로 불러옵니다.
import streamlit as st

# 선언 --------------------------

# 브라우저 주소의 loginout 값을 가져옵니다.
# 주소에 loginout 값이 없으면 기본값으로 "logout"을 사용합니다.
loginout = st.query_params.get("loginout","logout")

# 세션에 아이디 입력값을 저장할 공간이 없으면 빈 문자열로 처음 생성합니다.
# session_state를 사용하면 Streamlit 코드가 다시 실행되어도 입력값을 기억할 수 있습니다.
if "input_login_id" not in st.session_state:
    st.session_state.input_login_id = ""

# 세션에 비밀번호 입력값을 저장할 공간이 없으면 빈 문자열로 처음 생성합니다.
if "input_login_pwd" not in st.session_state:
    st.session_state.input_login_pwd = ""

# ID와 비밀번호 입력값을 모두 비우는 함수입니다.
# 사용자가 RESET 버튼을 누르면 이 함수가 실행됩니다.
def reset():
    st.session_state.input_login_id = ""
    st.session_state.input_login_pwd = ""

# 화면 --------------------------

# loginout 값이 "logout"이면 로그인 전 화면을 표시합니다.
if loginout == "logout":
    # 페이지 상단에 LOGIN 제목을 표시합니다.
    st.title("LOGIN")

    # ID, 비밀번호, 버튼을 login_form이라는 하나의 폼으로 묶습니다.
    with st.form("login_form"):
        # ID 입력창을 만들고 입력값을 input_login_id라는 세션 키에 저장합니다.
        input_id = st.text_input("ID입력", key="input_login_id")

        # 비밀번호 입력창을 만들고 입력값을 input_login_pwd라는 세션 키에 저장합니다.
        # type="password"를 사용하므로 입력한 문자가 화면에서 가려집니다.
        input_pwd = st.text_input("PWD입력",type="password", key="input_login_pwd")

        # 화면을 동일한 너비의 두 영역으로 나눠 버튼을 나란히 배치합니다.
        submit_area , reset_area = st.columns(2)

        # 첫 번째 영역에 LOGIN 버튼을 배치합니다.
        with submit_area:
            login_submit = st.form_submit_button("LOGIN")

        # 두 번째 영역에 RESET 버튼을 배치합니다.
        # 버튼을 누르면 위에서 만든 reset 함수가 호출됩니다.
        with reset_area:
            reset_submit = st.form_submit_button("RESET", on_click=reset)

        # LOGIN 버튼을 눌렀을 때만 로그인 검사를 실행합니다.
        if login_submit:
            # 입력한 ID와 비밀번호가 지정된 값과 모두 같은지 확인합니다.
            if input_id == "id01" and input_pwd == "pwd01":
               # 로그인에 성공하면 주소의 loginout 값을 "login"으로 변경합니다.
               st.query_params["loginout"] = "login"

               # 변경된 로그인 상태를 즉시 반영하도록 코드를 처음부터 다시 실행합니다.
               st.rerun()
            else:
                # ID 또는 비밀번호가 다르면 로그인 실패 알림을 표시합니다.
                st.toast("로그인 실패")

# loginout 값이 "logout"이 아니면 로그인 후 화면을 표시합니다.
else:
    # 로그인 성공 안내 메시지를 표시합니다.
    st.info("로그인 했습니다.")

    # 사용자가 로그아웃할 수 있는 LOGOUT 버튼을 만듭니다.
    logout = st.button("LOGOUT")

    # LOGOUT 버튼을 눌렀을 때 로그아웃 처리를 실행합니다.
    if logout:
        # 주소의 loginout 값을 "logout"으로 변경합니다.
        st.query_params["loginout"] = "logout"

        # 변경된 로그아웃 상태를 즉시 반영하도록 코드를 처음부터 다시 실행합니다.
        st.rerun()
    
# 코드 --------------------------
