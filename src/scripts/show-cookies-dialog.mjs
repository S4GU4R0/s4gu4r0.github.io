function setCookies() {
  const dialog = document.querySelector('[data-cookie-dialog]');
  const button = dialog.querySelector('[data-cookie-close]');

  if (!document.cookie.includes('cookieConsent=accepted')) {
    dialog.show();
  }

  button.addEventListener('click', () => {
    document.cookie = 'cookieConsent=accepted; Max-Age=31536000; Path=/';
    dialog.close();
  });
}

export default setCookies;