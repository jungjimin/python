# demoLoop.py

value = 5
while value > 0:
    print(value)
    value -= 1

print("---for in---")
#list
lst = [100,"apple",3.14]
for item in lst:
    print(item,type(item))

#dict
fruits = {100:"apple",200:"banana"}
for item in fruits.items():
    print(item)

print("---수열함수---")
print(list(range(1,11)))
print(list(range(2000,2026)))
print(list(range(1,32)))

print("---리스트내장---")
lst = list(range(1,11))
print(lst)

print([i**2 for i in lst if i>5] ) #for in loop + if 조건문 추가 가능.
#36 49 ~100

tp=("apple","kiwi")
print([len(i) for i in tp])
      
#기존에는 이렇게      
#필터링 함수
lst = [10,25,30]
def getBiggerThan20(i):
    return i>20

#필터링
itemL = filter(getBiggerThan20, lst)
for item in itemL:
    print(item) 

#람다를 쓰면 몇줄로 끝  (일회성으로만 쓸거야.)
print("---람다함수사용---")
itemL = filter(lambda x:x>20, lst)
for item in itemL:
    print(item) #25,30