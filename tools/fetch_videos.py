"""Fetches the video lists from YouTube and RuTube into data/videos.json.

Runs inside GitHub Actions (the build server can reach both sites).
If a source fails, the previous data for that source is kept, so the site
never loses its video section because of a temporary error.

Usage: python3 tools/fetch_videos.py .
"""
import json, os, subprocess, sys, urllib.request

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = os.path.join(ROOT, 'data', 'videos.json')
YT_URL = 'https://www.youtube.com/@STRATEGYNikulina'
RT_CHANNEL = '30327202'
UA = {'User-Agent': 'Mozilla/5.0 (site video list builder)'}


def log(*a):
    print('[videos]', *a, flush=True)


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))


def ytdlp_flat(url):
    out = subprocess.run(['yt-dlp', '--flat-playlist', '--dump-single-json', '--no-warnings', url],
                         capture_output=True, text=True, timeout=300)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip()[-500:])
    return json.loads(out.stdout).get('entries') or []


def fetch_youtube():
    videos = []
    for tab, short in (('videos', False), ('shorts', True)):
        try:
            entries = ytdlp_flat(YT_URL + '/' + tab)
        except Exception as e:
            log('youtube', tab, 'failed:', e)
            continue
        for e in entries:
            vid = e.get('id')
            if not vid or not e.get('title'):
                continue
            videos.append({'id': vid, 'title': e['title'].strip(), 'short': short,
                           'thumb': 'https://i.ytimg.com/vi/%s/hqdefault.jpg' % vid,
                           'embed': 'https://www.youtube-nocookie.com/embed/%s' % vid,
                           'url': 'https://www.youtube.com/watch?v=%s' % vid})
        log('youtube', tab, len(entries), 'entries')
    return videos


def fetch_rutube():
    videos, page = [], 1
    try:
        while page <= 20:
            data = get_json('https://rutube.ru/api/video/person/%s/?page=%d' % (RT_CHANNEL, page))
            for v in data.get('results', []):
                vid = v.get('id')
                if not vid or not v.get('title'):
                    continue
                videos.append({'id': vid, 'title': v['title'].strip(), 'short': False,
                               'thumb': v.get('thumbnail_url') or '',
                               'embed': v.get('embed_url') or 'https://rutube.ru/play/embed/%s' % vid,
                               'url': v.get('video_url') or 'https://rutube.ru/video/%s/' % vid,
                               'date': v.get('publication_ts') or v.get('created_ts') or ''})
            if not data.get('has_next'):
                break
            page += 1
        log('rutube api', len(videos), 'videos')
        return videos
    except Exception as e:
        log('rutube api failed:', e)
    try:
        entries = ytdlp_flat('https://rutube.ru/channel/%s/videos/' % RT_CHANNEL)
        for e in entries:
            vid = e.get('id')
            if vid and e.get('title'):
                videos.append({'id': vid, 'title': e['title'].strip(), 'short': False,
                               'thumb': e.get('thumbnail') or '',
                               'embed': 'https://rutube.ru/play/embed/%s' % vid,
                               'url': 'https://rutube.ru/video/%s/' % vid})
        log('rutube yt-dlp', len(videos), 'videos')
    except Exception as e:
        log('rutube yt-dlp failed:', e)
    return videos


def main():
    old = {'youtube': [], 'rutube': []}
    if os.path.exists(OUT):
        with open(OUT, encoding='utf-8') as f:
            old.update(json.load(f))
    new = {'youtube': fetch_youtube(), 'rutube': fetch_rutube()}
    for k in new:
        if not new[k]:
            log(k, 'empty, keeping previous', len(old[k]))
            new[k] = old[k]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(new, f, ensure_ascii=False, indent=1)
    for k, v in new.items():
        log(k, 'total', len(v), 'with thumbnails:', sum(1 for x in v if x.get('thumb')))
        for x in v:
            log('  -', x['id'], '|', x['title'])


main()
