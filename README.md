# Bilingual professional website

Job-focused website for Lee Long Sheng, built with Jekyll/Minima. English and Traditional Chinese pages share navigation, page-matched language switching, and one resume download configuration.

## Routes and language ownership

| Content | English | Traditional Chinese |
| --- | --- | --- |
| Home | `/` | `/zh-tw/` |
| Resume and PDF download | `/resume/` | `/zh-tw/resume/` |
| Contact | `/about/` | `/zh-tw/about/` |
| Writing | `/blog/` | `/zh-tw/blog/` |
| Not found | `/404.html` | `/zh-tw/404.html` |

`/cv/` and `/zh-tw/cv/` redirect to the matching Resume page. The small `_layouts/legacy-redirect.html` preserves section fragments for normal JavaScript-enabled navigation and provides a no-JavaScript redirect/link fallback. Former CV section IDs remain on Resume. CV aliases are not separate translations or navigation entries.

English sources stay at the root; Chinese sources live in `zh/` with explicit `/zh-tw/` permalinks. Paired content pages share a unique `translation_key` and declare `lang: en` or `lang: zh-Hant`. Native language links open the matching page. The site-title link opens the current language's homepage.

`header_pages` in `_config.yml` owns the three-link navigation order: Resume, Blog, Contact. `_includes/header.html` resolves each source to its same-key/current-language counterpart. `_data/locales.yml` owns shared UI labels. Minima's default layout consumes `page.lang`.

`_includes/head.html` retains SEO/RSS/CSS integration and adds reciprocal `hreflang` plus English `x-default` only for actual translations. Existing posts remain in their original language; the Chinese option on an untranslated post explicitly opens the Chinese article listing, not a claimed translation. `_layouts/home.html` localizes listing chrome.

## Content and public assets

- Homepage: concise DRAM-validation/firmware overview, Phison experience, relevant skills, education, contact, and resume/PDF actions.
- Resume: professional summary, official job titles and promotion dates, technical skills, education/project, activities, languages, and contact. It replaces the former separate CV and download landing pages.
- Current approved files live directly in `assets/documents/`; no extra 2026 source/public duplicate is needed.
- `_config.yml` owns `resume_pdf` (firmware resume), `resume_validation_pdf` (validation resume), `cv_pdf` (full CV), and their shared `resume_version`. Preserve supplied filenames, including the underscore in `resume-11-2026-dram_validation.pdf`.
- Both homepages keep the owner's inline arrangement: View Resume (or 查看履歷) beside the language/version note and Other Resumes & Full CV (or 其他履歷與完整 CV). Shared spacing rules align the row and allow supporting text to wrap on narrow screens without moving it outside the row. The links open the matching Resume page and `#documents`; PDFs and version details also remain in the shared Resume download section.
- Both languages share 16px body text, 24px section headings, 20px subheadings/list titles and semibold emphasis across Home, Resume, Contact, Blog and project content. Resume retains detailed career information while matching the homepage's role/date presentation and technical labels. Both homepages end with direct Email, LinkedIn and GitHub links; the project article remains in its original English and Chinese project links identify its language.
- All three current PDFs are English-only and remain unchanged. Phone numbers remain in the supplied PDFs with the owner's permission; HTML contact sections do not repeat them.
- All public PDFs live only in `assets/documents/`. The archived April 2025 document remains at `assets/documents/cv-04-2025.pdf`; the duplicate `CV_version/` directory is retired. Internal PDF links must target assets. Previously shared `/CV_version/04_2025.pdf` links are not preserved by this consolidation and will return 404 after deployment; no HTML redirect is placed at a `.pdf` URL.
- Historical project notes are kept locally in `.hermes/handoff/`; the redundant root `memory.md` is retired. Backups and exact removal reports live in `.hermes/backups/` and must not be published.
- `assets/images/profile-small.jpg` is the public portrait. Full-size originals stay local. Git ignore and Jekyll exclusions serve different purposes; preserve both.
- `.hermes/`, `Personal/`, development notes, tests, and local scripts must not appear in generated website output.

## Preview

From this repository, using the existing user-installed Jekyll:

```sh
"$HOME/.gem/ruby/2.6.0/bin/jekyll" serve --host 127.0.0.1 --port 4174
```

Use a free port and do not stop someone else's preview. Restart after `_config.yml` changes. A running server watches the directory it was started from.

## Verification and publication

```sh
python3 -m unittest discover -s tests -v
"$HOME/.gem/ruby/2.6.0/bin/jekyll" build --destination /path/to/disposable-output
python3 tests/verify_build.py /path/to/disposable-output
```

Also build with `--baseurl /verification` and pass `/verification` as the verifier's second argument. Use canonical paths in the configured Hermes scratch directory for disposable copies. Verify legacy CV redirects in a browser, including fragments, desktop/mobile layout, bilingual switches and the current download.

The two Jekyll starter posts were removed with local backups at the owner's request. The remaining final-year-project post uses the explicit, date-independent permalink `/blog/rubiks-cube-solving-guides-with-ar/`. Its visible work-in-progress notice remains until the owner fills in the article. No site timezone change is needed for that stable project URL.

Local edits and verification do not authorize staging, committing, pushing, or publishing. Review the diff before a separately authorized Git update.
