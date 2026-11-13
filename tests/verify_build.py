"""Check rendered Jekyll output: python3 tests/verify_build.py OUTPUT [BASEURL]."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import sys
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.links = []
        self.alternates = {}
        self.lang = None
        self.documents = 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.documents += 1
            self.lang = a.get('lang')
        if 'id' in a:
            self.ids.append(a['id'])
        for key in ('href', 'src'):
            if key in a:
                self.links.append(a[key])
        if tag == 'link' and 'hreflang' in a:
            self.alternates[a['hreflang']] = a['href']


def verify(output, baseurl=''):
    pages = {p: Page(p.read_text()) for p in output.rglob('*.html')}
    for path, page in pages.items():
        assert page.documents == 1, path
        assert len(page.ids) == len(set(page.ids)), path
        route = '/' + path.relative_to(output).as_posix()
        if route.endswith('/index.html'):
            route = route[:-10]
        current = baseurl + route
        for link in page.links:
            url = urlsplit(urljoin('https://kennylongsheng.github.io' + current, link))
            if url.scheme not in ('http', 'https') or url.netloc != 'kennylongsheng.github.io':
                continue
            target = unquote(url.path)
            if baseurl:
                assert target == baseurl or target.startswith(baseurl + '/'), (path, link)
                target = target[len(baseurl):]
            destination = output / target.lstrip('/')
            if destination.is_dir():
                destination /= 'index.html'
            assert destination.is_file(), (path, link, destination)
            if url.fragment and destination in pages:
                assert unquote(url.fragment) in pages[destination].ids, (path, link)
    for route in ('', 'cv/', 'resume/', 'about/', 'blog/', '404.html'):
        relative = route if route.endswith('.html') else route + 'index.html'
        en = pages[output / relative]
        zh = pages[output / 'zh-tw' / relative]
        assert en.lang == 'en' and zh.lang == 'zh-Hant', route
        for page in (en, zh):
            assert page.alternates['en'].endswith(baseurl + '/' + route), route
            assert page.alternates['zh-Hant'].endswith(baseurl + '/zh-tw/' + route), route
            assert page.alternates['x-default'] == page.alternates['en'], route
            assert baseurl + '/' + route in page.links, route
            assert baseurl + '/zh-tw/' + route in page.links, route
    for path in output.rglob('*'):
        assert not set(path.relative_to(output).parts) & {'Personal', '.hermes', 'tests', '.git'}, path
        assert path.name not in ('memory.md', 'README.md', 'jekyll_livereload.sh'), path
    pdf = output / 'assets/documents/cv-04-2025.pdf'
    assert pdf.read_bytes() == (output / 'CV_version/04_2025.pdf').read_bytes()
    ET.parse(output / 'feed.xml')
    for path, page in pages.items():
        if 'blogpost' in path.parts:
            assert not page.alternates, path
    print(f'PASS: {len(pages)} HTML pages, six language pairs, links/fragments, metadata, RSS, PDF compatibility and privacy exclusions; baseurl={baseurl!r}')


if __name__ == '__main__':
    verify(Path(sys.argv[1]).resolve(), sys.argv[2] if len(sys.argv) > 2 else '')
