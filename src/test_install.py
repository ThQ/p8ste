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

libs = [
    {"package": "feedparser", "url":"http://feedparser.org"},
    {"package": "pygments", "url":"http://pygments.org"},
    {"package": "recaptcha-client", "url":"http://pypi.python.org/pypi/recaptcha-client"}
]

def has_module(name):
    found = True
    try:
        __import__(name)
    except ImportError:
        found = False
    return found


print "Checking python libraries..."

for lib in libs:
    print " * " + lib["package"] + "... ",
    if has_module(lib["package"]) or has_module("libs." + lib["package"]):
        print "OK"
    else:
        print "Not found ! Download the package from " + lib["url"]

