import sys
from PyQt5.QtWidgets import QApplication
from order_dialog import OrderDialog
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MainWindow()
    w = OrderDialog(m)
    
    w.show()
    m.show()
    app.exec_()
