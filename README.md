# S4GU4R0.wtf

A minimal, terminal-aesthetic personal website built with XHTML, CSS, and following the rule of least power.

## Philosophy

- **Rule of Least Power**: Uses the simplest technology that works (XHTML for structure, CSS for presentation)
- **Mobile-First**: Designed for mobile devices first, scales up gracefully
- **Terminal Aesthetic**: Green text on black background, monospace fonts, ASCII art decorations
- **Accessibility**: Semantic HTML, skip links, proper heading hierarchy, works without CSS/JS
- **No JavaScript**: Site is fully functional without any JavaScript

## File Structure

```
/
├── index.html          # Homepage with post list and links
├── style.css           # All styles (terminal aesthetic)
├── feed.xml           # RSS feed
├── posts/
│   └── welcome.html   # Sample blog post
└── README.md          # This file
```

## Adding a New Post

### 1. Create the HTML file

Copy `posts/welcome.html` and modify it:

```bash
cp posts/welcome.html posts/your-post-name.html
```

Update:
- `<title>` tag
- `<meta>` description
- `og:title`, `og:description`, `og:url`
- Post date in `[YYYY-MM-DD]` format
- Post title in `<h2>`
- Post content in the `.post-content` div

### 2. Add to index.html

In `index.html`, add a new list item to the "Recent Posts" section:

```html
<li><span class="date">[2024-12-20]</span> <a href="posts/your-post-name.html">Your Post Title</a></li>
```

Keep posts in reverse chronological order (newest first).

### 3. Update feed.xml

Add a new `<item>` to the RSS feed (at the top, before other items):

```xml
<item>
  <title>Your Post Title</title>
  <link>https://s4gu4r0.wtf/posts/your-post-name.html</link>
  <description>Brief description of your post.</description>
  <pubDate>Fri, 20 Dec 2024 12:00:00 GMT</pubDate>
  <guid>https://s4gu4r0.wtf/posts/your-post-name.html</guid>
</item>
```

Update `<lastBuildDate>` in the feed to match the newest post date.

## Updating Links

### Social Media Links

Edit the "External Links" section in `index.html`. Links are organized by category:

- **Support**: Wishlist, payment platforms
- **Social Media**: Ranked by activity (most to least)
- **Chat/Communities**: Ranked by activity
- **Gaming**: Gaming platforms
- **Forums**: Forum links

### Activity Indicators

The activity bars use block characters:
- `████████░░` = 8/10 (daily/very active)
- `██████░░░░` = 6/10 (weekly/active)
- `███░░░░░░░` = 3/10 (monthly/occasional)

Adjust the ratio of filled (█) to empty (░) blocks to represent activity level.

## Customizing the Design

### Colors

Edit CSS variables in `style.css`:

```css
:root {
    --bg-primary: #000000;      /* Background color */
    --text-primary: #00ff00;    /* Primary text color */
    --text-dim: #00aa00;        /* Dimmed text */
    --text-inactive: #006600;   /* Inactive/label text */
    --link-hover: #00ffff;      /* Link hover color */
}
```

### Typography

The site uses monospace fonts. To change:

```css
body {
    font-family: 'Courier New', 'Courier', monospace;
}
```

Replace with your preferred monospace font stack.

### Spacing

Adjust the spacing unit:

```css
:root {
    --spacing-unit: 1rem;  /* Base spacing (16px default) */
}
```

## Deployment

This is a static site - upload all files to any web host:

- **GitHub Pages**: Push to a repo, enable Pages
- **Netlify**: Drag and drop the folder
- **Neocities**: Upload via web interface
- **Traditional hosting**: FTP/SFTP upload

No build process required - just upload the files as-is.

## Validation

To validate your XHTML:
- Visit https://validator.w3.org/
- Upload your HTML files or enter the URL

To validate your RSS feed:
- Visit https://validator.w3.org/feed/
- Upload feed.xml or enter the URL

## Accessibility Features

- Semantic HTML5 elements
- Skip link for keyboard navigation
- Proper heading hierarchy
- Alt text support for images (when added)
- High contrast support
- Reduced motion support
- Touch-friendly tap targets (44px minimum)

## Browser Support

Works in all modern browsers and degrades gracefully in older browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

Works without CSS, works without JavaScript, works with screen readers.

## License

Content and code by Saguaro Prole.
