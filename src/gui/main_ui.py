""" Main Graphical User Interface of Formi. """

from PyQt5.QtCore import (Qt,
                          QSettings)
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QPlainTextEdit,
                             QGridLayout,
                             QVBoxLayout,
                             QHBoxLayout,
                             QGroupBox,
                             QCheckBox,
                             QRadioButton,
                             QLabel)
from src.core import formi

__version__ = '0.2.4'


class Formi(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.clipboard = QApplication.clipboard()
        self.formatted_text = ''
        self.settings = QSettings()
        self._widgets()
        self._properties()
        self._layouts()
        self._connections()
        self._read_settings()

    def _read_settings(self):

        self.restoreGeometry(self.settings.value('formi_geometry', self.saveGeometry()))

    def _widgets(self):

        self.vertical_inputTextEdit = QPlainTextEdit()
        self.horizontal_outputTextEdit = QPlainTextEdit()
        self.verticalCountLabel = QLabel()
        self.horizontalCountLabel = QLabel()
        self.operationsGroupBox = QGroupBox()
        self.removeDuplicateCheckBox = QCheckBox()

    def _properties(self):

        self.vertical_inputTextEdit.setPlaceholderText('Sample input text:\n\nbanana\napple\nkiwi\norange')
        self.vertical_inputTextEdit.setObjectName('vertical_inputTextEdit')
        self.horizontal_outputTextEdit.setPlaceholderText('Output text:\n\nbanana, apple, kiwi, orange')
        self.horizontal_outputTextEdit.setObjectName('horizontal_inputTextEdit')
        self.verticalCountLabel.setText('Count:')
        self.horizontalCountLabel.setText('Count:')
        self.operationsGroupBox.setTitle('Operations')
        self.removeDuplicateCheckBox.setText('Remove &duplicates')
        self.setWindowTitle(f'Formi {__version__} - text formatter For Humans')
        self.resize(471, 240)   # width, height

    def _layouts(self):

        groupbox_layout = QVBoxLayout()
        groupbox_layout.addWidget(self.removeDuplicateCheckBox)
        groupbox_layout.addStretch()
        self.operationsGroupBox.setLayout(groupbox_layout)

        grid = QGridLayout()
        grid.addWidget(self.vertical_inputTextEdit, 0, 0)
        grid.addWidget(self.horizontal_outputTextEdit, 0, 1)
        grid.addWidget(self.operationsGroupBox, 0, 2)
        grid.addWidget(self.verticalCountLabel, 1, 0)
        grid.addWidget(self.horizontalCountLabel, 1, 1)

        self.setLayout(grid)

    def _connections(self):

        # [] TODO: test these connections to prevent from changing signals and slots
        self.vertical_inputTextEdit.textChanged.connect(self.on_TextEdit_textChanged)
        self.vertical_inputTextEdit.textChanged.connect(self.on_removeDuplicateCheckBox_clicked)

        self.removeDuplicateCheckBox.clicked.connect(self.on_removeDuplicateCheckBox_clicked)

    def on_TextEdit_textChanged(self):

        widget = self.sender()
        if widget.objectName() == 'vertical_inputTextEdit':
            self.on_vertical_inputTextEdit_textChanged()
            self.expand_text_horizontally()
            print(widget.objectName())
        else:
            self.on_horizontal_inputTextEdit_textChanged()
            self.expand_text_vertically()
            print(widget.objectName())

    def on_vertical_inputTextEdit_textChanged(self):

        input_text = self.vertical_inputTextEdit.toPlainText().strip()
        self.formatted_text = formi.join_string(input_text)
        self.verticalCountLabel.setText(f'Count: {formi.count_input(input_text)}')
        print(f'input count: {formi.count_input(input_text)}')
        print(f'output count: {len(self.formatted_text.split(","))}')

    def expand_text_horizontally(self):

        self.horizontal_outputTextEdit.setPlainText(self.formatted_text)
        self.clipboard.setText(self.formatted_text)

    # [] TODO: implement horizontal strings with comma to the vertical_inputTextEdit
    def on_horizontal_inputTextEdit_textChanged(self):

        input_text = self.horizontal_outputTextEdit.toPlainText().strip()
        self.formatted_text = formi.expand_string(input_text)

    def expand_text_vertically(self):

        self.vertical_inputTextEdit.setPlainText(self.formatted_text)
        self.clipboard.setText(self.formatted_text)

    # [] TODO: if unchecked, outputTextEdit should display text based on the original input
    def on_removeDuplicateCheckBox_clicked(self):

        if self.removeDuplicateCheckBox.isChecked():
            expand = formi.expand_string(self.formatted_text)
            unique = formi.remove_duplicate(expand)
            self.formatted_text = ', '.join(unique)
            self.horizontal_outputTextEdit.setPlainText(self.formatted_text)
            self.clipboard.setText(self.horizontal_outputTextEdit.toPlainText())

        print(f'output count: {len(self.formatted_text.split(","))}')
        output_len = len(self.formatted_text.split(','))
        self.horizontalCountLabel.setText(f'Count: {output_len}')

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()

    def closeEvent(self, event):

        self._write_settings()

    def _write_settings(self):

        self.settings.setValue('formi_geometry', self.saveGeometry())
