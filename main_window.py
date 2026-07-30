# main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 관리")
        self.db = DB(**DB_CONFIG)


        self.selected_product_id = None

        # 중앙 위젯 및 레이아웃
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)

        # 상단: 입력 폼 + 추가 버튼
        form_box = QHBoxLayout()
        self.input_product_name = QLineEdit()
        self.input_price = QLineEdit()
        self.input_number = QLineEdit()
        self.btn_add = QPushButton("추가")
        self.btn_add.clicked.connect(self.save_product)
        self.btn_delete =QPushButton("삭제")
        self.btn_delete.clicked.connect(self.delete_product)
        self.btn_delete.setEnabled(False)

        form_box.addWidget(QLabel("제품명"))
        form_box.addWidget(self.input_product_name)
        form_box.addWidget(QLabel("가격"))
        form_box.addWidget(self.input_price)
        form_box.addWidget(QLabel("갯수"))
        form_box.addWidget(self.input_number)
        form_box.addWidget(self.btn_add)
        form_box.addWidget(self.btn_delete)

        # 중앙: 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "제품명", "가격", "갯수","선택"])
        self.table.setEditTriggers(self.table.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        # 배치
        vbox.addLayout(form_box)
        vbox.addWidget(self.table)

        # 초기 데이터 로드
        self.load_products()

    def load_products(self):
        rows = self.db.fetch_product()
        self.table.setRowCount(len(rows))
        for r, (pid, product_name, price, stock) in enumerate(rows):
            self.table.setItem(r, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(r, 1, QTableWidgetItem(product_name))
            self.table.setItem(r, 2, QTableWidgetItem(str(price)))
            self.table.setItem(r, 3, QTableWidgetItem(str(stock)))
            btn_select = QPushButton("선택")

            btn_select.clicked.connect(
                lambda checked = False,pid = pid, product_name = product_name, price = price, stock = stock: self.select_product(pid,product_name,price,stock)
            )
            self.table.setCellWidget(r, 4, btn_select)

        self.table.resizeColumnsToContents()

    def save_product(self):
        product_name = (
            self.input_product_name.text().strip()
        )
        price_text = self.input_price.text().strip()
        number_text = self.input_number.text().strip()

        if not product_name or not price_text or not number_text:
            QMessageBox.warning(
                self,
                "입력 오류",
                "제품명, 가격, 개수를 모두 입력하세요.",
            )
            return

        try:
            price = int(price_text)
            number = int(number_text)

            if price < 0 or number < 0:
                raise ValueError

        except ValueError:
            QMessageBox.warning(
                self,
                "입력 오류",
                "가격과 개수는 0 이상의 숫자로 입력하세요.",
            )
            return
        if self.selected_product_id is None:
            result = self.db.insert_product(
                product_name,
                price,
                number,
            )

            if result:
                QMessageBox.information(
                    self,
                    "완료",
                    "상품이 추가되었습니다.",
                )

        else:
            result = self.db.update_product(
                self.selected_product_id,
                product_name,
                price,
                number,
            )

            if result:
                QMessageBox.information(
                    self,
                    "완료",
                    "상품이 수정되었습니다.",
                )

        if not result:
            QMessageBox.critical(
                self,
                "실패",
                "상품 처리 중 오류가 발생했습니다.",
            )
            return

        self.reset_form()
        self.load_products()

    def select_product(
        self,
        product_id,
        product_name,
        price,
        stock,
    ):
        self.selected_product_id = product_id
        self.input_product_name.setText(str(product_name))
        self.input_price.setText(str(price))
        self.input_number.setText(str(stock))

        self.btn_add.setText("수정")
        self.btn_delete.setEnabled(True)

    def delete_product(self):
        if self.selected_product_id is None:
            return

        answer = QMessageBox.question(
            self,
            "상품 삭제",
            "선택한 상품을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        result = self.db.delete_product(
            self.selected_product_id
        )

        if result:
            QMessageBox.information(
                self,
                "완료",
                "상품이 삭제되었습니다.",
            )
            self.reset_form()
            self.load_products()

        else:
            QMessageBox.critical(
                self,
                "실패",
                "상품 삭제 중 오류가 발생했습니다.",
            )
    def reset_form(self):
        self.selected_product_id = None

        self.input_product_name.clear()
        self.input_price.clear()
        self.input_number.clear()

        self.btn_add.setText("추가")
        self.btn_delete.setEnabled(False)