print("Start ...")

import sys

while True:
    print("Menu Start")

    cmd = input("명령어를 입력하세요. 종료는 q: ")
    print(f"입력하신 정보는 {cmd}")

    if cmd == "q":
        print("bye...")
        sys.exit()

    print("end ....")

print("프로그램 종료")