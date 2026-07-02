"""Test per il modulo tailscale_client."""

import pytest
from tailscale_client import TailscaleClient, TailscaleError
from config_loader import Device


class TestTailscaleClient:
    def test_generate_commands_basic(self):
        client = TailscaleClient(auth_key="test-key")
        device = Device(
            name="test-device",
            hostname="test-host",
            role="iot",
        )
        commands = client.generate_commands(device)
        assert len(commands) == 1
        assert "tailscale up" in commands[0]
        assert "--authkey test-key" in commands[0]
        assert "--hostname test-host" in commands[0]

    def test_generate_commands_with_routes(self):
        client = TailscaleClient(auth_key="test-key")
        device = Device(
            name="gateway",
            hostname="gw-1",
            role="gateway",
            advertise_routes=["10.0.0.0/24", "192.168.1.0/24"],
        )
        commands = client.generate_commands(device)
        assert "--advertise-routes 10.0.0.0/24,192.168.1.0/24" in commands[0]
