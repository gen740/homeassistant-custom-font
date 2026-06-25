const DEFAULT_FONTS = ["Roboto", "Noto Sans JP"];
const CODE_FONTS = ["Roboto Mono"];

function fontsFromModuleUrl() {
  const params = new URL(import.meta.url).searchParams;
  const values = params.getAll("family").flatMap((value) => value.split(","));
  const fonts = values.map((value) => value.trim()).filter(Boolean);

  return fonts.length > 0 ? fonts : DEFAULT_FONTS;
}

function quoteFont(font) {
  return `"${font.replaceAll("\\", "\\\\").replaceAll('"', '\\"')}"`;
}

function googleFamily(font) {
  return encodeURIComponent(font.trim()).replaceAll("%20", "+");
}

function fontStack(fonts, generic) {
  return [...fonts.map(quoteFont), generic].join(", ");
}

function googleFontsUrl(fonts) {
  const families = [...new Set(fonts.length > 0 ? [...CODE_FONTS, ...fonts] : [])].map((font) => {
    return `family=${googleFamily(font)}`;
  });

  return families.length > 0 ? `https://fonts.googleapis.com/css2?${families.join("&")}&display=block` : "";
}

function fontCss(fonts) {
  const bodyStack = fontStack(fonts, "sans-serif");
  const codeStack = fontStack(fonts.length > 0 ? [...CODE_FONTS, ...fonts] : [], "monospace");

  return `html {
  --ha-font-family-body: ${bodyStack};
  --ha-font-family-heading: ${bodyStack};
  --ha-font-family-code: ${codeStack};
  --primary-font-family: ${bodyStack};
  --paper-font-common-base_-_font-family: ${bodyStack};
  --mdc-typography-font-family: ${bodyStack};
  font-family: ${bodyStack};
}

body {
  font-family: ${bodyStack};
}
`;
}

function apply() {
  if (!document.head) {
    setTimeout(apply, 100);
    return;
  }

  const fonts = fontsFromModuleUrl();
  const url = googleFontsUrl(fonts);

  document.getElementById("home-assistant-custom-font-google")?.remove();
  document.getElementById("home-assistant-custom-font")?.remove();

  if (url) {
    const link = document.createElement("link");
    link.id = "home-assistant-custom-font-google";
    link.rel = "stylesheet";
    link.href = url;
    document.head.append(link);
  }

  const style = document.createElement("style");
  style.id = "home-assistant-custom-font";
  style.textContent = fontCss(fonts);
  document.head.append(style);
}

apply();
setTimeout(apply, 1000);
