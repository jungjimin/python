# BankAccount.py

#은행의 계정을 표현한 클래스 
class BankAccount:
    # 초기화 메서드
    def __init__(self, id, name, balance):
        #이름 숨김 : __변수명
        #self.id = id
        self.__id = id
        self.__name = name
        self.__balance = balance
    # 입금
    def deposit(self, amount):
        self.__balance += amount
    # 출금
    def withdraw(self, amount):
        self.__balance -= amount
    def __str__(self):
        return "{0} , {1} , {2}".format(self.__id, \
            self.__name, self.__balance)

#인스턴스 객체를 생성
account1 = BankAccount(100, "전우치", 15000)
account1.deposit(5000)
account1.withdraw(3000) #account1. 누르면 멤버변수가 다 보인다. 보이면 안됨.
#account1.balance = 150000000 #잔고를 수정할 수 있음;;;
print(account1)

#외부에서 접근
#print(account1.__balance) #에러 발생(내부에서만 접근가능하여 외부에서 접근불가.)
