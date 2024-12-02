import os
import random
from agents.generic import SNMPAgent


class TransactionSNMPAgent(SNMPAgent):
    """
    A specialized SNMP agent for handling transaction-related SNMP
    notifications.

    Extends the SNMPAgent to provide additional functionality specific to
    transaction data, such as setting transaction status, type, amount, entity,
    and various timestamps for tracking purposes.

    Attributes:
        ipv4_host (str): IP address of the SNMP target, fetched from
            environment variables.
        port (int): Port number of the SNMP target, fetched from environment
            variables.
        notification_OID (str, optional): The OID for the SNMP notification
            type.
        varbinds (list(Varbind), optional): List of varbinds with Varbind
            containing OID(str) and message(str).
    """

    def __init__(self,
                 ipv4_host: str = os.getenv('IPv4_HOST_IP'),
                 port: str = os.getenv('PORT'),
                 notification_OID: str = None,
                 varbinds: list = None):
        """
        Initializes the TransactionSNMPAgent with host details and optional
        varbinds.

        Args:
            ipv4_host (str): IP address of the SNMP target, retrieved from
                environment variables.
            port (int): Port number of the SNMP target, retrieved from
                environment variables.
            notification_OID (str, optional): OID representing the type of
                SNMP notification.
            varbinds (dict, optional): Dictionary of varbinds with OID keys
                and values.
        """
        super().__init__(ipv4_host, port, notification_OID, varbinds)

    @staticmethod
    def generate_random_mid(length: int = 8):
        """
        Generates a random Merchant ID (MID) for transactions.

        Args:
            length (int): The desired length of the generated MID. Default is
                8 characters.

        Returns:
            str: A randomly generated MID consisting of uppercase letters and
                digits.
        """
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                      k=length))

    def set_status(self, OID, value):
        """
        Sets the transaction status in varbinds.

        Args:
            OID (str): The OID representing transaction status.
            value (str): The status value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)

    def set_type(self, OID, value):
        """
        Sets the transaction type in varbinds.

        Args:
            OID (str): The OID representing transaction type.
            value (str): The type value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)

    def set_amount(self, OID, value):
        """
        Sets the transaction amount in varbinds.

        Args:
            OID (str): The OID representing transaction amount.
            value (str): The amount value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)

    def set_entity(self, OID, value):
        """
        Sets the transaction entity in varbinds.

        Args:
            OID (str): The OID representing transaction entity.
            value (str): The entity value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)

    def set_mid(self, OID, value):
        """
        Sets the Merchant ID (MID) in varbinds.

        Args:
            OID (str): The OID representing the MID.
            value (str): The MID value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)

    def set_deposit_datetime(self, OID, value):
        """
        Sets the deposit date and time in varbinds.

        Args:
            OID (str): The OID representing the deposit date and time.
            value (str): The datetime value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)

    def set_open_datetime(self, OID, value):
        """
        Sets the open date and time in varbinds.

        Args:
            OID (str): The OID representing the open date and time.
            value (str): The datetime value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)

    def set_close_datetime(self, OID, value):
        """
        Sets the close date and time in varbinds.

        Args:
            OID (str): The OID representing the close date and time.
            value (str): The datetime value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)

    def set_submission_datetime(self, OID, value):
        """
        Sets the submission date and time in varbinds.

        Args:
            OID (str): The OID representing the submission date and time.
            value (str): The datetime value to associate with the OID.
        """
        SNMPAgent.edit_varbind(self, OID, value)
