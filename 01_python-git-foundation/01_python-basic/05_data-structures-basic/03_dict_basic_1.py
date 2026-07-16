student: dict[str, object] = {
    "name": "Jean",
    "ko": 95,
    "en": 85,
    "math": 90,
    "science": 80,
}

# student의 점수 합과 평균을 구하고
sum_score = 0
count_score = 0
for key, value in student.items():
    if key in ["ko", "en", "math", "science"]:
        sum_score += value
        count_score += 1
#  "sum","evg" 를 추가하고 
student["sum"] = sum_score
average_score = sum_score / count_score

# 출력하시오.
for key, value in student.items():
    print(key, "=", value)
    




