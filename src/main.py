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


from google.appengine.api import apiproxy_stub_map
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

import paste
import page.about.features
import page.about.thanks
import page.error.error404
import page.languages.autodetected
import page.pasties.add
import page.pasties.diff
import page.pasties.index
import page.pasties.index_atom
import page.pasties.list
import page.pasties.pasty
import page.pasties.pasty_txt
import page.pasties.pasty_atom
import page.pasties.recount
import page.pasties.remote_diff
import page.pasties.sitemap
import page.pasties.update
import page.threads.thread
import page.threads.thread_atom
import page.users.signin
import page.users.signup
import page.users.signout
import page.users.user


template.register_template_library('common.url')

# Datastore query logging
if paste.config["env"] == "debug":
    import paste.appengine.hook
    paste.appengine.hook.datastore_logs = []
    apiproxy_stub_map.apiproxy.GetPreCallHooks().Append('db_log', paste.appengine.hook.hook_datastore, 'datastore_v3')

re_paste = "P[a-zA-Z0-9_-]+"
re_user = "[a-zA-Z0-9_-]+"

pages = [
    ('/', page.pasties.add.Add),

    # Pastes
    ('/(' + re_paste + ')', page.pasties.pasty.Pasty),
    ('/(' + re_paste + '(?:%2B' + re_paste + ')+)', page.pasties.list.List),
    ('/pastes/', page.pasties.index.Index),
    ('/pastes.atom', page.pasties.index_atom.IndexAtom),
    ('/(' + re_paste + ')/fork', page.pasties.add.Add),
    ('/(' + re_paste + ').txt', page.pasties.pasty_txt.PastyTxt),
    ('/(' + re_paste + ').atom', page.pasties.pasty_atom.PastyAtom),
    ('/(' + re_paste + ')/diff', page.pasties.remote_diff.RemoteDiff),
    ('/(' + re_paste + ')/diff/(' + re_paste + ')', page.pasties.diff.Diff),
    ('/(' + re_paste + ')/recount', page.pasties.recount.Recount),
    ('/(' + re_paste + ')/update', page.pasties.update.Update),
    ('/users/(' + re_user + ')', page.users.user.User),
    ('/threads/(' + re_paste + ')', page.threads.thread.Thread),
    ('/threads/(' + re_paste + ').atom', page.threads.thread_atom.ThreadAtom),
    ('/sitemap.xml', page.pasties.sitemap.Sitemap),
    ('/sign-in', page.users.signin.SignIn),
    ('/sign-up', page.users.signup.SignUp),
    ('/sign-out', page.users.signout.SignOut),
    ('/about/thanks', page.about.thanks.Thanks),
    ('/about/features', page.about.features.Features),
    ('/languages/auto-detected', page.languages.autodetected.AutoDetected),
    ('/.*', page.error.error404.Error404)
]
application = webapp.WSGIApplication(pages, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
