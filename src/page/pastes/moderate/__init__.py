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


import app.web


class Moderate (app.web.pastes.PasteRequestHandler):
    """
    A page for moderating a paste.
    """

    def __init__ (self):
        app.web.pastes.PasteRequestHandler.__init__(self)
        self.paste = None

    def get (self, paste_slug):
        self.set_module(__name__ + ".__init__")

        if self.user.is_google_admin:
            self.paste = self.get_paste(paste_slug)

            if self.paste:
                tpl_paste = {}
                tpl_paste["slug"] = self.paste.slug
                tpl_paste["u"] = self.paste.get_url()
                tpl_paste["u_moderate"] = self.paste.get_moderate_url()
                tpl_paste["u_real_moderate"] = self.paste.get_real_moderate_url()
                self.content["paste"] = tpl_paste

                user_is_sure = self.request.get("sure", "") == "yes"

                if not user_is_sure:
                    self.write_out("./are_you_sure.html")
                else:
                    self.moderate_paste()
                    self.write_out("./moderated.html")


    def moderate_paste (self):
        self.paste.status = app.model.kPASTE_STATUS_MODERATED
        return self.paste.put()
