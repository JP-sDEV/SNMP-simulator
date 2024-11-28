from PySide6 import QtWidgets
from helpers.validation import validate_OID


class SNMPNotification(QtWidgets.QWidget):
    """
    Represents a SNMP Notification OID. Attached to the SNMP trap message.

    Attributes:
        parent: parent Widget
        notification_OID (QtWidgets.QLineEdit): QLineEdit widget for
            notification OID.
        update_state_callback (function): method to update state from parent
            widget.
    """
    def __init__(self,
                 parent,
                 notification_OID: QtWidgets.QLineEdit,
                 update_state_callback):
        super().__init__(parent)

        self.parent = parent
        self.notification_OID = notification_OID
        self.update_state_callback = update_state_callback

        self.layout = QtWidgets.QHBoxLayout()

        self.notification_OID.editingFinished.connect(
           lambda: self.update_notification_OID(self.notification_OID)
        )

        self.layout.addWidget(QtWidgets.QLabel("Notification OID:"))
        self.layout.addWidget(self.notification_OID)

        self.setLayout(self.layout)

    def update_notification_OID(self, oid_edit):
        """
        Wrapper function to validate the notification OID field and update
        validation state in parent.

        Args:
            oid_edit (QtWidgets.QLineEdit): New value in the OID field.
        """
        oid_text = oid_edit.text().strip()

        if validate_OID(oid_text):
            oid_edit.setStyleSheet("")
            self.parent.update_notification(oid_text)
            self.update_state_callback('notification_OID', True)

        else:
            oid_edit.setStyleSheet("border: 1px solid red;")
            self.update_state_callback('notification_OID', False)
