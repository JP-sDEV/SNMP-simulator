from pysnmp.hlapi.asyncio import SnmpEngine, CommunityData, \
    UdpTransportTarget, ContextData, NotificationType, send_notification, \
    ObjectType, ObjectIdentity
from pyasn1.type import univ
import asyncio


async def send_trap():
    snmp_engine = SnmpEngine()

    # Set up SNMP target to send the trap to (localhost on port 2162)
    target = await UdpTransportTarget.create(('localhost', 2162))

    # SNMPv2c community and context data
    community = CommunityData('public', mpModel=1)  # v2c
    context = ContextData()

    # Constructing the SNMP trap
    notification = NotificationType(
        ObjectIdentity('1.3.6.1.6.3.1.1.5.1')  # OID for "coldStart" event
    ).add_varbinds(
        # Additional var-binds (OID-value pairs)
        # Use OctetString for string values
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'),
                   univ.OctetString('Device is up')),
        # Use Integer for integer values
        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'), univ.Integer(12345))
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
    print("Trap sent successfully.")

# Run the async trap-sending function
asyncio.run(send_trap())
