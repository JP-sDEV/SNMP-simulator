from PySide6 import QtWidgets


class SNMPAgentTarget(QtWidgets.QWidget):
    def __init__(self,
                 parent,
                 ipv4_host: QtWidgets.QLineEdit,
                 port: QtWidgets.QLineEdit):
        super().__init__(parent)

        self.parent = parent
        self.ipv4_host = ipv4_host
        self.port = port

        layout = QtWidgets.QVBoxLayout()

        # Connect signals to parent's update methods
        self.ipv4_host.textChanged.connect(parent.update_ipv4_host)
        self.port.textChanged.connect(parent.update_port)

        layout.addWidget(self.ipv4_host)
        layout.addWidget(self.port)

        self.setLayout(layout)
