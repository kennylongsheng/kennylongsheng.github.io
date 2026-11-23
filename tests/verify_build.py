"""Check rendered Jekyll output: python3 tests/verify_build.py OUTPUT [BASEURL]."""
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import sys
import re
import xml.etree.ElementTree as ET


PROJECT_ROUTE = '/blog/rubiks-cube-solving-guides-with-ar/'
RETIRED_POST_SLUGS = ('welcome-to-jekyll', 'birth')
VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
             'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Element:
    """Small HTML tree for ancestry-aware assertions, not markup snapshots."""
    def __init__(self, tag, attrs=(), parent=None):
        self.tag = tag
        self.attrs = dict(attrs)
        self.parent = parent
        self.content = []

    @property
    def text(self):
        return ''.join(item.text if isinstance(item, Element) else item
                       for item in self.content)

    def find(self, tag=None, class_name=None):
        found = []
        for item in self.content:
            if not isinstance(item, Element):
                continue
            if (tag is None or item.tag == tag) and (
                    class_name is None or class_name in item.attrs.get('class', '').split()):
                found.append(item)
            found.extend(item.find(tag, class_name))
        return found


def is_retired_post(value):
    path = unquote(urlsplit(str(value)).path).lower().rstrip('/')
    if path.endswith('/index.html'):
        path = path[:-11]
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', Path(path).stem)
    return slug in RETIRED_POST_SLUGS


def one(elements, message):
    assert len(elements) == 1, (message, len(elements))
    return elements[0]


def check_role_rows(page, chinese=False):
    rows = page.root.find('p', 'experience-role')
    expected = [('資深韌體工程師', ('2024 年 11 月', '2026 年 8 月')),
                ('韌體工程師', ('2021 年 3 月', '2024 年 10 月'))] if chinese else [
                    ('Senior Firmware Engineer', ('Nov 2024', 'Aug 2026')),
                    ('Firmware Engineer', ('Mar 2021', 'Oct 2024'))]
    assert len(rows) == len(expected), 'Two distinct career role rows are required'
    for row, (title, dates) in zip(rows, expected):
        strong = one(row.find('strong'), 'Role title')
        date = one(row.find('span', 'experience-dates'), 'Role dates')
        assert strong.parent is row and date.parent is row, 'Role and dates must share a row'
        assert strong.text.strip() == title, (strong.text, title)
        assert all(value in date.text for value in dates), (date.text, dates)
        assert date.text.index(dates[0]) < date.text.index(dates[1]), date.text


def check_home_design(page, resume_route, project_route, contacts, chinese=False, version=None):
    actions = one(page.root.find('nav', 'profile-actions'), 'Resume action navigation')
    links = actions.find('a')
    labels = ['查看履歷', '其他履歷與完整 CV'] if chinese else ['View Resume', 'Other Resumes & Full CV']
    assert [(a.text.strip(), a.attrs.get('href')) for a in links] == list(zip(
        labels, [resume_route, resume_route + '#documents'])), 'Two localized Resume actions'
    note = one(actions.find('p', 'resume-version'), 'Inline document metadata')
    assert note.parent is actions, 'Document metadata must be directly inside the action row'
    assert len(page.root.find('p', 'resume-version')) == 1, 'No detached metadata copy'
    assert ('英文 PDF' if chinese else 'English PDFs') in note.text, note.text
    if version:
        assert version in note.text, 'Document version must remain visible in the action row'
    assert not any(urlsplit(link).path.lower().endswith('.pdf') for link in page.links), 'No direct homepage PDF'
    check_role_rows(page, chinese)
    skills = one(page.root.find('dl', 'profile-skills'), 'Technical focus')
    assert [item.text.strip() for item in skills.find('dt')] == (
        ['韌體', 'DRAM', '除錯'] if chinese else ['Firmware', 'DRAM', 'Debugging'])
    descriptions = skills.find('dd')
    assert len(descriptions) == 3, 'Three skill descriptions'
    for label in ('DDR4', 'LPDDR4', 'LPDDR5', 'delay/Vref'):
        assert label in descriptions[1].text, label
    debugging = descriptions[2].text.strip()
    assert all(tool in debugging for tool in ('Eclipse', 'UART', 'Python', 'Git')), debugging
    assert re.search(r'示波器[^、，；。]*[。.]?\s*$' if chinese else
                     r'per-channel oscilloscope analysis[.]?\s*$', debugging), debugging
    degree = one(page.root.find('p', 'education-degree'), 'Degree and dates')
    assert '2016' in degree.text and '2021' in degree.text, degree.text
    project = one(page.root.find('p', 'education-project'), 'Final-year project')
    link = one(project.find('a'), 'Project title link')
    assert link.attrs.get('href') == project_route and link.text.strip(), 'Stable English project URL'
    if chinese:
        assert '英文' in project.text, 'Chinese project reference must identify the English article'
    heading = one([node for node in page.root.find('h2')
                   if node.attrs.get('id') == 'background-heading'], 'Education heading')
    assert heading.text.strip() == ('學歷' if chinese else 'Education'), heading.text
    closing = one(page.root.find('section', 'profile-closing'), 'Closing section')
    contact_nav = one(closing.find('nav', 'profile-contact-links'), 'Direct contact navigation')
    expected_labels = ['電子郵件', 'LinkedIn', 'GitHub'] if chinese else ['Email', 'LinkedIn', 'GitHub']
    assert [(a.text.strip(), a.attrs.get('href')) for a in contact_nav.find('a')] == list(zip(
        expected_labels, contacts)), 'Closing links must go directly to contact destinations'
    assert closing.find('a') == contact_nav.find('a'), 'No extra Blog/Contact detours'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.root = Element('document')
        self.stack = [self.root]
        self.ids = []
        self.links = []
        self.alternates = {}
        self.lang = None
        self.documents = 0
        self.canonical = None
        self.primary_links = []
        self.in_primary_nav = False
        self.action_links = []
        self.in_action_nav = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Element(tag, attrs, self.stack[-1])
        self.stack[-1].content.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)
        a = dict(attrs)
        if tag == 'nav' and 'site-nav' in (a.get('class') or '').split():
            self.in_primary_nav = True
        if tag == 'nav' and 'profile-actions' in (a.get('class') or '').split():
            self.in_action_nav = True
        if tag == 'a' and self.in_primary_nav:
            self.primary_links.append(a.get('href'))
        if tag == 'a' and self.in_action_nav:
            self.action_links.append(a.get('href'))
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href')
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

    def handle_data(self, data):
        self.stack[-1].content.append(data)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break
        if tag == 'nav':
            self.in_primary_nav = False
            self.in_action_nav = False


def config_value(config, key):
    match = re.search(r'^' + re.escape(key) + r': (.+)$', config, re.M)
    assert match is not None, 'Missing configuration: ' + key
    return match.group(1).strip().strip('\"\'')


def document_version(config, chinese=False):
    value = config_value(config, 'resume_version')
    if not chinese:
        return value
    date = datetime.strptime(value, '%B %Y')
    return f'{date.year} 年 {date.month} 月'


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
            if target.lower().endswith('.pdf'):
                assert target.startswith('/assets/'), (path, link, 'PDF links must target assets/')
            destination = output / target.lstrip('/')
            if destination.is_dir():
                destination /= 'index.html'
            assert destination.is_file(), (path, link, destination)
            if url.fragment and destination in pages:
                assert unquote(url.fragment) in pages[destination].ids, (path, link)
    for route in ('', 'resume/', 'about/', 'blog/', '404.html'):
        relative = route if route.endswith('.html') else route + 'index.html'
        en = pages[output / relative]
        zh = pages[output / 'zh-tw' / relative]
        assert en.lang == 'en' and zh.lang == 'zh-Hant', route
        for page in (en, zh):
            assert page.alternates['en'].endswith(baseurl + '/' + route), route
            assert page.alternates['zh-Hant'].endswith(baseurl + '/zh-tw/' + route), route
            assert page.alternates['x-default'] == page.alternates['en'], route
            expected_canonical = page.alternates['zh-Hant' if page.lang == 'zh-Hant' else 'en']
            assert page.canonical == expected_canonical, route
            assert baseurl + '/' + route in page.links, route
            assert baseurl + '/zh-tw/' + route in page.links, route
        for page, prefix in [(en, '/'), (zh, '/zh-tw/')]:
            assert page.primary_links == [baseurl + prefix + name + '/' for name in ('resume', 'blog', 'about')], (route, page.primary_links)
    for prefix, lang in [('', 'en'), ('zh-tw/', 'zh-Hant')]:
        alias = pages[output / prefix / 'cv/index.html']
        target = baseurl + '/' + prefix + 'resume/'
        assert alias.lang == lang and not alias.alternates, prefix
        assert alias.canonical == 'https://kennylongsheng.github.io' + target, prefix
        assert target in alias.links, prefix
        assert 'window.location.hash' in (output / prefix / 'cv/index.html').read_text(), prefix
    for path in output.rglob('*'):
        assert not set(path.relative_to(output).parts) & {'Personal', '.hermes', 'tests', '.git'}, path
        assert path.name not in ('memory.md', 'README.md', 'jekyll_livereload.sh'), path
    source = Path(__file__).resolve().parents[1]
    for pdf in output.rglob('*'):
        if pdf.is_file() and pdf.suffix.lower() == '.pdf':
            relative = pdf.relative_to(output)
            assert relative.parts[0] == 'assets', relative
            assert pdf.read_bytes() == (source / relative).read_bytes(), relative
    assert not (output / 'CV_version').exists(), 'Retired document directory must not be published'
    config = (source / '_config.yml').read_text()
    document_paths = []
    for key in ('resume_pdf', 'resume_validation_pdf', 'cv_pdf'):
        match = re.search(r'^' + key + r': (.+)$', config, re.M)
        assert match is not None, 'Missing document configuration: ' + key
        document_path = match.group(1).strip().lstrip('/')
        document_paths.append('/' + document_path)
        assert (output / document_path).read_bytes() == (source / document_path).read_bytes(), document_path
        assert (output / document_path).read_bytes().startswith(b'%PDF-'), document_path
    for prefix, labels in [('', ('Firmware resume', 'Validation resume', 'Full CV', 'English PDFs')),
                           ('zh-tw/', ('韌體履歷', '驗證履歷', '完整 CV', '英文 PDF'))]:
        resume = pages[output / prefix / 'resume/index.html']
        text = (output / prefix / 'resume/index.html').read_text()
        for document_path in document_paths:
            assert baseurl + document_path in resume.links, (prefix, document_path)
        for label in labels:
            assert label in text, (prefix, label)
        for anchor in ('documents', 'experience', 'technical-background', 'education-projects', 'activities', 'languages', 'contact'):
            assert anchor in resume.ids, (prefix, anchor)
        homepage = pages[output / prefix / 'index.html']
        resume_route = baseurl + '/' + prefix + 'resume/'
        assert homepage.action_links == [resume_route, resume_route + '#documents'], prefix
        contacts = ['mailto:' + config_value(config, 'email'),
                    'https://www.linkedin.com/in/kennylongsheng/',
                    'https://github.com/' + config_value(config, 'github_username')]
        check_home_design(homepage, resume_route, baseurl + PROJECT_ROUTE, contacts,
                          chinese=bool(prefix), version=document_version(config, bool(prefix)))
        check_role_rows(resume, chinese=bool(prefix))
        education = one([node for node in resume.root.find('h2')
                         if node.attrs.get('id') == 'education-projects'], 'Resume Education anchor')
        assert education.text.strip() == ('學歷' if prefix else 'Education'), prefix
        assert baseurl + PROJECT_ROUTE in resume.links, prefix
        assert ('DDR5 僅限規範研讀' if prefix else 'DDR5 specification study only') in text, prefix
        assert not any(baseurl + path in homepage.links for path in document_paths), prefix
    project = pages[output / PROJECT_ROUTE.strip('/') / 'index.html']
    assert project.lang == 'en' and not project.alternates, 'No fabricated project translation'
    assert project.canonical == 'https://kennylongsheng.github.io' + baseurl + PROJECT_ROUTE
    assert 'Work in progress' in project.root.text, 'Unfinished article must remain labeled'
    assert not (output / 'zh-tw' / PROJECT_ROUTE.strip('/')).exists()
    language_nav = one(project.root.find('nav', 'language-switch'), 'Project language switch')
    fallback = one([link for link in language_nav.find('a')
                    if link.attrs.get('lang') == 'zh-Hant'], 'Untranslated project fallback')
    assert fallback.attrs.get('href') == baseurl + '/zh-tw/blog/'
    assert '本文尚無翻譯' in fallback.attrs.get('aria-label', ''), 'No false translation promise'
    for prefix in ('', 'zh-tw/'):
        blog = pages[output / prefix / 'blog/index.html']
        assert baseurl + PROJECT_ROUTE in blog.links, prefix
    for path, page in pages.items():
        assert not is_retired_post(path.relative_to(output).as_posix()), path
        assert not any(is_retired_post(link) for link in page.links), path
    feed = ET.parse(output / 'feed.xml')
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    feed_links = [link.attrib.get('href', '') for link in feed.findall('.//atom:entry/atom:link', ns)]
    assert any(link.endswith(baseurl + PROJECT_ROUTE) for link in feed_links), 'Project missing from RSS'
    assert not any(is_retired_post(link) for link in feed_links)
    for path, page in pages.items():
        if 'blogpost' in path.parts:
            assert not page.alternates, path
    print(f'PASS: {len(pages)} HTML pages, five language pairs, CV aliases, three-link navigation, links/fragments, inline bilingual metadata/design, direct contacts, English-only WIP project, retired posts, RSS, three configured PDF downloads, asset-only PDF sources/links, privacy exclusions; baseurl={baseurl!r}')


if __name__ == '__main__':
    verify(Path(sys.argv[1]).resolve(), sys.argv[2] if len(sys.argv) > 2 else '')
