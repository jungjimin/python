# demoClass.py
#1)클래스 정의
class Person:
    #초기화 메서드
    def __init__(self):
        self.name = "default name"
    def print(self):
        #if-string문법 : 포맷 스트링
        #print("My name is {0}".format(self.name))
        print(f"My name is {self.name}")

#2)인스턴스생성
p1 = Person()
p2 = Person()
p1.name = "전우치" #자바는 멤버변수 접근 x(private) 파이썬은 접근한다. python은 기본은 pubilc이라고 생각하면 됨.
#3)메서드 호출
p1.print()
p2.print()