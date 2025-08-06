# demoOS.py

from os.path import *
from os import *
import glob # glob 모듈을 사용하여 파일 검색

fName = "sample.txt"
print(abspath(fName))
print(basename(r"c:\work\sample.txt"))  # 파일 이름만 출력

if (exists(r"c:\python310\python.exe")):  # 파일이 존재하는지 확인
    print("파일크기:", getsize(r"C:\python310\python.exe"))  # 파일 크기 출력
else:
    print("파일이 존재하지 않습니다.")

print("운영체제명:", name)  # 운영체제 이름 출력
print("환경변수:", environ)  # 환경변수 출력
system("notepad.exe") # 메모장 실행

print(glob.glob("*.py"))  # 현재 디렉토리의 모든 .py 파일 목록 출력
for item in glob.glob("*.py"):
    print(item)
