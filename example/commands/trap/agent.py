import os
from pysnmp.hlapi.asyncio import SnmpEngine, CommunityData, \
    UdpTransportTarget, ContextData, NotificationType, send_notification, \
    ObjectType, ObjectIdentity
from pysnmp.proto import rfc1902 as univ
import asyncio
import random
import datetime


# Function to generate a random Merchant ID (MID)
def generate_random_mid(length=8):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                  k=length))


async def send_trap():
    snmp_engine = SnmpEngine()

    # Set up SNMP target to send the trap to (localhost on port 162)
    target = await UdpTransportTarget.create((os.getenv('IPv4_HOST_IP'),
                                              os.getenv('PORT')))

    # SNMPv2c community and context data
    community = CommunityData('public', mpModel=1)  # v2c
    context = ContextData()

    # Generate random MID and current timestamps
    mid = generate_random_mid()
    deposit_date_time = datetime.datetime.now().isoformat()
    open_date_time = datetime.datetime.now().isoformat()
    close_date_time = (datetime.datetime.now() +
                       datetime.timedelta(hours=1)).isoformat()
    submission_date_time = datetime.datetime.now().isoformat()

    # Constructing the SNMP trap for settlement information
    notification = NotificationType(
        # OID for settlement status
        ObjectIdentity(os.getenv('OID_SETTLEMENT_STATUS'))
    ).add_varbinds(
        # Include the type, status, and amount as strings
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_TYPE')),
                   univ.OctetString('settlement')),  # Type
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_STATUS')),
                   univ.OctetString('submitted')),  # Status
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_AMOUNT')),
                   univ.OctetString('$1000.00')),  # Amount
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_ENTITY')),
                   univ.OctetString('merchant')),  # Entity
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_MID')),
                   univ.OctetString(mid)),  # Merchant ID
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_DEPOSIT_DATE')),
                   univ.OctetString(deposit_date_time)),  # Deposit Date Time
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_OPEN_DATE')),
                   univ.OctetString(open_date_time)),  # Open Date Time
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_CLOSE_DATE')),
                   univ.OctetString(close_date_time)),  # Close Date Time
        ObjectType(ObjectIdentity(os.getenv('OID_SETTLEMENT_SUBMISSION_DATE')),
                   # Submission Date Time
                   univ.OctetString(submission_date_time))
    )

    # Send the trap
    await send_notification(
        snmp_engine,
        community,
        target,
        context,
        'trap',
        notification
    )
    print("Settlement trap sent successfully.")

# Run the async trap-sending function
asyncio.run(send_trap())
