from PySide6 import QtWidgets


class ChildWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        layout = QtWidgets.QVBoxLayout()

        # Button to update parent's state
        self.button = QtWidgets.QPushButton("Update Parent State", self)
        self.button2 = QtWidgets.QPushButton("Update 2 Parent State", self)
        self.button.clicked.connect(lambda: self.request_update('1'))
        self.button2.clicked.connect(lambda: self.request_update('2'))

        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        self.setLayout(layout)

    def request_update(self, txt):
        # Request the parent to update its state
        self.parent.update_state(txt)
