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
                             QLabel,
                             QLineEdit)
from src.core import formi

__version__ = '0.2.6'


class Formi(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.clipboard = QApplication.clipboard()
        self.input_text = str           # raw text input
        self.formatted_text = str       # formatted/processed text after certain operation(s)
        self.output_text = str          # text to display as result
        self.unique_items = list
        self.separator_char = ','
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
        self.separatorLineEdit = QLineEdit()
        self.separatorLabel = QLabel()

    def _properties(self):

        self.vertical_inputTextEdit.setPlaceholderText('Sample input text:\n\nbanana\napple\nkiwi\norange')
        self.vertical_inputTextEdit.setObjectName('vertical_inputTextEdit')
        self.horizontal_outputTextEdit.setPlaceholderText('Output text:\n\nbanana, apple, kiwi, orange')
        self.horizontal_outputTextEdit.setObjectName('horizontal_inputTextEdit')
        self.verticalCountLabel.setText('Count:')
        self.horizontalCountLabel.setText('Count:')
        self.operationsGroupBox.setTitle('Operations')
        self.removeDuplicateCheckBox.setText('Remove &duplicates')
        self.separatorLineEdit.setMaxLength(1)
        self.separatorLineEdit.setMaximumWidth(14)
        self.separatorLineEdit.setAlignment(Qt.AlignCenter)
        self.separatorLabel.setText('&Separator')
        self.separatorLabel.setBuddy(self.separatorLineEdit)
        self.setWindowTitle(f'Formi {__version__} - text formatter For Humans')
        self.resize(471, 240)   # width, height

    def _layouts(self):

        separator_widgets = QHBoxLayout()
        separator_widgets.addWidget(self.separatorLineEdit)
        separator_widgets.addWidget(self.separatorLabel)

        groupbox_layout = QVBoxLayout()
        groupbox_layout.addWidget(self.removeDuplicateCheckBox)
        groupbox_layout.addLayout(separator_widgets)
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
        # self.vertical_inputTextEdit.textChanged.connect(self.on_removeDuplicateCheckBox_clicked)    # see self.on_operation_widget_slot
        # self.vertical_inputTextEdit.textChanged.connect(self.on_separatorLineEdit_textChanged)      # see self.on_operation_widget_slot
        self.vertical_inputTextEdit.textChanged.connect(self.on_operation_widget_slot)

        # self.removeDuplicateCheckBox.clicked.connect(self.on_removeDuplicateCheckBox_clicked)
        # self.separatorLineEdit.textChanged.connect(self.on_separatorLineEdit_textChanged)

        # [] TODO: connect operations widget's signals to one slot
        self.removeDuplicateCheckBox.clicked.connect(self.on_operation_widget_slot)
        self.separatorLineEdit.textChanged.connect(self.on_operation_widget_slot)

    def on_TextEdit_textChanged(self):

        widget = self.sender()
        if widget.objectName() == 'vertical_inputTextEdit':
            self.on_vertical_inputTextEdit_textChanged()
            self.expand_text_horizontally()
            self.count_items()
            print(widget.objectName())
        else:
            self.on_horizontal_inputTextEdit_textChanged()
            self.expand_text_vertically()
            self.count_items()
            print(widget.objectName())

    def on_vertical_inputTextEdit_textChanged(self):

        self.input_text = self.vertical_inputTextEdit.toPlainText().strip()
        print(f'input_text: {self.input_text}')
        self.output_text = formi.join_string(self.input_text)
        self.verticalCountLabel.setText(f'Count: {formi.count_input(self.input_text)}')
        print(f'input count: {formi.count_input(self.input_text)}')
        print(f'output count: {len(self.output_text.split(","))}')

    def expand_text_horizontally(self):

        self.horizontal_outputTextEdit.setPlainText(self.output_text)
        self.clipboard.setText(self.output_text)

    def count_items(self):

        # default operations
        print('this -> ', self.separator_char)
        print(self.output_text, self.output_text.split(f"{self.separator_char}"))
        print(f'output count: {len(self.output_text.split(f"{self.separator_char}"))}')
        output_len = len(self.output_text.split(f'{self.separator_char}'))
        self.horizontalCountLabel.setText(f'Count: {output_len}')

    # [] TODO: implement horizontal strings with comma to the vertical_inputTextEdit
    def on_horizontal_inputTextEdit_textChanged(self):

        input_text = self.horizontal_outputTextEdit.toPlainText().strip()
        self.output_text = formi.expand_string(input_text)

    def expand_text_vertically(self):

        self.vertical_inputTextEdit.setPlainText(self.output_text)
        self.clipboard.setText(self.output_text)

    # [] TODO: if unchecked, outputTextEdit should display text based on the original input
    def on_removeDuplicateCheckBox_clicked(self):

        if self.removeDuplicateCheckBox.isChecked():
            expand = formi.expand_string(self.output_text)
            self.unique_items = formi.remove_duplicate(expand)
            self.formatted_text = self.unique_items
            self.output_text = f'{self.separator_char} '.join(self.unique_items)
            self.horizontal_outputTextEdit.setPlainText(self.output_text)
            self.clipboard.setText(self.horizontal_outputTextEdit.toPlainText())

    # [] TODO: add test to separate items on the input strings
    def on_separatorLineEdit_textChanged(self):

        input_text = self.vertical_inputTextEdit.toPlainText().strip()
        self.separator_char = self.separatorLineEdit.text()

        if self.separatorLineEdit.text():
            # custom delimiter
            self.output_text = formi.join_string(input_text, self.separatorLineEdit.text())
        else:
            # default delimiter, comma
            self.output_text = formi.join_string(input_text)

        self.horizontal_outputTextEdit.setPlainText(self.output_text)
        self.clipboard.setText(self.output_text)

    # TEST: combining operation widget's activated signals into a single slot
    def on_operation_widget_slot(self):

        if self.removeDuplicateCheckBox.isChecked():
            print('removeDuplicateCheckBox')
            # do operations to remove duplicate
            self.on_removeDuplicateCheckBox_clicked()

        if self.separatorLineEdit.text():
            print('separatorLineEdit')
            # do operations to separate strings
            self.on_separatorLineEdit_textChanged()

        if self.removeDuplicateCheckBox.isChecked() and self.separatorLineEdit.text():
            print('both operations:')
            self.output_text = f'{self.separatorLineEdit.text()} '.join(self.unique_items)

        self.horizontal_outputTextEdit.setPlainText(self.output_text)
        self.clipboard.setText(self.output_text)
        self.count_items()

    def keyPressEvent(self, event):

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()

    def closeEvent(self, event):

        self._write_settings()

    def _write_settings(self):

        self.settings.setValue('formi_geometry', self.saveGeometry())
