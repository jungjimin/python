score = int(input('점수를 입력: ')) #input 의 return 은 str이다. 그래서 점수를 int()를 써서 정수로 변환

if 90 <= score <= 100:
    grade = "A"
elif 80 <= score < 90:
    grade = "B"
elif 70 <= score < 80:
    grade = "C"
elif 60 <= score < 70:
    grade = "D"
else:
    grade = "F" # grace 오타인 경우, 지역변수라서 오류로 잡지 않는다. 느슨한 언어..아쉬운점 
    
print("Grade is " + grade)
