# coding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import re 

#User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

f = open("todayhumor.txt", "wt", encoding="utf-8")
for n in range(1,11):
        #오늘의 유머 베스트 게시판에서 글을 찾는다.
        data ='https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=' + str(n)
        print(data)
        #웹브라우져 헤더 추가 
        req = urllib.request.Request(data, headers = hdr)
        #req = urllib.request.Request(data, \
        #                             headers = hdr)  #\로 줄바꿈 가능
        data = urllib.request.urlopen(req).read()
        #한글이 깨지는 경우
        page = data.decode('utf-8', 'ignore') #글자가 깨져도 무시하고 읽기
        soup = BeautifulSoup(page, 'html.parser')
        list = soup.findAll('td', attrs={'class':'subject'})

        for item in list:
                try:
                        # 내부에 있는 a태그를 찾는다.
                        title = item.find('a').text.strip() #공백 제거
                        if (re.search('미국', title)):
                            print(title)
                            f.write(title + "\n")
                except: #에러처리(skip)
                        pass
                
f.close()
        
#<a href="/board/view.php?table=bestofbest&amp;no=480460&amp;s_no=480460&amp;page=1" target="_top">미국 마트에서 딸기 다 쏟은 한국인</a>