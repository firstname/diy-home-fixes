import os
import sys
from dotenv import load_dotenv

# The `pelican` console script does not put the project root on sys.path, so `config` would
# not be importable. `python -m pelican` (used in CI) does, but make both work.
sys.path.append(os.curdir)

from config.site_vars import *  # noqa: E402,F401,F403  (AUTHOR, SITENAME, TIMEZONE, ...)

load_dotenv()  # loads .env in local/dev; in CI, real env vars are already set by Actions

SITEURL = os.environ.get("LOCAL_SITEURL", "http://localhost:8000")
PATH = "content"

# Default ARTICLE_PATHS is [''], which scans all of content/ and tries to parse
# content/templates/*.html as articles. Restrict it to the posts directory.
ARTICLE_PATHS = ["posts"]
PAGE_PATHS = ["pages"]

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
    # The flex theme reads GOOGLE_ADSENSE.ads.<slot> for every ad position; without this
    # key Jinja raises UndefinedError. Empty dict = no ad units until slots are configured.
    "ads": {},
}
GOOGLE_ANALYTICS = os.environ.get("GOOGLE_ANALYTICS_ID", "")
