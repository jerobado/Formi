""" Main UI of Formi """

import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_ui import Formi


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    APP.setOrganizationName('GIPSC COS Team')
    APP.setApplicationName('Formi')
    window = Formi()
    window.show()
    APP.exec()
