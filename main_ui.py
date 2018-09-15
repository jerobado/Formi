""" Main Graphical User Interface of Formi. """

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPlainTextEdit,
                             QHBoxLayout)
import formi

__version__ = '0.1'


class Formi(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.clipboard = QApplication.clipboard()
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        self.inputTextEdit = QPlainTextEdit()
        self.outputTextEdit = QPlainTextEdit()

    def _properties(self):

        self.inputTextEdit.setPlaceholderText('Sample input text:\n\nbanana\napple\nkiwi\norange')
        self.outputTextEdit.setPlaceholderText('Output text:\n\nbanana, apple, kiwi, orange')
        self.setWindowTitle(f'Formi {__version__} - text formatter For Humans')
        self.resize(471, 240)   # width, height

    def _layouts(self):

        hor = QHBoxLayout()
        hor.addWidget(self.inputTextEdit)
        hor.addWidget(self.outputTextEdit)
        self.setLayout(hor)

    def _connections(self):

        self.inputTextEdit.textChanged.connect(self.on_inputTextEdit_textChanged)

    def on_inputTextEdit_textChanged(self):

        input_text = self.inputTextEdit.toPlainText()
        formatted_text = formi.join_string(input_text)

        self.outputTextEdit.setPlainText(formatted_text)
        self.clipboard.setText(formatted_text)

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()
