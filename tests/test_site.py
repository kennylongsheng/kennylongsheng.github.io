"""Source checks for the Jekyll site. Run: python3 -m unittest discover -s tests -v."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SiteTests(unittest.TestCase):
    def test_home_uses_layout_without_nested_document(self):
        source = (ROOT / 'index.html').read_text()
        self.assertTrue(source.startswith('---\nlayout: page\n'))
        self.assertNotRegex(source.lower(), r'<!doctype|</?(?:html|head|body)\b')
        self.assertIn("'/blog/' | relative_url", source)
        self.assertIn("'/about/' | relative_url", source)
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

    def test_cv_page_links_to_dated_pdf_and_is_in_navigation(self):
        page = ROOT / 'cv.markdown'
        self.assertTrue(page.is_file(), 'The CV page must exist')
        source = page.read_text()
        self.assertIn('permalink: /cv/', source)
        self.assertIn("'/assets/documents/cv-04-2025.pdf' | relative_url", source)
        self.assertIn("'/cv/' | relative_url", (ROOT / 'index.html').read_text())
        self.assertIn('  - cv.markdown', (ROOT / '_config.yml').read_text())
        legacy = (ROOT / 'CV_version/04_2025.pdf').read_bytes()
        self.assertTrue(legacy.startswith(b'%PDF-'))
        self.assertEqual((ROOT / 'assets/documents/cv-04-2025.pdf').read_bytes(), legacy)


if __name__ == '__main__':
    unittest.main()
