#개발자 클래스 정의
#개발자 클래스는 Person 클래스를 상속받아 개발자 정보를 추가로 가짐
class Developer:   
    def __init__(self, id, name, programming_language):
        self.id = id
        self.name = name    
        self.programming_language = programming_language  # 프로그래밍 언어 속성 추가

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Programming Language: {self.programming_language}")

#인스턴스를 2개 생성
dev1 = Developer(7, "김개발", "Python")
dev2 = Developer(8, "이개발", "Java")

#정보 출력
print(dev1.printInfo())
print(dev2.printInfo())