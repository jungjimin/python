import requests
from bs4 import BeautifulSoup

# 1. 세션 객체 생성
session = requests.Session()

# 2. 로그인 정보 입력
login_info = {
    'userId': '너의_아이디',
    'userPassword': '너의_비밀번호'
}

# 3. 로그인 요청 (해당 URL은 사이트마다 다름)
login_url = "https://www.clien.net/service/login"

# 실제 로그인은 POST로 보냄 (폼 데이터와 함께)
res = session.post(login_url, data=login_info)

# 4. 로그인 성공 후, 크롤링할 페이지 접근
target_url = "https://www.clien.net/service/board/sold"
res = session.get(target_url)

# 5. HTML 파싱
soup = BeautifulSoup(res.text, "html.parser")

# 6. 원하는 데이터 추출
for tag in soup.find_all("span", attrs={'data-role': "list-title-text"}):
    title = tag.text.strip()
    print(title)
