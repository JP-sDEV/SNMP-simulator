import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def send_trap():
    snmpEngine = SnmpEngine()

    # Define the target for the trap (IP and port)
    target = await UdpTransportTarget.create(("127.0.0.1", 2162))

    # Configure the trap message
    errorIndication, errorStatus, errorIndex, varBinds = await send_notification(
        snmpEngine,
        CommunityData("public", mpModel=0),
        target,
        ContextData(),
        "trap",
        NotificationType(ObjectIdentity("1.3.6.1.6.3.1.1.5.2"))
        .load_mibs("SNMPv2-MIB")
        .add_varbinds(
            ("1.3.6.1.6.3.1.1.4.3.0", "1.3.6.1.4.1.20408.4.1.1.2"),
            ("1.3.6.1.2.1.1.1.0", OctetString("Test system message")),
        ),
    )

    # Handle any errors that might occur
    if errorIndication:
        print(f"Error sending trap: {errorIndication}")
    else:
        print("Trap sent successfully!")

    # Close the SNMP engine
    snmpEngine.close_dispatcher()

# Run the trap sender
asyncio.run(send_trap())
