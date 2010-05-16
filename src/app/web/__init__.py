# Copyright 2008 Thomas Quemard
#
# Paste-It is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3.0, or (at your option)
# any later version.
#
# Paste-It  is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.


import feedparser
from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
import os

import app
import app.appengine.hook
import app.user
import settings


class Path:
    def __init__ (self):
        self.path = []

    def add (self, text, link=""):
        self.path.append({"text": text, "link":link})

class RequestHandler (webapp.RequestHandler):
    def __init__(self):
        import app.appengine.hook
        app.appengine.hook.datastore_logs = []

        webapp.RequestHandler.__init__(self)
        self.path = Path()
        self.module = ""
        self.module_directory = ""
        self.module_url = ""
        self.content = {}
        self.content["APP"] = {}
        self.scripts = []
        self.feeds = []
        self.styles = []
        self.user = app.user.get_current_user()
        if self.user:
            self.user.refresh()

        self.content["APP"]["SHOW_TWITTER"] = settings.SHOW_TWITTER and settings.TWITTER_ACCOUNT
        if self.content["APP"]["SHOW_TWITTER"]:
            tweet = memcache.get("twitter/latest")
            if tweet is None:
                feed = feedparser.parse("http://twitter.com/statuses/user_timeline/" + settings.TWITTER_ACCOUNT + ".rss")
                if len(feed.entries) > 0:
                    tweet = feed.entries[0].description[len(settings.TWITTER_ACCOUNT) + 2:]
                    memcache.add("twitter/latest", tweet, settings.TWITTER_UPDATE_FREQUENCY)
            self.content["APP"]["U_TWITTER"] = "http://twitter.com/" + settings.TWITTER_ACCOUNT
            self.content["APP"]["TWEET"] = tweet

    def add_atom_feed (self, url, title, rel):
        self.add_feed (url, "application/atom+xml", title, rel)

    def add_feed (self, url, type, title, rel):
        feed = {"url":url, "type": type, "title": title, "rel": rel}
        self.feeds.append(feed)

    def set_header(self, name, value):
        if not name in self.response.headers:
            self.response.headers.add_header(name, value)
        else:
            self.response.headers[name] = value

    def set_module(self, name):
        self.module_directory = "/".join(name.split(".")[0:-1])
        self.module = name.replace(".", "/") + ".py"
        self.module_url = "http://github.com/thomas-quemard/p8ste/blob/master/src/" + self.module
        self.module_history_url = "http://github.com/thomas-quemard/p8ste/commits/master/src/" + self.module

    def use_template(self, name):
        self.template_name = name

    def use_script(self, url):
        self.scripts.append(url)

    def use_style (self, url):
        self.styles.append(url)

    def write_out(self, template_path=""):

        if template_path != "":
            self.use_template(template_path)

        if settings.ENV == "debug":
            self.content["debug"] = True
        self.content["header_scripts"] = self.scripts
        self.content["feeds"] = self.feeds
        self.content["styles"] = self.styles
        self.content["module"] = self.module
        self.content["u_home"] = app.url("")
        self.content["u_pastes"] = app.url("pastes/")
        self.content["u_module"] = self.module_url
        self.content["u_about_thanks"] = app.url("about/thanks")
        self.content["u_about_features"] = app.url("about/features")
        self.content["u_module_history"] = self.module_history_url
        self.content["u_blank_image"] = app.url("images/blank.gif")
        self.content["APP_NAME"] = settings.APP_NAME
        self.content["path__"] = self.path.path

        if settings.ENV != "debug" and settings.USE_GANALYTICS:
            self.content["GANALYTICS_ID"] = settings.GANALYTICS_ID

        if "user-agent" in self.request.headers:
            self.content["bad_browser__"] = self.request.headers["user-agent"].find("MSIE") != -1

        if self.user.is_logged_in:
            self.content['user_signed_in__'] = True
            self.content['user_id__'] = self.user.id
            self.content['user_paste_count__'] = self.user.paste_count
            self.content["u_user__"] = self.user.url
            self.content["u_user_gravatar__"] = self.user.db_user.get_gravatar(16)
        else:
            self.content['user_signed_in__'] = False

        self.content["user_logged_in_google__"] = self.user.is_logged_in_google
        self.content["u_user_signup__"] = app.url("sign-up?url=%s", self.request.url)

        if self.user.is_logged_in_google:
            self.content['u_user_logout__'] = app.url("sign-out?url=%s", self.request.url)
        else:
            self.content['u_user_login__'] = app.url("sign-in?url=%s", self.request.url)

        if settings.ENV == "debug":
            self.content["datastore_logs"] = app.appengine.hook.datastore_logs

        tpl_path = ""
        if self.template_name.startswith("./"):
            tpl_path = self.module_directory + "/" + self.template_name[2:]
        else:
            tpl_path = self.template_name

        rendered_template = template.render(tpl_path, self.content)
        self.response.out.write(rendered_template)


class UserRequestHandler (RequestHandler):

    def get_user (self, user_id):
        qry_user = app.model.User.all()
        qry_user.filter("id =", user_id)
        return qry_user.get()
