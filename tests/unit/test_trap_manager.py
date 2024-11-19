import os
import pytest
import asyncio
from src.commands.trap.manager import SNMPManager
from src.client.agents.transaction import TransactionSNMPAgent


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


@pytest.mark.asyncio
async def test_snmp_manager():
    manager = SNMPManager()
    manager_task = asyncio.create_task(manager.run_async())

    try:
        await asyncio.sleep(1)
        assert manager._running is True  # Check that the manager is running
    finally:
        manager.stop()  # Ensure the manager stops
        await manager_task  # Wait for the task to finish
        assert manager._running is False


@pytest.mark.asyncio
async def test_trap_capture(capfd):
    # Initialize and start the SNMP manager
    notification_OID = os.getenv('OID_SETTLEMENT_STATUS')

    manager = SNMPManager()
    manager_task = asyncio.create_task(manager.run_async())

    # Initialize the SNMP agent
    agent = TransactionSNMPAgent(notification_OID=notification_OID,
                                 varbinds=sample_varbinds)

    try:
        # Allow some time for the manager to start
        await asyncio.sleep(1)
        assert manager._running is True  # Verify the manager is running

        # Send a trap from the agent
        await agent.send_trap()

        # Allow some time for the trap to be processed
        await asyncio.sleep(1)

        # Capture the printed output
        captured = capfd.readouterr()
        print_output = captured.out

        print(print_output)
        # # Perform assertions on the captured output
        assert "Notification message from" in print_output
        # Check for values in log
        assert "settlement" in print_output
        assert "submitted" in print_output

    finally:
        # Ensure the manager stops and the task completes
        manager.stop()
        await manager_task
        assert manager._running is False
