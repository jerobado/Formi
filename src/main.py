""" Main UI of Formi """

import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_ui import Formi


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    window = Formi()
    window.show()
    APP.exec()
