import sys
from PySide6 import QtWidgets
from agents.transaction import TransactionSNMPAgent
from components.target import SNMPAgentTarget
from components.varbinds import SNMPAgentVarbinds
from helpers.validation import validate_host_ip, validate_port


class SNMPAgentClient(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Application State
        # Target
        self.ipv4_host = QtWidgets.QLineEdit(self)
        self.port = QtWidgets.QLineEdit(self)
        self.notification_OID = QtWidgets.QLineEdit(self)

        # Varbinds
        self.varbinds = []
        # self.varbinds = SNMPAgentVarbinds(varbinds={}, parent=self)

        # Layout
        layout = QtWidgets.QVBoxLayout()

        # Add labels and fields for `ipv4_host` and `port`
        layout.addWidget(QtWidgets.QLabel("IPv4 Host:"))
        layout.addWidget(self.ipv4_host)

        layout.addWidget(QtWidgets.QLabel("Port:"))
        layout.addWidget(self.port)

        layout.addWidget(QtWidgets.QLabel("Notification OID:"))
        layout.addWidget(self.notification_OID)

        # Agent
        self.target = SNMPAgentTarget(parent=self,
                                      ipv4_host=self.ipv4_host,
                                      port=self.port)

        self.agent_varbinds = SNMPAgentVarbinds(varbinds=self.varbinds,
                                                parent=self)

        layout.addWidget(self.agent_varbinds)
        layout.addWidget(self.target)

        # Send
        self.send_btn = QtWidgets.QPushButton('Send')
        # self.send_btn.clicked.connect(self.send)
        self.send_btn.clicked.connect(self.handle_send)
        layout.addWidget(self.send_btn)

        # Save/Load
        self.save_btn = QtWidgets.QPushButton('Save')
        layout.addWidget(self.save_btn)

        self.load_btn = QtWidgets.QPushButton('Load')
        layout.addWidget(self.load_btn)

        self.setLayout(layout)

    def handle_send(self):
        import asyncio
        asyncio.run(self.send())

    def update_ipv4_host(self, new_host: str):
        new_host = new_host.strip()
        if validate_host_ip(new_host):  # Check if the host is valid
            self.ipv4_host.setText(new_host)
            print(f'new host: {self.ipv4_host.text()}')
        else:
            # Handle validation failure (e.g., show error message)
            print("Invalid host IP, failed to update.")

    def update_port(self, new_port):
        new_port = new_port.strip()
        if validate_port(new_port):
            self.port.setText(new_port)
            print(f'new PORT: {self.port.text()}')
        else:
            # Handle validation failure
            print("Invalid PORT, failed to update.")

    async def send(self):
        agent = TransactionSNMPAgent(
                ipv4_host=(self.ipv4_host.text()),
                port=(self.port.text()),
                notification_OID=self.notification_OID
                .text(),
                varbinds=self.varbinds)

        await agent._send_trap_async()

        print(f'Target IP: {self.ipv4_host.text()}')
        print(f'Target Port: {self.port.text()}')
        print(f'Target Notification OID: {self.notification_OID.text()}')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = SNMPAgentClient()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
