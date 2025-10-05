const puppeteer = require('puppeteer');

async function testFooterVisual() {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const pages = [
        { url: 'http://localhost:8000/', lang: 'uk', name: 'Ukrainian' },
        { url: 'http://localhost:8000/index-en.html', lang: 'en', name: 'English' },
        { url: 'http://localhost:8000/index-ja.html', lang: 'ja', name: 'Japanese' }
    ];

    console.log('📸 Testing Footer Visual Appearance\n');
    console.log('=' .repeat(60));

    for (const pageInfo of pages) {
        console.log(`\n🌐 ${pageInfo.name} page...`);

        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });
        await page.goto(pageInfo.url, { waitUntil: 'networkidle0' });

        // Scroll to footer
        await page.evaluate(() => {
            const footer = document.querySelector('.footer');
            if (footer) {
                footer.scrollIntoView({ behavior: 'instant', block: 'center' });
            }
        });

        await new Promise(resolve => setTimeout(resolve, 500));

        // Get footer contact information
        const footerInfo = await page.evaluate(() => {
            const footerContact = document.querySelector('.footer-contact');
            if (!footerContact) return null;

            const items = Array.from(footerContact.querySelectorAll('.contact-item'));
            return items.map(item => {
                const icon = item.querySelector('i');
                const text = item.querySelector('span, a');
                return {
                    icon: icon ? icon.getAttribute('data-lucide') : null,
                    text: text ? text.textContent.trim() : null,
                    hasLink: !!item.querySelector('a')
                };
            });
        });

        console.log('   Contact Items:');
        if (footerInfo) {
            footerInfo.forEach((item, idx) => {
                const linkIcon = item.hasLink ? '🔗' : '  ';
                console.log(`   ${idx + 1}. ${linkIcon} [${item.icon}] ${item.text}`);
            });
        } else {
            console.log('   ❌ Footer contact section not found!');
        }

        // Take screenshot of footer
        const footerElement = await page.$('.footer');
        if (footerElement) {
            await footerElement.screenshot({ 
                path: `test-screenshots/footer-${pageInfo.lang}.png` 
            });
            console.log(`   ✓ Screenshot saved: test-screenshots/footer-${pageInfo.lang}.png`);
        }

        await page.close();
    }

    await browser.close();

    console.log('\n' + '=' .repeat(60));
    console.log('\n✅ Footer visual test completed!\n');
}

testFooterVisual()
    .then(() => process.exit(0))
    .catch(error => {
        console.error('Fatal error:', error);
        process.exit(1);
    });

