import time

print(dir(time))
print(time.time())  # 현재 시간을 초 단위로 출력

print(time.sleep(10))  # 10초 동안 대기
print(time.localtime())  # 현재 시간을 구조체로 출력
print(time.asctime(time.localtime()))  # 현재 시간을 읽기 쉬운 형식으로 출력
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))  # 현재 시간을 지정된 형식으로 출력

from datetime import *
print(dir())

print(MAXYEAR)  # 최대 연도 출력
print(MINYEAR)  # 최소 연도 출력

d1 = date(2025, 7, 1)  # 날짜 객체 생성
print(d1)  # 날짜 출력

datetime.date(2025, 8, 6)  #수정해야함 왜 안되는지...
d2 = date.today()  # 오늘 날짜 객체 생성
print(d2)  # 오늘 날짜 출력

datetime.date(2025, 7, 6)
d3 = datetime.now()
print(d3)

datetime.datetime(2025,8,6,10,44,31,104558)
d4=timedelta(days=100)
print(d4)  # timedelta 객체 출력

d1+d4
print(d1 + d4)  # 날짜에 timedelta를 더하기
datetime.date(2025,10,9)
d1-d4
print(d1 - d4)  # 날짜에서 timedelta를 빼기
datetime.date(2025,3,23)

import random
print(dir(random))

print(random.random())
print(random.random())
print(random.uniform(2.0, 5.0))  # 2.0과 5.0 사이의 실수 반환
print(random.uniform(2.0, 5.0))  # 2.0과 5.0 사이의 실수 반환
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])
print([random.randrange(20) for i in range(10)])
print([random.sample(range(20), 10)])
print([random.sample(range(20), 10)])