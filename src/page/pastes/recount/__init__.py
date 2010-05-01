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

import calendar
import copy
import datetime


import paste
import paste.lang
import paste.model
import paste.util
import paste.web.pastes
import settings

class Recount (paste.web.pastes.PasteRequestHandler):

    def __init__ (self):
        paste.web.pastes.PasteRequestHandler.__init__(self)

        self.paste = None

        self.set_module("page.pasties.recount.__init__")

    def get (self, paste_slug):
        self.paste = self.get_paste(paste_slug)

        self.content["u_pastes"] = paste.url("pastes/")
        self.content["u_paste"] = paste.url("%s", paste_slug)
        self.content["paste_slug"] = paste_slug

        if self.paste:
            self.get_200()
        else:
            self.get_404()

    def get_200 (self):
        self.pastes_in_hour = 0
        self.pastes_in_day = 0
        self.pastes_in_month = 0
        self.pastes_in_year = 0

        self.day_start, self.day_end = self.get_day()
        self.hour_start, self.hour_end = self.get_hour()
        self.month_start, self.month_end = self.get_month()

        self.update_hour()
        self.update_day()
        self.update_month()

        self.content["pasted_at"] = self.paste.posted_at.strftime(settings.DATETIME_FORMAT)
        self.content["month_start"] = self.month_start.strftime(settings.DATETIME_FORMAT)
        self.content["month_end"] = self.month_end.strftime(settings.DATETIME_FORMAT)
        self.content["pastes_in_month"] = self.pastes_in_month
        self.content["hour_start"] = self.hour_start.strftime(settings.DATETIME_FORMAT)
        self.content["hour_end"] = self.hour_end.strftime(settings.DATETIME_FORMAT)
        self.content["pastes_in_hour"] = self.pastes_in_hour
        self.content["day_start"] = self.day_start.strftime(settings.DATETIME_FORMAT)
        self.content["day_end"] = self.day_end.strftime(settings.DATETIME_FORMAT)
        self.content["pastes_in_day"] = self.pastes_in_day
        self.write_out("page/pasties/recount/200.html")

    def get_404 (self):
        self.write_out("page/pasties/recount/404.html")

    def get_hour (self):
        hour_start = copy.copy(self.paste.posted_at)
        hour_start -= datetime.timedelta(0, hour_start.second, 0, 0, hour_start.minute)

        hour_end = copy.copy(hour_start)
        hour_end += datetime.timedelta(0, 59, 0, 0, 59)

        return hour_start, hour_end

    def get_day (self):
        day_start = copy.copy(self.paste.posted_at)
        day_start -= datetime.timedelta(0, day_start.second, 0, 0, day_start.minute, day_start.hour)

        day_end = copy.copy(day_start)
        day_end += datetime.timedelta(0, 59, 0, 0, 59, 23)

        return day_start, day_end

    def get_month (self):
        month_start = copy.copy(self.paste.posted_at)
        month_start -= datetime.timedelta(month_start.day - 1, month_start.second, 0, 0, month_start.minute, month_start.hour)

        days_in_month = calendar.monthrange(month_start.year, month_start.month)[1]

        month_end = copy.copy(month_start)
        month_end += datetime.timedelta(days_in_month - 1, 59, 0, 0, 59, 23)

        return month_start, month_end

    def update_hour (self):
        while True:
            qry_pastes = paste.model.Pasty.all()
            qry_pastes.filter("posted_at >", self.hour_start)
            qry_pastes.order("posted_at")
            db_pastes = qry_pastes.fetch(20)
            if db_pastes:
                i = 0
                for db_paste in db_pastes:
                    if db_paste.posted_at <= self.hour_end:
                        i += 1
                        self.pastes_in_hour += 1
                    else:
                        break
                if i < 20:
                    break

        hour_path ="hour"
        hour_path += "/" + str(self.hour_start.year)
        hour_path += "/" + str(self.hour_start.month)
        hour_path += "/" + str(self.hour_start.day)
        hour_path += "." + str(self.hour_start.hour)

        qry_hour = paste.model.PasteCount.all()
        qry_hour.filter("path =", hour_path)
        hour = qry_hour.get()

        if not hour:
            hour = paste.model.PasteCount()
            hour.path = hour_path

        hour.last_checked = datetime.datetime.now()
        hour.count = self.pastes_in_hour
        hour.put()

    def update_day (self):
        for hour in xrange(1, 24):
            hour_path ="hour"
            hour_path += "/" + str(self.day_start.year)
            hour_path += "/" + str(self.day_start.month)
            hour_path += "/" + str(self.day_start.day)
            hour_path += "." + str(hour)

            qry_hour = paste.model.PasteCount.all()
            qry_hour.filter("path =", hour_path)
            db_hour = qry_hour.get()

            if db_hour:
                self.pastes_in_day += db_hour.count

        day_path = "day"
        day_path += "/" + str(self.day_start.year)
        day_path += "/" + str(self.day_start.month)
        day_path += "/" + str(self.day_start.day)

        qry_day = paste.model.PasteCount.all()
        qry_day.filter("path = ", day_path)
        day = qry_day.get()

        if not day:
            day = paste.model.PasteCount()
            day.path = day_path

        day.last_checked = datetime.datetime.now()
        day.count = self.pastes_in_day
        day.put()

    def update_month (self):
        days_in_month = calendar.monthrange(self.month_start.year, self.month_start.month)[1]

        self.pastes_in_month = 0
        for day in xrange(1, days_in_month):
            day_path ="day/" + str(self.day_start.year) + "/" + str(self.day_start.month) + "/" + str(day)
            qry_day = paste.model.PasteCount.all()
            qry_day.filter("path =", day_path)
            db_day = qry_day.get()

            if db_day:
                self.pastes_in_month += db_day.count

        month_path ="month/" + str(self.day_start.year) + "/" + str(self.day_start.month)
        qry_month = paste.model.PasteCount.all()
        qry_month.filter("path = ", month_path)
        month = qry_month.get()

        if not month:
            month = paste.model.PasteCount()
            month.path = month_path

        month.last_checked = datetime.datetime.now()
        month.count = self.pastes_in_month
        month.put()
