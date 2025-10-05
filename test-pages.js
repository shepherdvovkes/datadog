#!/usr/bin/env node

/**
 * DATADOG Website Testing Script
 * Tests all language versions for errors, broken links, and functionality
 */

const http = require('http');
const { JSDOM } = require('jsdom');

const BASE_URL = 'http://localhost:8000';
const PAGES = [
    { url: '/', name: 'Ukrainian (index.html)', lang: 'uk' },
    { url: '/index-en.html', name: 'English', lang: 'en' },
    { url: '/index-ja.html', name: 'Japanese', lang: 'ja' }
];

const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function fetchPage(url) {
    return new Promise((resolve, reject) => {
        http.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                if (res.statusCode === 200) {
                    resolve({ html: data, status: res.statusCode });
                } else {
                    reject(new Error(`HTTP ${res.statusCode}`));
                }
            });
        }).on('error', reject);
    });
}

async function testPage(page) {
    log(`\n${'='.repeat(60)}`, 'cyan');
    log(`Testing: ${page.name}`, 'bright');
    log(`URL: ${BASE_URL}${page.url}`, 'blue');
    log('='.repeat(60), 'cyan');

    const errors = [];
    const warnings = [];
    const successes = [];

    try {
        // Fetch page
        log('\n[1/6] Fetching page...', 'yellow');
        const { html, status } = await fetchPage(`${BASE_URL}${page.url}`);
        successes.push(`✓ Page loaded successfully (HTTP ${status})`);

        // Parse HTML
        log('[2/6] Parsing HTML...', 'yellow');
        const dom = new JSDOM(html, { url: `${BASE_URL}${page.url}`, runScripts: 'outside-only' });
        const document = dom.window.document;
        successes.push('✓ HTML parsed successfully');

        // Check basic structure
        log('[3/6] Checking HTML structure...', 'yellow');
        const title = document.querySelector('title');
        if (!title || !title.textContent.includes('DATADOG')) {
            errors.push('✗ Missing or invalid <title> tag');
        } else {
            successes.push(`✓ Valid title: "${title.textContent.substring(0, 50)}..."`);
        }

        const nav = document.querySelector('nav.navbar');
        if (!nav) {
            errors.push('✗ Missing navigation bar');
        } else {
            successes.push('✓ Navigation bar found');
        }

        // Check language attribute
        const htmlLang = document.documentElement.getAttribute('lang');
        if (page.lang === 'uk' && htmlLang !== 'uk') {
            warnings.push(`⚠ Expected lang="uk" but got lang="${htmlLang}"`);
        } else if (page.lang === 'en' && htmlLang !== 'en') {
            warnings.push(`⚠ Expected lang="en" but got lang="${htmlLang}"`);
        } else if (page.lang === 'ja' && htmlLang !== 'ja') {
            warnings.push(`⚠ Expected lang="ja" but got lang="${htmlLang}"`);
        } else {
            successes.push(`✓ Correct language attribute: lang="${htmlLang}"`);
        }

        // Check sections
        log('[4/6] Checking page sections...', 'yellow');
        const sections = ['mission', 'values', 'tech', 'nato', 'capabilities'];
        sections.forEach(id => {
            const section = document.getElementById(id);
            if (!section) {
                errors.push(`✗ Missing section: #${id}`);
            } else {
                successes.push(`✓ Section found: #${id}`);
            }
        });

        // Check language switcher
        log('[5/6] Checking language switcher...', 'yellow');
        const langSwitcher = document.querySelector('.lang-switcher');
        if (!langSwitcher) {
            errors.push('✗ Language switcher not found');
        } else {
            const langSelect = langSwitcher.querySelector('select#langSelect');
            if (!langSelect) {
                errors.push('✗ Language select dropdown not found');
            } else {
                const options = langSelect.querySelectorAll('option');
                if (options.length !== 3) {
                    warnings.push(`⚠ Expected 3 language options, found ${options.length}`);
                } else {
                    successes.push(`✓ Language switcher with ${options.length} options`);
                }
            }
        }

        // Check external resources
        log('[6/6] Checking external resources...', 'yellow');
        const stylesheets = document.querySelectorAll('link[rel="stylesheet"]');
        if (stylesheets.length === 0) {
            errors.push('✗ No stylesheets linked');
        } else {
            successes.push(`✓ ${stylesheets.length} stylesheet(s) linked`);
        }

        const scripts = document.querySelectorAll('script[src]');
        if (scripts.length < 2) {
            warnings.push(`⚠ Only ${scripts.length} external script(s) found (expected at least 2)`);
        } else {
            successes.push(`✓ ${scripts.length} script(s) linked`);
        }

        // Check for Lucide icons
        const lucideScript = Array.from(scripts).find(s => s.src.includes('lucide'));
        if (!lucideScript) {
            errors.push('✗ Lucide icons library not loaded');
        } else {
            successes.push('✓ Lucide icons library found');
        }

        // Check for data-lucide attributes
        const icons = document.querySelectorAll('[data-lucide]');
        if (icons.length === 0) {
            warnings.push('⚠ No Lucide icons found in HTML');
        } else {
            successes.push(`✓ ${icons.length} Lucide icon(s) found`);
        }

    } catch (error) {
        errors.push(`✗ CRITICAL ERROR: ${error.message}`);
    }

    // Print results
    log('\n' + '─'.repeat(60), 'cyan');
    log('RESULTS:', 'bright');
    log('─'.repeat(60), 'cyan');

    if (successes.length > 0) {
        log('\nSuccesses:', 'green');
        successes.forEach(s => log(`  ${s}`, 'green'));
    }

    if (warnings.length > 0) {
        log('\nWarnings:', 'yellow');
        warnings.forEach(w => log(`  ${w}`, 'yellow'));
    }

    if (errors.length > 0) {
        log('\nErrors:', 'red');
        errors.forEach(e => log(`  ${e}`, 'red'));
    }

    const totalTests = successes.length + warnings.length + errors.length;
    const passed = successes.length;
    const failed = errors.length;

    log('\n' + '─'.repeat(60), 'cyan');
    log(`Summary: ${passed}/${totalTests} tests passed`, failed === 0 ? 'green' : 'yellow');
    if (failed > 0) {
        log(`${failed} error(s) found!`, 'red');
    } else {
        log('All critical tests passed! ✓', 'green');
    }
    log('─'.repeat(60), 'cyan');

    return { successes: passed, warnings: warnings.length, errors: failed };
}

async function main() {
    log('\n╔════════════════════════════════════════════════════════════╗', 'cyan');
    log('║           DATADOG Website Testing Suite                   ║', 'bright');
    log('╚════════════════════════════════════════════════════════════╝', 'cyan');

    const results = [];

    for (const page of PAGES) {
        const result = await testPage(page);
        results.push({ page: page.name, ...result });
    }

    // Overall summary
    log('\n\n' + '═'.repeat(60), 'cyan');
    log('OVERALL SUMMARY', 'bright');
    log('═'.repeat(60), 'cyan');

    let totalSuccess = 0;
    let totalWarnings = 0;
    let totalErrors = 0;

    results.forEach(r => {
        const status = r.errors === 0 ? '✓ PASS' : '✗ FAIL';
        const color = r.errors === 0 ? 'green' : 'red';
        log(`\n${r.page}:`, 'bright');
        log(`  ${status} | Passed: ${r.successes} | Warnings: ${r.warnings} | Errors: ${r.errors}`, color);
        
        totalSuccess += r.successes;
        totalWarnings += r.warnings;
        totalErrors += r.errors;
    });

    log('\n' + '─'.repeat(60), 'cyan');
    log(`Total Tests: ${totalSuccess + totalWarnings + totalErrors}`, 'bright');
    log(`  Passed: ${totalSuccess}`, 'green');
    log(`  Warnings: ${totalWarnings}`, 'yellow');
    log(`  Errors: ${totalErrors}`, totalErrors === 0 ? 'green' : 'red');
    log('─'.repeat(60), 'cyan');

    if (totalErrors === 0) {
        log('\n✓ ALL PAGES PASSED TESTING!', 'green');
        log('The website is ready for production.', 'green');
    } else {
        log('\n✗ SOME TESTS FAILED', 'red');
        log('Please review the errors above.', 'yellow');
        process.exit(1);
    }

    log('\nSlava Ukraini! 🇺🇦\n', 'blue');
}

// Run tests
if (require.main === module) {
    main().catch(err => {
        log(`\nFATAL ERROR: ${err.message}`, 'red');
        log('Make sure the server is running on http://localhost:8000', 'yellow');
        process.exit(1);
    });
}

module.exports = { testPage };

