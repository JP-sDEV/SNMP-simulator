import os
import pytest
from src.client.agents.generic import SNMPAgent

sample_varbinds = {
            os.getenv('OID_SETTLEMENT_TYPE'): 'settlement',
            os.getenv('OID_SETTLEMENT_STATUS'): 'submitted',
            os.getenv('OID_SETTLEMENT_AMOUNT'): '1000',
            os.getenv('OID_SETTLEMENT_ENTITY'): 'merchant',
            os.getenv('OID_SETTLEMENT_MID'): 'abc123',
            os.getenv('OID_SETTLEMENT_DEPOSIT_DATE'): '123',
            os.getenv('OID_SETTLEMENT_OPEN_DATE'): '321',
            os.getenv('OID_SETTLEMENT_CLOSE_DATE'): '111',
            os.getenv('OID_SETTLEMENT_SUBMISSION_DATE'): '222',
            }


# init
@pytest.mark.asyncio
async def test_good_ipv4_port():
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    # Initialize the SNMP agent
    agent = SNMPAgent(notification_OID=notification_OID,
                      varbinds=sample_varbinds)

    assert isinstance(agent, SNMPAgent)


@pytest.mark.asyncio
async def test_empty_ipv4():
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')

    with pytest.raises(ValueError):
        # Initialize the SNMP agent
        SNMPAgent(ipv4_host=None,
                  notification_OID=notification_OID,
                  varbinds=sample_varbinds)


@pytest.mark.asyncio
async def test_empty_port():
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')

    with pytest.raises(TypeError):
        # Initialize the SNMP agent
        SNMPAgent(port=None,
                  notification_OID=notification_OID,
                  varbinds=sample_varbinds)


@pytest.mark.asyncio
async def test_set_notification_type():
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')

    # Initialize the SNMP agent
    agent = SNMPAgent(notification_OID=notification_OID,
                      varbinds=sample_varbinds)
    agent.set_notifcation_type('123')
    agent_notification_OID = agent.get_notification_OID()

    assert agent_notification_OID == '123'


@pytest.mark.asyncio
async def test_empty_notification_type():
    # Initialize the SNMP agent
    agent = SNMPAgent(notification_OID=None,
                      varbinds=sample_varbinds)

    # SNMPAgent created with no issue
    assert isinstance(agent, SNMPAgent)


@pytest.mark.asyncio
async def test_empty_varbinds():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')

    agent = SNMPAgent(notification_OID=notification_OID,
                      varbinds={})

    # SNMPAgent created with no issue
    assert isinstance(agent, SNMPAgent)


# add_varbind
@pytest.mark.asyncio
async def test_add_varbind():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    agent.add_varbind('1.2.3.4', 'test')
    varbinds = agent.get_varbinds()
    assert varbinds['1.2.3.4'] == 'test'


@pytest.mark.asyncio
async def test_none_varbind_OID():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.add_varbind(None, 'test')


@pytest.mark.asyncio
async def test_nonstr_varbind_OID():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.add_varbind(123, 'test')


@pytest.mark.asyncio
async def test_none_varbind_value():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.add_varbind('1.2.3.4', None)


@pytest.mark.asyncio
async def test_nonstr_varbind_value():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.add_varbind('1.2.3.4', 123)


@pytest.mark.asyncio
async def test_add_existing_varbind():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID,
                      varbinds={})

    agent.add_varbind('1.2.3.4', 'test')

    with pytest.raises(KeyError):
        # duplicate varbind
        agent.add_varbind('1.2.3.4', 'test')


# remove_varbind
@pytest.mark.asyncio
async def test_remove_varbind():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID, varbinds={})

    varbind_OID = '1.2.3.4'
    varbind_value = 'test'

    agent.add_varbind(varbind_OID, varbind_value)
    agent.remove_varbind(varbind_OID)
    varbinds = agent.get_varbinds()
    assert varbind_OID not in varbinds


@pytest.mark.asyncio
async def test_remove_none_varbind_OID():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.remove_varbind(None)


@pytest.mark.asyncio
async def test_remove_nonstr_varbind_OID():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.remove_varbind(123)


@pytest.mark.asyncio
async def test_nonexist_varbind_OID():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID, varbinds={})

    with pytest.raises(KeyError):
        agent.remove_varbind('1.2.3.4')


# edit_varbind
@pytest.mark.asyncio
async def test_edit_varbind():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID, varbinds={})

    agent.add_varbind('1.2.3.4', 'test')
    agent.edit_varbind('1.2.3.4', 'edited')
    varbinds = agent.get_varbinds()
    assert varbinds['1.2.3.4'] == 'edited'


@pytest.mark.asyncio
async def test_edit_none_varbind_OID():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.edit_varbind(None, 'test')


@pytest.mark.asyncio
async def test_edit_nonstr_varbind_OID():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.edit_varbind(123, 'test')


@pytest.mark.asyncio
async def test_edit_none_varbind_value():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.edit_varbind('1.2.3.4', None)


@pytest.mark.asyncio
async def test_edit_nonstr_varbind_value():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID)

    with pytest.raises(ValueError):
        agent.edit_varbind('1.2.3.4', 123)


@pytest.mark.asyncio
async def test_edit_non_existing_varbind():
    # Initialize the SNMP agent
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')
    agent = SNMPAgent(notification_OID=notification_OID,
                      varbinds={})

    with pytest.raises(KeyError):
        # varbind does not exist
        agent.edit_varbind('1.2.3.4', 'test')
