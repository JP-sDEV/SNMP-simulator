import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp import hlapi

# OID for sysDescr (System Description)
OID_SYS_DESCR = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)

# Agent's system description
system_description = 'My SNMP Agent'

async def send_trap(snmp_engine):
    """Send a trap notification."""
    errorIndication, errorStatus, errorIndex, varBinds = await send_notification(
        snmp_engine,
        CommunityData('public', mpModel=0),
        await UdpTransportTarget.create(('localhost', 162)),
        ContextData(),
        'trap',
        NotificationType(OID_SYS_DESCR)
        .load_mibs('SNMPv2-MIB')
        .add_varbinds(
            (OID_SYS_DESCR, OctetString(system_description)),
        ),
    )

    if errorIndication:
        print(f"Trap error: {errorIndication}")

async def handle_snmp_request(snmp_engine):
    """Handle incoming SNMP requests."""
    # Define a MIB variable for sysDescr
    snmp_var_binds = {
        OID_SYS_DESCR: OctetString(system_description)
    }

    # Create an SNMP transport
    await UdpTransport().listen(161)

    # Loop to listen for SNMP requests
    while True:
        try:
            # Wait for a request
            request = await snmp_engine.transportDispatcher.read(1)
            if request:
                print("Received SNMP request")
                for oid, value in snmp_var_binds.items():
                    await hlapi.send_response(request, var_binds=[(oid, value)])

        except Exception as e:
            print(f"Error handling request: {e}")

async def main():
    # Create an SNMP engine instance
    snmp_engine = SnmpEngine()

    # Start the SNMP request handler
    asyncio.create_task(handle_snmp_request(snmp_engine))

    # Periodically send traps
    while True:
        await send_trap(snmp_engine)
        await asyncio.sleep(5)  # Send a trap every 5 seconds

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
