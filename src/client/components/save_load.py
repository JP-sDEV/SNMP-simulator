from components.varbinds import SNMPAgentVarbinds
from PySide6 import QtWidgets
import json


class SaveLoadConfig(QtWidgets.QWidget):
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
        self.save_config_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_config_button)
        # Load config
        self.load_config_button = QtWidgets.QPushButton("Load Config")
        self.load_config_button.clicked.connect(self.load_config)
        self.layout.addWidget(self.load_config_button)

        # Set layout to this widget
        self.setLayout(self.layout)

    def save_config(self):
        state = {
            "ipv4_host": self.ipv4_host.text(),
            "port": self.port.text(),
            "notification_OID": self.notification_OID.text(),
            "varbinds": []
        }

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
                    good_msg.exec_()
            except Exception as e:
                # Show error popup
                error_msg = QtWidgets.QMessageBox()
                error_msg.setIcon(QtWidgets.QMessageBox.Critical)
                error_msg.setWindowTitle("Error Saving File")
                error_msg.setText("Failed to save configuration.")
                error_msg.setInformativeText(str(e))
                error_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                error_msg.exec_()

    def load_config(self):
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
