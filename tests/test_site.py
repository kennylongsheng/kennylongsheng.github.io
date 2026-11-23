"""Source checks for the Jekyll site. Run: python3 -m unittest discover -s tests -v."""
from pathlib import Path
import os
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SiteTests(unittest.TestCase):
    def test_publishable_pdfs_have_only_asset_locations(self):
        outside_assets = []
        excluded = {'.git', '.hermes', '_site', '.sass-cache', '.jekyll-cache', '__pycache__', 'Personal'}
        for folder, directories, filenames in os.walk(ROOT):
            directories[:] = [name for name in directories if name not in excluded]
            for name in filenames:
                if name.lower().endswith('.pdf'):
                    relative = (Path(folder) / name).relative_to(ROOT)
                    if relative.parts[0] != 'assets':
                        outside_assets.append(str(relative))
        self.assertEqual(outside_assets, [], 'Public PDF sources belong under assets/')

    def test_resume_is_the_only_professional_navigation_entry(self):
        config = (ROOT / '_config.yml').read_text()
        header = config.split('header_pages:\n', 1)[1].split('\n\n', 1)[0]
        self.assertEqual(header.splitlines(), [
            '  - resume.markdown', '  - blog.markdown', '  - about.markdown'])

    def test_resume_has_stable_route_and_shared_download(self):
        page = ROOT / 'resume.markdown'
        self.assertTrue(page.is_file(), 'A stable resume download page must exist')
        source = page.read_text()
        self.assertIn('permalink: /resume/', source)
        self.assertIn('{% include resume-downloads.html %}', source)
        config = (ROOT / '_config.yml').read_text()
        download = (ROOT / '_includes/resume-downloads.html').read_text()
        self.assertIn('site.resume_pdf', download)
        self.assertIn('{% include resume-version.html %}', download)
        self.assertIn('  - resume.markdown', config)
        match = re.search(r'^resume_pdf: (.+)$', config, re.M)
        assert match is not None, 'Missing resume_pdf configuration'
        pdf_path = match.group(1).strip()
        self.assertTrue((ROOT / pdf_path.lstrip('/')).read_bytes().startswith(b'%PDF-'))
        self.assertRegex(config, r'(?m)^resume_version: "[^"\n]+"$')
        self.assertIn('site.resume_version', (ROOT / '_includes/resume-version.html').read_text())

    def test_bilingual_page_pairs(self):
        for english, chinese, key in [
            ('index.html', 'zh/index.html', 'home'),
            ('resume.markdown', 'zh/resume.markdown', 'resume'),
            ('about.markdown', 'zh/about.markdown', 'about'),
            ('blog.markdown', 'zh/blog.markdown', 'blog'),
            ('404.html', 'zh/404.html', '404'),
        ]:
            with self.subTest(key=key):
                en = (ROOT / english).read_text()
                zh = (ROOT / chinese).read_text()
                match = re.search(r'^translation_key: (.+)$', en, re.M)
                assert match is not None, 'Missing translation_key: ' + english
                en_key = match.group(1)
                self.assertIn('translation_key: ' + en_key + '\n', zh)
                self.assertIn('lang: en\n', en)
                self.assertIn('lang: zh-Hant\n', zh)
                self.assertIn('permalink: /zh-tw/', zh)
        header = (ROOT / '_includes/header.html').read_text()
        self.assertIn('page.translation_key', header)
        self.assertIn('aria-current="page"', header)
        self.assertIn('本文尚無翻譯', header)
        head = (ROOT / '_includes/head.html').read_text()
        self.assertIn('hreflang=', head)
        self.assertIn('x-default', head)

    def test_home_uses_layout_without_nested_document(self):
        source = (ROOT / 'index.html').read_text()
        self.assertTrue(source.startswith('---\nlayout: page\n'))
        self.assertNotRegex(source.lower(), r'<!doctype|</?(?:html|head|body)\b')
        self.assertIn("'/assets/images/profile-small.jpg' | relative_url", source)
        self.assertIn('engineer', source.lower())


    def test_pages_have_finished_content_and_blog_navigation(self):
        config = (ROOT / '_config.yml').read_text()
        self.assertIn('url: "https://kennylongsheng.github.io"', config)
        self.assertNotIn('(Testing)', config)
        self.assertNotIn('twitter_username: N/A', config)
        self.assertRegex(config, r'header_pages:\n(?:  - .+\n)*  - blog.markdown')
        self.assertRegex(config, r'exclude:\n(?:  - .+\n)*  - tests')
        about = (ROOT / 'about.markdown').read_text()
        self.assertIn('title: Contact\n', about)
        self.assertIn('permalink: /about/\n', about)
        self.assertIn('[LinkedIn](https://www.linkedin.com/in/kennylongsheng/)', about)
        self.assertIn('[GitHub](https://github.com/{{ site.github_username }})', about)
        self.assertIn('[Email](mailto:{{ site.email }})', about)
        self.assertNotIn('base Jekyll theme', about)
        blog = (ROOT / 'blog.markdown').read_text()
        self.assertIn('title: Blog', blog)
        self.assertIn('permalink: /blog/', blog)
        self.assertIn('redirect_from:', blog)
        for name in ['index.html', 'about.markdown', 'blog.markdown', '_config.yml']:
            text = (ROOT / name).read_text()
            self.assertNotRegex(text, r'\[Check\]|Ramdom|(?i:photograph)')


    def test_development_files_are_excluded(self):
        config = (ROOT / '_config.yml').read_text()
        exclusions = config.split('exclude:\n', 1)[1]
        for name in ['memory.md', 'jekyll_livereload.sh']:
            with self.subTest(name=name):
                self.assertIn('  - ' + name, exclusions)

    def test_private_portrait_directory_is_excluded(self):
        exclusions = (ROOT / '_config.yml').read_text().split('exclude:\n', 1)[1]
        self.assertIn('  - Personal\n', exclusions)
        self.assertIn('/Personal/\n', (ROOT / '.gitignore').read_text())

    def test_resume_owns_professional_content_and_legacy_pdf_is_preserved(self):
        page = ROOT / 'resume.markdown'
        self.assertTrue(page.is_file(), 'The Resume page must exist')
        source = page.read_text()
        self.assertIn('permalink: /resume/', source)
        self.assertIn('{% include resume-downloads.html %}', source)
        self.assertIn('## Experience {#experience}', source)
        self.assertIn('## Education {#education-projects}', source)
        self.assertIn("'/resume/' | relative_url", (ROOT / 'index.html').read_text())
        self.assertNotIn('  - cv.markdown', (ROOT / '_config.yml').read_text())
        legacy = (ROOT / 'assets/documents/cv-04-2025.pdf').read_bytes()
        self.assertTrue(legacy.startswith(b'%PDF-'))


if __name__ == '__main__':
    unittest.main()
