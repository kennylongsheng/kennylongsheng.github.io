# Kenny's Blog

Personal website built with Jekyll and the Minima theme.

## Editing

- `index.html`: homepage content (the layout supplies the HTML document).
- `about.markdown`: introduction and contact links.
- `blog.markdown`: blog listing at `/blog/`; old `/blog` and `/blog.html` links redirect here.
- `_posts/`: existing posts, preserved during cleanup.
- `_config.yml`: site settings and navigation. Restart Jekyll after editing it.

The CV page (`cv.markdown`) links to `CV_version/04_2025.pdf`, labelled April
2025. To publish a newer version, add its PDF to `CV_version/` and update the
link and date on the CV page. These files will be public when the site is published.

## Local preview

On the currently configured Mac:

```sh
export PATH="$(ruby -r rubygems -e 'puts Gem.user_dir')/bin:$PATH"
jekyll serve --host 127.0.0.1
```

Open http://127.0.0.1:4000. Stop with Ctrl-C. This does not publish the site.

## Verification

```sh
python3 -m unittest discover -s tests -v
jekyll build
git diff --check
```

A local build was verified using Jekyll 3.9.5 and Minima 2.5.1. Ruby dependencies
were installed in the current user's gem directory, not the system gem directory.
The system Ruby is 2.6, so installing unpinned latest dependencies may fail.
A modern supported Ruby is recommended for future development.

The tests and this README are excluded from the published website.
