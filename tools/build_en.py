import re, sys, os
root = sys.argv[1]
ru_path = os.path.join(root, 'annanikulina/index.html')
s = open(ru_path, encoding='utf-8').read()

SW_CSS = ('<style id="lang-switch-css">.lang-switch{position:fixed;top:16px;right:16px;z-index:1000;display:flex;gap:2px;padding:3px;'
  'border-radius:999px;background:rgba(255,255,255,.88);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);'
  'box-shadow:0 2px 12px rgba(0,0,0,.18);font-family:"Open Sans",Arial,sans-serif}'
  '.lang-switch a{display:block;min-width:38px;padding:7px 12px;border-radius:999px;font-size:13px;font-weight:600;line-height:1;'
  'letter-spacing:.06em;text-align:center;text-decoration:none;color:#1f2a3a;transition:background .2s,color .2s}'
  '.lang-switch a:hover{background:rgba(31,42,58,.08)}.lang-switch a[aria-current="page"]{background:#1f2a3a;color:#fff;cursor:default}'
  '@media (max-width:639px){.lang-switch{top:12px;right:12px}.lang-switch a{padding:8px 13px}}</style>')

def switch(active):
    ru = '<a href="../annanikulina/" lang="ru" hreflang="ru"%s>RU</a>' % (' aria-current="page"' if active=='ru' else '')
    en = '<a href="../en/" lang="en" hreflang="en"%s>EN</a>' % (' aria-current="page"' if active=='en' else '')
    return '<nav class="lang-switch" aria-label="Language / Язык">%s%s</nav>' % (ru, en)

HREFLANG = ('<link rel="alternate" hreflang="ru" href="https://nikuanna.github.io/mysite/annanikulina/">'
            '<link rel="alternate" hreflang="en" href="https://nikuanna.github.io/mysite/en/">')

def add_switch(html, active):
    html = re.sub(r'<style id="lang-switch-css">.*?</style>', '', html, flags=re.S)
    html = re.sub(r'<nav class="lang-switch".*?</nav>', '', html, flags=re.S)
    html = re.sub(r'<link rel="alternate" hreflang="[a-z]+"[^>]*>', '', html)
    html = html.replace('</head>', HREFLANG + SW_CSS + '</head>', 1)
    html = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + switch(active), html, count=1)
    return html

def must(html, old, new):
    assert html.count(old) == 1, (old, html.count(old))
    return html.replace(old, new)

# --- RU page: add switcher ---
open(ru_path, 'w', encoding='utf-8').write(add_switch(s, 'ru'))

# --- EN page ---
e = s
e = e.replace('<html lang="ru">', '<html lang="en">', 1)
TITLE = 'Anna Nikulina | Independent Director, Venture Investor, Strategic Advisor'
DESC = 'Independent director, venture investor and strategic advisor with 15+ years of executive leadership in banking, fintech and consumer brands.'
e = must(e, '<title>Анна Никулина</title>', '<title>%s</title>' % TITLE)
e = must(e, '<meta name="description" content="Анна Никулина">', '<meta name="description" content="%s">' % DESC)
e = must(e, '<meta name="keywords" content="Анна, Никулина">', '<meta name="keywords" content="Anna Nikulina, independent director, board member, venture investor, strategic advisor, CBDO">')
e = must(e, '<meta property="og:title" content="Анна Никулина">', '<meta property="og:title" content="Anna Nikulina">')
e = must(e, '<meta property="og:description" content="">', '<meta property="og:description" content="%s">' % DESC)
e = must(e, '<meta name="twitter:title" content="Анна Никулина">', '<meta name="twitter:title" content="Anna Nikulina">')
e = must(e, '<meta name="twitter:description" content="">', '<meta name="twitter:description" content="%s">' % DESC)
e = must(e, 'sb-font-title">Анна Никулина</h4>', 'sb-font-title">Anna Nikulina</h4>')
e = must(e, 'Независимый директор | Венчурный инвестор | Предприниматель | Директор по развитию | Советник по стратегическому развитию',
         'Independent&nbsp;Director | Venture&nbsp;Investor | Entrepreneur | Chief&nbsp;Business&nbsp;Development&nbsp;Officer | Strategic&nbsp;Advisor')

HEAD = [
 ('Предпринимательский опыт B2B | B2C', 'Entrepreneurship: B2B | B2C'),
 ('Законодательная деятельность', 'Policy &amp; Legislation'),
 ('Инвестор', 'Venture Investing'),
 ('Банковский сектор', 'Banking'),
 ('Управленческий опыт', 'Executive Leadership'),
 ('Для инвесторов', 'For Investors'),
 ('Для собственников бизнеса', 'For Business Owners'),
 ('Для стартапов и бизнеса', 'For Startups &amp; Growing Companies'),
 ('Контакты для профессиональных запросов', 'Professional Inquiries'),
]
for ru, en in HEAD:
    e, n = re.subn(r'(<h5[^>]*>)' + re.escape(ru) + r'(<br[^>]*>)?(</h5>)', lambda m: m.group(1) + en + m.group(3), e)
    assert n == 1, ru

BODY = [
 ['Co-owner of a Russian health &amp; beauty brand', 'Co-founder of a global tech startup', 'Former founder of a fintech startup in Russia'],
 ['Contributed to drafting Federal Law', 'No.&nbsp;259-FZ on investment platforms', '(crowdfunding) in Russia, representing', 'the business community'],
 ['Venture investor in early-stage tech startups', '(global markets, with a successful exit)', 'Invited expert and judge', 'at startup pitch competitions'],
 ['Former Managing Director', 'at Top&nbsp;10 Russian banks', '(10,000+ employees, RUB&nbsp;2&nbsp;trillion in assets)',
  'Built and managed multibillion-ruble', 'corporate loan portfolios',
  'Expert in credit risk and', 'financial resilience assessment', 'for businesses and projects,', 'from SMBs to industrial majors',
  'Risk manager with a track record', 'in crisis and turnaround management'],
 ['15+ years in executive leadership', '(50+ branches, international teams)', 'Risk-based and crisis management'],
 ['Investment analysis and due diligence', 'for projects at every stage', 'Risk and opportunity assessment'],
 ['Strategy consulting and identifying growth levers', 'Operational management',
  'Board service as an Independent Director', 'at privately held companies'],
 ['An investor&#8217;s perspective and mentorship', 'Review of positioning, business model', 'and growth prospects at any stage'],
]

def replace_div_content(html, start_tag_pos, new_inner):
    open_end = html.index('>', start_tag_pos) + 1
    depth, i = 1, open_end
    tag = re.compile(r'<(/?)div\b[^>]*>')
    while depth:
        m = tag.search(html, i)
        depth += -1 if m.group(1) else 1
        i = m.end()
    close_start = i - len('</div>')
    return html[:open_end] + new_inner + html[close_start:]

for idx, lines in enumerate(BODY):
    pos = [m.start() for m in re.finditer(r'<div class="sb-font-p3">', e)][idx]
    e = replace_div_content(e, pos, '<br>'.join(lines))

e = must(e, '>LinkedIn</a> и <a', '>LinkedIn</a> and <a')
e = must(e, 'Мой Telegram-канал: <a', 'My Telegram channel (in Russian): <a')

left = re.findall(r'>([^<>]*[А-Яа-яЁё][^<>]*)<', e[e.find('<body'):])
assert not left, left
os.makedirs(os.path.join(root, 'en'), exist_ok=True)
open(os.path.join(root, 'en/index.html'), 'w', encoding='utf-8').write(add_switch(e, 'en'))
print('ok')
