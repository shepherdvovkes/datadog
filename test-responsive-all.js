const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Конфигурация устройств для тестирования
const devices = [
    // Мобильные устройства
    { name: 'iPhone SE', width: 320, height: 568, deviceScaleFactor: 2 },
    { name: 'iPhone 8', width: 375, height: 667, deviceScaleFactor: 2 },
    { name: 'iPhone 12', width: 390, height: 844, deviceScaleFactor: 3 },
    { name: 'iPhone 14 Pro Max', width: 430, height: 932, deviceScaleFactor: 3 },
    { name: 'Galaxy S20', width: 360, height: 800, deviceScaleFactor: 3 },
    { name: 'Pixel 5', width: 393, height: 851, deviceScaleFactor: 2.75 },
    
    // Планшеты
    { name: 'iPad Mini', width: 768, height: 1024, deviceScaleFactor: 2 },
    { name: 'iPad Air', width: 820, height: 1180, deviceScaleFactor: 2 },
    { name: 'iPad Pro 11', width: 834, height: 1194, deviceScaleFactor: 2 },
    { name: 'iPad Pro 12.9', width: 1024, height: 1366, deviceScaleFactor: 2 },
    
    // Десктопы
    { name: 'Laptop', width: 1366, height: 768, deviceScaleFactor: 1 },
    { name: 'Desktop HD', width: 1920, height: 1080, deviceScaleFactor: 1 },
    { name: 'Desktop 2K', width: 2560, height: 1440, deviceScaleFactor: 1 },
    { name: 'Desktop 4K', width: 3840, height: 2160, deviceScaleFactor: 2 },
];

// Языковые версии
const languages = [
    { name: 'Ukrainian', file: 'index.html', code: 'uk' },
    { name: 'English', file: 'index-en.html', code: 'en' },
    { name: 'Japanese', file: 'index-ja.html', code: 'ja' },
];

// Создание директории для скриншотов и отчетов
const screenshotsDir = path.join(__dirname, 'test-screenshots');
const reportsDir = path.join(__dirname, 'test-reports');

if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
}
if (!fs.existsSync(reportsDir)) {
    fs.mkdirSync(reportsDir, { recursive: true });
}

// Функция для проверки overflow
async function checkOverflow(page) {
    return await page.evaluate(() => {
        const body = document.body;
        const html = document.documentElement;
        
        const hasHorizontalOverflow = body.scrollWidth > html.clientWidth || 
                                     body.offsetWidth > html.clientWidth;
        
        return {
            hasOverflow: hasHorizontalOverflow,
            bodyWidth: body.scrollWidth,
            viewportWidth: html.clientWidth,
            overflowElements: Array.from(document.querySelectorAll('*'))
                .filter(el => {
                    const rect = el.getBoundingClientRect();
                    return rect.right > html.clientWidth;
                })
                .map(el => ({
                    tag: el.tagName,
                    class: el.className,
                    width: el.scrollWidth,
                    right: el.getBoundingClientRect().right
                }))
                .slice(0, 5) // Первые 5 элементов
        };
    });
}

// Функция для проверки видимости элементов
async function checkElementsVisibility(page) {
    return await page.evaluate(() => {
        const selectors = [
            '.navbar',
            '.hero',
            '.hero-title',
            '.hero-stats',
            '.mission-grid',
            '.values-grid',
            '.uav-grid',
            '.capabilities-grid',
            '.footer',
            '.lang-switcher'
        ];
        
        const results = {};
        selectors.forEach(selector => {
            const element = document.querySelector(selector);
            if (element) {
                const rect = element.getBoundingClientRect();
                const styles = window.getComputedStyle(element);
                results[selector] = {
                    visible: rect.width > 0 && rect.height > 0,
                    display: styles.display,
                    opacity: styles.opacity,
                    width: rect.width,
                    height: rect.height
                };
            } else {
                results[selector] = { visible: false, error: 'Element not found' };
            }
        });
        
        return results;
    });
}

// Функция для проверки CSS ошибок
async function checkCSSIssues(page) {
    return await page.evaluate(() => {
        const issues = [];
        
        // Проверка на элементы с overflow
        const allElements = document.querySelectorAll('*');
        allElements.forEach(el => {
            const styles = window.getComputedStyle(el);
            if (styles.overflowX !== 'hidden' && styles.overflowX !== 'visible') {
                const rect = el.getBoundingClientRect();
                if (rect.width > window.innerWidth) {
                    issues.push({
                        type: 'overflow',
                        element: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
                        width: rect.width,
                        viewportWidth: window.innerWidth
                    });
                }
            }
        });
        
        // Проверка текста на читабельность
        const textElements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, span, a, li');
        textElements.forEach(el => {
            const styles = window.getComputedStyle(el);
            const fontSize = parseFloat(styles.fontSize);
            if (fontSize < 12) {
                issues.push({
                    type: 'small-text',
                    element: el.tagName,
                    fontSize: fontSize + 'px'
                });
            }
        });
        
        return issues.slice(0, 10); // Первые 10 проблем
    });
}

// Основная функция тестирования
async function runTests() {
    console.log('🚀 Запуск комплексного тестирования адаптивности...\n');
    
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const allResults = [];
    let totalTests = 0;
    let passedTests = 0;
    let failedTests = 0;
    
    for (const lang of languages) {
        console.log(`\n${'='.repeat(60)}`);
        console.log(`📖 Тестирование языка: ${lang.name} (${lang.file})`);
        console.log(`${'='.repeat(60)}\n`);
        
        for (const device of devices) {
            totalTests++;
            
            const page = await browser.newPage();
            
            // Установка viewport
            await page.setViewport({
                width: device.width,
                height: device.height,
                deviceScaleFactor: device.deviceScaleFactor
            });
            
            const url = `http://localhost:8080/${lang.file}`;
            
            try {
                console.log(`  📱 Устройство: ${device.name} (${device.width}x${device.height})`);
                
                // Загрузка страницы с timeout
                await page.goto(url, { 
                    waitUntil: 'networkidle2',
                    timeout: 30000 
                });
                
                // Ожидание загрузки всех элементов
                await page.waitForSelector('.navbar', { timeout: 5000 });
                await page.waitForTimeout(1000); // Дополнительное время для анимаций
                
                // Проверки
                const consoleErrors = [];
                page.on('console', msg => {
                    if (msg.type() === 'error') {
                        consoleErrors.push(msg.text());
                    }
                });
                
                const overflowCheck = await checkOverflow(page);
                const visibilityCheck = await checkElementsVisibility(page);
                const cssIssues = await checkCSSIssues(page);
                
                // Создание скриншота
                const screenshotName = `${lang.code}_${device.name.replace(/\s+/g, '_')}.png`;
                const screenshotPath = path.join(screenshotsDir, screenshotName);
                await page.screenshot({ 
                    path: screenshotPath, 
                    fullPage: true 
                });
                
                // Определение статуса теста
                const hasIssues = overflowCheck.hasOverflow || 
                                 cssIssues.length > 0 || 
                                 Object.values(visibilityCheck).some(v => !v.visible);
                
                const testStatus = hasIssues ? 'FAILED' : 'PASSED';
                
                if (testStatus === 'PASSED') {
                    passedTests++;
                    console.log(`    ✅ ${testStatus}`);
                } else {
                    failedTests++;
                    console.log(`    ❌ ${testStatus}`);
                }
                
                // Сохранение результата
                const result = {
                    language: lang.name,
                    languageCode: lang.code,
                    device: device.name,
                    resolution: `${device.width}x${device.height}`,
                    status: testStatus,
                    screenshot: screenshotName,
                    overflow: overflowCheck,
                    visibility: visibilityCheck,
                    cssIssues: cssIssues,
                    consoleErrors: consoleErrors
                };
                
                allResults.push(result);
                
                // Вывод проблем
                if (overflowCheck.hasOverflow) {
                    console.log(`    ⚠️  Обнаружен горизонтальный overflow: ${overflowCheck.bodyWidth}px > ${overflowCheck.viewportWidth}px`);
                }
                
                if (cssIssues.length > 0) {
                    console.log(`    ⚠️  Найдено CSS проблем: ${cssIssues.length}`);
                }
                
            } catch (error) {
                failedTests++;
                console.log(`    ❌ FAILED: ${error.message}`);
                
                allResults.push({
                    language: lang.name,
                    languageCode: lang.code,
                    device: device.name,
                    resolution: `${device.width}x${device.height}`,
                    status: 'ERROR',
                    error: error.message
                });
            }
            
            await page.close();
        }
    }
    
    await browser.close();
    
    // Генерация отчета
    console.log(`\n${'='.repeat(60)}`);
    console.log('📊 ИТОГОВЫЕ РЕЗУЛЬТАТЫ');
    console.log(`${'='.repeat(60)}\n`);
    console.log(`Всего тестов: ${totalTests}`);
    console.log(`✅ Пройдено: ${passedTests} (${Math.round(passedTests/totalTests*100)}%)`);
    console.log(`❌ Провалено: ${failedTests} (${Math.round(failedTests/totalTests*100)}%)`);
    console.log(`\nСкриншоты сохранены в: ${screenshotsDir}`);
    
    // Сохранение JSON отчета
    const jsonReport = {
        timestamp: new Date().toISOString(),
        summary: {
            total: totalTests,
            passed: passedTests,
            failed: failedTests,
            successRate: Math.round(passedTests/totalTests*100)
        },
        results: allResults
    };
    
    const jsonPath = path.join(reportsDir, 'responsive-test-report.json');
    fs.writeFileSync(jsonPath, JSON.stringify(jsonReport, null, 2));
    console.log(`JSON отчет сохранен: ${jsonPath}`);
    
    // Генерация HTML отчета
    generateHTMLReport(jsonReport);
    
    return jsonReport;
}

// Функция для генерации HTML отчета
function generateHTMLReport(data) {
    const html = `
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DATADOG - Отчет о тестировании адаптивности</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e1a;
            color: #f9fafb;
            padding: 20px;
        }
        .header {
            text-align: center;
            padding: 30px;
            background: #111827;
            border-radius: 12px;
            margin-bottom: 30px;
            border: 1px solid #1f2937;
        }
        .header h1 {
            font-size: 2.5rem;
            color: #3b82f6;
            margin-bottom: 10px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #111827;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #1f2937;
            text-align: center;
        }
        .stat-value {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 10px;
        }
        .stat-value.total { color: #3b82f6; }
        .stat-value.passed { color: #10b981; }
        .stat-value.failed { color: #ef4444; }
        .stat-label {
            color: #9ca3af;
            font-size: 1rem;
        }
        .results {
            display: grid;
            gap: 15px;
        }
        .result-card {
            background: #111827;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #1f2937;
            transition: transform 0.3s ease;
        }
        .result-card:hover {
            transform: translateX(4px);
        }
        .result-card.passed {
            border-left: 4px solid #10b981;
        }
        .result-card.failed {
            border-left: 4px solid #ef4444;
        }
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .result-title {
            font-size: 1.25rem;
            font-weight: 700;
        }
        .status-badge {
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .status-badge.passed {
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
        }
        .status-badge.failed {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }
        .result-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            color: #9ca3af;
            font-size: 0.9rem;
        }
        .screenshot {
            margin-top: 15px;
        }
        .screenshot img {
            max-width: 300px;
            border-radius: 8px;
            border: 1px solid #1f2937;
        }
        .issues {
            margin-top: 15px;
            padding: 15px;
            background: rgba(239, 68, 68, 0.1);
            border-radius: 8px;
        }
        .issues h4 {
            color: #ef4444;
            margin-bottom: 10px;
        }
        .filter-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 10px 20px;
            background: #1a1f2e;
            border: 1px solid #3b82f6;
            border-radius: 8px;
            color: #f9fafb;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .filter-btn:hover, .filter-btn.active {
            background: #3b82f6;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Отчет о тестировании адаптивности</h1>
        <p>Дата: ${new Date(data.timestamp).toLocaleString('uk-UA')}</p>
    </div>

    <div class="summary">
        <div class="stat-card">
            <div class="stat-value total">${data.summary.total}</div>
            <div class="stat-label">Всего тестов</div>
        </div>
        <div class="stat-card">
            <div class="stat-value passed">${data.summary.passed}</div>
            <div class="stat-label">Пройдено</div>
        </div>
        <div class="stat-card">
            <div class="stat-value failed">${data.summary.failed}</div>
            <div class="stat-label">Провалено</div>
        </div>
        <div class="stat-card">
            <div class="stat-value ${data.summary.successRate === 100 ? 'passed' : 'failed'}">${data.summary.successRate}%</div>
            <div class="stat-label">Успешность</div>
        </div>
    </div>

    <div class="filter-buttons">
        <button class="filter-btn active" onclick="filterResults('all')">Все</button>
        <button class="filter-btn" onclick="filterResults('passed')">Пройденные</button>
        <button class="filter-btn" onclick="filterResults('failed')">Проваленные</button>
        <button class="filter-btn" onclick="filterResults('Ukrainian')">🇺🇦 Українська</button>
        <button class="filter-btn" onclick="filterResults('English')">🇬🇧 English</button>
        <button class="filter-btn" onclick="filterResults('Japanese')">🇯🇵 日本語</button>
    </div>

    <div class="results" id="results">
        ${data.results.map(result => `
            <div class="result-card ${result.status.toLowerCase()}" data-status="${result.status}" data-language="${result.language}">
                <div class="result-header">
                    <div class="result-title">${result.language} - ${result.device}</div>
                    <div class="status-badge ${result.status.toLowerCase()}">${result.status}</div>
                </div>
                <div class="result-info">
                    <div>Разрешение: ${result.resolution}</div>
                    <div>Язык: ${result.language}</div>
                </div>
                ${result.screenshot ? `
                    <div class="screenshot">
                        <a href="../test-screenshots/${result.screenshot}" target="_blank">
                            <img src="../test-screenshots/${result.screenshot}" alt="Screenshot">
                        </a>
                    </div>
                ` : ''}
                ${result.overflow && result.overflow.hasOverflow ? `
                    <div class="issues">
                        <h4>⚠️ Проблемы с overflow</h4>
                        <p>Ширина body: ${result.overflow.bodyWidth}px</p>
                        <p>Ширина viewport: ${result.overflow.viewportWidth}px</p>
                    </div>
                ` : ''}
                ${result.cssIssues && result.cssIssues.length > 0 ? `
                    <div class="issues">
                        <h4>⚠️ CSS проблемы: ${result.cssIssues.length}</h4>
                        <pre>${JSON.stringify(result.cssIssues, null, 2)}</pre>
                    </div>
                ` : ''}
            </div>
        `).join('')}
    </div>

    <script>
        function filterResults(filter) {
            const cards = document.querySelectorAll('.result-card');
            const buttons = document.querySelectorAll('.filter-btn');
            
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            cards.forEach(card => {
                if (filter === 'all') {
                    card.style.display = 'block';
                } else if (filter === 'passed' || filter === 'failed') {
                    card.style.display = card.dataset.status.toLowerCase() === filter ? 'block' : 'none';
                } else {
                    card.style.display = card.dataset.language === filter ? 'block' : 'none';
                }
            });
        }
    </script>
</body>
</html>
    `.trim();
    
    const htmlPath = path.join(reportsDir, 'responsive-test-report.html');
    fs.writeFileSync(htmlPath, html);
    console.log(`HTML отчет сохранен: ${htmlPath}\n`);
}

// Запуск тестов
runTests().catch(error => {
    console.error('❌ Ошибка при выполнении тестов:', error);
    process.exit(1);
});

