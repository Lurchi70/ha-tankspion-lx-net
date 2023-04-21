"""Platform for sensor integration."""
from __future__ import annotations

import datetime as dt

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
)
from .coordinator import LXNetCoordinator

from .sensor_description import (
    SENSOR_TYPES_BASE,
    SENSOR_TYPES_TANK,
    LXNetSensorEntityDescription,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Add sensor entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        LXNetSensor(coordinator, description) for description in SENSOR_TYPES_BASE
    )
    async_add_entities(
        LXNetSensor(coordinator, description) for description in SENSOR_TYPES_TANK
    )


class LXNetSensor(CoordinatorEntity[LXNetCoordinator], SensorEntity):
    """Representation of a Sensor."""

    entity_description: LXNetSensorEntityDescription

    def __init__(
        self,
        coordinator: LXNetCoordinator,
        description: LXNetSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_name = f"{coordinator.name} {description.name}"
        self._attr_unique_id = f"{coordinator.unique_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.unique_id)},
            manufacturer=coordinator.manufacturer,
            model=coordinator.model,
            name=coordinator.name,
            configuration_url=coordinator.target_url,
        )

    @property
    def native_value(self) -> int | float | dt.datetime | None:
        """Return the native sensor value."""

        if self.entity_description.key in self.coordinator.data.data:
            the_data_point = self.coordinator.data.data[self.entity_description.key]

            if the_data_point is None:
                return None
            if the_data_point["Key"] == "NA":
                return None

            the_value = the_data_point["Value"]

            if self.entity_description.value:
                converted_val = self.entity_description.value(the_value)
                return converted_val

            return the_value

        return None
