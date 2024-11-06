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
    def __init__(self, notification_type_OID, varbinds):
        self.notification_type_OID = notification_type_OID
        self.varbinds = varbinds

    def create(self):
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
    def __init__(self,
                 ipv4_host=os.getenv('IPv4_HOST_IP'),
                 port=os.getenv('PORT'),
                 notification_OID=None,
                 varbinds=None):

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

    # varbinds
    def set_notifcation_type(self, OID):
        self.notification_OID = OID

    def add_varbind(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            self.varbinds[OID] = value

    def remove_varbind(self, OID):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            del self.varbinds[OID]

    def edit_varbind(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            self.varbinds[OID] = value

    async def send_trap(self):
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
