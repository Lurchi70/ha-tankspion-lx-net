"""Tankspion LX-Net integration."""
from datetime import timedelta
import logging

from .tankspion_lx_net import LXNetReader

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import update_coordinator

from .const import (
    CONF_OPTION_NUMBER,
    CONF_UPDATE_TIMESPAN,
    DEFAULT_MANUFACTURER,
    DEFAULT_MODEL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class LXNetCoordinator(update_coordinator.DataUpdateCoordinator):
    """Get and update the latest data."""

    target_url: str
    username: str
    password: str
    number_of_sensors: int
    update_: int

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the data object."""
        super().__init__(
            hass,
            _LOGGER,
            name="LXNetCoordinator",
            update_interval=timedelta(seconds=600),
        )

        entry.async_on_unload(entry.add_update_listener(update_listener))
        host_entry = entry.data[CONF_HOST]
        self.username = entry.data[CONF_USERNAME]
        self.password = entry.data[CONF_PASSWORD]

        self.number_of_sensors = entry.data[CONF_OPTION_NUMBER]

        update_ = entry.data[CONF_UPDATE_TIMESPAN]
        if 10 >= update_ <= 3600:
            self.update_interval = timedelta(seconds=update_)

        self.unique_id = entry.entry_id
        self.name = entry.title
        self.target_url = f"""http://{host_entry}/xml"""
        self.manufacturer = DEFAULT_MANUFACTURER
        self.model = DEFAULT_MODEL

    async def _async_update_data(self):
        """Update the data from the LX-Net device."""
        try:
            data = await self.hass.async_add_executor_job(
                LXNetReader, self.target_url, self.username, self.password
            )
        except BaseException as err:
            raise update_coordinator.UpdateFailed(err)

        return data


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    update_ = entry.data[CONF_UPDATE_TIMESPAN]
    if 10 >= update_ <= 3600:
        coordinator.update_interval = timedelta(seconds=update_)
