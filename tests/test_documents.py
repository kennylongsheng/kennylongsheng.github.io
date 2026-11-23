"""Current document choices, localization and latest supplied CV capabilities."""
from pathlib import Path
import re
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentTests(unittest.TestCase):
    def test_homepage_has_two_resume_actions_with_document_metadata(self):
        for name, labels, route in [
            ('index.html', ['View Resume', 'Other Resumes &amp; Full CV'], '/resume/'),
            ('zh/index.html', ['查看履歷', '其他履歷與完整 CV'], '/zh-tw/resume/'),
        ]:
            with self.subTest(name=name):
                source = re.sub(r'<!--.*?-->', '', (ROOT / name).read_text(), flags=re.S)
                match = re.search(r'<nav class="profile-actions"[^>]*>(.*?)</nav>', source, re.S)
                self.assertIsNotNone(match)
                assert match is not None
                actions = match.group(1)
                self.assertEqual(len(re.findall(r'<a\b', actions)), 2)
                for label in labels:
                    self.assertIn('>' + label + '</a>', actions)
                self.assertIn("'" + route + "' | relative_url", actions)
                self.assertIn("'" + route + "#documents' | relative_url", actions)
                self.assertNotIn('site.resume_pdf', source)
                self.assertIn('resume-version.html', source)
                self.assertIn('class="resume-version"', actions)
                self.assertIn('resume-version.html', actions)
                self.assertIn('English PDFs' if name == 'index.html' else '英文 PDF', actions)

    def test_shared_inline_document_note_clears_block_margins(self):
        css = (ROOT / 'assets/main.scss').read_text()
        match = re.search(r'(?m)^\.profile-actions\s*>\s*\.resume-version\s*\{([^}]+)\}', css)
        self.assertIsNotNone(match, 'Inline metadata needs a shared spacing rule for both languages')
        assert match is not None
        self.assertRegex(match.group(1), r'\bmargin:\s*0\s*;')

    def test_three_distinct_configured_pdfs_exist_without_duplicate_copies(self):
        config = (ROOT / '_config.yml').read_text()
        paths = []
        hashes = []
        for key in ['resume_pdf', 'resume_validation_pdf', 'cv_pdf']:
            match = re.search(r'^' + key + r': (.+)$', config, re.M)
            self.assertIsNotNone(match, key)
            assert match is not None
            path = match.group(1).strip()
            self.assertTrue(path.startswith('/assets/documents/'), path)
            pdf = ROOT / path.lstrip('/')
            self.assertTrue(pdf.is_file(), path)
            self.assertTrue(pdf.read_bytes().startswith(b'%PDF-'), path)
            hashes.append(hashlib.sha256(pdf.read_bytes()).hexdigest())
            paths.append(path)
        self.assertEqual(len(set(paths)), 3)
        self.assertEqual(len(set(hashes)), 3, 'Document choices must not be duplicate copies')
        self.assertIn('firmware', paths[0])
        self.assertIn('validation', paths[1])

    def test_shared_download_section_is_used_in_both_languages(self):
        include = ROOT / '_includes/resume-downloads.html'
        self.assertTrue(include.is_file())
        text = include.read_text()
        for key in ['site.resume_pdf', 'site.resume_validation_pdf', 'site.cv_pdf']:
            self.assertIn(key, text)
        for label in ['Firmware resume', 'Validation resume', 'Full CV',
                      '韌體履歷', '驗證履歷', '完整 CV', 'English PDFs', '英文 PDF']:
            self.assertIn(label, text)
        self.assertIn('resume-version.html', text)
        self.assertIn('id="documents"', text)
        for name in ['resume.markdown', 'zh/resume.markdown']:
            source = (ROOT / name).read_text()
            self.assertIn('{% include resume-downloads.html %}', source)
            for anchor in ['experience', 'technical-background', 'education-projects',
                           'activities', 'languages', 'contact']:
                self.assertIn('{#' + anchor + '}', source)

    def test_latest_cv_capabilities_are_reflected_without_ddr5_ownership(self):
        en = (ROOT / 'resume.markdown').read_text()
        zh = (ROOT / 'zh/resume.markdown').read_text()
        self.assertIn('per-channel oscilloscope waveform analysis', en)
        self.assertIn('DDR5 specification study only', en)
        self.assertIn('示波器', zh)
        self.assertIn('DDR5', zh)
        self.assertIn('DDR5 僅限規範研讀', zh)
        for name, route in [('index.html', '/resume/#documents'),
                            ('zh/index.html', '/zh-tw/resume/#documents')]:
            self.assertIn("'" + route + "' | relative_url", (ROOT / name).read_text())


if __name__ == '__main__':
    unittest.main()
