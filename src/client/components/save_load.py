from PySide6 import QtWidgets


class SNMPAgentVarbinds(QtWidgets.QWidget):
    def __init__(self, ipv4_host: str, port: str, varbinds: list, parent=None):
        super().__init__(parent)

        # List to hold Varbind instances and their layouts
        self.varbinds = varbinds

        # Set up the main layout
        self.layout = QtWidgets.QVBoxLayout()

        # Button to add new Varbinds
        self.add_field_button = QtWidgets.QPushButton("Add New Field Set")
        self.add_field_button.clicked.connect(self.add_varbind)
        self.layout.addWidget(self.add_field_button)

        # Set layout to this widget
        self.setLayout(self.layout)
