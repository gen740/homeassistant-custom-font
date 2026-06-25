# Home Assistant Custom Font CSS

Single-page GitHub Pages helper for generating a Home Assistant font override JavaScript module from Google Font names.

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

The page includes editable preview text and a button to download the generated JavaScript as a file.

The page generates JavaScript like:

```js
(() => {
  const id = "home-assistant-custom-font";
  document.getElementById(id)?.remove();
  const style = document.createElement("style");
  style.id = id;
  style.dataset.homeAssistantCustomFont = "true";
  style.textContent = "@import url(\"https://fonts.googleapis.com/css2?family=Roboto+Mono&family=Roboto&family=Noto+Sans+JP&display=swap\");\n\nhtml { ... }";
  document.head.append(style);
})();
```

GitHub Pages is static hosting, so it cannot return a dynamic response based on query parameters. This page generates and displays the JavaScript client-side.

## Apply to Home Assistant

1. Download the generated JavaScript file.
2. Place it under `/config/www/`.
3. Add the downloaded file URL to `configuration.yaml`:

```yaml
frontend:
  extra_module_url:
    - /local/homeassistant-font-roboto-noto-sans-jp.js
```

4. Restart Home Assistant, then hard refresh the browser or clear the frontend cache.
