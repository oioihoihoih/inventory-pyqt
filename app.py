import sys
from PyQt5.QtWidgets import QApplication
from order_dialog import OrderDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = OrderDialog()
    w.show()
    app.exec_()
