def input_natural_number():
    while True:
        number_input = input(
            "자연수를 입력하세요(q: 종료): "
            ).strip().lower()

        # q를 입력하면 반복 종료
        if number_input == "q":
            print("프로그램을 종료합니다.")
            return None

        is_natural_number = True

        # 아무것도 입력하지 않은 경우
        if number_input == "":
            is_natural_number = False

        # 입력값을 한 글자씩 검사
        for char in number_input:
            if char not in "0123456789":
                is_natural_number = False

        if is_natural_number:
            number = int(number_input)

            if number > 0:
                print(f"입력한 자연수는 {number}입니다.")
            else:
                print("1 이상의 자연수를 입력해주세요.")
        else:
            print("숫자만 입력해주세요.")
input_natural_number()
# 위에서 만든 함수 실행
