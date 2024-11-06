import os
from pysnmp.hlapi.asyncio import SnmpEngine, CommunityData, \
    UdpTransportTarget, ContextData, NotificationType, send_notification, \
    ObjectType, ObjectIdentity
from pysnmp.proto import rfc1902 as univ
import asyncio
from dotenv import load_dotenv

# Determine which .env file to load
env_file = '.env.test' if os.getenv('PYTEST_CURRENT_TEST') else '.env'
load_dotenv(env_file)  # Load the appropriate environment file


class SNMPNotification:
    """
    Represents an SNMP notificaiton for sending a trap message.

    This class allows the construction of an SNMP notification with dynamic
    varbinds (key-value pairs) representing different attributes of a
    transaction or status update. It is useful for sending SNMP trap messages
    with specific OIDs and associated values.

    Attributes:
        notification_type_OID (str): The OID for the notification type.
        varbinds (dict [str:str]): Key-value pairs where each OID (str) is
            associated with a value (str) to be sent in the notification
    """
    def __init__(self, notification_type_OID, varbinds):
        """
        Initializes a SNMPNotification instance with the provided notification
        type OID and a dictionary of varbinds.

        Args:
            notification_type_OID (str): The object identifier for the type of
            notification.
            varbinds (dict): Key-value pairs where each key is an OID (str)
                and each value is the data (str) to be sent in the
                notification.

        Example:
            varbinds = {
                '1.3.6.1.4.1.9.9.599.1.3.1': 'status',
                '1.3.6.1.4.1.9.9.599.1.3.2': 'success'
            }
            notification = SNMPNotification('1.3.6.1.4.1.9.9.599.1.1',
                                            varbinds)

        """
        self.notification_type_OID = notification_type_OID
        self.varbinds = varbinds

    def create(self):
        """
        Creates an SNMP NotificationType object based on the provided OID and
        varbinds.

        Iterates over the varbinds dictionary to add each OID-value pair to the
        NotificationType object as a varbind.

        Returns:
            NotificationType: A configured SNMP notification with all varbinds
            added.
        """
        # Create the NotificationType object
        notification = NotificationType(ObjectIdentity(
            self.notification_type_OID))

        # Add varbinds to the notification from the dictionary
        for oid, value in self.varbinds.items():
            notification.add_varbinds(
                ObjectType(
                    ObjectIdentity(oid),
                    univ.OctetString(value)
                )
            )
        return notification


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
        varbinds (dict): Dictionary of OIDs and their associated values.
    """
    def __init__(self,
                 ipv4_host=os.getenv('IPv4_HOST_IP'),
                 port=os.getenv('PORT'),
                 notification_OID=None,
                 varbinds=None):
        """
        Initializes the SNMPAgent with host details, notification OID, and
        varbinds.

        Args:
            ipv4_host (str): IP address of the SNMP target.
            port (int): Port number of the SNMP target.
            notification_OID (str, optional): OID for the type of SNMP
                notification.
            varbinds (dict, optional): Dictionary of varbinds where each key
                is an OID (str) and value is the data associated with it.
        """

        self.snmp_engine = SnmpEngine()
        self.community = CommunityData('public', mpModel=1)  # SNMPv2c
        self.context = ContextData()
        # TRAP details
        self.target = {
            'ip': str(ipv4_host),
            'port': int(port)
        }
        self.notification_OID = notification_OID
        self.varbinds = varbinds

    # Varbinds
    def set_notifcation_type(self, OID):
        """
        Sets the OID for the SNMP notification type.

        Args:
            OID (str): The Object Identifier (OID) for the notification type.
        """
        self.notification_OID = OID

    def add_varbind(self, OID, value):
        """
        Adds a new varbind to the agent's varbind dictionary.

        Args:
            OID (str): The Object Identifier (OID) for the varbind.
            value (str): The value to be associated with the OID.

        Raises:
            KeyError: If the OID already exists in the varbinds dictionary.
        """
        if OID in self.varbinds:
            raise KeyError(f"OID '{OID}' already exists in varbinds. Please\
                           ensure OID is not already in use.")
        else:
            self.varbinds[OID] = value

    def remove_varbind(self, OID):
        """
        Removes a varbind from the agent's varbind dictionary.

        Args:
            OID (str): The Object Identifier (OID) to remove from varbinds.

        Raises:
            KeyError: If the OID is not found in the varbinds dictionary.
        """
        if OID not in self.varbinds:
            raise KeyError(f"OID '{OID}' not found in varbinds. Please ensure\
                           it exists before removing.")
        else:
            del self.varbinds[OID]

    def edit_varbind(self, OID, value):
        """
        Edits the value of an existing varbind in the agent's varbind
        dictionary.

        Args:
            OID (str): The Object Identifier (OID) of the varbind to edit.
            value (str): The new value to associate with the OID.

        Raises:
            KeyError: If the OID is not found in the varbinds dictionary.
        """
        if OID not in self.varbinds:
            raise KeyError(f"OID '{OID}' not found in varbinds. Please ensure\
                           it exists before editing.")
        else:
            self.varbinds[OID] = value

    def get_varbinds(self):
        """
        Returns the agent's varbinds dictionary
        """
        return self.varbinds

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
        print("Settlement trap sent successfully.")


# Example usage
if __name__ == "__main__":
    agent = SNMPAgent()
    asyncio.run(agent.send_trap())
