#!/usr/bin/env python
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

import os.path
import sys

cur_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(cur_dir, "libs"))

from google.appengine.api import apiproxy_stub_map
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import app
import page.about.features
import page.about.index
import page.about.thanks
import page.error.error404
import page.languages.autodetected
import page.pastes.add
import page.pastes.diff
import page.pastes.index
import page.pastes.index_atom
import page.pastes.list
import page.pastes.moderate
import page.pastes.paste
import page.pastes.paste_txt
import page.pastes.paste_atom
import page.pastes.recount
import page.pastes.remote_diff
import page.pastes.sitemap
import page.pastes.update
import page.threads.thread
import page.threads.thread_atom
import page.users.signin
import page.users.signup
import page.users.signout
import page.users.user
import settings


template.register_template_library('common.url')

# Datastore query logging
if settings.ENV == "debug":
    import app.appengine.hook
    app.appengine.hook.datastore_logs = []
    apiproxy_stub_map.apiproxy.GetPreCallHooks().Append(
        'db_log',
        app.appengine.hook.hook_datastore,
        'datastore_v3')

re_paste = "P[a-zA-Z0-9_-]+"
re_user = "[a-zA-Z0-9_-]+"

pages = [
    ('/', page.pastes.add.Add),

    # Pastes
    ('/(' + re_paste + ')', page.pastes.paste.Paste),
    ('/(' + re_paste + '(?:%2B' + re_paste + ')+)', page.pastes.list.List),
    ('/pastes/', page.pastes.index.Index),
    ('/pastes.atom', page.pastes.index_atom.IndexAtom),
    ('/(' + re_paste + ')/fork', page.pastes.add.Add),
    ('/(' + re_paste + ')/moderate', page.pastes.moderate.Moderate),
    ('/(' + re_paste + ').txt', page.pastes.paste_txt.PasteTxt),
    ('/(' + re_paste + ').atom', page.pastes.paste_atom.PasteAtom),
    ('/(' + re_paste + ')/diff', page.pastes.remote_diff.RemoteDiff),
    ('/(' + re_paste + ')/diff/(' + re_paste + ')', page.pastes.diff.Diff),
    ('/(' + re_paste + ')/recount', page.pastes.recount.Recount),
    ('/(' + re_paste + ')/update', page.pastes.update.Update),
    # Users
    ('/users/(' + re_user + ')', page.users.user.User),
    # Threads
    ('/threads/(' + re_paste + ')', page.threads.thread.Thread),
    ('/threads/(' + re_paste + ').atom', page.threads.thread_atom.ThreadAtom),
    ('/sitemap.xml', page.pastes.sitemap.Sitemap),
    ('/sign-in', page.users.signin.SignIn),
    ('/sign-up', page.users.signup.SignUp),
    ('/sign-out', page.users.signout.SignOut),
    # About
    ('/about', page.about.index.Index),
    ('/about/thanks', page.about.thanks.Thanks),
    ('/about/features', page.about.features.Features),
    ('/languages/auto-detected', page.languages.autodetected.AutoDetected),
    ('/.*', page.error.error404.Error404)]

application = webapp.WSGIApplication(pages, debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()
