from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from dotenv import load_dotenv
import os

load_dotenv()


# noinspection PyUnusedLocal
def __callback(transportDispatcher, transportDomain, transportAddress,
               wholeMsg):
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.PROTOCOL_MODULES:
            pMod = api.PROTOCOL_MODULES[msgVer]

        else:
            print("Unsupported SNMP version %s" % msgVer)
            return

        reqMsg, wholeMsg = decoder.decode(
            wholeMsg,
            asn1Spec=pMod.Message(),
        )

        print(
            "Notification message from {}:{}: ".format(
                transportDomain, transportAddress
            )
        )

        reqPDU = pMod.apiMessage.get_pdu(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            varBinds = pMod.apiPDU.get_varbinds(reqPDU)

            print("Var-binds:")

            for oid, val in varBinds:
                print(f"{oid.prettyPrint()} = {val.prettyPrint()}")

    return wholeMsg


transportDispatcher = AsyncioDispatcher()

transportDispatcher.register_recv_callback(__callback)

# UDP/IPv4
transportDispatcher.register_transport(
    udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_server_mode(
        (os.getenv('IPv4_HOST_IP'), os.getenv('PORT')))
)

# UDP/IPv6
transportDispatcher.register_transport(
    udp6.DOMAIN_NAME, udp6.Udp6AsyncioTransport()
    .open_server_mode((os.getenv('IPv6_HOST_IP'), os.getenv('PORT')))
)

transportDispatcher.job_started(1)

try:
    print("This program needs to run as root/administrator to monitor\
          port 162.")
    print("Started. Press Ctrl-C to stop")
    # Dispatcher will never finish as job#1 never reaches zero
    transportDispatcher.run_dispatcher()

except KeyboardInterrupt:
    print("Shutting down...")

finally:
    transportDispatcher.close_dispatcher()
