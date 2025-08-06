# demoWebCrwawling.py
from bs4 import BeautifulSoup
import urllib.request
import re

url = "https://www.clien.net/service/board/sold"

# 페이지를 로딩
# <span class="subject_fixed" data-role="list-title-text" title="아이폰 13미니 256 팝니다">
# 	아이폰 13미니 256 팝니다
# </span>

#함수 체인(메서드 체인)
data = urllib.request.urlopen(url)
soup = BeautifulSoup(data, "html.parser")
for tag in soup.find_all("span", attrs={'data-role': "list-title-text"}):
	title = tag.text.strip()  # 태그 안의 텍스트를 추출, strip()으로 공백 제거
	title = title.replace("\n", "")  # 줄바꿈 제거
	print(title)