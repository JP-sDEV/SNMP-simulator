import os
from pysnmp.hlapi.asyncio import SnmpEngine, CommunityData, \
    UdpTransportTarget, ContextData, NotificationType, send_notification, \
    ObjectType, ObjectIdentity
from pysnmp.proto import rfc1902 as univ
import asyncio
import random
import datetime
from dotenv import load_dotenv

# Determine which .env file to load
env_file = '.env.test' if os.getenv('PYTEST_CURRENT_TEST') else '.env'
load_dotenv(env_file)  # Load the appropriate environment file


class SNMPAgent:
    def __init__(self, amount=1000.00, ipv4_host=os.getenv('IPv4_HOST_IP'),
                 port=os.getenv('PORT')):
        self.snmp_engine = SnmpEngine()
        self.community = CommunityData('public', mpModel=1)  # SNMPv2c
        self.context = ContextData()
        # TRAP details
        self.target = {
            'ip': str(ipv4_host),
            'port': int(port)
        }
        self.varbinds = {}
        self.amount = amount

    @staticmethod
    def generate_random_mid(length=8):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                      k=length))

    def get_amount(self):
        return self.amount

    # varbinds
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

        # Generate MID and timestamps
        mid = self.generate_random_mid()
        deposit_date_time = datetime.datetime.now().isoformat()
        open_date_time = datetime.datetime.now().isoformat()
        close_date_time = (datetime.datetime.now() + datetime.timedelta
                           (hours=1)).isoformat()
        submission_date_time = datetime.datetime.now().isoformat()

        # Construct the notification
        notification = NotificationType(
            ObjectIdentity(os.getenv('OID_SETTLEMENT_STATUS'))
        ).add_varbinds(
            ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_TYPE')),
                       univ.OctetString('settlement')),
            ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_STATUS')),
                       univ.OctetString('submitted')),
            ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_AMOUNT')),
                       univ.OctetString("$" + str(self.amount))),
            ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_ENTITY')),
                       univ.OctetString('merchant')),
            ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_MID')),
                       univ.OctetString(mid)),
            ObjectType(ObjectIdentity(
                os.getenv('OID_SETTLEMENT_DEPOSIT_DATE')),
                univ.OctetString(deposit_date_time)),
            ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_OPEN_DATE')),
                       univ.OctetString(open_date_time)),
            ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_CLOSE_DATE')),
                       univ.OctetString(close_date_time)),
            ObjectType(
                ObjectIdentity(os.getenv('OID_SETTLEMENT_SUBMISSION_DATE')),
                univ.OctetString(submission_date_time))
        )

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
