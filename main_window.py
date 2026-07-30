# main_window.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, \
    QLabel, QLineEdit, QPushButton, QMessageBox
from db_helper import DB, DB_CONFIG

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("재고 관리")
        self.db = DB(**DB_CONFIG)

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
        self.btn_add.clicked.connect(self.add_product)

        form_box.addWidget(QLabel("제품명"))
        form_box.addWidget(self.input_product_name)
        form_box.addWidget(QLabel("가격"))
        form_box.addWidget(self.input_price)
        form_box.addWidget(QLabel("갯수"))
        form_box.addWidget(self.input_number)
        form_box.addWidget(self.btn_add)

        # 중앙: 테이블 위젯
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "제품명", "가격", "갯수"])
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
            self.table.setItem(r, 2, QTableWidgetItem(price))
            self.table.setItem(r, 2, QTableWidgetItem(stock))

        self.table.resizeColumnsToContents()

    def add_product(self):
        product_name = self.input_product_name.text().strip()
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

            if price < 0 or number <= 0:
                raise ValueError

        except ValueError:
            QMessageBox.warning(
                self,
                "입력 오류",
                "가격은 0 이상, 개수는 1 이상의 숫자로 입력하세요.",
            )
            return

        result = self.db.insert_or_update_product(
            product_name,
            price,
            number,
        )

        if result == "inserted":
            QMessageBox.information(
                self,
                "상품 추가 완료",
                f"{product_name} 상품이 추가되었습니다.",
            )

        elif result == "updated":
            QMessageBox.information(
                self,
                "상품 수정 완료",
                f"{product_name}의 가격이 변경되고 재고가 추가되었습니다.",
            )

        else:
            QMessageBox.critical(
                self,
                "실패",
                "상품 처리 중 오류가 발생했습니다.",
            )
            return

        self.input_product_name.clear()
        self.input_price.clear()
        self.input_number.clear()
        self.load_products()
