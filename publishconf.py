import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: F401,F403
from dotenv import load_dotenv

load_dotenv()

_user = os.environ["GITHUB_USERNAME"]      # hard fail if missing — never guess/hardcode
_repo = os.environ["GITHUB_REPO"]
_custom_domain = os.environ.get("SITE_DOMAIN", "").strip()

SITEURL = f"https://{_custom_domain}" if _custom_domain else f"https://{_user}.github.io/{_repo}"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True
