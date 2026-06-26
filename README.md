# Home Assistant Custom Font

Single-page GitHub Pages helper and HACS custom integration for applying Google Fonts to Home Assistant.

## GitHub Pages Helper

Open the Pages URL with `family` query parameters in fallback order:

```text
https://gen740.github.io/homeassistant-custom-font/?family=Roboto&code=Roboto+Mono
```

Comma separated values also work:

```text
https://gen740.github.io/homeassistant-custom-font/?family=Roboto,Noto+Sans+JP&code=Roboto+Mono
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

## Setup

There are two ways to use this project. Pick one — you do not need both.

### Option A: HACS integration (UI)

Recommended if you prefer a UI and want the loader served from your own Home
Assistant instance instead of GitHub Pages.

1. Add this repository to HACS as a custom repository and select the
   `Integration` category.
2. Install `Home Assistant Custom Font`, then restart Home Assistant.
3. Open **Settings > Devices & services > Add integration** and search for
   **Home Assistant Custom Font**.
4. Enter Google Font names in fallback order, separated by commas:

   ```text
   font-family: Roboto, Noto Sans JP
   code-font-family: Roboto Mono
   ```

5. Hard refresh the browser or clear the frontend cache.

The integration serves its bundled loader from a URL like
`/homeassistant_custom_font/font-loader.js?family=Roboto&family=Noto+Sans+JP&code=Roboto+Mono`
and registers it with Home Assistant's frontend module loader automatically.
Fonts can be changed later from the integration's **Configure** dialog.

### Option B: `configuration.yaml` (manual)

No HACS or custom component required. This loads the hosted `font-loader.js`
directly via the frontend's extra module loader.

Add the following to `configuration.yaml`, then restart Home Assistant:

```yaml
frontend:
  extra_module_url:
    - https://gen740.github.io/homeassistant-custom-font/font-loader.js?family=Roboto&family=Noto+Sans+JP&code=Roboto+Mono
```

Pass each font as its own `family=` parameter (or comma-separated in a single
`family=`) in fallback order, and use `code=` for the monospace stack. After
restarting, hard refresh the browser or clear the frontend cache.
