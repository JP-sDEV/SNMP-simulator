import os
from pysnmp.hlapi.asyncio import SnmpEngine, CommunityData, \
    UdpTransportTarget, ContextData, NotificationType, send_notification, \
    ObjectType, ObjectIdentity
from pysnmp.proto import rfc1902 as univ
import asyncio


class SNMPNotification:
    """
    Represents an SNMP notificaiton for sending a trap message.

    This class allows the construction of an SNMP notification with dynamic
    varbinds (key-value pairs) representing different attributes of a
    transaction or status update. It is useful for sending SNMP trap messages
    with specific OIDs and associated values.

    Attributes:
        notification_type_OID (str): The OID for the notification type.
        varbinds (list [Varbind(str:str)]): list of varbinds, where
            each varbind contains a OID(str) and a message(str) to be sent
            in the notification.
    """
    def __init__(self, notification_type_OID: str, varbinds: list = []):
        """
        Initializes a SNMPNotification instance with the provided notification
        type OID and a dictionary of varbinds.

        Args:
            notification_type_OID (str): The object identifier for the type of
                notification.
            varbinds (list [Varbind(str:str)]): list of varbinds, where
                each varbind contains a OID(str) and a message(str) to be sent
                in the notification.

        Example:
            varbinds = [
                Varbind('1.3.6.1.4.1.9.9.599.1.3.1', 'status'),
                Varbind('1.3.6.1.4.1.9.9.599.1.3.2', 'success')
            ]
            notification = SNMPNotification('1.3.6.1.4.1.9.9.599.1.1',
                                            varbinds)

        """
        self.notification_type_OID = notification_type_OID
        self.varbinds = varbinds

    def create(self):
        """
        Creates an SNMP NotificationType object based on the provided OID and
        varbinds.

        Iterates over the varbinds list to add each Varbind to the
        NotificationType object as a varbind.

        Returns:
            NotificationType: A configured SNMP notification with all varbinds
            added.
        """
        if (self.notification_type_OID is None or
                self.notification_type_OID == ''):
            raise AttributeError('notification_type_OID is not specficied')

        if (not isinstance(self.varbinds, list)):
            raise AttributeError(f'varbinds is {type(self.varbinds)} type,\
                                 must be list of Varbinds')

        if (not isinstance(self.notification_type_OID, str)):
            raise AttributeError('notification_type_OID is not type str')

        # Create the NotificationType object
        notification = NotificationType(ObjectIdentity(
            self.notification_type_OID))

        if (self.varbinds):
            # Add varbinds to the notification from the list of varbinds
            for varbind in self.varbinds:
                notification.add_varbinds(
                    ObjectType(
                        ObjectIdentity(varbind.OID),
                        univ.OctetString(varbind.message)
                    )
                )

        return notification

    def get_varbinds(self):
        """
        Returns the agent's varbinds dictionary
        """
        return self.varbinds


class SNMPAgent:
    """
    A class to represent an SNMP agent that constructs and sends SNMP traps
    (notifications) with customizable varbinds and notification types.

    Attributes:
        snmp_engine (SnmpEngine): The SNMP engine for sending traps.
        community (CommunityData): SNMP community data using SNMPv2c.
        context (ContextData): SNMP context data.
        target (dict): Target IP and port for the SNMP trap.
        notification_OID (str): The Object Identifier (OID) for the
        notification type.
        varbinds (list(Varbind)): Dictionary of OIDs and their associated
            varbinds.
    """
    def __init__(self,
                 ipv4_host=os.getenv('IPv4_HOST_IP'),
                 port=os.getenv('PORT'),
                 notification_OID=None,
                 varbinds: dict = {}):
        """
        Initializes the SNMPAgent with host details, notification OID, and
        varbinds.

        Args:
            ipv4_host (str): IP address of the SNMP target.
            port (int): Port number of the SNMP target.
            notification_OID (str, optional): OID for the type of SNMP
                notification.
            varbinds (list(Varbind), optional): Dictionary of varbinds where
                each key is an OID (str) and value is the data associated with
                it.
        """

        self.snmp_engine = SnmpEngine()
        self.community = CommunityData('public', mpModel=1)  # SNMPv2c
        self.context = ContextData()
        # TRAP details
        self.target = {
            'ip': str(ipv4_host),
            # Raises 'TypeError' if port is not 'int' type
            'port': int(port)
        }
        self.notification_OID = notification_OID
        self.varbinds = varbinds

        if ipv4_host is None:
            raise ValueError('Argument "ipv4_host" cannot be empty')

    # Varbinds
    def set_notifcation_type(self, OID: str):
        """
        Sets the OID for the SNMP notification type.

        Args:
            OID (str): The Object Identifier (OID) for the notification type.
        """
        if (OID is None or OID == ''):
            raise ValueError('Argument "OID" cannot be empty')

        if (not isinstance(OID, str)):
            raise ValueError('Argument "OID" cannot be non-string')

        self.notification_OID = OID

    def add_varbind(self, OID: str, value: str):
        """
        Adds a new varbind to the agent's varbind dictionary.

        Args:
            OID (str): The Object Identifier (OID) for the varbind.
            value (str): The value to be associated with the OID.

        Raises:
            KeyError: If the OID already exists in the varbinds dictionary.
        """
        if (OID is None or OID == ''):
            raise ValueError('Argument "OID" cannot be empty')

        if (not isinstance(OID, str)):
            raise ValueError('Argument "OID" cannot be non-string')

        if (value is None):
            raise ValueError('Argument "value" cannot be empty')

        if (not isinstance(value, str)):
            raise ValueError('Argument "value" cannot be non-string')

        if OID in self.varbinds:
            raise KeyError("OID already exists in varbinds. Please\
                           ensure OID is not already in use.")

        self.varbinds[OID] = value

    def remove_varbind(self, OID: str):
        """
        Removes a varbind from the agent's varbind dictionary.

        Args:
            OID (str): The Object Identifier (OID) to remove from varbinds.

        Raises:
            KeyError: If the OID is not found in the varbinds dictionary.
        """
        if (OID is None or OID == ''):
            raise ValueError('Argument "OID" cannot be empty')

        if (not isinstance(OID, str)):
            raise ValueError('Argument "OID" cannot be non-string')

        if OID not in self.varbinds:
            raise KeyError(f"OID '{OID}' not found in varbinds. Please ensure\
                           it exists before removing.")
        else:
            del self.varbinds[OID]

    def edit_varbind(self, OID: str, value: str):
        """
        Edits the value of an existing varbind in the agent's varbind
        dictionary.

        Args:
            OID (str): The Object Identifier (OID) of the varbind to edit.
            value (str): The new value to associate with the OID.

        Raises:
            KeyError: If the OID is not found in the varbinds dictionary.
        """
        if (OID is None or OID == ''):
            raise ValueError('Argument "OID" cannot be empty')

        if (not isinstance(OID, str)):
            raise ValueError('Argument "OID" cannot be non-string')

        if (value is None):
            raise ValueError('Argument "value" cannot be empty')

        if (not isinstance(value, str)):
            raise ValueError('Argument "value" cannot be non-string')

        if OID not in self.varbinds:
            raise KeyError("OID not found in varbinds. Please ensure\
                           it exists before editing.")

        self.varbinds[OID] = value

    def get_varbinds(self):
        """
        Returns the agent's varbinds dictionary
        """
        return self.varbinds

    def get_notification_OID(self):
        """
        Returns the agent's notification OID
        """
        return self.notification_OID

    async def send_trap(self):
        """
        Constructs and sends an SNMP trap (notification) using the specified
        varbinds and notification type.

        Uses `SNMPNotification` to create the notification object, then sends
        it to the target IP and port.

        Raises:
            Exception: If the trap cannot be sent due to connection issues.
        """
        # Set up SNMP target
        if (self.target['ip'] is None or self.target['port'] is None):
            raise ValueError('Attributes in "target" cannot be empty')

        if (self.notification_OID is None):
            raise ValueError('Attribute "notification_OID" cannot be empty')

        if (self.varbinds is None):
            raise ValueError('Attribute "varbinds" cannot be empty')

        target = await UdpTransportTarget.create((self.target['ip'],
                                                  int(self.target['port'])))

        # Construct the notification
        notification = SNMPNotification(self.notification_OID, self.varbinds)
        notification = notification.create()

        # Send the trap
        await send_notification(
            self.snmp_engine,
            self.community,
            target,
            self.context,
            'trap',
            notification
        )
        if os.getenv('PYTEST_CURRENT_TEST'):
            print("Settlement trap sent successfully.")

    async def _send_trap_async(self):
        """
        Constructs and sends an SNMP trap (notification) using the specified
        varbinds and notification type.

        This method is asynchronous.
        """
        # Input validation
        if self.target['ip'] is None or self.target['port'] is None:
            raise ValueError('Attributes in "target" cannot be empty')

        if self.notification_OID is None:
            raise ValueError('Attribute "notification_OID" cannot be empty')

        # if not self.varbinds:
        #     raise ValueError('Attribute "varbinds" cannot be empty')

        # Set up SNMP target
        target = await UdpTransportTarget.create(
            (self.target['ip'], int(self.target['port']))
        )

        # Construct the notification
        notification = SNMPNotification(self.notification_OID, self.varbinds)
        notification = notification.create()

        # Send the trap
        await send_notification(
            self.snmp_engine,
            self.community,
            target,
            self.context,
            'trap',
            notification
        )


# Example usage
if __name__ == "__main__":
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID,
                      varbinds={'1.3.6.1.4.1.9.9.599.1.3.1': 'status_test'})
    asyncio.run(agent.send_trap())
