import os
import random
from src.agents.generic import SNMPAgent
from dotenv import load_dotenv

# Determine which .env file to load
env_file = '.env.test' if os.getenv('PYTEST_CURRENT_TEST') else '.env'
load_dotenv(env_file)  # Load the appropriate environment file


class TransactionSNMPAgent(SNMPAgent):
    def __init__(self,
                 ipv4_host=os.getenv('IPv4_HOST_IP'),
                 port=os.getenv('PORT'),
                 notification_OID=None,
                 varbinds=None):
        super().__init__(ipv4_host, port, notification_OID, varbinds)

    @staticmethod
    def generate_random_mid(length=8):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                      k=length))

    def set_status(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)

    def set_type(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)

    def set_amount(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)

    def set_entity(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)

    def set_mid(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)

    def set_deposit_datetime(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)

    def set_open_datetime(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)

    def set_close_datetime(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)

    def set_submission_datetime(self, OID, value):
        if OID not in self.varbinds:
            # raise error
            pass
        else:
            SNMPAgent.edit_varbind(self, OID, value)
