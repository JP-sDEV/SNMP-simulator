from PySide6 import QtWidgets


class SNMPAgentVarbinds(QtWidgets.QWidget):
    def __init__(self, varbinds, parent=None):
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

    def add_varbind(self):
        # Create a new Varbind instance
        new_varbind = Varbind()
        self.varbinds.append(new_varbind)

        # Create a horizontal layout for the input fields and labels
        field_layout = QtWidgets.QHBoxLayout()

        # Label and QLineEdit for OID
        oid_label = QtWidgets.QLabel("OID:")
        oid_edit = QtWidgets.QLineEdit()
        oid_edit.textChanged.connect(lambda text, varbind=new_varbind:
                                     setattr(varbind, "OID", text))
        field_layout.addWidget(oid_label)
        field_layout.addWidget(oid_edit)

        # Label and QLineEdit for message
        message_label = QtWidgets.QLabel("Message:")
        message_edit = QtWidgets.QLineEdit()
        message_edit.textChanged.connect(lambda text, varbind=new_varbind:
                                         setattr(varbind, "message", text))
        field_layout.addWidget(message_label)
        field_layout.addWidget(message_edit)

        # Delete button for removing this set of fields
        delete_button = QtWidgets.QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_varbind(field_layout,
                                                                  new_varbind))
        field_layout.addWidget(delete_button)

        # Add the field layout to the main layout
        self.layout.addLayout(field_layout)

    def delete_varbind(self, field_layout, varbind):
        # Remove the varbind from the list
        self.varbinds.remove(varbind)

        # Remove the layout and all its widgets
        while field_layout.count():
            widget = field_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # Remove the layout from the main layout
        self.layout.removeItem(field_layout)


# Application setup
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Create main window and add the widget
    main_window = QtWidgets.QMainWindow()
    snmp_varbinds_widget = SNMPAgentVarbinds()
    main_window.setCentralWidget(snmp_varbinds_widget)
    main_window.setWindowTitle("SNMP Agent Varbinds")
    main_window.resize(400, 300)
    main_window.show()

    app.exec()
