# Сайт Анны Никулиной

Персональный сайт (RU + EN), собственный код без конструктора. Хостинг: GitHub Pages.
Адреса: https://nikuanna.github.io/mysite/annanikulina/ (RU), https://nikuanna.github.io/mysite/en/ (EN).

## Структура
- `tools/build.py` — ЕДИНСТВЕННЫЙ источник текстов и разметки. Словарь `CONTENT` содержит обе версии (ru, en). Шаблон страницы в функции `page()`.
- `annanikulina/index.html`, `en/index.html` — СГЕНЕРИРОВАННЫЕ файлы. Руками не править, пересобирать: `python3 tools/build.py .`
- `assets/site.css` — дизайн (палитра: ink #0d1320, ivory, gold #c4a473; шрифты Cormorant Garamond + Manrope, лежат в `assets/fonts/`).
- `assets/site.js` — параллакс (`data-speed`), появление блоков, состояние меню.
- `assets/img/` — фото, `og-cover.jpg` (превью для соцсетей 1200x630), `favicon.svg`.
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
- Фото-портрет пока 336x336, при замене брать минимум 1000px.
