import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def get_snmp_sys_descr():
    """Asynchronously retrieves the system description from an SNMP agent."""
    
    # Create an SNMP engine instance
    snmp_engine = SnmpEngine()

    # Specify the community string (for SNMPv2c)
    community_data = CommunityData('public')

    # Define the SNMP agent's address and port
    target_address = ('demo.pysnmp.com', 161)
    transport_target = await UdpTransportTarget.create(target_address)

    # Define the OID for sysDescr in the SNMPv2-MIB
    oid_sys_descr = ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))

    # Send the SNMP GET request and await the response
    error_indication, error_status, error_index, var_binds = await get_cmd(
        snmp_engine,
        community_data,
        transport_target,
        ContextData(),
        oid_sys_descr
    )

    # Process the response
    if error_indication:
        print(f"Error: {error_indication}")
    elif error_status:
        print(f"Error: {error_status.prettyPrint()} at index {error_index and var_binds[int(error_index) - 1] or '?'}")
    else:
        for var_bind in var_binds:
            print(f"Received: {var_bind.prettyPrint()}")
            

# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(get_snmp_sys_descr())
