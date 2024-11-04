from src.commands.trap.agent import SNMPAgent
from src.commands.trap.manager import SNMPManager


def test_func():
    agent = SNMPAgent()
    manager = SNMPManager()
    assert 1+1 == 2
