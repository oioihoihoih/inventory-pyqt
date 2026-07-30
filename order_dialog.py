from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QMainWindow, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QSpinBox
from PyQt5.QtCore import pyqtSignal
from db_helper import DB, DB_CONFIG
from datetime import date


class OrderDialog(QMainWindow):
    order_completed = pyqtSignal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setWindowTitle("주문")
        self.db = DB(**DB_CONFIG)
        self.main_window = parent


        self.username = QLineEdit()
        self.phonenumber = QLineEdit()

        self.products = self.db.fetch_product()

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
        a = 0 
        for product in self.products:
            number = self.number_inputs[product[1]].value()
            print(type(number),number)
            if number == 0:
                continue
            stock = self.db.fetch_stock(product[1])[0]
            if  stock < number:
                QMessageBox.warning(self, f"{product[1]} 재고가 부족합니다", f"{product[3]}개 이하로 다시 시도해주세요")
                return
            else: 
                self.db.update_stock(product[1],number)
                total += product[2] * number

                self.db.insert_order(a ,product[1],number)
        self.db.insert_customer( name, total, phone, date.today())
        self.db.change_customer_id(a,customer_id)

        if self.main_window is not None:
            self.main_window.load_products()
            self.show_receipt()


    def show_receipt(self):

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["제품명", "갯수"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        
        rows = self.db.fetch_receipts()
        print(rows)
        self.table.setRowCount(len(rows))
        for r, (product_name, number) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(product_name))
            self.table.setItem(r, 1, QTableWidgetItem(str(number)))
        self.table.resizeColumnsToContents()
        self.centralWidget().layout().addWidget(self.table)