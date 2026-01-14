import path from 'path';
import {fileURLToPath} from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.dirname(__dirname);

export const isApacheServer = true;
export const DEV_MODE = process.env.NODE_ENV === 'development';

export const projectPaths = {
  srcDir: path.join(rootDir, 'src'),
  distDir: path.join(rootDir, 'dist'),
  assetsDir: path.join(rootDir, 'assets'),
  templates: {
    dir: path.join(rootDir,'src','template'),
    index: path.join(rootDir, 'src', 'template', 'index.ejs'),
    sitemap: path.join(rootDir, 'src', 'template', 'sitemap.ejs'),
    rss: path.join(rootDir, 'src', 'template', 'rss.ejs')
  },
  articles: {
    srcDir: path.join(rootDir, 'src', 'articles'),
    distDir: path.join(rootDir, 'dist', 'articles'),
    metaData: path.join(rootDir, 'src', 'template', 'articles.json')
  },
  styles: {
    src: path.join(rootDir, 'src', 'styles', 'main.scss'),
    srcDir: path.join(rootDir, 'src', 'styles'),
    dist: path.join(rootDir, 'dist', 'main.css')
  },
  js: {
    src: path.join(rootDir, 'src', 'scripts', 'index.mjs'),
    scriptsDir: path.join(rootDir, 'src', 'scripts'),
    dist: path.join(rootDir, 'dist', 'index.mjs')
  },
  images: {
    srcDir: path.join(rootDir, 'assets', 'img'),
    distDir: path.join(rootDir, 'dist', 'img'),
    exclude: ['icon_src_512.png', 'icon_src.svg', 'readme.md']
  }
};

export const config = {
  browserSync: {
    files: [
      path.posix.join(projectPaths.distDir, '**', '*.{html,css,js,mjs}')
    ],
    ignore: [
      path.posix.join(projectPaths.distDir, 'pagefind', '**', '*')
    ],
    server: {
      baseDir: projectPaths.distDir,
      middleware: [(req, res, next) => {
        if (req.url.endsWith('.html')) {
          res.setHeader('Cache-Control', 'no-cache, no-store');
        }
        next();
      }]
    },
    injectChanges: true,
    notify: false,
    browser: path.join(__dirname, 'open-incognito-firefox.zsh')
    // browser: path.join(__dirname, 'open-incognito-chromium.zsh'),
    // browser: 'firefox-developer-edition',
    // browser: 'chromium',
    // proxy: 'myDomain.local',
    // logLevel: 'debug',
    // port: 3000,
    // snippetOptions: {
    //   rule: {
    //     match: /<\/head>/i, // Match the closing </head> tag
    //     fn: function(snippet, match) {
    //       return snippet + match; // inject snippet before closing </head>
    //     }
    //   }
    // }
  },

  html: {
    collapseWhitespace: true,
    removeComments: true,
    minifyCSS: true,
    minifyJS: {compress: {expression: false, sequences: false}},
    processScripts: ['application/ld+json'],
    removeAttributeQuotes: true,
    removeEmptyAttributes: true,
    removeRedundantAttributes: true,
    removeScriptTypeAttributes: true,
    removeStyleLinkTypeAttributes: true,
    useShortDoctype: true
  },
  sass: {
    style: 'compressed',
    sourceMap: false
  },

  esbuild: {
    entryPoints: [projectPaths.js.src],
    outfile: projectPaths.js.dist,
    minify: true,
    bundle: true,
    format: 'esm',
    sourcemap: false,
    define: {
      DEV_MODE: `${process.env.NODE_ENV === 'development'}`,
      timestamp: `${Date.now()}`
    },
    drop: process.env.NODE_ENV === 'development' ? [] : ['console', 'debugger']
  },
  images: {
    jpeg: {quality: 75, mozjpeg: true},
    png: {quality: 75, compressionLevel: 9},
    webp: {quality: 75}
  }
};