from components.varbinds import SNMPAgentVarbinds
from PySide6 import QtWidgets
import json


class LoadConfig(QtWidgets.QWidget):
    """
    Custom QtPy widget to prompt user to load a SNMP target config .json file.
    Sets the config in the client in their respective fields.

    Attributes:
        ipv4_host (QtWidgets.QLineEdit): QLineEdit widget for IPv4 host.
        port (QtWidgets.QLineEdit): QLineEdit widget for port.
        varbinds_widget (SNMPAgentVarbinds): SNMPAgentVarbinds widget from
            parent widget.
        notification_OID (QtWidgets.QLineEdit):  QLineEdit widget for
            notification OID.
        varbinds (list(Varbinds)): List of varbinds.
        parent (QtWidget): Parent widget.
    """
    def __init__(self,
                 ipv4_host: QtWidgets.QLineEdit,
                 port: QtWidgets.QLineEdit,
                 varbinds_widget: SNMPAgentVarbinds,
                 varbinds: list,
                 notification_OID: QtWidgets.QLineEdit,
                 parent=None):
        super().__init__(parent)

        # List to hold Varbind instances and their layouts
        self.ipv4_host = ipv4_host
        self.port = port
        self.varbinds = varbinds
        self.notification_OID = notification_OID
        self.varbinds_widget = varbinds_widget
        self.parent = parent

        # Set up the main layout
        self.layout = QtWidgets.QVBoxLayout()

        # Load config
        self.load_config_button = QtWidgets.QPushButton("Load Config")
        self.load_config_button.clicked.connect(self.load_config)
        self.layout.addWidget(self.load_config_button)

        # Set layout to this widget
        self.setLayout(self.layout)

    def load_config(self):
        """
        Load config from .json file. Sets the config into respective fields.
        """
        # Prompt user to select a file to load
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Load Configuration File",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )

        if file_path:
            try:
                # Read from the selected JSON file
                with open(file_path, "r") as file:
                    state = json.load(file)

                # Restore general state
                self.parent.update_ipv4_host(state.get("ipv4_host", ""))
                self.parent.update_port(state.get("port", ""))
                self.parent.update_notification(state.get("notification_OID",
                                                          ""))

                # Clear existing varbinds
                while self.varbinds_widget.varbinds:
                    varbind_to_remove = self.varbinds_widget.varbinds[0]
                    self.varbinds_widget.delete_varbind(
                        self.varbinds_widget.layout.itemAt(0),
                        varbind_to_remove
                    )

                # Add varbinds from the configuration
                for varbind in state.get("varbinds", []):
                    for oid, message in varbind.items():
                        self.varbinds_widget.load_varbind(OID=oid,
                                                          message=message)

                # Show a success message
                QtWidgets.QMessageBox.information(
                    self,
                    "Configuration Loaded",
                    "Configuration has been successfully loaded."
                )

            except Exception as e:
                # Show error message
                QtWidgets.QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to load configuration:\n{str(e)}"
                )
