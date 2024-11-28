from PySide6 import QtWidgets
from helpers.validation import validate_host_ip, validate_port


class SNMPAgentTarget(QtWidgets.QWidget):
    """
    Custom QtPy widget to capture and validate user input for target IPv4 and
    port.

    Attributes:
        parent (QtWidget): Parent widget.
        ipv4_host (QtWidgets.QLineEdit): QLineEdit widget for IPv4 host.
        port (QtWidgets.QLineEdit): QLineEdit widget for port.
        update_state_callback (function): method to update state from parent
            widget.
    """

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
        """
        Wrapper function to validate the IP field and update validation
        state in parent.

        Args:
            ip_edit (QtWidgets.QLineEdit): New value in the IP field.
        """
        ip_text = ip_edit.text().strip()

        if validate_host_ip(ip_text):
            ip_edit.setStyleSheet("")
            self.parent.update_ipv4_host(ip_text)

        else:
            ip_edit.setStyleSheet("border: 1px solid red;")

    def update_port(self, port_edit):
        """
        Wrapper function to validate the port field and update validation
        state in parent.

        Args:
            port_edit (QtWidgets.QLineEdit): New value in the port field.
        """
        port_text = port_edit.text().strip()

        if validate_port(port_text):
            port_edit.setStyleSheet("")
            self.parent.update_port(port_text)

        else:
            port_edit.setStyleSheet("border: 1px solid red;")
