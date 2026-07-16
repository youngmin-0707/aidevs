student:list [dict[str,object]] = [ 

{
    "name": "Jean",
    "score": 95,
   \
},
{
    "name": "Mina",
    "score": 99,
   \
},
{
    "name": "Tom",
    "score": 96,
   \
},
]

# 학생들 정보를 출력합니다. for반복문을 사용하여 학생들의 이름과 점수를 출력하시오.
for s in student:
    total_score += s["score"]
    print(f"이름: {s['name']}, 점수: {s['score']}")

#학생들 성적의 합과 평균을 출력하시오.
average_score = total_score / len(student)
print(f"학생들 성적의 합: {total_score}, 평균: {average_score}")

