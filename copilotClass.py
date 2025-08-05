class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")

class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Title: {self.title}")

class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Skill: {self.skill}")

# 테스트 코드
def test_person():
    p = Person(1, "홍길동")
    assert p.id == 1
    assert p.name == "홍길동"

def test_person_printInfo(capsys):
    p = Person(2, "김철수")
    p.printInfo()
    captured = capsys.readouterr()
    assert "ID: 2, Name: 김철수" in captured.out

def test_manager():
    m = Manager(3, "이영희", "팀장")
    assert m.id == 3
    assert m.name == "이영희"
    assert m.title == "팀장"

def test_manager_printInfo(capsys):
    m = Manager(4, "박민수", "부장")
    m.printInfo()
    captured = capsys.readouterr()
    assert "ID: 4, Name: 박민수, Title: 부장" in captured.out

def test_employee():
    e = Employee(5, "최지우", "Python")
    assert e.id == 5
    assert e.name == "최지우"
    assert e.skill == "Python"

def test_employee_printInfo(capsys):
    e = Employee(6, "정우성", "Java")
    e.printInfo()
    captured = capsys.readouterr()
    assert "ID: 6, Name: 정우성, Skill: Java" in captured.out

def test_inheritance_manager():
    m = Manager(7, "김태희", "이사")
    assert isinstance(m, Person)

def test_inheritance_employee():
    e = Employee(8, "이준기", "C++")
    assert isinstance(e, Person)

def test_manager_override_printInfo(capsys):
    m = Manager(9, "송혜교", "대표")
    m.printInfo()
    captured = capsys.readouterr()
    assert "Title: 대표" in captured.out

def test_employee_override_printInfo(capsys):
    e = Employee(10, "유재석", "Go")
    e.printInfo()
    captured = capsys.readouterr()
    assert "Skill: Go" in captured.out

if __name__ == "__main__":
    p = Person(1, "홍길동")
    p.printInfo()

    m = Manager(2, "김철수", "팀장")
    m.printInfo()

    e = Employee(3, "이영희", "Python")
    e.printInfo()

# pytest로 테스트하려면 파일을 저장 후 터미널에서 아래 명령어 실행
# pytest copilotClass.py