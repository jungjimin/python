import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sqlite3

# UI 파일 연결
form_class = uic.loadUiType("electronics.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initDB()
        self.initUI()
        
        # 버튼 연결
        self.btnAdd.clicked.connect(self.addProduct)
        self.btnUpdate.clicked.connect(self.updateProduct)
        self.btnDelete.clicked.connect(self.deleteProduct)
        self.btnSearch.clicked.connect(self.searchProduct)
        self.btnShowAll.clicked.connect(self.showAllProducts)
        
        # 테이블 클릭 이벤트 연결
        self.tblProducts.itemClicked.connect(self.tableItemClicked)
        
        # 초기 데이터 로드
        self.showAllProducts()
        
    def initUI(self):
        # 윈도우 설정
        self.setWindowTitle('전자제품 관리 시스템')
        self.setMinimumSize(800, 600)
        
        # 테이블 위젯 설정
        self.tblProducts.setAlternatingRowColors(True)
        self.tblProducts.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblProducts.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tblProducts.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # 스타일 시트 적용
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #bbb;
                border-radius: 3px;
                background-color: white;
                min-height: 25px;
            }
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1084E3;
            }
            QPushButton:pressed {
                background-color: #006CC1;
            }
            QTableWidget {
                border: 1px solid #bbb;
                border-radius: 3px;
                background-color: white;
                gridline-color: #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #0078D7;
                color: white;
            }
            QHeaderView::section {
                background-color: #0078D7;
                color: white;
                padding: 8px;
                border: none;
                border-right: 1px solid #006CC1;
            }
            QLabel {
                font-weight: bold;
            }
            QStatusBar {
                background-color: #f8f8f8;
                color: #333;
                padding: 5px;
            }
        """)

    def initDB(self):
        con = sqlite3.connect("electronics.db")
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS MyProducts
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             price INTEGER NOT NULL)""")
        con.commit()
        con.close()

    def tableItemClicked(self, item):
        row = item.row()
        self.txtId.setText(self.tblProducts.item(row, 0).text())
        self.txtName.setText(self.tblProducts.item(row, 1).text())
        self.txtPrice.setText(self.tblProducts.item(row, 2).text())
        
    def addProduct(self):
        name = self.txtName.text()
        price = self.txtPrice.text()
        if name and price:
            try:
                con = sqlite3.connect("electronics.db")
                cur = con.cursor()
                cur.execute("INSERT INTO MyProducts (name, price) VALUES (?, ?)",
                          (name, int(price)))
                con.commit()
                self.statusBar().showMessage("제품이 추가되었습니다.")
                self.clearInputs()
                self.showAllProducts()
            except Exception as e:
                self.statusBar().showMessage(f"에러 발생: {str(e)}")
            finally:
                con.close()
                
    def updateProduct(self):
        id = self.txtId.text()
        name = self.txtName.text()
        price = self.txtPrice.text()
        if id and name and price:
            try:
                con = sqlite3.connect("electronics.db")
                cur = con.cursor()
                cur.execute("UPDATE MyProducts SET name=?, price=? WHERE id=?",
                          (name, int(price), int(id)))
                con.commit()
                self.statusBar().showMessage("제품이 수정되었습니다.")
                self.clearInputs()
                self.showAllProducts()
            except Exception as e:
                self.statusBar().showMessage(f"에러 발생: {str(e)}")
            finally:
                con.close()
                
    def deleteProduct(self):
        id = self.txtId.text()
        if id:
            reply = QMessageBox.question(self, '확인', 
                                       '정말로 삭제하시겠습니까?',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    con = sqlite3.connect("electronics.db")
                    cur = con.cursor()
                    cur.execute("DELETE FROM MyProducts WHERE id=?", (int(id),))
                    con.commit()
                    self.statusBar().showMessage("제품이 삭제되었습니다.")
                    self.clearInputs()
                    self.showAllProducts()
                except Exception as e:
                    self.statusBar().showMessage(f"에러 발생: {str(e)}")
                finally:
                    con.close()
                
    def searchProduct(self):
        name = self.txtName.text()
        try:
            con = sqlite3.connect("electronics.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM MyProducts WHERE name LIKE ?",
                      (f"%{name}%",))
            self.showSearchResults(cur.fetchall())
        except Exception as e:
            self.statusBar().showMessage(f"에러 발생: {str(e)}")
        finally:
            con.close()
            
    def showAllProducts(self):
        try:
            con = sqlite3.connect("electronics.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM MyProducts")
            self.showSearchResults(cur.fetchall())
        except Exception as e:
            self.statusBar().showMessage(f"에러 발생: {str(e)}")
        finally:
            con.close()
            'l'
    def showSearchResults(self, rows):
        self.tblProducts.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.tblProducts.setItem(i, j, item)
                
    def clearInputs(self):
        self.txtId.clear()
        self.txtName.clear()
        self.txtPrice.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())