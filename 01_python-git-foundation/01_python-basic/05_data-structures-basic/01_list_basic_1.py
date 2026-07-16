numbers:list[int] = [1,2,3,4,5]

# 1.출력
print("numbers:", numbers)
# 2.마지막에 6을 추가
numbers.append(6)


# 3.전체 합과 평균을 출력 for
sum_number = 0
for number in numbers:
    sum_number += number

# 3-1.전체 합과 평균을 출력 단, 짝수만 평균을 구합니다.
sum_number = 0
count_even = 0
for number in numbers:
    if number % 2 == 0:
        sum_number += number
        count_even += 1

average_even = sum_number / count_even
print(f"짝수의 합계: {sum_number}, 평균: {average_even}")


print("합계:", sum_number)
average_number = sum_number / len(numbers)
print(f"평균:{average_number}"과 합계: {average_number}")
      
      

total = sum(numbers)
average = total / len(numbers)
print("합계:", total)
print("평균:", average)

