import datetime
import os

if not "SERVER_NAME" in os.environ or os.environ["SERVER_NAME"] == "localhost":
    ENV = "debug"
else:
    ENV = "production"


# -----------------------------------------------------------------------------
# APPLICATION
# -----------------------------------------------------------------------------

# This name will appear in the title, in the headers, in the path bar...
APP_NAME = "PrengePASTE"


# -----------------------------------------------------------------------------
# PASTES
# -----------------------------------------------------------------------------

# The maximum length of a line in a paste
PASTE_CODE_LINE_MAX_LENGTH = 500

# The maximum lines a paste can have
PASTE_CODE_MAX_LINES = 500

# The maximum size of a paste
PASTE_CODE_MAX_LENGTH = 100000

# The delay after which a paste form is expired
PASTE_FORM_EXPIRATION_DELTA = datetime.timedelta(minutes=20)

# The maximum length of a paste snippet
PASTE_SNIPPET_MAX_LENGTH = 50


# -----------------------------------------------------------------------------
# DATES
# -----------------------------------------------------------------------------

# The default date format
DATE_FORMAT = "%b, %d %Y"

# The default date format
DATETIME_FORMAT = "%b, %d %Y - %I:%M%p %z"

# The date format for atom feeds
ATOM_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


# -----------------------------------------------------------------------------
# USERS
# -----------------------------------------------------------------------------

# The maximum length of a user name
USER_NAME_MAX_LENGTH = 100

# The default user name (when the user is not logged in)
DEFAULT_USER_NAME = "John Doe"


# -----------------------------------------------------------------------------
# GOOGLE ANALYTICS
# -----------------------------------------------------------------------------

# Whether to use Google Analytics or not.
USE_GANALYTICS = False

# Your Google Analytics ID, something like <UA-123456-5>
GANALYTICS_ID = ""


# -----------------------------------------------------------------------------
# RECAPTCHA
# -----------------------------------------------------------------------------

# Whether or not use the recaptcha test when pasting anonymously.
USE_RECAPTCHA = False

RECAPTCHA_PUBLIC_KEY = ""

RECAPTCHA_PRIVATE_KEY = ""


# -----------------------------------------------------------------------------
# TWITTER
# You'll need feedparser from http://www.feedparser.org to use that.
# -----------------------------------------------------------------------------

# Whether to fetch the latest tweet or not.
SHOW_TWITTER = False

# The twitter account to fetch.
TWITTER_ACCOUNT = ""

# How often do we have to update twitter news (in seconds)
TWITTER_UPDATE_FREQUENCY = 60 * 60 * 2
