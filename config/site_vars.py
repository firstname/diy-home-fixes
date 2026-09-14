"""
Single source of truth for constants shared across pelicanconf.py and publishconf.py.
Nothing secret goes here — this file IS committed to git.
"""

AUTHOR = "DIY Expert"
SITENAME = "The Ultimate DIY Hub"
TIMEZONE = "Pacific/Auckland"
DEFAULT_LANG = "en"

DEFAULT_PAGINATION = 12
SUMMARY_MAX_LENGTH = 30

ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html"
PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"
