students = [
    {"name": "Jean", "score": 95},
    {"name": "Mina", "score": 82},
    {"name": "Jun", "score": 58}, 
    {"name": "Tim", "score": 95},
    {"name": "Tom", "score": 72},
    {"name": "Jain", "score": 68},
]


# 학생들의 평균점수를 출력한다.
# calculate_average(students:list)-> float:
def calculate_average(students: list[int]) -> float:
    # 모든 점수를 더합니다.
    total = sum(students)
    # 학생 수를 구합니다.
    count = len(students)
    #  평균의 공식은 점수의 합 / 학생수 입니다.
    return total / count


score_list: list[int] = [90, 85, 77, 92]
average = calculate_average(score_list)
print("평균 점수:", average)
score_list: list = [90, 85, 77, 92]



# 학생의 학점(9,8,7,6)과 패스여부(60)를 출력한다.
# filter_passed_students(student: dict)->tuple(str,bool):
def filter_passed_students(student: dict) -> tuple[str, bool]:

    score = student["score"]

    # 학점 계산
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    # 패스 여부 계산
    is_passed = score >= 60

    # 학점과 패스 여부를 함께 반환
    return grade, is_passed



#모든 학생의 평균점수보다 낮은 학생들을 출력한다.
#filter_passed_students(students: list)->tuple():
students = [
    {"name": "철수", "score": 90},
    {"name": "영희", "score": 80},
    {"name": "민수", "score": 70},
]


def filter_passed_students(students: list) -> tuple:
    total = 0

    # 모든 학생의 점수를 더하기
    for student in students:
        total += student["score"]

    # 평균 구하기
    average = total /len(students)
    print("전체 평균:", average)
    print(f"평균보다 점수가 낮은 학생:{'name'}")


    # 평균보다 점수가 낮은 학생 찾기
for student in students:
    if student["score"] <average:
        print(f"점수가 낮은 학생:{'name'}")
    break

