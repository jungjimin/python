# demoForm2.py
# DemoForm2.ui(화면) +  demoForm2.py(로직) 연결
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from bs4 import BeautifulSoup #HTML이 고정되어 있고 간단한 데이터 추출 시 사용
import urllib.request
import re 

#디자인한 파일을 로딩
form_class = uic.loadUiType("DemoForm2.ui")[0]
#DemoForm 클래스를 정의 (QMainWindow를 상속받음)
class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 설정
        self.label.setText("원하는 버튼을 누르시오") #라벨에 텍스트 설정
    def firstClick(self):  # UI 설정
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
                                if (re.search('한국', title)):
                                    f.write(title + "\n")
                                    self.label_2.setText(title)
                        except: #에러처리(skip)
                                pass                        
        f.close()
        self.label.setText("랄랄라")
    def secondClick(self):  # UI 설정
        self.label.setText("두번째 버튼 클릭했습니다~")
    def thirdClick(self):  # UI 설정
        self.label.setText("세번째 버튼 클릭입니다요")


#진입점을 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    myWindow = DemoForm()  # DemoForm 객체 생성
    myWindow.show()  # 윈도우를 화면에 표시
    app.exec_()  # 이벤트 루프 시작