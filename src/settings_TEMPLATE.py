import datetime
import os

if os.environ["SERVER_NAME"] == "localhost":
    ENV = "debug"
else:
    ENV = "production"


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
# RECAPTCHA
# -----------------------------------------------------------------------------

# Whether or not use the recaptcha test when pasting anonymously.
USE_RECAPTCHA = False

RECAPTCHA_PUBLIC_KEY = ""

RECAPTCHA_PRIVATE_KEY = ""
