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


import os
import urllib


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
