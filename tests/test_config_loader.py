"""Test per il modulo config_loader."""

import pytest
from config_loader import ConfigLoader, ConfigValidationError, Device


class TestConfigLoader:
    def test_missing_required_field(self, tmp_path):
        config = tmp_path / "devices.yaml"
        config.write_text("devices:\n  - name: test\n")
        loader = ConfigLoader(str(config))
        with pytest.raises(ConfigValidationError):
            loader.load()

    def test_valid_device(self, tmp_path):
        config = tmp_path / "devices.yaml"
        config.write_text(
            "devices:\n"
            "  - name: hub\n"
            "    hostname: hub-1\n"
            "    role: hub\n"
            "    advertise_routes:\n"
            "      - 10.0.0.0/24\n"
        )
        loader = ConfigLoader(str(config))
        devices = loader.load()
        assert len(devices) == 1
        assert devices[0].name == "hub"
        assert devices[0].hostname == "hub-1"
        assert devices[0].role == "hub"
