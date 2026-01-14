/**
 * @type {import('fs-extra')}
 */
import fs from 'fs-extra';
import ejs from 'ejs';
import {minify} from 'html-minifier-terser';
import {build} from 'esbuild';
import {readFile, writeFile, mkdir} from 'fs/promises';
import {existsSync} from 'fs';
import path from 'path';
import sharp from 'sharp';
import png2icons from 'png2icons';
import imagemin from 'imagemin';
import imageminPngquant from 'imagemin-pngquant';
import {optimize} from 'svgo';
import {projectPaths, config, isApacheServer, DEV_MODE} from './build.config.js';
import {exec} from 'child_process';
import {compileAsync} from 'sass';

fs.emptyDir(projectPaths.distDir);

const articles = JSON.parse(await fs.readFile(projectPaths.articles.metaData, 'utf8'));

export async function generateHtml() {
  const template = await fs.readFile(projectPaths.templates.index, 'utf8');

  for (const article of articles) {
    const basePath = article.name === 'index' ? './' : '../';
    const html = ejs.render(template, {articles, ...article, basePath, isApacheServer, DEV_MODE }, { filename: projectPaths.templates.index });
    const outputPath = article.name === 'index' ?
      path.join(projectPaths.distDir, 'index.html')
      : path.join(projectPaths.articles.distDir, `${article.name}.html`);
    await fs.ensureDir(path.dirname(outputPath));
    const finalContent = DEV_MODE ? html : await minify(html, config.html);
    await fs.writeFile(outputPath, finalContent);
  }
}

async function generateSitemap() {
  const sitemapTemplate = await fs.readFile(projectPaths.templates.sitemap, 'utf8');
  const sitemap = ejs.render(sitemapTemplate, {articles});
  fs.writeFile(path.join(projectPaths.distDir, 'sitemap.xml'), sitemap);
}

async function generateRss() {
  try {
    const rssTemplate = await fs.readFile(projectPaths.templates.rss, 'utf8');
    const rssContent = ejs.render(rssTemplate, {articles});
    await fs.writeFile(path.join(projectPaths.distDir, 'feed.xml'), rssContent);
  } catch (err) {
    console.error('RSS ERR:', err);
  }
}

async function optimizeImages() {
  await fs.mkdirp(projectPaths.images.distDir, {recursive: true});
  const files = await fs.readdir(projectPaths.images.srcDir);

  await Promise.all(files.map(async (file) => {
    const input = path.join(projectPaths.images.srcDir, file);
    const output = path.join(projectPaths.images.distDir, file);
    const ext = path.extname(file).toLowerCase();

    try {
      if (projectPaths.images.exclude.some(ex => ex === file)) { return; }
      if (file === 'icon-mask.png') {
        await sharp(input).png(config.images.png).toFile(path.join(projectPaths.distDir, file));
        return;
      }
      switch (ext) {
      case '.jpg':
      case '.jpeg':
        await sharp(input).jpeg(config.images.jpeg).toFile(output);
        break;
      case '.png':
        await sharp(input).png(config.images.png).toFile(output);
        break;
      case '.webp':
        await sharp(input).webp(config.images.webp).toFile(output);
        break;
      case '.svg':
        const svgContent = await fs.readFile(input, 'utf8');
        const optimizedSvg = optimize(svgContent).data;
        await fs.writeFile(output, optimizedSvg);
        break;
      default:
        await fs.copy(input, output);
        break;
      }
    } catch (err) {
      console.error(`optimizeImages() | Failed to process ${name}:`, err);
    }
  })
  );
}

export async function compileSass() {
  try {
    const result = await compileAsync(projectPaths.styles.src, config.sass);
    fs.writeFile(projectPaths.styles.dist, result.css);
  } catch (err) {
    console.error('SASS ERR:', err);
  }
}

export async function bundleJs() {
  try {
    await build(config.esbuild);
  } catch (err) {
    console.error('JS ERR:', err);
  }
}

async function copyFiles() {
  try {
    fs.copy(projectPaths.assetsDir, projectPaths.distDir, {
      overwrite: true,
      filter: (src) => {
        if (!isApacheServer && path.basename(src) === '.htaccess') { return false; }
        // exclude img folder from copying; images processed by optimizeImages()
        const rel = path.relative(projectPaths.assetsDir, src);
        const parts = rel.split(path.sep);
        return parts[0] !== path.parse(projectPaths.images.srcDir).base;
      }
    });
  } catch (err) {
    console.error('FILE COPY ERR:', err);
  }
}

async function generateFavicons() {
  const srcPng = path.join(projectPaths.images.srcDir, projectPaths.images.exclude[0]);
  const srcSvg = path.join(projectPaths.images.srcDir, projectPaths.images.exclude[1]);

  if (!existsSync(projectPaths.distDir)) {
    await mkdir(projectPaths.distDir, {recursive: true});
  }

  const pngBuffer = await readFile(srcPng);

  const optimizedPngBuffer = await sharp(pngBuffer).
    resize(32, 32, {fit: 'contain', background: {r: 0, g: 0, b: 0, alpha: 0}}).
    png({compressionLevel: 9, palette: true, colors: 128}).toBuffer();

  const icoBuffer = png2icons.createICO(optimizedPngBuffer, 2, 256, true);
  await writeFile(path.join(projectPaths.distDir, 'favicon.ico'), icoBuffer);

  const pngSizes = [
    {name: 'favicon-16x16.png', size: 16},
    {name: 'favicon-32x32.png', size: 32},
    {name: 'favicon-48x48.png', size: 48},
    {name: 'apple-touch-icon.png', size: 180},
    {name: 'icon-192.png', size: 192},
    {name: 'icon-512.png', size: 512}
  ];

  await Promise.all(pngSizes.map(async ({name, size}) => {
    try {
      const outputPath = path.join(projectPaths.distDir, name);
      await sharp(pngBuffer).resize(size, size, {fit: 'contain', background: {r: 0, g: 0, b: 0, alpha: 0}}).
        png({compressionLevel: 6}).toFile(outputPath);

      await imagemin([outputPath], {
        destination: projectPaths.distDir,
        plugins: [imageminPngquant({quality: [0.7, 0.85]})]
      });

    } catch (err) {
      console.log(`generateFavicons | Failed to process ${name}:`, err);
    }
  })
  );

  try {
    const svgContent = await readFile(srcSvg, 'utf8');
    const optimizedSvg = optimize(svgContent, {
      multipass: true,
      plugins: [{
        name: 'preset-default',
        params: {overrides: {removeViewBox: false}}
      }]
    });
    await writeFile(path.join(projectPaths.distDir, 'favicon.svg'), optimizedSvg.data);
  } catch (err) {
    console.log('generateFavicons | Failed to process SVG:', err);
  }
}

async function createSearchIndex(outputDir) {
  try {
    exec(`npx -y pagefind --site ${outputDir}`);
  } 
  catch (error) {
    console.error('CREATE INDEX ERROR:', error.message);
  }
}

async function runBuild() {
  await fs.emptyDir(projectPaths.distDir);

  await Promise.all([
    generateFavicons(),
    generateHtml(),
    generateSitemap(),
    generateRss(),
    bundleJs(),
    copyFiles(),
    compileSass()
  ]);
  await createSearchIndex(projectPaths.distDir);
  await optimizeImages();
}

runBuild().catch((err) => console.error('BUILD ERR:', err));