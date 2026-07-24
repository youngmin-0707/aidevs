# 01_login_local.py
# Streamlit 라이브러리를 st라는 짧은 이름으로 불러옵니다.
import streamlit as st

# 브라우저의 Local Storage를 사용하기 위한 LocalStorage 클래스를 불러옵니다.
from streamlit_local_storage import LocalStorage

# 선언 --------------------------
# 이전에 사용했던 쿼리 파라미터 방식의 코드입니다.
# 현재 코드에서는 실행하지 않도록 앞에 #을 붙여 주석 처리했습니다.
# loginout = st.query_params.get("loginout","logout")

# Local Storage를 사용할 수 있는 storage 객체를 만듭니다.
storage = LocalStorage()

# Local Storage에서 loginout이라는 이름으로 저장된 값을 가져옵니다.
# 저장된 값이 없다면 loginout에는 None이 들어갑니다.
loginout = storage.getItem("loginout")

# session_state에 input_login_id가 없을 때만 빈 문자열로 초기화합니다.
# session_state를 사용하면 Streamlit 코드가 다시 실행되어도 입력값을 기억할 수 있습니다.
if "input_login_id" not in st.session_state:
    st.session_state.input_login_id = ""

# session_state에 input_login_pwd가 없을 때만 빈 문자열로 초기화합니다.
if "input_login_pwd" not in st.session_state:
    st.session_state.input_login_pwd = ""

# ID와 비밀번호 입력값을 모두 지우는 함수입니다.
# RESET 버튼을 누르면 이 함수가 실행됩니다.
def reset():
    st.session_state.input_login_id = ""
    st.session_state.input_login_pwd = ""

# 화면 --------------------------
# loginout이 "logout"이거나 저장된 값이 없으면 로그인 화면을 표시합니다.
if loginout == "logout" or loginout is None:
    # 화면 위쪽에 LOGIN이라는 큰 제목을 표시합니다.
    st.title("LOGIN")

    # ID, 비밀번호, 버튼을 login_form이라는 하나의 폼으로 묶습니다.
    # 폼 안의 입력값은 버튼을 눌렀을 때 한꺼번에 처리됩니다.
    with st.form("login_form"):
        # ID 입력창을 만들고 입력값을 session_state의 input_login_id에 연결합니다.
        input_id = st.text_input("ID입력", key="input_login_id")

        # 비밀번호 입력창을 만들고 입력값을 input_login_pwd에 연결합니다.
        # type="password"를 사용하면 입력한 문자가 화면에서 가려집니다.
        input_pwd = st.text_input("PWD입력",type="password", key="input_login_pwd")

        # 화면을 동일한 크기의 두 영역으로 나누어 버튼을 나란히 배치합니다.
        submit_area , reset_area = st.columns(2)

        # 첫 번째 영역에 LOGIN 버튼을 배치합니다.
        with submit_area:
            login_submit = st.form_submit_button("LOGIN")

        # 두 번째 영역에 RESET 버튼을 배치합니다.
        # 버튼을 누르면 위에서 만든 reset 함수가 실행됩니다.
        with reset_area:
            reset_submit = st.form_submit_button("RESET", on_click=reset)

        # 사용자가 LOGIN 버튼을 눌렀을 때만 아래 코드를 실행합니다.
        if login_submit:
            # 입력한 ID와 비밀번호가 지정된 값과 모두 같은지 검사합니다.
            if input_id == "id01" and input_pwd == "pwd01":
                # 로그인에 성공하면 Local Storage의 loginout 값을 "login"으로 저장합니다.
                storage.setItem("loginout","login")

            # Streamlit 코드를 즉시 다시 실행하려고 작성했던 코드입니다.
            # 현재는 앞에 #이 있으므로 실행되지 않습니다.
            #    st.rerun()
            else:
                # ID 또는 비밀번호가 다르면 로그인 실패 알림을 표시합니다.
                st.toast("로그인 실패")

# loginout 값이 "logout"도 아니고 None도 아니면 로그인된 화면을 표시합니다.
else:
    # 로그인 완료 안내 메시지를 표시합니다.
    st.info("로그인 했습니다.")

    # LOGOUT 버튼을 만들고 버튼을 눌렀는지 여부를 logout에 저장합니다.
    logout = st.button("LOGOUT")

    # 사용자가 LOGOUT 버튼을 눌렀을 때만 아래 코드를 실행합니다.
    if logout:
        # Local Storage의 loginout 값을 "logout"으로 변경합니다.
        storage.setItem("loginout","logout")

        # Streamlit 코드를 즉시 다시 실행하려고 작성했던 코드입니다.
        # 현재는 앞에 #이 있으므로 실행되지 않습니다.
        # st.rerun()
    
# 코드 --------------------------
