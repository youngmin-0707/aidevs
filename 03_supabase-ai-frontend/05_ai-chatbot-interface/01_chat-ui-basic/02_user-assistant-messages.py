import streamlit as st

st.title("역할별 메시지 출력")


# 최초 실행 시에만 messages 생성
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []


# 함수 밖에서 초기화 함수 호출
init_state()


# 저장된 모든 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# 새로운 질문 입력
prompt = st.chat_input("질문을 입력하세요")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # 사용자 메시지 즉시 출력
    with st.chat_message("user"):
        st.write(prompt)

    # 임시 AI 답변
    answer = f"입력한 질문은 '{prompt}'입니다."

    # AI 답변 저장
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    # AI 답변 즉시 출력
    with st.chat_message("assistant"):
        st.write(answer)