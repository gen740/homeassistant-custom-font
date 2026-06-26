"""Config flow for Home Assistant Custom Font."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_CODE_FONT_FAMILY,
    CONF_FONT_FAMILY,
    DEFAULT_CODE_FONT_FAMILY,
    DEFAULT_FONT_FAMILY,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

GOOGLE_FONTS_CSS2_URL = "https://fonts.googleapis.com/css2"


def _parse_fonts(value: str) -> list[str]:
    return [font.strip() for font in value.split(",") if font.strip()]


def _format_fonts(value: list[str]) -> str:
    return ", ".join(value)


async def _async_invalid_fonts(hass: HomeAssistant, fonts: list[str]) -> list[str]:
    """Return the font names that Google Fonts does not recognize.

    The css2 endpoint answers with HTTP 400 for an unknown family. If Google
    Fonts cannot be reached we cannot tell, so every font is treated as valid
    and the flow is never blocked on a transient network error.
    """
    session = async_get_clientsession(hass)
    invalid: list[str] = []
    for font in fonts:
        try:
            async with session.get(
                GOOGLE_FONTS_CSS2_URL,
                params={"family": font},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                if response.status == 400:
                    invalid.append(font)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return []
    return invalid


def _schema(default_font_family: list[str], default_code_font_family: list[str]) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(
                CONF_FONT_FAMILY,
                default=_format_fonts(default_font_family),
            ): str,
            vol.Required(
                CONF_CODE_FONT_FAMILY,
                default=_format_fonts(default_code_font_family),
            ): str,
        }
    )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Home Assistant Custom Font."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> OptionsFlow:
        """Create the options flow."""
        return OptionsFlow(config_entry)

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial setup step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        errors: dict[str, str] = {}
        if user_input is not None:
            font_family = _parse_fonts(user_input[CONF_FONT_FAMILY])
            code_font_family = _parse_fonts(user_input[CONF_CODE_FONT_FAMILY])
            invalid = await _async_invalid_fonts(
                self.hass, [*font_family, *code_font_family]
            )
            if invalid:
                _LOGGER.warning("Unknown Google Fonts names: %s", ", ".join(invalid))
                errors["base"] = "font_not_found"
            else:
                return self.async_create_entry(
                    title="Home Assistant Custom Font",
                    data={
                        CONF_FONT_FAMILY: font_family,
                        CONF_CODE_FONT_FAMILY: code_font_family,
                    },
                )

        schema = _schema(DEFAULT_FONT_FAMILY, DEFAULT_CODE_FONT_FAMILY)
        if user_input is not None:
            schema = self.add_suggested_values_to_schema(schema, user_input)
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )


class OptionsFlow(config_entries.OptionsFlow):
    """Handle custom font options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage the custom font options."""
        current_font_family = self._config_entry.options.get(
            CONF_FONT_FAMILY,
            self._config_entry.data.get(CONF_FONT_FAMILY, DEFAULT_FONT_FAMILY),
        )
        current_code_font_family = self._config_entry.options.get(
            CONF_CODE_FONT_FAMILY,
            self._config_entry.data.get(
                CONF_CODE_FONT_FAMILY, DEFAULT_CODE_FONT_FAMILY
            ),
        )

        errors: dict[str, str] = {}
        if user_input is not None:
            font_family = _parse_fonts(user_input[CONF_FONT_FAMILY])
            code_font_family = _parse_fonts(user_input[CONF_CODE_FONT_FAMILY])
            invalid = await _async_invalid_fonts(
                self.hass, [*font_family, *code_font_family]
            )
            if invalid:
                _LOGGER.warning("Unknown Google Fonts names: %s", ", ".join(invalid))
                errors["base"] = "font_not_found"
            else:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_FONT_FAMILY: font_family,
                        CONF_CODE_FONT_FAMILY: code_font_family,
                    },
                )

        schema = _schema(current_font_family, current_code_font_family)
        if user_input is not None:
            schema = self.add_suggested_values_to_schema(schema, user_input)
        return self.async_show_form(
            step_id="init", data_schema=schema, errors=errors
        )
