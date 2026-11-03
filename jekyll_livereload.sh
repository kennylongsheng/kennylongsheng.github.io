export PATH="$(ruby -r rubygems -e 'puts Gem.user_dir')/bin:$PATH"
jekyll serve --host 127.0.0.1 --port 4000 --livereload
