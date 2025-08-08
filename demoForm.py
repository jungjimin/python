# demoForm.py
# DemoForm.ui(화면) +  demoForm.py(로직) 연결
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

#디자인한 파일을 로딩
form_class = uic.loadUiType("DemoForm.ui")[0]
#DemoForm 클래스를 정의
class DemoForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 설정
        self.label.setText("첫번째 문자열 출력")
        
#진입점을 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    myWindow = DemoForm()  # DemoForm 객체 생성
    myWindow.show()  # 윈도우를 화면에 표시
    app.exec_()  # 이벤트 루프 시작