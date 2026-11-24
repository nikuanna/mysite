"""Builds both language versions of the site from one template.

Usage:  python3 tools/build.py .
Output: annanikulina/index.html (RU) and en/index.html (EN)

All texts live in CONTENT below. Edit them there, then run the script.
"""
import datetime, html, json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
BASE = 'https://www.annanikulina.pro'
PORTRAIT = '../assets/img/anna-portrait-home.jpg'  # light bg blur, orange sofa toned to rose; original: anna-portrait-home-original.jpg
OG_IMG = BASE + '/assets/img/og-cover.jpg'

LINKEDIN = 'https://www.linkedin.com/in/anna-nikulina-cbdo/'
TG_PERSONAL = 'https://t.me/Anna_Niku'
TG_CHANNEL = 'https://t.me/STRATEGYNikulina'
YOUTUBE = 'https://www.youtube.com/@STRATEGYNikulina'
RUTUBE = 'https://rutube.ru/channel/30327202'

def load_videos():
    path = os.path.join(ROOT, 'data', 'videos.json')
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {'youtube': [], 'rutube': []}


VIDEOS = load_videos()
SELF_NAMES = {'анна никулина', 'anna nikulina'}


# Words that keep their own spelling in video titles: abbreviations and proper names.
TITLE_FIXES = {'Искусственный интеллект билет в будущее': 'Искусственный интеллект: билет в будущее'}
KEEP_CASE = {'сд': 'СД', 'm&a': 'M&A', 'ии': 'ИИ', 'китай': 'Китай', 'китае': 'Китае', 'китая': 'Китая',
             'россия': 'Россия', 'россии': 'России', 'mena': 'MENA', 'ai': 'AI', 'it': 'IT', 'ит': 'ИТ',
             'china': 'China', 'russia': 'Russia', 'uae': 'UAE', 'dubai': 'Dubai'}


def sentence_case(title):
    """Uniform titles: lowercase, first word capitalized, abbreviations and names kept."""
    words = title.split()
    out = []
    for i, w in enumerate(words):
        core = w.strip('.,:;!?«»"()')
        low = core.lower()
        if low in KEEP_CASE:
            fixed = KEEP_CASE[low]
        elif i == 0:
            fixed = low[:1].upper() + low[1:]
        else:
            fixed = low
        out.append(w.replace(core, fixed, 1) if core else w)
    return ' '.join(out)


# English titles for the EN page (keyed by YouTube video id) and Latin spelling of guest names.
EN_TITLES = {
    'cvLB6uWxBnk': 'Subsidiary liability of board members and owners',
    'VuuB7uzdvwo': 'The robot revolution',
    'n84INQQOz0Q': 'Home as a service',
    'jWN5XPts_jQ': 'Behind the scenes of M&A',
    'KyPmCVrwbLU': 'A strategy for country living',
    '8VpxzIJPAVs': 'Artificial intelligence: a ticket to the future',
    'xlhwJ3_e-nw': 'How to expand your business into China',
}
EN_GUESTS = {
    'Павел Викторов': 'Pavel Viktorov', 'Артём Лукин': 'Artem Lukin', 'Артем Лукин': 'Artem Lukin',
    'Артём Бабинов': 'Artem Babinov', 'Артем Бабинов': 'Artem Babinov', 'Иван Скавыш': 'Ivan Skavysh',
    'Евгений Антифеев': 'Evgeny Antifeev', 'Тимур Эль-Гохари': 'Timur El-Gohary', 'Виктор Соковнин': 'Viktor Sokovnin',
}


def thumb_img(url):
    """YouTube: high-resolution cover (1280x720) with a fallback to the standard one."""
    url = html.escape(url, quote=True)
    if 'i.ytimg.com' in url and 'hqdefault' in url:
        hi = url.replace('hqdefault', 'maxresdefault')
        return ('<img src="%s" alt="" loading="lazy" decoding="async" '
                'onerror="this.onerror=null;this.src=\'%s\'">' % (hi, url))
    return '<img src="%s" alt="" loading="lazy" decoding="async">' % url


def prepare_videos(vids, lang='ru'):
    """Full episodes only: no teasers, no Shorts, no duplicates. Splits 'Title | Guest, Anna' into title + guest."""
    out, seen = [], {}
    for v in vids:
        if v.get('short') or re.match(r'\s*тизер|\s*teaser', v['title'], re.I):
            continue
        main, _, rest = v['title'].partition(' | ')
        guests = [g.strip() for g in rest.split(',') if g.strip() and g.strip().lower() not in SELF_NAMES]
        if lang == 'en':
            main = EN_TITLES.get(v['id'], main)
            guests = [EN_GUESTS.get(g, g) for g in guests]
        main = sentence_case(main.strip())
        main = TITLE_FIXES.get(main, main)
        item = dict(v, main=main, guest=', '.join(guests))
        key = item['main'].lower()
        if key in seen:
            if item['guest'] and not out[seen[key]]['guest']:
                out[seen[key]] = item
            continue
        seen[key] = len(out)
        out.append(item)
    return out

ICONS = {
    'play': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>',
    'close': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    'chart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M3 20h18M6 16l4-5 3 3 5-7"/><path d="M15 7h3v3"/></svg>',
    'building': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M4 21V5l8-3 8 3v16M4 21h16M9 9h.01M15 9h.01M9 13h.01M15 13h.01M10 21v-4h4v4"/></svg>',
    'spark': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/></svg>',
    'in': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM10 9.5h3.8v1.6h.06c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.79-1.7-2.79-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/></svg>',
    'yt': '<svg viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.75 15.02V8.98L15.5 12z"/></svg>',
    'rt': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.6" y="2.6" width="18.8" height="18.8" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8.6 17V7.2h4.5a2.8 2.8 0 0 1 0 5.6H8.6M12.5 12.8l3 4.2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="17" cy="7" r="1.4" fill="currentColor"/></svg>',
    'tg': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.9 4.3 18.7 19.4c-.24 1.07-.87 1.33-1.76.83l-4.87-3.59-2.35 2.26c-.26.26-.48.48-.98.48l.35-4.96 9.03-8.16c.39-.35-.09-.54-.61-.2L6.36 13.1l-4.8-1.5c-1.04-.33-1.06-1.04.22-1.54L20.5 2.85c.87-.32 1.63.2 1.4 1.45z"/></svg>',
}

CONTENT = {
    'ru': {
        'lang': 'ru', 'dir': 'annanikulina', 'url': BASE + '/annanikulina/',
        'title': 'Анна Никулина | Независимый директор, Advisory Board, венчурный инвестор',
        'description': 'Анна Никулина: независимый директор, Advisory Board Member, венчурный инвестор. 13+ лет в банках ТОП-10 РФ. Корпоративное управление, риски, финтех, MENA.',
        'keywords': 'Анна Никулина, независимый директор, член совета директоров, совет директоров, Advisory Board, советник по стратегическому развитию, директор по развитию, венчурный инвестор, корпоративное управление, риск-менеджмент, кредитные риски, финтех, краудфандинг, MENA',
        'job_titles': ['Независимый директор', 'Основатель', 'Advisory Board Member', 'Советник по стратегическому развитию', 'Директор по развитию', 'Венчурный инвестор'],
        'knows_about': ['Корпоративное управление', 'Работа совета директоров', 'Независимый директор', 'Риск-менеджмент', 'Кредитные риски', 'Корпоративное кредитование', 'Антикризисное управление', 'Стратегическое развитие бизнеса', 'Венчурные инвестиции', 'Финтех', 'Краудфандинг', 'M&A', 'Due diligence', 'Цифровая трансформация', 'Рынок MENA', 'GR и регулирование'],
        'org_member': 'Ассоциация независимых директоров (АНД)',
        'location': 'Москва',
        'brand': 'А<span>.</span> Никулина',
        'nav': [('#experience', 'Опыт'), ('#services', 'Экспертиза'), ('#videos', 'Видео'), ('#contact', 'Контакты')],
        'vd_source': 'rutube', 'vd_channel_url': RUTUBE, 'vd_eyebrow': 'Видео',
        'vd_title': 'Разговоры о <b>бизнесе</b>', 'vd_intro': 'Интервью с предпринимателями и экспертами на моём канале. Нажмите на выпуск, и он откроется прямо здесь.',
        'vd_more': 'Показать все видео', 'vd_less': 'Свернуть', 'vd_channel': 'Канал на RuTube', 'vd_close': 'Закрыть', 'vd_guest': 'Гость:', 'vd_latest': 'Новый выпуск',
        'eyebrow': 'Независимый&nbsp;директор&nbsp;в&nbsp;СД · Основатель · Венчурный&nbsp;инвестор',
        'h1_1': 'Анна', 'h1_2': 'Никулина',
        'lead': 'Директор по развитию и советник по стратегическому развитию. Помогаю собственникам, инвесторам и стартапам принимать решения, которые выдерживают проверку временем.',
        'cta_main': 'Связаться', 'cta_second': 'Telegram-канал',
        'portrait_alt': 'Анна Никулина',
        'tag_num': '15+', 'tag_text': 'лет в управлении',
        'scroll': 'Листайте',
        'stats': [('15+', 'лет управленческого опыта'), ('50+', 'филиалов банка курировала'),
                  ('₽2&nbsp;трлн', 'активы банка из ТОП-10 РФ'), ('10&nbsp;000+', 'сотрудников в банках, где я работала'),
                  ('$1&nbsp;млрд+', 'оценка техстартапов из портфеля'), ('B2B&nbsp;·&nbsp;B2C', 'запуск бизнесов с нуля')],
        'xp_eyebrow': 'Опыт', 'xp_title': 'Опыт, подтверждённый <b>результатами</b>',
        'xp_intro': '13+ лет в банковском секторе, включая банки ТОП-10 РФ; собственные компании от запуска до экзита; венчурный портфель на глобальных рынках; участие в формировании регулирования финтеха. Смотрю на бизнес одновременно глазами собственника, инвестора и риск-менеджера.',
        'xp': [
            ('Корпоративное управление', ['Член Ассоциации независимых директоров (АНД)', 'Курс «Независимый директор в совете директоров», АНД, 2024', 'Член Advisory Board глобальной ИТ-компании']),
            ('Банковский сектор', ['13+ лет в роли ЛПР в банках Промсвязьбанк, МДМ Банк, УРАЛСИБ, СДМ&#8209;Банк в кредитовании крупного и среднего бизнеса и управлении кредитными рисками', 'Управление процессами при слиянии банков, внедрение кредитного конвейера в рамках цифровой трансформации', 'Курирование и развитие кредитования в 50+ филиалах', 'Создание и управление многомиллиардными корпоративными кредитными портфелями', 'Оценка финансовой устойчивости бизнеса и проектов: от МСБ до крупных промышленных компаний', 'Антикризисное управление']),
            ('Опыт основателя B2B&nbsp;|&nbsp;B2C', ['Основатель финтех-стартапа в России: краудлендинговая платформа, созданная с нуля (продана)', 'Глобальный B2B ИТ-стартап с выручкой, регион MENA: платформа для управления и цифровой трансформации бизнеса. Сооснователь и директор по развитию, сейчас Advisory Board Member', 'Собственный бренд нутрицевтиков: первый в России anti&#8209;age нутрицевтик с клинически значимой концентрацией эластина']),
            ('Венчурные инвестиции', ['Венчурный инвестор в технологические стартапы ранних стадий на глобальных рынках', 'Оценка компаний портфеля: более $1&nbsp;млрд', 'В портфельные компании инвестировали или стали их партнёрами Airbus, NASA, NEOM, Barclays и другие', 'Экзит в аэрокосмической отрасли (Aerospace)', 'Приглашённый эксперт и член жюри конкурсов стартапов']),
            ('Регулирование и GR', ['Взаимодействие с регулятором (Банк&nbsp;России)', 'Участие в разработке Федерального закона № 259-ФЗ «О привлечении инвестиций с использованием инвестиционных платформ» (закон о краудфандинге) со стороны бизнеса, в рамках работы Ассоциации инвестиционных платформ с Банком России']),
            ('Управленческий опыт', ['15+ лет на руководящих позициях, международные команды', 'Риск-ориентированное управление']),
        ],
        'band_eyebrow': 'Советы директоров', 'band_word': 'Advisory Board',
        'band_sub': 'Глубокое понимание рисков и взгляд предпринимателя: от запуска бизнеса, в том числе на глобальных рынках, до экзита. Задаю неудобные вопросы, которые защищают компанию от системных&nbsp;ошибок.',
        'band_horizon': 'Венчурный опыт научил меня <b>смотреть за горизонт</b>: замечаю тренды и риски раньше рынка и помогаю бизнесу быть на&nbsp;шаг&nbsp;впереди.',
        'band_text': 'Что я привношу в <b>совет директоров</b> и&nbsp;<b>Advisory&nbsp;Board</b>',
        'sv_eyebrow': 'Экспертиза', 'sv_title': 'Чем я могу быть <b>полезна</b>',
        'sv_intro': 'Работаю с теми, кому важен взгляд со стороны: независимый, системный и основанный на реальном опыте.',
        'services': [
            ('chart', 'Для инвесторов', ['Анализ инвестиционной привлекательности проектов на всех стадиях', 'Оценка рисков и возможностей']),
            ('building', 'Для собственников бизнеса', ['Стратегический консалтинг и поиск точек роста', 'Операционное управление', 'Работа в советах директоров частных компаний в роли независимого директора']),
            ('spark', 'Для стартапов и бизнеса', ['Экспертное мнение инвестора и менторинг', 'Оценка позиционирования, бизнес-модели и перспектив на любой стадии']),
        ],
        'ct_eyebrow': 'Контакты', 'ct_title': 'Контакты для <b>профессиональных</b> запросов',
        'ct_sub': 'Напишите в LinkedIn или Telegram. Отвечаю лично.',
        'socials_title': 'Мои каналы и соцсети',
        'links': [('in', 'LinkedIn', 'LinkedIn: Anna Nikulina', LINKEDIN), ('tg', 'Telegram', 'Написать в Telegram: @Anna_Niku', TG_PERSONAL),
                  ('tg', 'Telegram-канал', 'Telegram-канал STRATEGY', TG_CHANNEL, 'канал'), ('yt', 'YouTube', 'YouTube-канал STRATEGY', YOUTUBE), ('rt', 'RuTube', 'RuTube-канал', RUTUBE)],
        'footer_left': '© 2026 Анна Никулина', 'footer_right': 'Независимый&nbsp;директор&nbsp;в&nbsp;СД · Основатель · Венчурный&nbsp;инвестор',
    },
    'en': {
        'lang': 'en', 'dir': 'en', 'url': BASE + '/en/',
        'title': 'Anna Nikulina | Non-Executive Director & Venture Investor',
        'description': 'Anna Nikulina: non-executive director, advisory board member, venture investor. 13+ years at top-10 Russian banks. Governance, risk, fintech, MENA.',
        'keywords': 'Anna Nikulina, independent director, non-executive director, NED, INED, board member, board of directors, advisory board, strategic advisor, venture investor, corporate governance, risk management, credit risk, fintech, crowdfunding, MENA',
        'job_titles': ['Non-Executive Director', 'Founder', 'Advisory Board Member', 'Strategic Advisor', 'Chief Business Development Officer', 'Venture Investor'],
        'knows_about': ['Corporate governance', 'Board of directors', 'Non-executive director', 'Risk management', 'Credit risk', 'Corporate lending', 'Crisis management', 'Business strategy', 'Venture capital', 'Fintech', 'Crowdfunding', 'Mergers and acquisitions', 'Due diligence', 'Digital transformation', 'MENA markets', 'Regulatory policy'],
        'org_member': 'Association of Independent Directors (AID), Russia',
        'location': 'Moscow',
        'brand': 'A<span>.</span> Nikulina',
        'nav': [('#experience', 'Track Record'), ('#services', 'Expertise'), ('#videos', 'Videos'), ('#contact', 'Contact')],
        'vd_source': 'youtube', 'vd_channel_url': YOUTUBE, 'vd_eyebrow': 'Videos',
        'vd_title': 'Conversations on <b>business</b>', 'vd_intro': 'Interviews with entrepreneurs and experts on my YouTube channel (mostly in Russian). Click any episode to play it right here.',
        'vd_more': 'Show all videos', 'vd_less': 'Show less', 'vd_channel': 'YouTube channel', 'vd_close': 'Close', 'vd_guest': 'Guest:', 'vd_latest': 'Latest episode',
        'eyebrow': 'Non&#8209;Executive&nbsp;Director · Founder · Venture&nbsp;Investor',
        'h1_1': 'Anna', 'h1_2': 'Nikulina',
        'lead': 'Chief Business Development Officer and Strategic Advisor. I help business owners, investors, and founders make decisions that stand the test of time.',
        'cta_main': 'Get in Touch', 'cta_second': 'Telegram Channel',
        'portrait_alt': 'Anna Nikulina',
        'tag_num': '15+', 'tag_text': 'years in leadership',
        'scroll': 'Scroll',
        'stats': [('15+', 'years of executive leadership'), ('50+', 'bank branches overseen'),
                  ('RUB 2T', 'in assets at a top-10 Russian bank'), ('10,000+', 'employees at the banks I worked for'),
                  ('$1B+', 'valuation of tech startups in my portfolio'), ('B2B&nbsp;·&nbsp;B2C', 'businesses launched from scratch')],
        'xp_eyebrow': 'Track Record', 'xp_title': 'Experience that <b>delivers</b> results',
        'xp_intro': '13+ years in banking, including top-10 Russian banks; companies built from launch to exit; a venture portfolio across global markets; and a hand in shaping Russia&#8217;s fintech regulation. I look at every business through three lenses at once: owner, investor, and risk manager.',
        'xp': [
            ('Corporate Governance', ['Member of the Association of Independent Directors (AID), Russia', 'Independent Board Director program, AID, 2024', 'Advisory Board Member at a global tech company']),
            ('Banking', ['13+ years as a senior decision-maker in large and mid-market corporate lending and credit risk management at Promsvyazbank (PSB), MDM Bank, Uralsib, and SDM Bank', 'Managed key processes during bank mergers; rolled out an automated loan origination pipeline as part of digital transformation', 'Oversaw and grew lending operations across 50+ branches', 'Built and managed multibillion-ruble corporate loan portfolios', 'Financial resilience assessment for businesses and projects, from SMBs to major industrial companies', 'Crisis and turnaround management']),
            ('Founder Experience: B2B&nbsp;|&nbsp;B2C', ['Founder of a Russian fintech startup: a crowdlending platform built from scratch (successfully sold)', 'Revenue-generating global B2B tech startup focused on MENA: a platform for business management and digital transformation. Co&#8209;founder and Chief Business Development Officer, now an Advisory Board Member', 'Own nutraceutical brand: Russia&#8217;s first anti&#8209;aging nutraceutical with a clinically significant concentration of elastin']),
            ('Venture Investing', ['Venture investor in early-stage tech startups across global markets', 'Portfolio companies valued at over $1&nbsp;billion', 'Portfolio companies have attracted investment or partnerships from Airbus, NASA, NEOM, Barclays, and others', 'Exit in the aerospace sector', 'Guest expert and judge at startup pitch competitions']),
            ('Regulatory Policy', ['Engagement with the regulator (Bank&nbsp;of&nbsp;Russia)', 'Helped shape Russia&#8217;s crowdfunding law on behalf of the business community, working with the Association of Investment Platforms and the Bank of Russia']),
            ('Executive Leadership', ['15+ years in senior leadership roles, international teams', 'Risk-based management']),
        ],
        'band_eyebrow': 'Board Service', 'band_word': 'Advisory Board',
        'band_sub': 'A deep understanding of risk and a founder&#8217;s perspective, from launching a business, including in global markets, all the way to exit. I ask the tough questions that protect a company from systemic&nbsp;mistakes.',
        'band_horizon': 'Venture investing has trained me to <b>look beyond the horizon</b>: I spot trends and risks before the market does and help businesses stay one step&nbsp;ahead.',
        'band_text': 'What I bring to the <b>boardroom</b> and <b>advisory&nbsp;boards</b>',
        'sv_eyebrow': 'Expertise', 'sv_title': 'How I can <b>help</b>',
        'sv_intro': 'For those who value an outside perspective: independent, structured, and grounded in real-world experience.',
        'services': [
            ('chart', 'For Investors', ['Investment analysis and due diligence for projects at every stage', 'Risk and opportunity assessment']),
            ('building', 'For Business Owners', ['Strategy consulting and identifying growth levers', 'Operations management', 'Serving as a non-executive director on private company boards']),
            ('spark', 'For Startups &amp; Growing Companies', ['An investor&#8217;s perspective and mentorship', 'Review of positioning, business model, and growth prospects at any stage']),
        ],
        'ct_eyebrow': 'Contact', 'ct_title': 'For <b>professional</b> inquiries',
        'ct_sub': 'Reach out on LinkedIn or Telegram. I reply personally.',
        'socials_title': 'Channels &amp; social media',
        'links': [('in', 'LinkedIn', 'LinkedIn: Anna Nikulina', LINKEDIN), ('tg', 'Telegram', 'Message on Telegram: @Anna_Niku', TG_PERSONAL),
                  ('tg', 'Telegram Channel', 'Telegram channel STRATEGY (in Russian)', TG_CHANNEL, 'channel'), ('yt', 'YouTube', 'YouTube channel STRATEGY (in Russian)', YOUTUBE), ('rt', 'RuTube', 'RuTube channel (in Russian)', RUTUBE)],
        'footer_left': '© 2026 Anna Nikulina', 'footer_right': 'Non&#8209;Executive&nbsp;Director · Founder · Venture&nbsp;Investor',
    },
}


def lis(items):
    return ''.join('<li>%s</li>' % i for i in items)


def json_ld(c, vids):
    other = CONTENT['en' if c['lang'] == 'ru' else 'ru']
    person = {
        '@type': 'Person', '@id': BASE + '/#person',
        'name': c['h1_1'] + ' ' + c['h1_2'],
        'alternateName': [other['h1_1'] + ' ' + other['h1_2']],
        'givenName': c['h1_1'], 'familyName': c['h1_2'],
        'url': c['url'], 'image': BASE + '/assets/img/anna-portrait-home.jpg',
        'description': c['description'],
        'jobTitle': c['job_titles'],
        'knowsAbout': c['knows_about'],
        'knowsLanguage': ['ru', 'en'],
        'memberOf': {'@type': 'Organization', 'name': c['org_member']},
        'homeLocation': {'@type': 'Place', 'name': c['location']},
        'sameAs': [LINKEDIN, TG_CHANNEL, TG_PERSONAL, YOUTUBE, RUTUBE],
    }
    graph = [
        {'@type': 'ProfilePage', '@id': c['url'] + '#page', 'url': c['url'], 'name': c['title'],
         'description': c['description'], 'inLanguage': 'ru-RU' if c['lang'] == 'ru' else 'en-US',
         'dateModified': datetime.date.today().isoformat(),
         'isPartOf': {'@id': BASE + '/#website'}, 'mainEntity': {'@id': BASE + '/#person'},
         'primaryImageOfPage': BASE + '/assets/img/anna-portrait-home.jpg'},
        {'@type': 'WebSite', '@id': BASE + '/#website', 'url': BASE + '/', 'name': c['h1_1'] + ' ' + c['h1_2'],
         'inLanguage': ['ru-RU', 'en-US']},
        person,
    ]
    if vids:
        items = []
        for i, v in enumerate(vids):
            vo = {'@type': 'VideoObject', 'name': v['main'],
                  'description': v['main'] + ('. ' + c['vd_guest'] + ' ' + v['guest'] if v['guest'] else ''),
                  'embedUrl': v['embed'], 'url': v['url']}
            if v.get('thumb') and v['thumb'].startswith('http'):
                vo['thumbnailUrl'] = v['thumb']
            if v.get('date'):
                vo['uploadDate'] = str(v['date'])[:10]
            items.append({'@type': 'ListItem', 'position': i + 1, 'item': vo})
        graph.append({'@type': 'ItemList', 'name': c['vd_eyebrow'], 'itemListElement': items})
    data = {'@context': 'https://schema.org', '@graph': graph}
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def page(c):
    other = 'en' if c['lang'] == 'ru' else 'ru'
    lang_sw = ('<nav class="lang" aria-label="Language">'
               '<a class="glow" href="../annanikulina/" hreflang="ru" lang="ru"%s>RU</a>'
               '<a class="glow" href="../en/" hreflang="en" lang="en"%s>EN</a></nav>') % (
        ' aria-current="page"' if c['lang'] == 'ru' else '',
        ' aria-current="page"' if c['lang'] == 'en' else '')
    stats = ''.join('<li class="reveal d%d"><div class="stat-num">%s</div><div class="stat-label">%s</div></li>' % (i, n, t)
                    for i, (n, t) in enumerate(c['stats']))
    xp = ''.join('<article class="xp-item reveal"><div class="xp-num">%02d</div><h3 class="xp-title">%s</h3><ul class="xp-list">%s</ul></article>'
                 % (i + 1, t, lis(items)) for i, (t, items) in enumerate(c['xp']))
    cards = ''.join('<article class="card reveal d%d"><div class="card-icon">%s</div><h3>%s</h3><ul>%s</ul></article>'
                    % (i + 1, ICONS[ic], t, lis(items)) for i, (ic, t, items) in enumerate(c['services']))
    def a(href, title):
        return '<a class="glow" href="%s" target="_blank" rel="noopener" aria-label="%s" title="%s">' % (href, title, title)
    links = ''.join('<li>%s<span class="social-ico">%s</span><span class="social-label">%s</span></a></li>'
                    % (a(l[3], l[2]), ICONS[l[0]], l[1]) for l in c['links'])
    def icon(l):
        word = l[4] if len(l) > 4 else ''
        if word:
            return '<li class="has-word">%s%s<span>%s</span></a></li>' % (a(l[3], l[2]), ICONS[l[0]], word)
        return '<li>%s%s</a></li>' % (a(l[3], l[2]), ICONS[l[0]])
    icons = ''.join(icon(l) for l in c['links'])
    vids = prepare_videos(VIDEOS.get(c['vd_source']) or [], c['lang'])
    VISIBLE = 7
    vcards = ''.join(
        '<li class="vcard%s%s"><button type="button" class="vcard-btn" data-embed="%s" data-title="%s">'
        '<span class="vcard-thumb">%s<span class="vcard-play">%s</span></span>'
        '<span class="vcard-text">%s<span class="vcard-title">%s</span>%s</span></button></li>' % (
            ' is-featured' if i == 0 else '', ' is-extra' if i >= VISIBLE else '',
            html.escape(v['embed'], quote=True), html.escape(v['main'] + (' · ' + v['guest'] if v['guest'] else ''), quote=True),
            thumb_img(v['thumb_local'] if v.get('thumb_local') and os.path.exists(os.path.join(ROOT, v['thumb_local'][3:])) else v['thumb']) if v.get('thumb') else '',
            ICONS['play'], ('<span class="vcard-badge">%s</span>' % c['vd_latest']) if i == 0 else '', html.escape(v['main']),
            ('<span class="vcard-guest">%s %s</span>' % (c['vd_guest'], html.escape(v['guest']))) if v['guest'] else '')
        for i, v in enumerate(vids))
    more_btn = ('<button type="button" class="btn btn-outline vmore" data-less="%s">%s</button>' % (c['vd_less'], c['vd_more'])) if len(vids) > VISIBLE else ''
    if vids:
        video_section = f'''
  <section class="section videos" id="videos">
    <div class="wrap">
      <div class="section-head">
        <div class="reveal"><div class="eyebrow">{c['vd_eyebrow']}</div><h2 class="h2">{c['vd_title']}</h2></div>
        <p class="reveal d1">{c['vd_intro']}</p>
      </div>
      <ul class="vgrid">{vcards}</ul>
      <div class="vactions">{more_btn}<a class="btn btn-wine" href="{c['vd_channel_url']}" target="_blank" rel="noopener">{c['vd_channel']}{ICONS['arrow']}</a></div>
    </div>
  </section>
  <dialog class="vmodal" aria-label="Video">
    <div class="vmodal-box"><button type="button" class="vmodal-close" aria-label="{c['vd_close']}">{ICONS['close']}</button>
    <div class="vmodal-frame"></div><p class="vmodal-title"></p></div>
  </dialog>'''
    else:
        video_section = ''
    nav_links = ''.join('<a class="glow" href="%s">%s</a>' % l for l in c['nav'] if l[0] != '#videos' or vids)
    desc = html.escape(c['description'], quote=True)
    plain_title = html.escape(c['title'], quote=True)

    return f'''<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{plain_title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{html.escape(c['keywords'], quote=True)}">
<meta name="author" content="{c['h1_1']} {c['h1_2']}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#ecc5c6">
<link rel="canonical" href="{c['url']}">
<link rel="alternate" hreflang="ru" href="{BASE}/annanikulina/">
<link rel="alternate" hreflang="en" href="{BASE}/en/">
<link rel="alternate" hreflang="x-default" href="{BASE}/annanikulina/">
<meta property="og:type" content="profile">
<meta property="og:site_name" content="{c['h1_1']} {c['h1_2']}">
<meta property="profile:first_name" content="{c['h1_1']}">
<meta property="profile:last_name" content="{c['h1_2']}">
<meta property="og:locale:alternate" content="{'en_US' if c['lang'] == 'ru' else 'ru_RU'}">
<meta property="og:image:alt" content="{c['portrait_alt']}">
<link rel="me" href="{LINKEDIN}">
<link rel="me" href="{TG_CHANNEL}">
<link rel="me" href="{YOUTUBE}">
<link rel="me" href="{RUTUBE}">
<link rel="sitemap" type="application/xml" href="{BASE}/sitemap.xml">
<script type="application/ld+json">{json_ld(c, vids)}</script>
<meta property="og:title" content="{plain_title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{c['url']}">
<meta property="og:image" content="{OG_IMG}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'ru_RU' if c['lang'] == 'ru' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{plain_title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{OG_IMG}">
<link rel="icon" href="../assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="../assets/fonts/inter-tight-{'cyrillic' if c['lang'] == 'ru' else 'latin'}-300-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" as="image" href="{PORTRAIT.replace('.jpg', '.webp')}" type="image/webp">
<link rel="stylesheet" href="../assets/site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body>

<header class="nav">
  <div class="wrap">
    <div class="nav-right">
      <nav class="nav-links" aria-label="Sections">{nav_links}</nav>
      {lang_sw}
    </div>
  </div>
</header>

<main id="top">
  <section class="hero">
    <div class="hero-orb" data-speed="0.5" data-x="-0.08" aria-hidden="true"></div>
    <div class="wrap">
      <div class="hero-text" data-speed="0.18" data-fade>
        <div class="eyebrow reveal">{c['eyebrow']}</div>
        <h1 class="reveal d1">{c['h1_1']}<span class="l2">{c['h1_2']}</span></h1>
        <p class="hero-lead reveal d2">{c['lead']}</p>
        <div class="hero-cta reveal d3">
          <a class="btn btn-wine glow" href="#contact">{c['cta_main']}{ICONS['arrow']}</a>
          <ul class="icon-row" aria-label="{c['socials_title']}">{icons}</ul>
        </div>
      </div>
      <div class="photo reveal d2" data-speed="-0.2">
        <picture><source srcset="{PORTRAIT.replace('.jpg', '.webp')}" type="image/webp"><img src="{PORTRAIT}" alt="{c['portrait_alt']}" width="1100" height="1393" fetchpriority="high" decoding="async"></picture>
        <div class="photo-tag"><b>{c['tag_num']}</b>{c['tag_text']}</div>
      </div>
    </div>
  </section>

  <section class="stats" aria-label="Key facts">
    <div class="wrap"><ul>{stats}</ul></div>
  </section>

  <section class="section" id="experience">
    <div class="wrap">
      <div class="section-head">
        <div class="reveal"><div class="eyebrow">{c['xp_eyebrow']}</div><h2 class="h2">{c['xp_title']}</h2></div>
        <p class="reveal d1">{c['xp_intro']}</p>
      </div>
      <div class="xp">{xp}</div>
    </div>
  </section>

  <section class="band on-dark">
    <div class="band-word-wrap" data-speed="0.25" data-x="0.08" aria-hidden="true"><div class="band-word">{c['band_word']}</div></div>
    <div class="wrap">
      <div class="eyebrow reveal">{c['band_eyebrow']}</div>
      <p class="band-text reveal d1">{c['band_text']}</p>
      <p class="band-sub reveal d2">{c['band_sub']}</p>
      <p class="band-horizon reveal d3">{c['band_horizon']}</p>
    </div>
  </section>

  <section class="section services" id="services">
    <div class="wrap">
      <div class="section-head">
        <div class="reveal"><div class="eyebrow">{c['sv_eyebrow']}</div><h2 class="h2">{c['sv_title']}</h2></div>
        <p class="reveal d1">{c['sv_intro']}</p>
      </div>
      <div class="cards">{cards}</div>
    </div>
  </section>

{video_section}
  <section class="section contact on-dark" id="contact">
    <div class="wrap">
      <div class="eyebrow reveal">{c['ct_eyebrow']}</div>
      <h2 class="h2 reveal d1">{c['ct_title']}</h2>
      <p class="sub reveal d2">{c['ct_sub']}</p>
      <ul class="socials reveal d3" aria-label="{c['socials_title']}">{links}</ul>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="wrap"><span>{c['footer_left']}</span><ul class="icon-row icon-row-sm" aria-label="{c['socials_title']}">{icons}</ul><span>{c['footer_right']}</span></div>
</footer>

<script src="../assets/site.js" defer></script>
</body>
</html>
'''


for key, c in CONTENT.items():
    out = os.path.join(ROOT, c['dir'], 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(page(c))
    print('built', out)

today = datetime.date.today().isoformat()
alts = ''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (k, CONTENT[k]['url']) for k in CONTENT) + \
    '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % CONTENT['ru']['url']
urls = ''.join('<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>%s</priority>%s</url>'
               % (CONTENT[k]['url'], today, '1.0' if k == 'ru' else '0.9', alts) for k in CONTENT)
with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">' + urls + '</urlset>\n')

with open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write('# Search engines and AI assistants are welcome to index this site.\n'
            'User-agent: *\nAllow: /\n\n'
            + ''.join('User-agent: %s\nAllow: /\n\n' % b for b in
                      ['Googlebot', 'Yandex', 'Bingbot', 'GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot',
                       'Claude-SearchBot', 'PerplexityBot', 'Google-Extended', 'Applebot-Extended'])
            + 'Sitemap: %s/sitemap.xml\n' % BASE)


def plain(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t)).replace('\xa0', ' ').replace('\u2011', '-')


def llms_section(c):
    out = ['## ' + ('Русская версия' if c['lang'] == 'ru' else 'English version'), '',
           '- Page: ' + c['url'], '- ' + plain(c['eyebrow']), '- ' + plain(c['lead']), '- ' + plain(c['band_sub']), '- ' + plain(c['band_horizon']), '']
    for title, items in c['xp']:
        out.append('### ' + plain(title))
        out += ['- ' + plain(x) for x in items]
        out.append('')
    out.append('### ' + plain(c['sv_title']))
    for _, title, items in c['services']:
        out.append('- ' + plain(title) + ': ' + '; '.join(plain(x) for x in items))
    out.append('')
    vids = prepare_videos(VIDEOS.get(c['vd_source']) or [], c['lang'])
    if vids:
        out.append('### ' + plain(c['vd_title']))
        out += ['- ' + v['main'] + (' (' + c['vd_guest'] + ' ' + v['guest'] + ')' if v['guest'] else '') + ': ' + v['url'] for v in vids]
        out.append('')
    return out


ru, en = CONTENT['ru'], CONTENT['en']
llms = ['# Anna Nikulina / Анна Никулина', '',
        '> ' + plain(en['description']), '> ' + plain(ru['description']), '',
        'Official personal website. Facts below are provided by Anna Nikulina herself.', '',
        '## Contacts and profiles', '',
        '- LinkedIn: ' + LINKEDIN, '- Telegram (personal): ' + TG_PERSONAL, '- Telegram channel STRATEGY (in Russian): ' + TG_CHANNEL,
        '- YouTube channel STRATEGY: ' + YOUTUBE, '- RuTube channel: ' + RUTUBE, '']
llms += llms_section(en) + llms_section(ru)
with open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(llms))
print('built sitemap.xml, robots.txt, llms.txt')
