# Home Assistant Custom Font CSS

Single-page GitHub Pages helper for generating Home Assistant font override CSS from Google Font names.

## Usage

Open the Pages URL with `family` query parameters in fallback order:

```text
https://YOUR_USER.github.io/homeassistant-custom-font.css/?family=Roboto&family=Noto+Sans+JP
```

Comma separated values also work:

```text
https://YOUR_USER.github.io/homeassistant-custom-font.css/?family=Roboto,Noto+Sans+JP
```

Find Google Font names at <https://fonts.google.com/>.

The page includes editable preview text and a button to download the generated CSS as a file.

The page generates CSS like:

```css
@import url("https://fonts.googleapis.com/css2?family=Roboto+Mono&family=Roboto&family=Noto+Sans+JP&display=swap");

html {
  --ha-font-family-body: "Roboto", "Noto Sans JP", sans-serif;
  --ha-font-family-heading: "Roboto", "Noto Sans JP", sans-serif;
  --ha-font-family-code: "Roboto Mono", "Roboto", "Noto Sans JP", monospace;

  --primary-font-family: "Roboto", "Noto Sans JP", sans-serif;
  --paper-font-common-base_-_font-family: "Roboto", "Noto Sans JP", sans-serif;
  --mdc-typography-font-family: "Roboto", "Noto Sans JP", sans-serif;

  font-family: "Roboto", "Noto Sans JP", sans-serif;
}

body {
  font-family: "Roboto", "Noto Sans JP", sans-serif;
}
```

GitHub Pages is static hosting, so it cannot return a dynamic `text/css` response based on query parameters. This page generates and displays the CSS client-side.

## Apply to Home Assistant Dashboard

1. Download the generated CSS file.
2. Place it under `/config/www/`.
3. Open Home Assistant and go to `Settings` -> `Dashboards`.
4. Open the dashboard menu and choose `Resources`.
5. Add the downloaded file URL as a `Stylesheet` resource, for example `/local/homeassistant-font-roboto-noto-sans-jp.css`.
6. Restart Home Assistant, then hard refresh the browser or clear the frontend cache.
