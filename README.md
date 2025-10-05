# 🛡️ DATAGOD - Intelligence Solutions for UAF

**Невидимий щит української армії** - веб-додаток для демонстрації технологій інтелектуального аналізу даних та машинного навчання для Збройних Сил України.

## 📁 Структура проекту

```
DATAGOD/
├── 📄 index.html                 # Головна сторінка (українська)
├── 📁 src/                       # Вихідний код
│   ├── 📁 pages/                 # HTML сторінки
│   │   ├── index-en.html         # Англійська версія
│   │   └── index-ja.html         # Японська версія
│   ├── 📁 assets/                # Статичні ресурси
│   │   ├── 📁 css/               # Стилі
│   │   │   └── styles.css        # Основні стилі
│   │   ├── 📁 js/                # JavaScript
│   │   │   └── script.js        # Основна логіка
│   │   └── 📁 images/            # Зображення
│   ├── 📁 config/                # Конфігурація
│   │   └── app.yaml             # Google Cloud конфігурація
│   └── 📁 docs/                  # Документація
├── 📁 public/                    # Публічні ресурси
│   ├── 📁 images/                # Публічні зображення
│   └── 📁 icons/                 # Іконки
├── 📁 tests/                     # Тести
│   ├── 📁 screenshots/           # Скриншоти тестів
│   ├── 📁 reports/               # Звіти тестів
│   ├── test-contact-info.js      # Тест контактної інформації
│   ├── test-footer-visual.js     # Візуальний тест футера
│   ├── test-language-switch.js   # Тест перемикання мов
│   └── test-pages.js            # Загальний тест сторінок
├── 📁 node_modules/             # Залежності Node.js
├── 📄 package.json              # Залежності проекту
├── 📄 package-lock.json         # Фіксовані версії залежностей
└── 📄 README.md                 # Цей файл
```

## 🚀 Швидкий старт

### Встановлення залежностей
```bash
npm install
```

### Запуск локального сервера
```bash
# За допомогою PM2 (рекомендовано)
pm2 start "python3 -m http.server 8000" --name datagod-server

# Або звичайний Python сервер
python3 -m http.server 8000
```

### Відкриття в браузері
- 🇺🇦 Українська: http://localhost:8000/
- 🇬🇧 English: http://localhost:8000/src/pages/index-en.html
- 🇯🇵 日本語: http://localhost:8000/src/pages/index-ja.html

## 🧪 Тестування

### Запуск всіх тестів
```bash
# Тест контактної інформації
node tests/test-contact-info.js

# Тест перемикання мов
node tests/test-language-switch.js

# Загальний тест сторінок
node tests/test-pages.js

# Візуальний тест футера
node tests/test-footer-visual.js
```

### Автоматичне тестування
```bash
# Запуск всіх тестів послідовно
npm test
```

## 🌐 Мультимовність

Сайт підтримує 3 мови:
- **🇺🇦 Українська** (основна) - `/index.html`
- **🇬🇧 English** - `/src/pages/index-en.html`
- **🇯🇵 日本語** - `/src/pages/index-ja.html`

Перемикання мов працює через JavaScript без перезавантаження сторінки.

## 🎨 Технології

- **HTML5** - Семантична розмітка
- **CSS3** - Сучасні стилі з Flexbox/Grid
- **JavaScript ES6+** - Інтерактивність
- **Lucide Icons** - Векторні іконки
- **Puppeteer** - Автоматизоване тестування

## 📱 Адаптивність

Сайт повністю адаптивний для:
- 📱 Мобільні пристрої (320px+)
- 📱 Планшети (768px+)
- 💻 Десктоп (1024px+)
- 🖥️ Великі екрани (1440px+)

## 🔒 Безпека

- **CSP заголовки** - Захист від XSS атак
- **HTTPS only** - Безпечне з'єднання
- **X-Frame-Options** - Захист від clickjacking
- **Content-Type-Options** - Захист від MIME sniffing

## 📊 Стандарти НАТО

Сайт містить повну базу знань стандартів НАТО для БПЛА:
- **STANAG 4586** - Стандартний інтерфейс управління
- **STANAG 4671** - Вимоги до льотної придатності
- **STANAG 4703** - Системи зв'язку
- **OGC стандарти** - Геопросторові дані
- **NATO SECRET** - Інформаційна безпека

## 🚀 Розгортання

### Google Cloud Platform
```bash
# Розгортання на GCP
gcloud app deploy config/app.yaml
```

### Статичний хостинг
```bash
# Копіювання файлів на статичний хостинг
rsync -avz . user@server:/var/www/datagod/
```

## 📞 Контакти

- **🌐 Сайт:** https://datadog.s0me.uk
- **📧 Email:** info@s0me.uk

## 📄 Ліцензія

© 2025 DATAGOD. Всі права захищено.

**Slava Ukraini! 🇺🇦**

---

*Розроблено для підтримки Збройних Сил України*
