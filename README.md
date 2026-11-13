# Bilingual professional website

CV-focused website for Lee Long Sheng, built with Jekyll/Minima. English and Traditional Chinese pages share navigation, language switching, and resume configuration.

## Routes and language ownership

| Content | English | Traditional Chinese |
| --- | --- | --- |
| Home | `/` | `/zh-tw/` |
| Full CV | `/cv/` | `/zh-tw/cv/` |
| Resume download | `/resume/` | `/zh-tw/resume/` |
| Contact | `/about/` | `/zh-tw/about/` |
| Writing | `/blog/` | `/zh-tw/blog/` |
| Not found | `/404.html` | `/zh-tw/404.html` |

English page sources stay at the root; Chinese sources live in `zh/` with explicit `/zh-tw/` permalinks. Paired pages share a unique `translation_key` and declare `lang: en` or `lang: zh-Hant`. These fields drive header switches and reciprocal alternate-language metadata. Site title links to the current language's homepage.

`header_pages` in `_config.yml` owns navigation order. `_includes/header.html` resolves each listed English page to its same-key counterpart in the current language. Add a translated counterpart when adding a new navigation page. `_data/locales.yml` owns shared UI labels. Minima's default layout already uses `page.lang` for the HTML language, so it is not copied.

The switch is ordinary links, not a JavaScript translation overlay or automatic redirect. Deep links retain the requested language. Existing posts are unmodified and retain their original language; both blog listings state this. On an untranslated post, the Chinese option explicitly opens the Chinese article listing, not an advertised translation of that post. Such posts do not receive alternate-language metadata pointing at a listing.

`_includes/head.html` retains Minima's SEO, RSS, CSS and optional analytics integration, adding reciprocal `hreflang` and English `x-default` only for real page pairs. `_layouts/home.html` only localizes blog listing chrome.

## Content and public assets

- Homepage: concise engineering overview, selected experience, strengths, and links to the full CV and PDF.
- CV: fuller supported professional background, education/project, activities, languages and contact.
- Resume page: stable download entry with the actual PDF version date.
- `resume_pdf` and `resume_version` in `_config.yml` are the single current download/date owner. When publishing an approved replacement, update both settings together and retain older PDF URLs. `_includes/resume-version.html` formats the same date in Chinese, without a separate date setting.
- The PDF remains the existing April 2025 English/Chinese document. HTML revisions do not update its contents. No new or comparison PDF is published.
- `assets/images/profile-small.jpg` is the existing public portrait. Do not copy full-size originals into public assets.
- `CV_version/04_2025.pdf` remains a byte-identical compatibility copy of `assets/documents/cv-04-2025.pdf`, preserving the legacy download URL.
- Git ignore and Jekyll exclusion rules for private originals and local notes remain intact. Do not commit private documents or `.hermes/`.

## Preview

From the repository, using the existing user-installed Jekyll:

```sh
"$HOME/.gem/ruby/2.6.0/bin/jekyll" serve --host 127.0.0.1 --port 4174
```

Use a free port; do not stop someone else's preview. The server watches the directory it was started from. Restart after `_config.yml` changes.

## Verification and publication

Run `python3 -m unittest discover -s tests -v` and build with real Jekyll before publishing. Check rendered language pairs, alternate-language metadata, local links/fragments, routes/redirects, RSS, PDF-byte integrity, private-file exclusions and a nonempty-baseurl variant.

Review visual changes before publication. Local editing, a successful preview, and committing are separate from pushing to GitHub. A push to the configured publishing branch may trigger GitHub Pages deployment.
