"""2026 job-focused content and compatibility contracts."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class JobFocusedTests(unittest.TestCase):
    def test_english_resume_matches_2026_career_and_document(self):
        text = (ROOT / 'resume.markdown').read_text() + (ROOT / '_includes/resume-downloads.html').read_text()
        for value in ['Senior Firmware Engineer', 'Nov 2024', 'Aug 2026',
                      'Mar 2021', 'Oct 2024', 'DDR4', 'LPDDR4', 'LPDDR5',
                      'delay/Vref', 'Python', 'ICE', 'English PDFs']:
            with self.subTest(value=value):
                self.assertIn(value, text)
        for anchor in ['experience', 'technical-background', 'education-projects',
                       'activities', 'languages', 'contact']:
            self.assertIn('{#' + anchor + '}', text)
        self.assertNotIn('IC Verification Engineer', text)
        self.assertNotIn('Includes English and Chinese', text)

    def test_homepages_use_current_specialization_and_resume_links(self):
        for name, route, unwanted in [('index.html', '/resume/', 'IC Verification Engineer'),
                                      ('zh/index.html', '/zh-tw/resume/', 'IC 驗證工程師')]:
            with self.subTest(name=name):
                text = (ROOT / name).read_text()
                self.assertIn("'" + route + "' | relative_url", text)
                self.assertNotIn('/cv/', text)
                self.assertNotIn(unwanted, text)
                self.assertIn('2026', text)
                self.assertIn('LPDDR5', text)

    def test_chinese_resume_is_a_profile_not_a_second_download_landing(self):
        text = (ROOT / 'zh/resume.markdown').read_text() + (ROOT / '_includes/resume-downloads.html').read_text()
        for value in ['title: 履歷\n', '資深韌體工程師', '2024 年 11 月',
                      '2026 年 8 月', '2021 年 3 月', '2024 年 10 月',
                      'delay/Vref', 'LPDDR5', '英文 PDF', '{#experience}']:
            with self.subTest(value=value):
                self.assertIn(value, text)
        self.assertNotIn('同一份文件內含英文版與中文版', text)

    def test_cv_aliases_have_one_owner_and_fragment_preserving_redirect(self):
        for name, old_route, target in [('cv.markdown', '/cv/', '/resume/'),
                                       ('zh/cv.markdown', '/zh-tw/cv/', '/zh-tw/resume/')]:
            with self.subTest(name=name):
                text = (ROOT / name).read_text()
                self.assertIn('layout: legacy-redirect\n', text)
                self.assertIn('permalink: ' + old_route + '\n', text)
                self.assertIn('redirect_target: ' + target + '\n', text)
                self.assertNotIn('translation_key:', text)
        layout = ROOT / '_layouts/legacy-redirect.html'
        self.assertTrue(layout.is_file())
        text = layout.read_text()
        self.assertIn('window.location.hash', text)
        self.assertIn('window.location.replace', text)
        self.assertIn('relative_url', text)
        self.assertIn('<noscript>', text)


if __name__ == '__main__':
    unittest.main()
