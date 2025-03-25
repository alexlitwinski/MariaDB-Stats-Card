"""MariaDB Stats integration."""
import logging
import os
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

_LOGGER = logging.getLogger(__name__)

DOMAIN = "mariadb_stats"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({})
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the MariaDB Stats component."""
    # Registrar o cartão personalizado
    hass.http.register_static_path(
        f"/mariadb_stats/mariadb-stats-card.js",
        os.path.join(os.path.dirname(__file__), "mariadb-stats-card.js"),
        True
    )
    
    # Adicionar o cartão para recursos disponíveis em Lovelace
    hass.components.frontend.async_register_built_in_panel(
        "lovelace",
        "mariadb_stats",
        "MariaDB Stats",
        "mdi:database"
    )
    
    # Carregar a plataforma de sensor
    hass.async_create_task(
        hass.helpers.discovery.async_load_platform("sensor", DOMAIN, {}, config)
    )
    
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MariaDB Stats from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_forward_entry_unload(entry, "sensor")
