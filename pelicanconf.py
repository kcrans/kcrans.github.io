import os
from datetime import date

# Used to get the file paths of all static files
def get_file_paths(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

AUTHOR = 'Kaleb Crans'
SITENAME = "kaleb's site"
SITEURL = "" # Taken care of with Github action

PATH = "content"

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%B %-d, %Y'
CURRENT_YEAR = date.today().year

THEME = 'themes/tufteblog'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
INDEX_SAVE_AS = 'posts/index.html'

# Blogroll
#LINKS = (
#    ("Pelican", "https://getpelican.com/"),
#    ("Python.org", "https://www.python.org/"),
#    ("Jinja2", "https://palletsprojects.com/p/jinja/"),
#    ("You can modify those links in your config file", "#"),
#)

# Social widget
#SOCIAL = (
#    ("You can add links in your config file", "#"),
#    ("Another social link", "#"),
#)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# File paths to be treated as static
STATIC_PATHS = [
        'images',
        'static',
]

# Exclude these paths from Pelican's article/page generator
ARTICLE_EXCLUDES = [
        'static'
        ]
# Change the location of static assets (instead of everything staying in the static dir)
file_paths = get_file_paths("content/static/")
prefix1 = len('content/')
prefix2 = prefix1 + len('static/')
the_dict = {file_path[prefix1:] : {'path': file_path[prefix2:]} for file_path in file_paths}
EXTRA_PATH_METADATA = the_dict 
