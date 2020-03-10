""" Main Graphical User Interface of Formi. """

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPlainTextEdit,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGroupBox,
                             QCheckBox,
                             QRadioButton)
from src.core import formi

__version__ = '0.2.2'


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
        self.operationsGroupBox = QGroupBox()
        self.removeDuplicateCheckBox = QCheckBox()

    def _properties(self):

        self.vertical_inputTextEdit.setPlaceholderText('Sample input text:\n\nbanana\napple\nkiwi\norange')
        self.vertical_inputTextEdit.setObjectName('vertical_inputTextEdit')
        self.horizontal_outputTextEdit.setPlaceholderText('Output text:\n\nbanana, apple, kiwi, orange')
        self.horizontal_outputTextEdit.setObjectName('horizontal_inputTextEdit')
        self.operationsGroupBox.setTitle('Operations')
        self.removeDuplicateCheckBox.setText('Remove &duplicates')
        self.setWindowTitle(f'Formi {__version__} - text formatter For Humans')
        self.resize(471, 240)   # width, height

    def _layouts(self):

        groupbox_layout = QVBoxLayout()
        groupbox_layout.addWidget(self.removeDuplicateCheckBox)
        groupbox_layout.addStretch()

        self.operationsGroupBox.setLayout(groupbox_layout)

        hor = QHBoxLayout()
        hor.addWidget(self.vertical_inputTextEdit)
        hor.addWidget(self.horizontal_outputTextEdit)
        hor.addWidget(self.operationsGroupBox)
        self.setLayout(hor)

    def _connections(self):

        # self.vertical_inputTextEdit.textChanged.connect(self.on_vertical_inputTextEdit_textChanged)
        # self.horizontal_outputTextEdit.textChanged.connect(self.on_horizontal_inputTextEdit_textChanged)

        # TEST: consolidate to one function
        self.vertical_inputTextEdit.textChanged.connect(self.on_TextEdit_textChanged)
        self.horizontal_outputTextEdit.textChanged.connect(self.on_TextEdit_textChanged)

        self.removeDuplicateCheckBox.clicked.connect(self.on_removeDuplicateCheckBox_clicked)

    def on_TextEdit_textChanged(self):

        widget = self.sender()
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
        print(f'input count: {formi.count_input(input_text)}')

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

    # [] TODO: not yet triggered when initially check before adding a new input
    def on_removeDuplicateCheckBox_clicked(self):

        if self.removeDuplicateCheckBox.isChecked():
            expand = formi.expand_string(self.formatted_text)
            unique = formi.remove_duplicate(expand)
            self.formatted_text = ', '.join(unique)
            self.horizontal_outputTextEdit.setPlainText(self.formatted_text)
            self.clipboard.setText(self.horizontal_outputTextEdit.toPlainText())

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()
