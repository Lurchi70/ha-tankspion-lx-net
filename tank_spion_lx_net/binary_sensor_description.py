"""Binary sensor descriptions for binary sensor data."""
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)


@dataclass
class LXNetBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes LX-Net binary sensor entity."""


BINARY_SENSOR_LX_NET = LXNetBinarySensorEntityDescription(
    key="tank_alarm",
    translation_key="tank_alarm",
    name="tank alarm",
    device_class=BinarySensorDeviceClass.PROBLEM,
)
