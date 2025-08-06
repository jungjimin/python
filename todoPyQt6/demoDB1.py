# demoDB1.py
import sqlite3

#연결객체를 리턴
#con = sqlite3.connect(":memory:")  # 메모리 내에 데이터베이스 생성
con = sqlite3.connect(r"c:\work\test.db")  # 파일로 데이터베이스 생성
#커서 객체를 리턴
cur = con.cursor()
#테이블 생성
cur.execute("DROP TABLE IF EXISTS PHONEBOOK;")  # 기존 테이블 삭제
cur.execute("CREATE TABLE PHONEBOOK (name text, phone text);")
#데이터 삽입
cur.execute("INSERT INTO PHONEBOOK VALUES ('전우치', '010-222-1234');")
#입력 파라미터 처리
name = '홍길동'
phone = '010-333-1234'
cur.execute("INSERT INTO PHONEBOOK VALUES (?, ?);", (name, phone)) #?에 변수 삽입
#여러건 입력
datalist = ("이순신", "010-444-1234"), ("강감찬", "010-555-1234")
cur.executemany("INSERT INTO PHONEBOOK VALUES (?, ?);", datalist) #executemany는 여러건 입력

#데이터 조회
cur.execute("SELECT * FROM PHONEBOOK;")
rows = cur.fetchall()
for row in rows:
    print(row)

#작업을 정상적 종료
con.commit()