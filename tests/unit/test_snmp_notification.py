import os
import pytest
from src.client.agents.generic import SNMPNotification
from src.client.components.varbinds import Varbind
from pysnmp.hlapi.asyncio import NotificationType

sample_varbinds = [
            Varbind(os.getenv('OID_SETTLEMENT_TYPE'), 'settlement'),
            Varbind(os.getenv('OID_SETTLEMENT_STATUS'), 'submitted'),
            Varbind(os.getenv('OID_SETTLEMENT_AMOUNT'), '1000'),
            Varbind(os.getenv('OID_SETTLEMENT_ENTITY'), 'merchant'),
            Varbind(os.getenv('OID_SETTLEMENT_MID'), 'abc123'),
            Varbind(os.getenv('OID_SETTLEMENT_DEPOSIT_DATE'), '123'),
            Varbind(os.getenv('OID_SETTLEMENT_OPEN_DATE'), '321'),
            Varbind(os.getenv('OID_SETTLEMENT_CLOSE_DATE'), '111'),
            Varbind(os.getenv('OID_SETTLEMENT_SUBMISSION_DATE'), '222')
]


@pytest.mark.asyncio
async def test_SNMPNotification_create():
    notification_type_OID = os.getenv('OID_SETTLEMENT_STATUS')
    notification = SNMPNotification(
        notification_type_OID=notification_type_OID,
        varbinds=sample_varbinds)
    notification.create()
    assert notification.get_varbinds() == sample_varbinds


@pytest.mark.asyncio
async def test_empty_notification_type_OID():
    notification = SNMPNotification(notification_type_OID=None,
                                    varbinds=sample_varbinds)
    with pytest.raises(AttributeError):
        notification.create()


@pytest.mark.asyncio
async def test_none_varbinds():
    notification_type_OID = os.getenv('OID_SETTLEMENT_STATUS')
    notification = SNMPNotification(
        notification_type_OID=notification_type_OID,
        varbinds=None)

    with pytest.raises(AttributeError):
        notification.create()


@pytest.mark.asyncio
async def test_notification_type():
    notification_type_OID = os.getenv('OID_SETTLEMENT_STATUS')
    notification = SNMPNotification(
        notification_type_OID=notification_type_OID,
        varbinds=sample_varbinds)

    assert isinstance(notification.create(), NotificationType)
