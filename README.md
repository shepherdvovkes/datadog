# DATADOG - Intelligence Solutions for UAF

Professional minimalist website for DATADOG, a data analytics and machine learning company providing intelligent solutions for the Armed Forces of Ukraine.

## Overview

DATADOG transforms battlefield data into tactical superiority and saved lives. The platform provides real-time intelligence solutions based on data analytics and machine learning, accelerating decision-making and improving mission effectiveness.

## Technologies

- **Pure JavaScript** - No frameworks, lightweight and fast
- **Lucide Icons** - Modern icon library loaded via CDN
- **CSS3** - Modern styling with animations and transitions
- **Responsive Design** - Mobile-first approach

## Features

- Clean, professional NASA/ESA-inspired design
- Dark theme optimized for readability
- Smooth scrolling and navigation
- Interactive cards with hover effects
- Parallax effects
- Mobile-responsive menu
- Intersection Observer animations
- Cursor trail effects

## Structure

```
/home/vovkes/DATADOG/
├── index.html      # Ukrainian version (main)
├── index-en.html   # English version
├── index-ja.html   # Japanese version
├── styles.css      # All styling and animations
├── script.js       # Interactive functionality
├── test-pages.js   # Automated test suite
├── package.json    # Project configuration
└── README.md       # Documentation
```

## Language Versions

The website is available in three languages:

- **Ukrainian (UA)** - `index.html` - Default version
- **English (EN)** - `index-en.html` - International version
- **Japanese (JP)** - `index-ja.html` - Japanese version

Each version includes a language switcher in the navigation bar (globe icon with dropdown) that allows users to seamlessly switch between languages.

## Sections

1. **Hero** - Main section with mission statement and key metrics
2. **Mission & Vision** - Company goals and strategic direction
3. **Core Values** - 5 fundamental principles
4. **UAV Types** - 4 categories of drones supported
5. **NATO Standards** - STANAG 4586, OGC, NATO SECRET compliance
6. **Capabilities** - 8 technological solutions
7. **Footer** - Contact information and technical details

## How to Run

Simply open `index.html` in a modern web browser. No build process or dependencies required.

```bash
# Option 1: Open directly
open index.html          # Ukrainian version
open index-en.html       # English version
open index-ja.html       # Japanese version

# Option 2: Use a local server (recommended)
python3 -m http.server 8000
# Then navigate to:
# http://localhost:8000           - Ukrainian
# http://localhost:8000/index-en.html  - English
# http://localhost:8000/index-ja.html  - Japanese

# Option 3: Use pm2 with http-server
npm install -g http-server
http-server -p 8000
```

## NATO Standards Implemented

- **STANAG 4586 (ED-1)** - UAV interoperability architecture
- **OGC Standards** - Geospatial data exchange formats
- **NATO SECRET** - Information protection standards

## Testing

The project includes comprehensive test suites that validate all three language versions:

### Static Tests (JSDOM)
```bash
# Install dependencies (first time only)
npm install

# Run static tests
npm test

# Run tests with fresh server
npm run test:full
```

**Static Test Coverage:**
- ✓ HTTP response validation
- ✓ HTML structure verification
- ✓ Language attribute checking
- ✓ Section presence validation
- ✓ Language switcher presence
- ✓ External resources (CSS/JS)
- ✓ Icon library integration
- ✓ All 5 main sections (#mission, #values, #tech, #nato, #capabilities)

**Static Test Results:**
- Ukrainian: 15/15 tests passed ✓
- English: 15/15 tests passed ✓
- Japanese: 15/15 tests passed ✓
- **Total: 45/45 tests passed**

### Browser Tests (Puppeteer)
```bash
# Run language switching tests in real browser
npm run test:switch

# Run all tests (static + browser)
npm run test:all
```

**Browser Test Coverage:**
- ✓ Load each language version
- ✓ Language selector functionality
- ✓ Switch from Ukrainian to English
- ✓ Switch from English to Japanese
- ✓ Switch back to Ukrainian
- ✓ Navigation links after switching
- ✓ URL updates correctly

**Browser Test Results:**
- Language Switching: 7/7 tests passed ✓
- Screenshots: 3/3 captured ✓
- **Total: 100% success rate**

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Design Principles

- No emojis, only professional icons
- No gradients in primary design
- Clean typography hierarchy
- Consistent spacing and alignment
- Professional color palette
- High contrast for readability

## Color Palette

- Primary Background: `#0a0e1a`
- Secondary Background: `#111827`
- Card Background: `#1a1f2e`
- Accent: `#3b82f6`
- Text Primary: `#f9fafb`
- Text Secondary: `#9ca3af`

## Performance

- Minimal external dependencies (only Lucide icons)
- Optimized animations with CSS transforms
- Lazy loading with Intersection Observer
- No heavy frameworks

---

**Slava Ukraini!** 🇺🇦

