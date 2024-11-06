from pysnmp.carrier.asyncio.dispatch import AsyncioDispatcher
from pysnmp.carrier.asyncio.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
from dotenv import load_dotenv
import asyncio
import os
import signal

# Determine which .env file to load
env_file = '.env.test' if os.getenv('PYTEST_CURRENT_TEST') else '.env'
load_dotenv(env_file)  # Load the appropriate environment file


class SNMPManager:
    def __init__(self, ipv4_host=os.getenv('IPv4_HOST_IP'),
                 ipv6_host=os.getenv('IPv6_HOST_IP'),
                 port=os.getenv('PORT')):

        self.transportDispatcher = AsyncioDispatcher()
        self.transportDispatcher.register_recv_callback(self._callback)
        self.ipv4_host = ipv4_host
        self.ipv6_host = ipv6_host
        self.port = port

        # UDP/IPv4 setup
        self.transportDispatcher.register_transport(
            udp.DOMAIN_NAME, udp.UdpAsyncioTransport().open_server_mode(
                (self.ipv4_host, self.port)
            )
        )

        # UDP/IPv6 setup
        self.transportDispatcher.register_transport(
            udp6.DOMAIN_NAME, udp6.Udp6AsyncioTransport().open_server_mode(
               (self.ipv6_host, self.port)
            )
        )

        self.transportDispatcher.job_started(1)
        self._running = True

        # Register signal handlers
        # Handle Ctrl-C
        signal.signal(signal.SIGINT, self.signal_handler)
        # Handle termination
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        print("Signal received, shutting down...")
        self.stop()

    async def run_async(self):
        print("Started SNMP Manager. Press Ctrl-C to stop.")
        while self._running:
            self.transportDispatcher.run_dispatcher()
            await asyncio.sleep(0.1)  # Yield control to the event loop

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

    async def run(self):
        try:
            await self.run_async()
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            self.transportDispatcher.close_dispatcher()

    def stop(self):
        self._running = False
        self.transportDispatcher.close_dispatcher()


async def start_manager():
    manager = SNMPManager()
    await manager.run()

if __name__ == '__main__':
    try:
        asyncio.run(start_manager())
    except RuntimeError as e:
        if "while another loop is running" in str(e):
            # Fallback if already in an environment with a running event loop
            print("An event loop is already running; switching to await.")
            asyncio.get_event_loop().run_until_complete(start_manager())
