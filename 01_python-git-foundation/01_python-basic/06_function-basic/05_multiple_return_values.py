"""여러 값을 반환하는 함수 예제입니다.

Python 함수는 여러 값을 한 번에 반환할 수 있습니다.
실제로는 tuple 형태로 반환되고, 이를 여러 변수에 나누어 받을 수 있습니다.
"""


def calculate(a, b)-> tuple[float,float,float,float]:
    add_result = a + b
    subtract_result = a - b
    multiply_result = a * b
    divide_result = a / b

    return add_result, subtract_result, multiply_result, divide_result

# tuple unpacking은 tuple 안의 값을 여러 변수에 나누어 담을 수 있습니다.
plus, minus, multiply, divide = calculate(10, 2)




print("더하기:", plus)
print("빼기:", minus)
print("곱하기:", multiply)
print("나누기:", divide)


def get_min_max(numbers:list[int])->tuple[int,int]:
    smallest = min(numbers)
    largest = max(numbers)
    return smallest, largest


scores = [80, 95, 70, 88]
min_score, max_score = get_min_max(scores)

print("최저 점수:", min_score)
print("최고 점수:", max_score)



print("-----------------------------------------------")

# 숫자로 되어 있는 list를 입력하면
# 최소값과 최대값 합계 평균을 반환하는 함수를 만들어 보세요.
# dict 형태로 반환하는 함수를 구현하시오.
# 함수명:total_datas

datas = [10,30,40,10,20,50,60]

def total_datas(numbers: list[int]) -> dict:
    minimum = min(numbers)
    maximum = max(numbers)
    total = sum(numbers)
    average = total /len(numbers)

    result = {
        "최소값": minimum,
        "최대값": maximum,
        "합계": total,
        "평균": average
    }

    return result
result = total_datas(datas)
print(result)






fruit_list = ["사과", "바나나", "딸기"]

def fruit_information(fruits: list[str]) -> dict:
    # 과일의 개수를 계산합니다.
    fruit_count = len(fruits)

    # 계산한 결과를 딕셔너리에 저장합니다.
    result = {
        "과일목록": fruits,
        "과일개수": fruit_count
    }

    # 완성한 딕셔너리를 반환합니다.
    return result




information = fruit_information(fruit_list)
print(information)



