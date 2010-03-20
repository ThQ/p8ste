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

import random

def filter_title(title, default_value = ""):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_:\\&()[]{}><*!?. "
    result = "" + "".join([ c for c in title if c in chars ])
    if result == "":
        result = default_value
    return result

def filter_user_name(name):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.@ "
    result = "" + "".join([ c for c in name if c in chars ])
    return result

def make_slug(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    char_count = len(chars)
    slug = "P"
    for i in range(0, length):
        at = random.randint(0, char_count)
        slug += chars[at : at + 1]
    return slug

def make_unique_slug(length):
    return make_slug(length)

def validate_code(code):
    result = True

    if len(code) == 0:
        result = False

    # @TODO: Check line count, line length, etc.

    return result
