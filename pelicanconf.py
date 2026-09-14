import os
from dotenv import load_dotenv
from config.site_vars import *  # noqa: F401,F403  (AUTHOR, SITENAME, TIMEZONE, ...)

load_dotenv()  # loads .env in local/dev; in CI, real env vars are already set by Actions

SITEURL = os.environ.get("LOCAL_SITEURL", "http://localhost:8000")
PATH = "content"

THEME = "themes/flex"
THEME_TEMPLATES_OVERRIDES = ["content/templates"]

STATIC_PATHS = ["images", "extra/custom.css"]
EXTRA_PATH_METADATA = {
    "extra/custom.css": {"path": "static/custom.css"},
}
CUSTOM_CSS = "static/custom.css"

# Feeds disabled for local/dev speed
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

GOOGLE_ADSENSE = {
    "ca_id": os.environ.get("GOOGLE_ADSENSE_CLIENT_ID", ""),
    "page_level_ads": True,
}
GOOGLE_ANALYTICS = os.environ.get("GOOGLE_ANALYTICS_ID", "")
