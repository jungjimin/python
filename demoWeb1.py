# demoWeb1.py
#크롤링 작업
from bs4 import BeautifulSoup

#페이지를 로딩
page = open("Chap09_test.html", "rt", encoding="utf-8")
#검색이 용이한 객체
soup = BeautifulSoup(page, "html.parser")
#전체 HTML 구조를 출력
#print(soup.prettify())
#<p> 전체 검색
#print(soup.find_all("p"))
#<p> 태그 중 첫 번째 검색
#print(soup.find("p")) #find : 첫 번째 하나만 검색
#특정 스타일 : <p class="outer-text">
#print(soup.find_all("p", class_="outer-text")) #BeautifulSoup 개발팀에서 정한 규칙임. class_ 이름 충돌을 피하기 위해
#print(soup.find(id='first')) #id 속성으로 검색
for tag in soup.find_all("p", class_="outer-text"):
    title = tag.text.strip() #태그 안의 텍스트를 추출 , strip()으로 공백 제거
    title = title.replace("\n", "") #줄바꿈 제거
    print(title)

