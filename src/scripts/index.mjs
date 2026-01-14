import setColorTheme from './set-color-theme.mjs';
import setCookies from './show-cookies-dialog.mjs';
import insertCurrentYear from './update-copyright-year.mjs';

// noinspection JSUnresolvedReference
if (DEV_MODE) {
  console.log('DEV_MODE');
}

// noinspection JSUnresolvedReference
new PagefindUI({ element: '[data-pagefind]', showSubResults: true, showImages: false});

setColorTheme();
setCookies();
insertCurrentYear();
