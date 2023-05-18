function setThemeClass() {
  document.documentElement.className = Telegram.WebApp.colorScheme;
}

export function initEvents() {
  Telegram.WebApp.onEvent("themeChanged", setThemeClass);

  setThemeClass();
}
