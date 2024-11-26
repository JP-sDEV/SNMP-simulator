from PySide6 import QtWidgets
from helpers.validation import validate_OID


class Varbind:
    def __init__(self, OID: str = "", message: str = ""):
        self.OID: str = OID
        self.message: str = message


class SNMPAgentVarbinds(QtWidgets.QWidget):
    def __init__(self, varbinds: list,
                 parent=None,
                 update_state_callback=None):
        super().__init__(parent)

        # List to hold Varbind instances
        self.varbinds = varbinds
        self.update_state_callback = update_state_callback

        # Set up the main layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # Scroll area to contain the fields
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Widget to hold the fields layout
        self.scroll_content = QtWidgets.QWidget()
        self.fields_layout = QtWidgets.QVBoxLayout(self.scroll_content)

        # Add the scroll content to the scroll area
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # Button to add new Varbinds (stays at the bottom)
        self.add_field_button = QtWidgets.QPushButton("Add New OID Message")
        self.add_field_button.clicked.connect(self.add_varbind)

        # Add the button below the scroll area
        self.main_layout.addWidget(self.add_field_button)

        # Set the main layout to this widget
        self.setLayout(self.main_layout)

    def add_varbind(self):
        # Create a new Varbind instance
        new_varbind = Varbind()
        self.varbinds.append(new_varbind)

        # Create a horizontal layout for the input fields and labels
        field_layout = QtWidgets.QHBoxLayout()

        # Label and QLineEdit for OID
        oid_label = QtWidgets.QLabel("OID:")
        oid_edit = QtWidgets.QLineEdit()
        oid_edit.editingFinished.connect(lambda oid_edit=oid_edit,
                                         varbind=new_varbind:
                                         self.update_OID(oid_edit, varbind))
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

        # Add the field layout at the top of the fields layout
        self.fields_layout.insertLayout(0, field_layout)

        # Update the scroll area's size
        self.scroll_content.adjustSize()

        # Scroll to the top of the scrollable area
        self.scroll_area.verticalScrollBar().setValue(0)

    def delete_varbind(self, field_layout, varbind):
        # Remove the varbind from the list
        self.varbinds.remove(varbind)

        # Remove the layout and all its widgets
        while field_layout.count():
            widget = field_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # Remove the layout from the fields layout
        self.fields_layout.removeItem(field_layout)

        # Update the scroll area's size
        self.scroll_content.adjustSize()

    def update_OID(self, oid_edit, varbind):
        """Validates the OID when editing is finished."""
        oid_text = oid_edit.text().strip()
        if validate_OID(oid_text):
            # OID is valid, update the Varbind
            varbind.OID = oid_text
            oid_edit.setStyleSheet("")  # Clear any error styles
            if self.update_state_callback:
                self.update_state_callback('varbinds', True)
        else:
            # OID is invalid, display an error
            oid_edit.setStyleSheet("border: 1px solid red;")
            if self.update_state_callback:
                self.update_state_callback('varbinds', False)

    def load_varbind(self, OID, message):
        """
        Load a varbind into the widget with the specified OID and message.

        :param OID: The OID string to load.
        :param message: The message string to load.
        """
        # Validate the OID before proceeding
        if not validate_OID(OID):
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid OID",
                f"The provided OID '{OID}' is invalid."
            )
            return

        # Create a new Varbind instance and add it to the varbinds list
        new_varbind = Varbind(OID=OID, message=message)
        self.varbinds.append(new_varbind)

        # Create a horizontal layout for the input fields and labels
        field_layout = QtWidgets.QHBoxLayout()

        # Label and QLineEdit for OID
        oid_label = QtWidgets.QLabel("OID:")
        oid_edit = QtWidgets.QLineEdit()
        oid_edit.setText(OID)  # Set the provided OID
        oid_edit.editingFinished.connect(lambda oid_edit=oid_edit,
                                         varbind=new_varbind:
                                         self.update_OID(oid_edit, varbind))
        field_layout.addWidget(oid_label)
        field_layout.addWidget(oid_edit)

        # Label and QLineEdit for message
        message_label = QtWidgets.QLabel("Message:")
        message_edit = QtWidgets.QLineEdit()
        message_edit.setText(message)  # Set the provided message
        message_edit.textChanged.connect(lambda text, varbind=new_varbind:
                                         setattr(varbind, "message", text))
        field_layout.addWidget(message_label)
        field_layout.addWidget(message_edit)

        # Delete button for removing this set of fields
        delete_button = QtWidgets.QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_varbind(field_layout,
                                                                  new_varbind))
        field_layout.addWidget(delete_button)

        # Add the field layout at the top of the fields layout
        self.fields_layout.insertLayout(0, field_layout)

        # Update the scroll area's size
        self.scroll_content.adjustSize()

        # Scroll to the top of the scrollable area
        self.scroll_area.verticalScrollBar().setValue(0)

        # Notify state update
        if self.update_state_callback:
            self.update_state_callback('varbinds', True)
