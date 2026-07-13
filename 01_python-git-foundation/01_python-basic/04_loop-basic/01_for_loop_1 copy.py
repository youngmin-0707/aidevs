# 1~5까지의 합과 평균을 구하시오

data_numbers:list = [1,2,3,4,5]
print(type(data_numbers))

total_number:int = 0

for data in data_numbers:
    total_number += data

print(total_number)
print(total_number/len(data_numbers))