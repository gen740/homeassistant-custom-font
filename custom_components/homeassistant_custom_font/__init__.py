"""Set up Home Assistant custom font frontend module."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

from homeassistant.components.frontend import add_extra_js_url, remove_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_CODE_FONT_FAMILY,
    CONF_FONT_FAMILY,
    DEFAULT_CODE_FONT_FAMILY,
    DEFAULT_FONT_FAMILY,
    DOMAIN,
    STATIC_URL_PATH,
)


def _module_url(font_family: list[str], code_font_family: list[str]) -> str:
    family_params = [("family", font) for font in font_family] or [("family", "")]
    code_params = [("code", font) for font in code_font_family] or [("code", "")]
    query = urlencode(
        [
            *family_params,
            *code_params,
        ]
    )
    return f"{STATIC_URL_PATH}/font-loader.js?{query}"


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up static files for the custom font frontend module."""
    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                STATIC_URL_PATH,
                str(Path(__file__).parent),
                False,
            )
        ]
    )
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the custom font frontend module from a config entry."""
    font_family = entry.options.get(
        CONF_FONT_FAMILY, entry.data.get(CONF_FONT_FAMILY, DEFAULT_FONT_FAMILY)
    )
    code_font_family = entry.options.get(
        CONF_CODE_FONT_FAMILY,
        entry.data.get(CONF_CODE_FONT_FAMILY, DEFAULT_CODE_FONT_FAMILY),
    )
    module_url = _module_url(font_family, code_font_family)

    add_extra_js_url(hass, module_url)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = module_url
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a custom font config entry."""
    if module_url := hass.data.get(DOMAIN, {}).pop(entry.entry_id, None):
        remove_extra_js_url(hass, module_url)
    return True


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the module URL when options change."""
    await hass.config_entries.async_reload(entry.entry_id)
