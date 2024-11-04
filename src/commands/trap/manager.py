from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()


class SNMPManager:
    def __init__(self):
        self.transportDispatcher = AsyncioDispatcher()
        self.transportDispatcher.register_recv_callback(self._callback)

        # UDP/IPv6 setup
        self.transportDispatcher.register_transport(
            udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_server_mode(
                (os.getenv('IPv4_HOST_IP'), os.getenv('PORT'))
            )
        )

        # UDP/IPv6 setup
        self.transportDispatcher.register_transport(
            udp6.DOMAIN_NAME, udp6.Udp6AsyncioTransport().open_server_mode(
                (os.getenv('IPv6_HOST_IP'), int(os.getenv('PORT')))
            )
        )

        self.transportDispatcher.job_started(1)

    async def run_async(self):
        print("Started SNMP Manager. Press Ctrl-C to stop.")
        # await asyncio.get_event_loop().run_in_executor(
        #     None, self.transportDispatcher.run_dispatcher)
        self.transportDispatcher.run_dispatcher()

    def _callback(self, transportDispatcher, transportDomain, transportAddress,
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
            print("Notification message from {}:{}: ".format(transportDomain,
                                                             transportAddress))
            reqPDU = pMod.apiMessage.get_pdu(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                varBinds = pMod.apiPDU.get_varbinds(reqPDU)
                print("Var-binds:")
                for oid, val in varBinds:
                    print(f"{oid.prettyPrint()} = {val.prettyPrint()}")
        return wholeMsg

    def run(self):
        try:
            asyncio.run(self.run_async())
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            self.transportDispatcher.close_dispatcher()


if __name__ == '__main__':
    manager = SNMPManager()
    manager.run()
