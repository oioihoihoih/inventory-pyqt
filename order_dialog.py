from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QSpinBox
from db_helper import DB, DB_CONFIG
from datetime import date


class OrderDialog(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("주문")
        self.db = DB(**DB_CONFIG)

        self.username = QLineEdit()
        self.phonenumber = QLineEdit()

        self.products = self.db.fetch_product()
        print(self.products)

        central = QWidget()
        self.setCentralWidget(central)



        self.number_inputs = {}

        layout = QVBoxLayout(central)
        
        form = QFormLayout()
        for product_name in self.products:
            number_input = QSpinBox()
            number_input.setMinimum(0)
            self.number_inputs[product_name[1]] = number_input

            form.addRow(product_name[1],number_input)
            print(product_name[1],number_input)
        form.addRow("이름", self.username)
        form.addRow("전화번호", self.phonenumber)


        self.btn_order = QPushButton("주문")
        self.btn_order.clicked.connect(self.try_order)
        
        
        layout.addLayout(form)
        layout.addWidget(self.btn_order)


    def try_order(self):
        total = 0
        name = self.username.text().strip()
        phone = self.phonenumber.text().strip()
        

        for product in self.products:
            number = self.number_inputs[product[1]].value()
            print(product)

            print(self.db.fetch_stock(product[1]))

            print(self.db.fetch_stock(product[1])[0])

            print(number)

            if number == 0:
                continue
            stock = self.db.fetch_stock(product[1])[0]
            if  stock < number:
                QMessageBox.warning(self, f"{product[1]} 재고가 부족합니다", f"{product[3]}개 이하로 다시 시도해주세요")
                return
            else: 
                # 계산하고, 재고 빼고, 주문서 테이블 추가 
                self.db.update_stock(product[1],number)
                total += product[2] * number
                self.db.insert_order(product[1],number)
        self.db.insert_customer( name, total, phone, date.today())
