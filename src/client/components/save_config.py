from components.varbinds import SNMPAgentVarbinds
from PySide6 import QtWidgets
import json


class SaveConfig(QtWidgets.QWidget):
    """
    Custom QtPy widget to validate before saving the current SNMP trap
    configuration as a .json
    file.

    Attributes:
        ipv4_host (QtWidgets.QLineEdit): QLineEdit widget for IPv4 host.
        port (QtWidgets.QLineEdit): QLineEdit widget for port.
        varbinds_widget (SNMPAgentVarbinds): SNMPAgentVarbinds widget from
            parent widget.
        notification_OID (QtWidgets.QLineEdit):  QLineEdit widget for
            notification OID.
        varbinds (list(Varbind)): List of varbinds.
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

        # Save config
        self.save_config_button = QtWidgets.QPushButton("Save Config")
        # initial disable
        self.save_config_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_config_button)

        # Set layout to this widget
        self.setLayout(self.layout)

    def save_config(self):
        """
        Check if current config is valid before prompting user to save current
        config as a .json file.
        """
        state = {
            "ipv4_host": self.ipv4_host.text(),
            "port": self.port.text(),
            "notification_OID": self.notification_OID.text(),
            "varbinds": []
        }

        if not self.parent.get_valid_state():
            invalid_msg = QtWidgets.QMessageBox()
            invalid_msg.setIcon(QtWidgets.QMessageBox.Critical)
            invalid_msg.setWindowTitle("Error")
            invalid_msg.setText("Invalid Config")
            invalid_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            invalid_msg.exec()
            return

        # Gather state data
        for varbind in self.varbinds:
            state['varbinds'].append({varbind.OID: varbind.message})

        # Prompt user to choose file location
        options = QtWidgets.QFileDialog.Options()
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Configuration File",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options)

        if file_path:
            # Save to the chosen file
            try:
                with open(file_path, "w") as file:
                    json.dump(state, file, indent=4)
                    good_msg = QtWidgets.QMessageBox()
                    good_msg.setWindowTitle("Saved Config")
                    good_msg.setText("Saved configuration complete.")
                    good_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    good_msg.exec()
            except Exception as e:
                # Show error popup
                error_msg = QtWidgets.QMessageBox()
                error_msg.setIcon(QtWidgets.QMessageBox.Critical)
                error_msg.setWindowTitle("Error Saving File")
                error_msg.setText("Failed to save configuration.")
                error_msg.setInformativeText(str(e))
                error_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                error_msg.exec()
