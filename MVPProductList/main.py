import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
from product_model import ProductModel

form_class = uic.loadUiType("Chap10_ProductList.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 모델 인스턴스
        self.model = ProductModel()

        # UI 초기화
        self.initUI()

    def initUI(self):
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setHorizontalHeaderLabels(["제품ID", "제품명", "가격"])
        self.tableWidget.setTabKeyNavigation(False)

        self.prodID.returnPressed.connect(lambda: self.focusNextChild())
        self.prodName.returnPressed.connect(lambda: self.focusNextChild())
        self.prodPrice.returnPressed.connect(lambda: self.focusNextChild())
        self.tableWidget.doubleClicked.connect(self.doubleClick)

    def addProduct(self):
        name = self.prodName.text()
        price = self.prodPrice.text()
        self.model.add_product(name, price)
        self.getProduct()

    def updateProduct(self):
        prod_id = self.prodID.text()
        name = self.prodName.text()
        price = self.prodPrice.text()
        self.model.update_product(prod_id, name, price)
        self.getProduct()

    def removeProduct(self):
        prod_id = self.prodID.text()
        self.model.delete_product(prod_id)
        self.getProduct()

    def getProduct(self):
        self.tableWidget.clearContents()
        products = self.model.get_all_products()
        for row, item in enumerate(products):
            itemID = QTableWidgetItem(str(item[0]))
            itemID.setTextAlignment(Qt.AlignRight)
            itemName = QTableWidgetItem(item[1])
            itemPrice = QTableWidgetItem(str(item[2]))
            itemPrice.setTextAlignment(Qt.AlignRight)

            self.tableWidget.setItem(row, 0, itemID)
            self.tableWidget.setItem(row, 1, itemName)
            self.tableWidget.setItem(row, 2, itemPrice)

    def doubleClick(self):
        row = self.tableWidget.currentRow()
        self.prodID.setText(self.tableWidget.item(row, 0).text())
        self.prodName.setText(self.tableWidget.item(row, 1).text())
        self.prodPrice.setText(self.tableWidget.item(row, 2).text())

    def closeEvent(self, event):
        self.model.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoForm = DemoForm()
    demoForm.show()
    app.exec_()
