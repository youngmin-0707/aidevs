import streamlit as st  # 웹 화면을 만드는 Streamlit을 st라는 짧은 이름으로 가져옵니다.
from pathlib import Path  # 파일과 폴더 경로를 편리하게 다루기 위해 가져옵니다.

# title()은 화면의 가장 큰 제목을 표시합니다.
st.title("FRONTEND 실습")

# selectbox()는 목록에서 한 가지 항목을 선택하는 입력창입니다.
# 사용자가 선택한 값은 option 변수에 저장됩니다.
# index=None은 처음 화면에서 아무 항목도 선택하지 않는다는 뜻입니다.
option = st.selectbox(
    "아래에서 선택하세요",
    ["1번", "2번", "3번"],
     index=None,
)

# radio()는 여러 항목을 라디오 버튼으로 보여 줍니다.
level = st.radio(
    "현재 학습 수준을 선택하세요",
    ["입문", "기초", "중급"],
)


# option과 level이 각각 정해진 목록에 포함되어 있는지 확인합니다.
# and로 연결했기 때문에 두 조건이 모두 참이어야 아래 코드가 실행됩니다.
if option in ["1번", "2번", "3번"] and level in ["입문", "기초", "중급"]:
    # f-string을 사용하면 문자열 안에 변수의 값을 넣을 수 있습니다.
    st.write(f"선택한 옵션은: {option}입니다.")
    st.write(f"현재 수준: {level}")
    # info()는 파란색 정보 안내창을 표시합니다.
    st.info("실습 성공입니다.")
else:
    # level을 아직 선택하지 않았다면 경고 안내창을 표시합니다.
    st.warning("위 항목을 모두 입력하세요")


# 현재 실행 중인 Python 파일의 전체 경로를 구합니다.
current_file = Path(__file__).resolve()

# 현재 파일의 상위 폴더에 있는 imgs 폴더 경로를 만듭니다.
# / 연산자를 사용하면 폴더 경로를 간단하게 연결할 수 있습니다.
image_dir = current_file.parent.parent / "imgs"


# glob()을 사용하여 imgs 폴더에서 확장자가 png, jpg, jpeg인 파일을 찾습니다.
# 여러 이미지 목록을 +로 합치고, sorted()로 파일 이름 순서대로 정렬합니다.
image_files = sorted(
    list(image_dir.glob("*.png"))
    + list(image_dir.glob("*.jpg"))
    + list(image_dir.glob("*.jpeg"))
)

# 이미지가 한 개도 없으면 image_files는 빈 목록이 됩니다.
if not image_files:
    st.warning(f"이미지 파일을 찾을 수 없습니다: {image_dir}")

else:
    # 이미지 파일명 목록의 맨 앞에 안내용 문구를 추가합니다.
    # image_file.name은 전체 경로에서 파일명만 가져옵니다.
    image_options = ["이미지를 선택하세요"] + [
        image_file.name for image_file in image_files
    ]

    # 이미지 파일명을 선택할 수 있는 입력창을 만듭니다.
    # 선택한 값은 selected_name 변수에 저장됩니다.
    selected_name = st.selectbox(
        "화면에 출력할 이미지를 선택하세요",
        image_options,
    )

    # 안내 문구가 선택된 동안에는 이미지를 보여 주지 않습니다.
    if selected_name == "이미지를 선택하세요":
        st.info("출력할 이미지를 선택해 주세요.")

    else:
        # 이미지 폴더 경로와 선택한 파일명을 합쳐 실제 파일 경로를 만듭니다.
        selected_image = image_dir / selected_name

        # image()는 이미지를 화면에 출력합니다.
        st.image(
            selected_image,
            caption=f"{selected_name} 파일을 출력했습니다.",
            use_container_width=True,  # 화면의 가로 너비에 맞게 이미지 크기를 조절합니다.
        )