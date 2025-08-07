# coding:utf-8
from bs4 import BeautifulSoup #HTML이 고정되어 있고 간단한 데이터 추출 시 사용
import urllib.request
import re 

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

for n in range(0,10):
        #클리앙의 중고장터 주소 
        data ='https://www.clien.net/service/board/sold?&od=T31&po=' + str(n)
        #웹브라우져 헤더 추가 
        req = urllib.request.Request(data, headers = hdr)
        #req = urllib.request.Request(data, \
        #                             headers = hdr)  #\로 줄바꿈 가능
        data = urllib.request.urlopen(req).read()
        #한글이 깨지는 경우
        page = data.decode('utf-8', 'ignore') #글자가 깨져도 무시하고 읽기
        soup = BeautifulSoup(page, 'html.parser')
        list = soup.findAll('span', attrs={'data-role':'list-title-text'})

        for item in list:
                try:
                        title = item.text.strip() #공백 제거
                        if (re.search('아이폰', title)):
                                print(title)
                except: #에러처리(skip)
                        pass
        
