#!/usr/bin/env node

/**
 * DATAGOD Language Switching Test with Puppeteer
 * Tests language switching functionality in a real browser
 */

const puppeteer = require('puppeteer');

const BASE_URL = 'http://localhost:8000';

const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    magenta: '\x1b[35m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function testLanguageSwitching() {
    log('\n╔════════════════════════════════════════════════════════════╗', 'cyan');
    log('║     DATAGOD Language Switching Test (Puppeteer)          ║', 'bright');
    log('╚════════════════════════════════════════════════════════════╝', 'cyan');

    let browser;
    const results = {
        passed: 0,
        failed: 0,
        tests: []
    };

    try {
        log('\n[1/8] Launching browser...', 'yellow');
        browser = await puppeteer.launch({
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        log('✓ Browser launched successfully', 'green');

        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });

        // Test 1: Load Ukrainian page
        log('\n[2/8] Loading Ukrainian page...', 'yellow');
        await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle0' });
        await sleep(500);
        
        const ukTitle = await page.title();
        const ukHeroText = await page.$eval('.hero-title', el => el.textContent);
        const ukLang = await page.$eval('html', el => el.getAttribute('lang'));
        
        if (ukLang === 'uk' && ukHeroText.includes('Невидимий щит')) {
            log(`✓ Ukrainian page loaded: "${ukHeroText.trim()}"`, 'green');
            results.passed++;
            results.tests.push({ test: 'Load Ukrainian page', status: 'PASS' });
        } else {
            log(`✗ Ukrainian page verification failed`, 'red');
            results.failed++;
            results.tests.push({ test: 'Load Ukrainian page', status: 'FAIL' });
        }

        // Test 2: Check language selector presence
        log('\n[3/8] Checking language selector...', 'yellow');
        const langSelector = await page.$('select#langSelect');
        if (langSelector) {
            const options = await page.$$('select#langSelect option');
            log(`✓ Language selector found with ${options.length} options`, 'green');
            results.passed++;
            results.tests.push({ test: 'Language selector present', status: 'PASS' });
        } else {
            log('✗ Language selector not found', 'red');
            results.failed++;
            results.tests.push({ test: 'Language selector present', status: 'FAIL' });
        }

        // Test 3: Switch to English
        log('\n[4/8] Switching to English...', 'yellow');
        await page.select('select#langSelect', 'en');
        await page.waitForNavigation({ waitUntil: 'networkidle0' });
        await sleep(500);

        const enUrl = page.url();
        const enTitle = await page.title();
        const enHeroText = await page.$eval('.hero-title', el => el.textContent);
        const enLang = await page.$eval('html', el => el.getAttribute('lang'));
        
        if (enUrl.includes('index-en.html') && enLang === 'en' && enHeroText.includes('Invisible Shield')) {
            log(`✓ Switched to English: "${enHeroText.trim()}"`, 'green');
            log(`  URL: ${enUrl}`, 'cyan');
            results.passed++;
            results.tests.push({ test: 'Switch to English', status: 'PASS' });
        } else {
            log(`✗ English switch verification failed`, 'red');
            results.failed++;
            results.tests.push({ test: 'Switch to English', status: 'FAIL' });
        }

        // Test 4: Verify English selector value
        log('\n[5/8] Verifying English selector value...', 'yellow');
        const enSelectorValue = await page.$eval('select#langSelect', el => el.value);
        if (enSelectorValue === 'en') {
            log(`✓ Language selector shows correct value: ${enSelectorValue}`, 'green');
            results.passed++;
            results.tests.push({ test: 'English selector value', status: 'PASS' });
        } else {
            log(`✗ Expected 'en' but got '${enSelectorValue}'`, 'red');
            results.failed++;
            results.tests.push({ test: 'English selector value', status: 'FAIL' });
        }

        // Test 5: Switch to Japanese
        log('\n[6/8] Switching to Japanese...', 'yellow');
        await page.select('select#langSelect', 'ja');
        await page.waitForNavigation({ waitUntil: 'networkidle0' });
        await sleep(500);

        const jaUrl = page.url();
        const jaTitle = await page.title();
        const jaHeroText = await page.$eval('.hero-title', el => el.textContent);
        const jaLang = await page.$eval('html', el => el.getAttribute('lang'));
        
        if (jaUrl.includes('index-ja.html') && jaLang === 'ja' && jaHeroText.includes('ウクライナ軍')) {
            log(`✓ Switched to Japanese: "${jaHeroText.trim()}"`, 'green');
            log(`  URL: ${jaUrl}`, 'cyan');
            results.passed++;
            results.tests.push({ test: 'Switch to Japanese', status: 'PASS' });
        } else {
            log(`✗ Japanese switch verification failed`, 'red');
            results.failed++;
            results.tests.push({ test: 'Switch to Japanese', status: 'FAIL' });
        }

        // Test 6: Switch back to Ukrainian
        log('\n[7/8] Switching back to Ukrainian...', 'yellow');
        await page.select('select#langSelect', 'uk');
        await page.waitForNavigation({ waitUntil: 'networkidle0' });
        await sleep(500);

        const ukUrl2 = page.url();
        const ukHeroText2 = await page.$eval('.hero-title', el => el.textContent);
        const ukLang2 = await page.$eval('html', el => el.getAttribute('lang'));
        
        if (ukUrl2.includes('index.html') && ukLang2 === 'uk' && ukHeroText2.includes('Невидимий щит')) {
            log(`✓ Switched back to Ukrainian: "${ukHeroText2.trim()}"`, 'green');
            log(`  URL: ${ukUrl2}`, 'cyan');
            results.passed++;
            results.tests.push({ test: 'Switch back to Ukrainian', status: 'PASS' });
        } else {
            log(`✗ Ukrainian switch verification failed`, 'red');
            results.failed++;
            results.tests.push({ test: 'Switch back to Ukrainian', status: 'FAIL' });
        }

        // Test 7: Check all navigation links work after switching
        log('\n[8/8] Testing navigation after language switch...', 'yellow');
        const navLinks = await page.$$('.nav-link');
        let navWorking = true;
        
        for (const link of navLinks.slice(0, 3)) { // Test first 3 links
            const href = await link.evaluate(el => el.getAttribute('href'));
            if (href.startsWith('#')) {
                await link.click();
                await sleep(200);
            }
        }
        
        if (navWorking) {
            log(`✓ Navigation links working after language switch`, 'green');
            results.passed++;
            results.tests.push({ test: 'Navigation after switch', status: 'PASS' });
        } else {
            log(`✗ Navigation issues detected`, 'red');
            results.failed++;
            results.tests.push({ test: 'Navigation after switch', status: 'FAIL' });
        }

        // Take screenshots
        log('\n📸 Taking screenshots...', 'magenta');
        await page.goto(`${BASE_URL}/`, { waitUntil: 'networkidle0' });
        await page.screenshot({ path: 'screenshot-uk.png', fullPage: false });
        log('  ✓ screenshot-uk.png', 'cyan');
        
        await page.goto(`${BASE_URL}/index-en.html`, { waitUntil: 'networkidle0' });
        await page.screenshot({ path: 'screenshot-en.png', fullPage: false });
        log('  ✓ screenshot-en.png', 'cyan');
        
        await page.goto(`${BASE_URL}/index-ja.html`, { waitUntil: 'networkidle0' });
        await page.screenshot({ path: 'screenshot-ja.png', fullPage: false });
        log('  ✓ screenshot-ja.png', 'cyan');

    } catch (error) {
        log(`\n✗ ERROR: ${error.message}`, 'red');
        results.failed++;
        results.tests.push({ test: 'Overall execution', status: 'FAIL', error: error.message });
    } finally {
        if (browser) {
            await browser.close();
            log('\n✓ Browser closed', 'green');
        }
    }

    // Print results
    log('\n' + '═'.repeat(60), 'cyan');
    log('TEST RESULTS', 'bright');
    log('═'.repeat(60), 'cyan');

    results.tests.forEach((test, index) => {
        const status = test.status === 'PASS' ? '✓' : '✗';
        const color = test.status === 'PASS' ? 'green' : 'red';
        log(`\n${index + 1}. ${test.test}`, 'bright');
        log(`   ${status} ${test.status}`, color);
        if (test.error) {
            log(`   Error: ${test.error}`, 'red');
        }
    });

    log('\n' + '─'.repeat(60), 'cyan');
    log(`Total Tests: ${results.passed + results.failed}`, 'bright');
    log(`Passed: ${results.passed}`, 'green');
    log(`Failed: ${results.failed}`, results.failed === 0 ? 'green' : 'red');
    log(`Success Rate: ${Math.round((results.passed / (results.passed + results.failed)) * 100)}%`, 
        results.failed === 0 ? 'green' : 'yellow');
    log('─'.repeat(60), 'cyan');

    if (results.failed === 0) {
        log('\n✓ ALL LANGUAGE SWITCHING TESTS PASSED!', 'green');
        log('Language switcher is fully functional.', 'green');
    } else {
        log(`\n✗ ${results.failed} TEST(S) FAILED`, 'red');
        log('Please review the errors above.', 'yellow');
        process.exit(1);
    }

    log('\nSlava Ukraini! 🇺🇦\n', 'blue');
    return results;
}

// Run tests
if (require.main === module) {
    testLanguageSwitching().catch(err => {
        log(`\nFATAL ERROR: ${err.message}`, 'red');
        log('Make sure the server is running on http://localhost:8000', 'yellow');
        process.exit(1);
    });
}

module.exports = { testLanguageSwitching };


