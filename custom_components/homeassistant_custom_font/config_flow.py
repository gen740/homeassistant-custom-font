"""Config flow for Home Assistant Custom Font."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries

from .const import (
    CONF_CODE_FONT_FAMILY,
    CONF_FONT_FAMILY,
    DEFAULT_CODE_FONT_FAMILY,
    DEFAULT_FONT_FAMILY,
    DOMAIN,
)


def _parse_fonts(value: str) -> list[str]:
    return [font.strip() for font in value.split(",") if font.strip()]


def _format_fonts(value: list[str]) -> str:
    return ", ".join(value)


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

    async def async_step_user(self, user_input: dict[str, Any] = None):
        """Handle the initial setup step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(
                title="Home Assistant Custom Font",
                data={
                    CONF_FONT_FAMILY: _parse_fonts(user_input[CONF_FONT_FAMILY]),
                    CONF_CODE_FONT_FAMILY: _parse_fonts(
                        user_input[CONF_CODE_FONT_FAMILY]
                    ),
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=_schema(DEFAULT_FONT_FAMILY, DEFAULT_CODE_FONT_FAMILY),
        )


class OptionsFlow(config_entries.OptionsFlow):
    """Handle custom font options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize the options flow."""
        self._config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] = None):
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

        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    CONF_FONT_FAMILY: _parse_fonts(user_input[CONF_FONT_FAMILY]),
                    CONF_CODE_FONT_FAMILY: _parse_fonts(
                        user_input[CONF_CODE_FONT_FAMILY]
                    ),
                },
            )

        return self.async_show_form(
            step_id="init",
            data_schema=_schema(current_font_family, current_code_font_family),
        )
