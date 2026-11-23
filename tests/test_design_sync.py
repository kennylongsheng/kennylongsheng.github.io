"""Semantic bilingual design contracts shared with rendered-build verification."""
from pathlib import Path
import re
import unittest

from verify_build import (Page, PROJECT_ROUTE, RETIRED_POST_SLUGS, check_home_design,
                          check_role_rows, config_value, document_version, is_retired_post)

ROOT = Path(__file__).resolve().parents[1]


def source_page(text):
    """Resolve only known Liquid values for source HTML assertions, not a build."""
    config = (ROOT / '_config.yml').read_text()
    text = re.sub(r"{{\s*'([^']+)'\s*\|\s*relative_url\s*}}", r'\1', text)
    for key in ('email', 'github_username'):
        text = re.sub(r'{{\s*site\.' + key + r'(?:\s*\|\s*escape)?\s*}}',
                      config_value(config, key), text)
    text = text.replace('{% include resume-version.html %}',
                        document_version(config, 'lang: zh-Hant' in text))
    return Page(text)


class DesignSyncTests(unittest.TestCase):
    def check_home(self, text, chinese=False):
        config = (ROOT / '_config.yml').read_text()
        contacts = ['mailto:' + config_value(config, 'email'),
                    'https://www.linkedin.com/in/kennylongsheng/',
                    'https://github.com/' + config_value(config, 'github_username')]
        check_home_design(source_page(text), '/zh-tw/resume/' if chinese else '/resume/',
                          PROJECT_ROUTE, contacts, chinese,
                          version=document_version(config, chinese))

    def test_homepage_design_is_synchronized_semantically(self):
        for name, chinese in [('index.html', False), ('zh/index.html', True)]:
            with self.subTest(name=name):
                self.check_home((ROOT / name).read_text(), chinese)

    def test_resume_role_rows_preserve_localized_career_dates(self):
        for name, chinese, heading in [('resume.markdown', False, 'Education'),
                                       ('zh/resume.markdown', True, '學歷')]:
            with self.subTest(name=name):
                text = (ROOT / name).read_text()
                check_role_rows(source_page(text), chinese)
                self.assertRegex(text, r'(?m)^## ' + heading + r' \{#education-projects\}$')
                self.assertIn("'" + PROJECT_ROUTE + "' | relative_url", text)

    def test_contact_pages_keep_direct_localized_destinations(self):
        for name, label in [('about.markdown', 'Email'), ('zh/about.markdown', '電子郵件')]:
            with self.subTest(name=name):
                text = (ROOT / name).read_text()
                self.assertIn('[' + label + '](mailto:{{ site.email }})', text)
                self.assertIn('[LinkedIn](https://www.linkedin.com/in/kennylongsheng/)', text)
                self.assertIn('[GitHub](https://github.com/{{ site.github_username }})', text)

    def test_project_remains_english_wip_without_invented_translation(self):
        posts = [p for p in (ROOT / '_posts').rglob('*') if p.is_file()]
        project = [p for p in posts if re.search(r'(?m)^permalink: ' + re.escape(PROJECT_ROUTE) + '$', p.read_text())]
        self.assertEqual(len(project), 1, 'The stable project permalink must have one owner')
        text = project[0].read_text()
        metadata, body = text.split('---', 2)[1:]
        self.assertRegex(metadata, r'(?m)^lang: en$')
        self.assertNotIn('translation_key:', metadata)
        visible = re.sub(r'<!--.*?-->', '', body, flags=re.S)
        self.assertIn('Work in progress', visible)
        self.assertIn('teammate', visible)
        for page in list((ROOT / 'zh').rglob('*.markdown')) + posts:
            metadata = page.read_text().split('---', 2)[1]
            self.assertNotIn('permalink: /zh-tw' + PROJECT_ROUTE, metadata)
        for name in ('resume.markdown', 'zh/resume.markdown', 'index.html', 'zh/index.html'):
            self.assertIn("'" + PROJECT_ROUTE + "' | relative_url", (ROOT / name).read_text())

    def test_retired_starter_posts_are_absent_from_public_sources(self):
        for old in ('_posts/1996-04-12-Birth.markdown',
                    '/blogpost/2022/08/29/welcome-to-jekyll.html',
                    '/verification/blog/welcome-to-jekyll/index.html'):
            self.assertTrue(is_retired_post(old), old)
        self.assertFalse(is_retired_post('/blog/birthday-notes/'))
        self.assertFalse(is_retired_post(PROJECT_ROUTE))
        for path in (ROOT / '_posts').rglob('*'):
            if path.is_file():
                self.assertFalse(is_retired_post(path.name), path)
        for name in ('blog.markdown', 'zh/blog.markdown', 'index.html', 'zh/index.html'):
            text = (ROOT / name).read_text().lower()
            for slug in RETIRED_POST_SLUGS:
                self.assertNotIn(slug, text, name)

    def test_error_pages_share_body_size_and_emphasis(self):
        css = (ROOT / 'assets/main.scss').read_text()
        body = re.search(r'(?m)^\.post-content,\s*\.home,\s*\.error-page\s*\{([^}]+)\}', css)
        emphasis = re.search(r'(?m)^\.post-content strong,\s*\.home strong,\s*\.error-page strong\s*\{([^}]+)\}', css)
        self.assertIsNotNone(body, 'Error-page body must share the content typography rule')
        self.assertIsNotNone(emphasis, 'Error-page emphasis must share the content weight rule')
        assert body is not None and emphasis is not None
        self.assertRegex(body.group(1), r'font-size:\s*16px\s*;')
        self.assertRegex(emphasis.group(1), r'font-weight:\s*600\s*;')

    def test_home_contract_rejects_detached_metadata_and_contact_detours(self):
        text = (ROOT / 'index.html').read_text()
        self.check_home(text)
        page = source_page(text)
        contacts = [a.attrs['href'] for a in page.root.find('nav', 'profile-contact-links')[0].find('a')]
        note = page.root.find('p', 'resume-version')[0]
        note.parent.content.remove(note)
        note.parent = page.root
        page.root.content.append(note)
        with self.assertRaises(AssertionError):
            check_home_design(page, '/resume/', PROJECT_ROUTE, contacts)
        for old, new in [('mailto:{{ site.email | escape }}', '/about/'),
                         ('/resume/#documents', '/assets/documents/incorrect.pdf'),
                         ('Nov 2024–Aug 2026', 'Nov 2024–Aug 2025'),
                         ('Git, and per-channel oscilloscope analysis.', 'per-channel oscilloscope analysis, and Git.')]:
            with self.subTest(regression=new):
                self.assertIn(old, text)
                with self.assertRaises(AssertionError):
                    self.check_home(text.replace(old, new))


if __name__ == '__main__':
    unittest.main()
