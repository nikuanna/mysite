# Сайт Анны Никулиной

Персональный сайт (RU + EN), собственный код без конструктора.
Основной домен: https://www.annanikulina.pro, хостинг GitHub Pages (Custom domain в Settings → Pages, DNS у REG.RU: A @ → 185.199.108-111.153, CNAME www → nikuanna.github.io). apex annanikulina.pro редиректит на www. RU: /annanikulina/, EN: /en/. Константа `BASE` в `tools/build.py`.
Vercel больше не основной хостинг (в России тормозил); `vercel.json` оставлен на случай возврата. Адрес nikuanna.github.io/mysite/ теперь редиректит на домен.
`vercel.json`: редирект / → /annanikulina/, trailingSlash, buildCommand (видео + сборка), заголовки безопасности (HSTS preload, CSP upgrade-insecure-requests, nosniff, X-Frame-Options). `.github/workflows/check-domain.yml` — ручная диагностика домена (DNS, HTTPS, файлы), смотреть логи в Actions.

## Структура
- `tools/build.py` — ЕДИНСТВЕННЫЙ источник текстов и разметки. Словарь `CONTENT` содержит обе версии (ru, en). Шаблон страницы в функции `page()`.
- `annanikulina/index.html`, `en/index.html` — СГЕНЕРИРОВАННЫЕ файлы. Руками не править, пересобирать: `python3 tools/build.py .`
- `assets/site.css` — дизайн. Палитра тон-в-тон с фото (оттенок 358°): фон первого экрана почти совпадает с фоном фото (#efcacb → #ebc4c5 → #d8adb2), пользователь просит держать их близкими, фон фото #ecc5c6, светлые блоки #fbf7f7 и #f6eeef, бордо #5a1828, тёмное вино #2c0b14, крем #fbf6f3. Шрифт Inter Tight (лежит в `assets/fonts/`). Без арок и антиквы: пользователю они не нравятся.
- `assets/site.js` — параллакс (`data-speed` по вертикали, `data-x` по горизонтали, `data-fade`), сияние кнопок за курсором и звёздочки при наведении и клике (класс `glow`, слой `.sparkle-layer`); фоновые надписи мягкие (полупрозрачная заливка) и целиком в экране, появление блоков, меню, видео-плеер.
- Портрет на сайте: `assets/img/anna-portrait-home.jpg` (1474x1866): лёгкое размытие фона, оранжевый диван и предметы фона переведены в розовый тон, сама Анна не тронута. Оригинал: `anna-portrait-home-original.jpg`. Прежние варианты: `anna-portrait-event*.jpg`, `anna-portrait.jpg`. Пользователь не любит «ИИ-вид»: обработка минимальная и естественная.
- `assets/img/og-cover.jpg` — превью для соцсетей 1200x630, `favicon.svg`.
- Видео: `tools/fetch_videos.py` при каждой сборке на GitHub (и ежедневно) забирает списки роликов в `data/videos.json`: RU-страница показывает RuTube (YouTube в РФ работает с перебоями), EN-страница показывает YouTube. На сайте только полные выпуски (без тизеров и Shorts), ролик открывается во всплывающем плеере. С этого сервера YouTube и RuTube недоступны, список смотреть в логах GitHub Actions.
- `index.html` в корне — редирект на `annanikulina/`.
- `.github/workflows/pages.yml` — автодеплой при каждом push.
- `.github/workflows/backup.yml` — бэкап: при каждом push и раз в месяц GitHub Release с ZIP всего сайта.

## Как вносить правки
1. Меняй тексты в `CONTENT` в `tools/build.py`, сразу в обеих версиях (RU и EN синхронно; EN: профессиональный американский деловой английский).
2. `python3 tools/build.py .`
3. Проверь в браузере (desktop + mobile), затем commit + push. Деплой и бэкап запускаются автоматически.

## Важно
- После каждой правки обязательно commit + push. Не оставляй изменения незакоммиченными.
- Откат: git history или ZIP из Releases (`backup-*`).
- Пользователь просит не использовать длинные тире в текстах.
- Не выдумывать факты о пользователе: только подтверждённые данные.
- В меню нет логотипа/имени слева (пользователь просил убрать). Фоновой надписи с фамилией на первом экране нет: дублировала имя.
- EN-термин роли: «Non-Executive Director» (решение пользователя). Должности в банках не указывать; в RU банки называть (ПСБ, МДМ Банк, УРАЛСИБ, СДМ-Банк), в EN «top-10 Russian banks» плюс названия. Номер закона (№ 259-ФЗ) указывать только в RU-версии.
- SEO/ИИ: `tools/build.py` генерирует JSON-LD (Person, ProfilePage, WebSite, ItemList видео), meta robots/keywords/og, `sitemap.xml`, `robots.txt` (открыт для поисковиков и ИИ-ботов) и `llms.txt` (факты для ИИ, RU+EN). Поля `keywords`, `job_titles`, `knows_about` в CONTENT. Description держать до ~160 символов.
- Обложки видео при сборке (GitHub Actions и Vercel) скачиваются в `assets/video-thumbs/` (в git не хранятся, см. .gitignore), страница не зависит от CDN YouTube/RuTube. Цель: сайт открывается без VPN в любой стране, кроме материкового Китая.
- Хостинг: из России Vercel тормозит (бесконечная загрузка), поэтому домен переводится на GitHub Pages (A-записи 185.199.108-111.153, www CNAME nikuanna.github.io).
