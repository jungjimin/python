#부모 클래스
#Person 클래스 정의
#이름(name)과 전화번호(phoneNumber)를 속성으로 가짐
class Person:
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber

    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, self.phoneNumber))

#자식 클래스
#Person 클래스를 상속받아 Student 클래스 정의
class Student(Person):
    #덮어쓰기(Overriding) 생성자
    def __init__(self, name, phoneNumber, subject, studentID):
        super().__init__(name, phoneNumber) # 부모 클래스의 생성자 호출
        self.subject = subject # 학과(subject) 속성 추가
        self.studentID = studentID # 학번(studentID) 속성 추가
    #덮어쓰기(Overriding) 메소드
    def printInfo(self):
        print("Info(이름:{0}, 전번: {1})".format(self.name, self.phoneNumber))    
        print("Info(학과:{0}, 학번: {1})".format(self.subject, self.studentID))


p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "컴공", "24001")
p.printInfo()
s.printInfo()



