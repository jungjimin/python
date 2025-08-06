#demoFile.py
# 블럭을 선택하고 주석처리 : ctrl + /
#파일쓰기
# f = open("c:\\work\\test.txt", "wt", encoding="utf-8")
# f.write("첫번째\n두번째\n세번째\n")
# f.close()

# #파일읽기(raw string notation)
# f = open(r"c:\work\test.txt", "rt", encoding="utf-8")
# print(f.read())
# f.close()   

#문자열처리
strA = "파이썬은 강력해"
strB = "python is very powerful"
print(len(strA)) # 문자열의 길이
print(len(strB))
print(strB.capitalize()) # 첫글자만 대문자로 변환
print(strB.upper())    # 대문자로 변환
print("MBC2580".isalnum()) #  영문자, 숫자만으로 구성되어 있는지 확인
print("2580".isdecimal()) #  숫자로만 구성되어 있는지 확인
data = "<<<   spam and ham  >>>"
result = data.strip()  # 양쪽 공백 제거
result = data.strip("<> ")  # 양쪽의 <, >, 공백 제거
print(data)
print(result)
result2 = result.replace("spam", "spam egg")  # 문자열 치환
print(result2)
#리스트로 리턴
lst = result2.split()  # 공백을 기준으로 분리
print(lst)
#하나의 문자열로 합치기
print(":)".join(lst))  # 리스트의 요소를 :로 연결하여 하나의 문자열로 합침

#정규표현식
import re

result = re.search("[0-9]*th", "  35th") #포함하는 걸 찾기
print(result)
print(result.group())  # 검색된 문자열 출력

# result = re.match("[0-9]*th", "  35th") #정확히 일치하는 것 찾기
# print(result)
# print(result.group())  # 검색된 문자열 출력

result = re.search("apple","this is an apple")  # apple이 포함된 문자열 찾기
print(result.group())  # 검색된 문자열 출력

result = re.search(r"\d{4}", "올해는 2025년 입니다.") #digit 4개 찾기
print(result.group())  # 검색된 문자열 출력

result = re.search(r"\d{5}", "우리 동네는 51200입니다.") #digit 5개 찾기
print(result.group())  # 검색된 문자열 출력
