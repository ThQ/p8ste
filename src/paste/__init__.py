# Copyright 2008 Thomas Quemard
#
# Paste-It is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3.0, or (at your option)
# any later version.
#
# Paste-It is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.

import datetime
import logging
import os
import urllib

import paste.log

def url (format, *args):
    domain = "http://" + os.environ["SERVER_NAME"]
    if os.environ["SERVER_PORT"] != "80":
        domain += ":" + os.environ["SERVER_PORT"]
    out = ""
    argc = 0
    i = 0
    format += " "
    i_max = len(format) - 1
    while i < i_max:
        if format[i:i+1] == "%":
            c = format[i + 1:i + 2]
            if c == "i":
                out += str(int(args[argc]))
                argc += 1
                i += 1
            elif c == "s":
                out += urllib.quote(args[argc])
                argc += 1
                i += 1
            else:
                out += "%" + format
        else:
            out += format[i:i + 1]
        i += 1
    return domain + "/" + out

config = {}
if os.environ["SERVER_NAME"] == "localhost":
    config["env"] = "debug"
    config["pasty_code_line_max_length"] = 100
    config["pasty_code_max_lines"] = 15
    config["pasty_expiration_delta"] = datetime.timedelta(minutes=10)
    config["pasty_form_expiration_delta"] = datetime.timedelta(seconds=60)
    config["pasty_title_max_length"] = 50
    config["pasty_tags_max_count"] = 10
    config["pasty_tags_max_length"] = 150
    config["user_name_max_length"] = 100

    h = paste.log.DebugHandler()
    logging.getLogger().addHandler(h)
else:
    config["env"] = "production"
    config["pasty_code_line_max_length"] = 500
    config["pasty_code_max_lines"] = 500
    config["pasty_expiration_delta"] = datetime.timedelta(days=7)
    config["pasty_form_expiration_delta"] = datetime.timedelta(minutes=30)
    config["pasty_title_max_length"] = 50
    config["pasty_tags_max_count"] = 10
    config["pasty_tags_max_length"] = 150
    config["user_name_max_length"] = 100

config["recaptcha::key::public"] = "6LclHgwAAAAAANgHdkrnhFf4GpH94dIAyUF8caht"
config["pasty_snippet_length"] = 50
config["default_user_name"] = "John_Doe"
config["datetime.format"] = "%b, %d %Y - %I:%M%p %z"
