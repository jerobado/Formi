""" Main Graphical User Interface of Formi. """

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPlainTextEdit,
                             QHBoxLayout)
import formi

__version__ = '0.2'


class Formi(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.clipboard = QApplication.clipboard()
        self.formatted_text = ''
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()

    def _widgets(self):

        self.vertical_inputTextEdit = QPlainTextEdit()
        self.horizontal_outputTextEdit = QPlainTextEdit()

    def _properties(self):

        self.vertical_inputTextEdit.setPlaceholderText('Sample input text:\n\nbanana\napple\nkiwi\norange')
        self.vertical_inputTextEdit.setObjectName('vertical_inputTextEdit')
        self.horizontal_outputTextEdit.setPlaceholderText('Output text:\n\nbanana, apple, kiwi, orange')
        self.horizontal_outputTextEdit.setObjectName('horizontal_inputTextEdit')
        self.setWindowTitle(f'Formi {__version__} - text formatter For Humans')
        self.resize(471, 240)   # width, height

    def _layouts(self):

        hor = QHBoxLayout()
        hor.addWidget(self.vertical_inputTextEdit)
        hor.addWidget(self.horizontal_outputTextEdit)
        self.setLayout(hor)

    def _connections(self):

        # self.vertical_inputTextEdit.textChanged.connect(self.on_vertical_inputTextEdit_textChanged)
        # self.horizontal_outputTextEdit.textChanged.connect(self.on_horizontal_inputTextEdit_textChanged)

        # TEST: consolidate to one function
        self.vertical_inputTextEdit.textChanged.connect(self.on_TextEdit_textChanged)
        self.horizontal_outputTextEdit.textChanged.connect(self.on_TextEdit_textChanged)

    def on_TextEdit_textChanged(self):

        widget = self.sender()
        print(widget.objectName())
        if widget.objectName() == 'vertical_inputTextEdit':
            self.horizontal_outputTextEdit.disconnect()
            self.on_vertical_inputTextEdit_textChanged()
            self.expand_text_horizontally()
            self.horizontal_outputTextEdit.textChanged.connect(self.on_TextEdit_textChanged)
            print(widget.objectName())
        else:
            self.vertical_inputTextEdit.disconnect()
            self.on_horizontal_inputTextEdit_textChanged()
            self.expand_text_vertically()
            self.vertical_inputTextEdit.textChanged.connect(self.on_TextEdit_textChanged)
            print(widget.objectName())

    def on_vertical_inputTextEdit_textChanged(self):

        # widget = self.sender()
        # print(widget.objectName())
        input_text = self.vertical_inputTextEdit.toPlainText().strip()
        self.formatted_text = formi.join_string(input_text)

    def expand_text_horizontally(self):

        self.horizontal_outputTextEdit.setPlainText(self.formatted_text)
        self.clipboard.setText(self.formatted_text)

    def on_horizontal_inputTextEdit_textChanged(self):

        # widget = self.sender()
        # print(widget.objectName())
        input_text = self.horizontal_outputTextEdit.toPlainText().strip()
        self.formatted_text = formi.expand_string(input_text)

    def expand_text_vertically(self):

        self.vertical_inputTextEdit.setPlainText(self.formatted_text)
        self.clipboard.setText(self.formatted_text)

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()
