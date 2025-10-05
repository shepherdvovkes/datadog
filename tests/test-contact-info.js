const puppeteer = require('puppeteer');

async function testContactInfo() {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const pages = [
        { url: 'http://localhost:8000/', lang: 'Ukrainian', contactHeader: 'Контакт' },
        { url: 'http://localhost:8000/src/pages/index-en.html', lang: 'English', contactHeader: 'Contact' },
        { url: 'http://localhost:8000/src/pages/index-ja.html', lang: 'Japanese', contactHeader: 'お問い合わせ' }
    ];

    let allPassed = true;

    console.log('🔍 Testing Contact Information\n');
    console.log('=' .repeat(60));

    for (const pageInfo of pages) {
        console.log(`\n📄 Testing ${pageInfo.lang} page...`);
        console.log(`   URL: ${pageInfo.url}`);

        try {
            const page = await browser.newPage();
            await page.goto(pageInfo.url, { waitUntil: 'networkidle0' });

            // Check for website URL
            const websiteLink = await page.evaluate(() => {
                const links = Array.from(document.querySelectorAll('a[href="https://datadog.s0me.uk"]'));
                return links.length > 0 ? links[0].textContent.trim() : null;
            });

            // Check for email
            const emailText = await page.evaluate(() => {
                const footerContact = document.querySelector('.footer-contact');
                if (!footerContact) return null;
                const spans = Array.from(footerContact.querySelectorAll('span'));
                for (const span of spans) {
                    if (span.textContent.includes('info@s0me.uk')) {
                        return span.textContent.trim();
                    }
                }
                return null;
            });

            // Check that old email is NOT present
            const hasOldEmail = await page.evaluate(() => {
                return document.body.innerHTML.includes('info@datadog.ua');
            });

            // Check that "Classified Location" is NOT present
            const hasClassifiedLocation = await page.evaluate(() => {
                return document.body.innerHTML.includes('Classified Location') || 
                       document.body.innerHTML.includes('機密の場所');
            });

            // Check for contact header
            const contactHeaderExists = await page.evaluate((header) => {
                const h4Elements = Array.from(document.querySelectorAll('.footer-section h4'));
                return h4Elements.some(h4 => h4.textContent.trim() === header);
            }, pageInfo.contactHeader);

            // Results
            console.log(`\n   ✅ Status Checks:`);
            
            if (websiteLink === 'datadog.s0me.uk') {
                console.log(`      ✓ Website link found: ${websiteLink}`);
            } else {
                console.log(`      ✗ Website link MISSING or incorrect: ${websiteLink}`);
                allPassed = false;
            }

            if (emailText === 'info@s0me.uk') {
                console.log(`      ✓ Email found: ${emailText}`);
            } else {
                console.log(`      ✗ Email MISSING or incorrect: ${emailText}`);
                allPassed = false;
            }

            if (!hasOldEmail) {
                console.log(`      ✓ Old email (info@datadog.ua) removed`);
            } else {
                console.log(`      ✗ Old email still present!`);
                allPassed = false;
            }

            if (!hasClassifiedLocation) {
                console.log(`      ✓ Physical address removed`);
            } else {
                console.log(`      ✗ Physical address still present!`);
                allPassed = false;
            }

            if (contactHeaderExists) {
                console.log(`      ✓ Contact section header found`);
            } else {
                console.log(`      ✗ Contact section header MISSING`);
                allPassed = false;
            }

            await page.close();

        } catch (error) {
            console.log(`   ✗ ERROR: ${error.message}`);
            allPassed = false;
        }
    }

    await browser.close();

    console.log('\n' + '=' .repeat(60));
    if (allPassed) {
        console.log('\n✅ ALL TESTS PASSED! Contact information is correct on all pages.');
    } else {
        console.log('\n❌ SOME TESTS FAILED! Please review the issues above.');
    }
    console.log('\n');

    return allPassed ? 0 : 1;
}

testContactInfo()
    .then(code => process.exit(code))
    .catch(error => {
        console.error('Fatal error:', error);
        process.exit(1);
    });

