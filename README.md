# EJS Blog

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

[![Support me on Boosty](https://img.shields.io/badge/Boosty-Support%20me-%23f15f2c?style=for-the-badge)](https://boosty.to/theEvilGrinch/donate)
[![Donate](https://img.shields.io/badge/Donate-%23702ff4?style=for-the-badge)](https://yoomity.ru/to/410016288289737)

Modern, fast-loading blog platform powered by EJS templates. Features built-in search, RSS feed, and sitemap generation, automatic image optimization, favicon generation, cookie consent dialog, color theme management, and more. Built with modern web standards, responsive design, and SEO best practices. Deploy anywhere as static site with minimal configuration.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Favicon Generation](#favicon-generation)
  - [Article Publishing](#article-publishing)
  - [Required Customization](#required-customization)
  - [Build for Production](#build-for-production)
- [Development](#development)
  - [Dependencies](#dependencies)
  - [Run Development Server](#run-development-server)
  - [Available Scripts](#available-scripts)
  - [Browser Launch Scripts](#browser-launch-scripts)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Lightweight & Performant** - Primarily built with vanilla JavaScript and modern web standards, with minimal framework dependencies only where they provide significant value (like PageFind for search functionality)
- **Blazing Fast** - Leverages ESBuild for near-instantaneous builds and optimized production output
- **Modern Styling** - Uses SCSS with helpful mixins for responsive typography and media queries
- **SEO Optimized** - Built with semantic HTML5, meta tags, and Schema.org structured data for technical articles and web pages
- **Responsive Design** - Flexible layouts using CSS Flexbox with responsive typography via `flex-text` mixin
- **Asset Optimization** - Automatic favicon generation, image optimization, and minification of HTML, CSS, and JavaScript
- **Smart Development Server** - Watches for file changes and triggers incremental builds for modified assets (EJS, SASS, JS) with automatic browser reload
- **Cookie Management** - Basic cookie consent dialog for tracking user preferences
- **Search Functionality** - Client-side search implementation with PageFind
- **RSS & Sitemap** - Automatic generation of RSS feed and sitemap.xml

## Project Structure

```
.
├── assets/                              # Static assets
│   ├── fonts/                           # Web fonts
│   ├── img/                             # Global images
│   ├── .htaccess                        # Apache server configuration
│   ├── 404.html                         # Custom 404 error page
│   ├── humans.txt                       # Information about the site's developers
│   ├── manifest.webmanifest             # Web app manifest
│   └── robots.txt                       # Instructions for web crawlers
├── build-system/                        # Build configuration and scripts
│   ├── build.config.js                  # Central build configuration
│   ├── build.js                         # Production build script
│   ├── open-incognito-chromium.zsh      # Open Chromium in incognito mode
│   ├── open-incognito-firefox.zsh       # Open Firefox in private browsing mode
│   └── watch.js                         # Development server script
└── src/                                 # Source files
    ├── articles/                        # Blog articles in HTML format
    ├── scripts/                         # JavaScript modules (ES modules)
    │   ├── index.mjs                    # Main JavaScript entry point
    │   ├── set-color-theme.mjs          # Theme management
    │   ├── show-cookies-dialog.mjs      # Cookie consent dialog
    │   └── update-copyright-year.mjs    # Dynamic copyright year in footer
    ├── styles/                          # SCSS styles and CSS
    │   ├── _custom.scss                 # Custom styles and overrides
    │   ├── _fonts.scss                  # Font face declarations
    │   ├── _template-styles.scss        # Template-specific styles
    │   ├── _search.scss                 # Styles for PageFind search 
    │   ├── core/                        # Core SCSS utilities
    │   │   ├── _index.scss              # Core utilities entry point
    │   │   ├── _mixins.scss             # SCSS mixins and functions
    │   │   └── _variables.scss          # Global SCSS variables
    │   ├── main.scss                    # Main stylesheet entry point
    │   └── reset.css                    # CSS reset for consistent rendering
    └── template/                        # EJS templates and layouts
        ├── _aside-left.ejs              # Left sidebar template
        ├── _aside-right.ejs             # Right sidebar template
        ├── _footer.ejs                  # Footer template
        ├── _head.ejs                    # Head section template
        ├── _header.ejs                  # Header template
        ├── _main.ejs                    # Main content wrapper
        ├── articles.json                # Articles metadata
        ├── index.ejs                    # Main index template
        ├── rss.ejs                      # RSS feed template
        ├── sitemap.ejs                  # Sitemap template
        ├── tech-article-microdata.json  # Schema.org structured data for tech articles
        └── webpage-microdata.json       # Schema.org structured data for web pages
├── eslint.config.js                     # ESLint configuration
├── package.json                         # Project configuration and dependencies
├── package-lock.json                    # Lock file for dependencies
├── .gitignore                           # Git ignore rules
├── .stylelintrc.json                    # Stylelint configuration
└── LICENSE                              # MIT License
```

## Getting Started

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm 9+
- git 2.28.0+

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/theEvilGrinch/ejs-blog-boilerplate.git
   cd ejs-blog-boilerplate
   ```

2. Install dependencies:
   ```bash
   npm install
   ```
### Favicon Generation

Build script automatically generates favicons in multiple formats from source files.

To use this feature, add these files to `assets/img/`:
- `icon_src.svg` - Vector source for SVG favicon
- `icon_src_512.png` (512x512px) - Source for PNG favicons

To disable automatic favicon generation, comment out or remove the `generateFavicons()` call in the `runBuild` function of `build.js`.

To enable Progressive Web App (PWA) support, manually create an `icon-mask.png` image with a resolution of 512x512 pixels, which is not generated automatically, and place it in the `assets/img` folder before running the build script. A maskable icon can be created using a service like [maskable.app](https://maskable.app/editor).

Build process will generate:
- `ICO` format for legacy browsers
- `SVG` favicon for modern browsers
- `PNG` favicons (16x16, 32x32, 48x48)
- Apple Touch Icon 
- Web App manifest icons

### Article Publishing

1. Create article content in HTML format in `src/articles/`. It will be used in `src/template/_main.ejs` and will become content of `<main>` tag.
2. Add article information to `src/template/articles.json`. Name property must match HTML filename in `src/articles/` without extension.

### Required Customization

Before using this template, make sure to:
- Remove all template placeholders and demo content 
- Replace all `<!-- TODO -->` comments with actual content 
- Update metadata in `package.json`, `assets/manifest.webmanifest`, and template files
- Replace the favicon and other assets in the assets directory

### Build for Production

To create an optimized production build:

```bash
npm run build
```

Command will:
1. Clean `dist` directory
2. Generate HTML files from EJS templates with minification
3. Generate RSS feed and sitemap
4. Compile and minify SCSS to CSS (no source maps)
5. Bundle and minify JavaScript with ESBuild (ES modules format)
6. Optimize images (75% quality for JPEG, PNG, WebP, 70% quality for AVIF)
7. Generate favicons in multiple formats
8. Copy static assets to `dist` directory
9. Generate PageFind search index

## Development

### Dependencies

- `@stylistic/stylelint-plugin`: Stylelint plugin for styling rules
- `browser-sync`: Development server with live reload
- `ejs`: Template engine for generating HTML
- `esbuild`: JavaScript bundler and minifier
- `eslint`: JavaScript linter
- `fs-extra`: File system operations
- `gh-pages`: Deployment to GitHub Pages
- `globals`: Global variables for ESLint
- `html-minifier-terser`: HTML minification
- `imagemin`: Image optimization
- `imagemin-pngquant`: PNG optimization
- `pagefind`: Full-text search
- `png2icons`: Favicon generation
- `sass`: CSS preprocessor
- `sharp`: Image processing
- `stylelint`: CSS/SCSS linter
- `svgo`: SVG optimization

### Run Development Server

Start the development server with file watching:

```bash
npm run dev
```

Command will:
1. Start development server at `http://localhost:3000`
2. Watch for changes in source files and trigger appropriate build tasks
3. Automatically reload browser when files change

### Available Scripts

- `npm run build` - Create an optimized production build in the `dist` directory
- `npm run dev` - Start development server with file watching
- `npm run clean` - Remove the `dist` directory
- `npm run stylelint:fix` - Fix auto-fixable style issues
- `npm run eslint:fix` - Fix auto-fixable JavaScript issues
- `npm run deploy` - Deploy to GitHub Pages (requires repository setup)
- `npm run predeploy` - Run before deployment to ensure clean build

### Browser Launch Scripts

Build system includes two shell scripts for launching browsers in incognito/private mode:
- `open-incognito-chromium.zsh` — launches Chromium-based browsers in incognito mode
- `open-incognito-firefox.zsh` — launches Firefox in private browsing mode

By default, `firefox-developer-edition` browser is used. Change browser by modifying `browser` option in `build.config.js`:
```js
browserSync: {
  // browser: 'firefox-developer-edition', // default browser
  // browser: path.join(__dirname, 'open-incognito-chromium.zsh'),
  browser: path.join(__dirname, 'open-incognito-firefox.zsh')
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
