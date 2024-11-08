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
    """
    A Simple Network Management Protocol (SNMP) manager that listens for SNMP
    notifications on both IPv4 and IPv6, and processes incoming SNMP messages
    asynchronously using the asyncio library.

    Attributes:
        ipv4_host (str): The IPv4 address on which the SNMP manager listens.
        ipv6_host (str): The IPv6 address on which the SNMP manager listens.
        port (int): The port on which the SNMP manager listens for
            notifications.
        transportDispatcher (AsyncioDispatcher): Manages the transport
            mechanism for SNMP messages.
        _running (bool): A flag indicating whether the manager is actively
            running.
    """

    def __init__(self, ipv4_host=os.getenv('IPv4_HOST_IP'),
                 ipv6_host=os.getenv('IPv6_HOST_IP'),
                 port=os.getenv('PORT')):
        """
        Initializes the SNMPManager instance, setting up the dispatcher to
        handle incoming SNMP messages on both IPv4 and IPv6.

        Args:
            ipv4_host (str): The IPv4 address to bind to.
            ipv6_host (str): The IPv6 address to bind to.
            port (int): The port to bind to for receiving SNMP messages.
        """
        self.transportDispatcher = AsyncioDispatcher()
        self.transportDispatcher.register_recv_callback(self._callback)
        self.ipv4_host = ipv4_host
        self.ipv6_host = ipv6_host
        self.port = int(port)

        # Set up transport mechanisms for IPv4 and IPv6
        self.transportDispatcher.register_transport(
            udp.DOMAIN_NAME,
            udp.UdpAsyncioTransport().open_server_mode((self.ipv4_host,
                                                        self.port))
        )
        self.transportDispatcher.register_transport(
            udp6.DOMAIN_NAME,
            udp6.Udp6AsyncioTransport().open_server_mode((self.ipv6_host,
                                                          self.port))
        )

        self.transportDispatcher.job_started(1)
        self._running = True

        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """
        Handles termination signals to gracefully stop the SNMP manager.

        Args:
            signum (int): Signal number.
            frame (FrameType): Current stack frame.
        """
        print("Signal received, shutting down...")
        self.stop()

    async def run_async(self):
        """
        Asynchronously runs the SNMP manager's dispatcher in a loop, allowing
        it to process incoming SNMP messages until stopped.
        """
        print("Started SNMP Manager. Press Ctrl-C to stop.")
        while self._running:
            self.transportDispatcher.run_dispatcher()
            await asyncio.sleep(0.1)  # Yield control to the event loop

    def _callback(self, transportDispatcher, transportDomain, transportAddress,
                  wholeMsg):
        """
        Callback function to process received SNMP messages.

        Args:
            transportDispatcher (AsyncioDispatcher): The dispatcher handling
                the transport.
            transportDomain (tuple): The transport domain (protocol) used
                (e.g., UDP).
            transportAddress (tuple): Address tuple of the sender.
            wholeMsg (bytes): The raw message received.

        Returns:
            bytes: Remaining message content after processing.
        """
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
            print("Notification message from {}:{}: ".format(
                transportDomain, transportAddress))
            reqPDU = pMod.apiMessage.get_pdu(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                varBinds = pMod.apiPDU.get_varbinds(reqPDU)
                print("Var-binds:")
                for oid, val in varBinds:
                    print(f"{oid.prettyPrint()} = {val.prettyPrint()}")
        return wholeMsg

    async def run(self):
        """
        Starts the SNMP manager and runs it asynchronously until interrupted.

        Catches KeyboardInterrupt to handle graceful shutdown.
        """
        try:
            await self.run_async()
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            self.transportDispatcher.close_dispatcher()

    def stop(self):
        """
        Stops the SNMP manager, halting the dispatcher and setting `_running`
        to False.
        """
        self._running = False
        self.transportDispatcher.close_dispatcher()


async def start_manager():
    """
    Creates and starts an instance of SNMPManager asynchronously.
    """
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
