from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QSpinBox
from db_helper import DB, DB_CONFIG
from datetime import date


class OrderDialog(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("주문")
        self.db = DB(**DB_CONFIG)

        self.number = QLineEdit()
        self.username = QLineEdit()
        self.phonenumber = QLineEdit()

        self.products = self.db.fetch_product()
        form = QFormLayout()
        for product_name in self.products:
            form.addRow(product_name[1],self.number)
        form.addRow("이름", self.username)
        form.addRow("전화번호", self.phonenumber)

        self.btn_order = QPushButton("주문")
        self.btn_order.clicked.connect(self.try_order)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.btn_order)
        self.setLayout(layout)            

    def try_order(self):
        total = 0
        name = self.username.text().strip()
        phone = self.phonenumber.text().strip()
        for product in self.products:
            number = int(self.number.text())
            if self.db.fetch_stock(product[1]) < number:
                QMessageBox.warning(self, product[1]+"의 재고가 부족합니다", product[3]+"개 이하로 다시 시도해주세요")
                return
            else: 
                # 계산하고, 재고 빼고, 주문서 테이블 추가 
                self.db.update_stock(product[1],number)
                total += product[2] * number
                self.db.insert_customer(name,total,phone,str(date.today()))
                self.db.insert_order(product[1],number)
            