import sys
from PySide6 import QtWidgets
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from agents.transaction import TransactionSNMPAgent
from components.target import SNMPAgentTarget
from components.varbinds import SNMPAgentVarbinds
from components.notification import SNMPNotification
from components.save_config import SaveConfig
from components.load_config import LoadConfig
from helpers.validation import validate_host_ip, validate_port, validate_OID


class SNMPAgentClient(QtWidgets.QWidget):
    """
    A client to set the IP, port, OID, and varbinds in the SNMPAgent class.
    """

    def __init__(self):
        super().__init__()

        # Agent State
        self.valid = {
            "target_ip": False,
            "target_port": False,
            "notification_OID": False,
            "varbinds": False
        }

        # Target
        self.ipv4_host = QtWidgets.QLineEdit(self)
        self.port = QtWidgets.QLineEdit(self)
        # Notification
        self.notification_OID = QtWidgets.QLineEdit(self)
        # Varbinds
        self.varbinds = []

        # Window Labels
        window_title = QtWidgets.QLabel("SNMPv2c Agent Simulator")
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        window_title.setFont(font)
        window_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWindowTitle("SNMP Agent Simulator")

        # Layouts
        main_layout = QtWidgets.QVBoxLayout()
        btn_layout = QtWidgets.QHBoxLayout()  # Save/Load buttons
        send_layout = QtWidgets.QVBoxLayout()

        # Agent
        self.target = SNMPAgentTarget(parent=self,
                                      ipv4_host=self.ipv4_host,
                                      port=self.port,
                                      update_state_callback=self.update_state)

        self.notification = SNMPNotification(
            parent=self,
            notification_OID=self.notification_OID,
            update_state_callback=self.update_state)

        self.agent_varbinds = SNMPAgentVarbinds(
            varbinds=self.varbinds,
            parent=self,
            update_state_callback=self.update_state)

        # Send
        self.send_btn = QtWidgets.QPushButton('Send')
        self.send_btn.clicked.connect(self.handle_send)

        # Save/Load Config
        self.save = SaveConfig(
            ipv4_host=self.ipv4_host,
            port=self.port,
            varbinds=self.varbinds,
            varbinds_widget=self.agent_varbinds,
            notification_OID=self.notification_OID,
            parent=self
        )

        self.load = LoadConfig(
            ipv4_host=self.ipv4_host,
            port=self.port,
            varbinds=self.varbinds,
            varbinds_widget=self.agent_varbinds,
            notification_OID=self.notification_OID,
            parent=self
        )

        btn_group = QtWidgets.QWidget()
        btn_group.setLayout(btn_layout)
        send_btn = QtWidgets.QWidget()
        send_btn.setLayout(send_layout)

        # Adding Widgets to window
        main_layout.addWidget(window_title)
        main_layout.addWidget(self.target)
        main_layout.addWidget(self.notification)
        main_layout.addWidget(self.agent_varbinds)
        send_layout.addWidget(self.send_btn)
        btn_layout.addWidget(self.save)
        btn_layout.addWidget(self.load)
        main_layout.addWidget(send_btn)
        main_layout.addWidget(btn_group)

        self.setLayout(main_layout)

    def handle_send(self):
        """
        Send SNMP Trap message to configured SNMP Manager, async process.
        """
        import asyncio
        asyncio.run(self.send())

    def update_state(self, state: str, new_state):
        """
        Update application state by field

        Args:
            state (str): name of state to update
            new_state (any): value to update state
        """
        if state in self.valid:
            self.valid[state] = new_state

    def get_valid_state(self):
        """
        Return True if all fields are True (i.e. valid)
        """
        return all(self.valid.values())

    def update_ipv4_host(self, new_host: str):
        """
        Update and validate the user inputted IPv4 host field and state.

        Args:
            new_host (str): The user input for target IPv4.
        """
        if validate_host_ip(new_host):
            self.ipv4_host.setText(new_host)
            self.update_state('target_ip', True)
        else:
            self.update_state('target_ip', False)

    def update_port(self, new_port: str):
        """
        Update and validate the user inputted port field and state.

        Args:
            new_port (str): The user input for target port.
        """
        if validate_port(new_port):
            self.port.setText(new_port)
            self.update_state('target_port', True)

        else:
            self.update_state('target_port', False)

    def update_notification(self, new_notification_OID: str):
        """
        Update and validate the user inputted notification OID field and state.

        Args:
            new_notification_OID (str): The user input for notification OID.
        """
        if validate_OID(new_notification_OID):
            self.notification_OID.setText(new_notification_OID)
            self.update_state('notification_OID', True)

        else:
            self.update_state('notification_OID', False)

    async def send(self):
        """
        Send the SNMP Trap message to the user configured target.
        """
        if not self.get_valid_state():
            invalid_msg = QtWidgets.QMessageBox()
            invalid_msg.setIcon(QtWidgets.QMessageBox.Critical)
            invalid_msg.setWindowTitle("Error")
            invalid_msg.setText("Invalid Config")
            invalid_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            invalid_msg.exec()
            return

        for child in self.findChildren(QtWidgets.QLineEdit):
            child.clearFocus()
        for field, status in self.valid.items():
            if status is False:
                return

        agent = TransactionSNMPAgent(
                ipv4_host=(self.ipv4_host.text().strip()),
                port=(self.port.text().strip()),
                notification_OID=self.notification_OID.text().strip(),
                varbinds=self.varbinds)

        await agent._send_trap_async()
        print("sent trap")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = SNMPAgentClient()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
