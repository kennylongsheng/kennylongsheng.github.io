# Website work log

## Working directory

`/Users/kennylongshengicloud.com/Desktop/Codes/Personal/github_io/kennylongsheng.github.io`

Repository: `kennylongsheng/kennylongsheng.github.io`
Public site: https://kennylongsheng.github.io

## Previous session, 2026-11-03

This log summarizes the previous Hermes conversation. Historical verification results below describe that session, not a fresh verification of the current files.

### Scope and decisions

- Kept the existing Jekyll and Minima foundation rather than rebuilding the site.
- Kept the content simple and engineering-focused. The owner is an engineer, not a photographer. Do not add photography content.
- Made local changes only. No commits, pushes, or publishing were performed.

### Content and navigation

- Replaced the homepage's nested HTML document structure with a normal Jekyll page and a simple engineer introduction.
- Cleaned up template About content and placeholder settings without inventing career details.
- Added Home, CV, Blog, and About navigation.
- Standardized the Blog URL at `/blog/` and added redirects for old URLs.
- Changed the configured site URL to HTTPS and removed an invalid Twitter setting.
- Initially removed a broken CV link. Later added a `/cv/` page linking to the dated PDF at `CV_version/04_2025.pdf`.

### Visual refresh

- Added a warm off-white background, dark text, and muted teal links.
- Improved typography, spacing, and simple section dividers.
- Added a compact footer with Email and GitHub links.
- Kept navigation visible on small screens.
- Avoided animations and external fonts.
- The user approved the appearance before the final verification run.

### Local development

- Installed user-level Ruby dependencies needed to run Jekyll locally.
- Added a README with editing and preview instructions.
- Added Python cache exclusions to `.gitignore`.
- Added source regression checks in `tests/test_site.py`.
- Ran a local preview at `http://127.0.0.1:4000/` during the session. This log does not establish whether that server is still running.

Preview command used in the session:

```sh
cd /Users/kennylongshengicloud.com/Desktop/Codes/Personal/github_io/kennylongsheng.github.io
"$HOME/.gem/ruby/2.6.0/bin/jekyll" serve --host 127.0.0.1 --port 4000
```

### Final verification recorded in the previous session

After the user's visual approval, a focused temporary script ran and was removed. The results were reported as ad-hoc verification, not comprehensive visual or browser testing.

- All 3 source regression tests passed.
- Jekyll built successfully and compiled the stylesheet.
- Checked 9 generated HTML pages for broken local links, nested HTML documents, duplicate IDs, and missing section labels.
- Checked footer contact links and key stylesheet rules.
- Confirmed the generated CV PDF matched the source PDF byte for byte.
- `git diff --check` passed.

### Main files involved

- `index.html`
- `_config.yml`
- `about.markdown`
- `blog.markdown`
- `cv.markdown`
- `CV_version/04_2025.pdf`
- `_includes/footer.html`
- `assets/main.scss`
- `README.md`
- `.gitignore`
- `tests/test_site.py`

## Handoff

- Website styling was approved and the checks above passed in the previous session.
- Changes remained uncommitted and unpublished.
- Inspect the current diff and obtain fresh verification before committing or publishing. Historical passing results do not prove the current working tree is unchanged.
- Preserve user-provided original files. For future requested edits, work on copies or provide a patch as appropriate.
- The separate editable Pages CV reconstruction was not the website styling task. This log does not claim that reconstruction was completed.
