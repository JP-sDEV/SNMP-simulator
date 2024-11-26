from PySide6 import QtWidgets
from helpers.validation import validate_host_ip, validate_port


class SNMPAgentTarget(QtWidgets.QWidget):
    def __init__(self,
                 parent,
                 ipv4_host: QtWidgets.QLineEdit,
                 port: QtWidgets.QLineEdit,
                 update_state_callback):
        super().__init__(parent)

        self.parent = parent
        self.ipv4_host = ipv4_host
        self.port = port
        self.update_state_callback = update_state_callback

        layout = QtWidgets.QHBoxLayout()

        self.ipv4_host.editingFinished.connect(
           lambda: self.update_ip(self.ipv4_host)
        )
        self.port.editingFinished.connect(
            lambda: self.update_port(self.port)
        )

        layout.addWidget(QtWidgets.QLabel("IPv4 Host:"))
        layout.addWidget(self.ipv4_host)
        layout.addWidget(QtWidgets.QLabel("Port:"))
        layout.addWidget(self.port)

        self.setLayout(layout)

    def update_ip(self, ip_edit):
        ip_text = ip_edit.text().strip()

        if validate_host_ip(ip_text):
            ip_edit.setStyleSheet("")
            self.parent.update_ipv4_host(ip_text)

        else:
            ip_edit.setStyleSheet("border: 1px solid red;")

    def update_port(self, port_edit):
        port_text = port_edit.text().strip()

        if validate_port(port_text):
            port_edit.setStyleSheet("")
            self.parent.update_port(port_text)

        else:
            port_edit.setStyleSheet("border: 1px solid red;")
