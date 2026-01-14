function setColorTheme() {
  const colorThemeButton = document.querySelector('[data-toggle-theme]');

  const savedTheme = localStorage.getItem('theme');
  const isBrowserThemeDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initialTheme = savedTheme || (isBrowserThemeDark ? 'dark-mode' : 'light-mode');

  document.body.classList.add(initialTheme);

  colorThemeButton.addEventListener('click', () => {
    const isCurrentThemeDark = document.body.classList.contains('dark-mode');
    const newTheme = isCurrentThemeDark ? 'light-mode' : 'dark-mode';

    document.body.classList.replace(isCurrentThemeDark ? 'dark-mode' : 'light-mode', newTheme);
    localStorage.setItem('theme', newTheme);
  });
}

export default setColorTheme;
