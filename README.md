# Home Assistant Custom Font

Single-page GitHub Pages helper and HACS custom integration for applying Google Fonts to Home Assistant.

## GitHub Pages Helper

Open the Pages URL with `family` query parameters in fallback order:

```text
https://gen740.github.io/homeassistant-custom-font.css/?family=Roboto&code=Roboto+Mono
```

Comma separated values also work:

```text
https://gen740.github.io/homeassistant-custom-font.css/?family=Roboto,Noto+Sans+JP&code=Roboto+Mono
```

`Noto Sans JP` is shown as an example fallback, but the default body font is only `Roboto`.

Find Google Font names at <https://fonts.google.com/>.

The page includes editable preview text and a button to copy the settings for the HACS integration UI.

The page generates settings like:

```text
font-family: Roboto
code-font-family: Roboto Mono
```

The standalone hosted `font-loader.js` still reads its own query parameters, adds a Google Fonts `<link>`, and injects a font override `<style>` tag.

## HACS Install

1. Add this repository to HACS as a custom repository.
2. Select the `Integration` category.
3. Install `Home Assistant Custom Font`.
4. Restart Home Assistant.

## Configure In Home Assistant

1. Open **Settings > Devices & services > Add integration**.
2. Search for **Home Assistant Custom Font**.
3. Enter Google Font names in fallback order, separated by commas.

```text
font-family: Roboto, Noto Sans JP
code-font-family: Roboto Mono
```

Restart Home Assistant, then hard refresh the browser or clear the frontend cache.

The integration serves its bundled loader from:

```text
/homeassistant_custom_font/font-loader.js?family=Roboto&family=Noto+Sans+JP&code=Roboto+Mono
```

It registers that query URL with Home Assistant's frontend module loader automatically.
