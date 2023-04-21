"""Sensordescriptions for LX Net Sensor Data."""
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfVolume, PERCENTAGE
from homeassistant.util.dt import as_local


@dataclass
class LXNetSensorEntityDescription(SensorEntityDescription):
    """Describes LX-Net sensor entity."""

    value: Callable[[float | int], float] | Callable[[datetime], datetime] | None = None


SENSOR_TYPES_BASE: tuple[LXNetSensorEntityDescription, ...] = (
    LXNetSensorEntityDescription(
        key="last_update",
        translation_key="last_update",
        name="last update",
        device_class=SensorDeviceClass.TIMESTAMP,
        value=as_local,
    ),
    LXNetSensorEntityDescription(
        key="operator",
        translation_key="operator",
        name="operator",
    ),
    LXNetSensorEntityDescription(
        key="location",
        translation_key="location",
        name="location",
    ),
)
SENSOR_TYPES_TANK: tuple[LXNetSensorEntityDescription, ...] = (
    LXNetSensorEntityDescription(
        key="tank_name",
        translation_key="tank_name",
        name="tank_name",
    ),
    LXNetSensorEntityDescription(
        key="tank_size",
        translation_key="tank_size",
        name="tank size",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.VOLUME_STORAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    LXNetSensorEntityDescription(
        key="tank_level",
        translation_key="tank_level",
        name="tank level",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    LXNetSensorEntityDescription(
        key="tank_level_percent",
        translation_key="tank_level_percent",
        name="tank level percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    LXNetSensorEntityDescription(
        key="tank_clearance",
        translation_key="tank_clearance",
        name="tank clearance",
        native_unit_of_measurement=UnitOfVolume.LITERS,
        device_class=SensorDeviceClass.VOLUME,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
