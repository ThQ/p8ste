import paste
import paste.model
import paste.util
import paste.web
import settings
import smoid.languages

class PasteRequestHandler (paste.web.RequestHandler):

    def get_paste (self, pasty_slug):
        qry_pastes = paste.model.Pasty.all()
        qry_pastes.filter("slug =", pasty_slug)
        return qry_pastes.get()


class PasteListRequestHandler (PasteRequestHandler):

    def templatize_pastes (self, pastes):
        tpl_pastes = []
        for o_paste in pastes:
            tpl_paste = {}
            tpl_paste["title"] = o_paste.get_title()
            tpl_paste["slug"] = o_paste.slug
            tpl_paste["u"] = o_paste.get_url()
            tpl_paste["u_fork"] = o_paste.get_fork_url()
            tpl_paste["u_atom"] = paste.url("%s.atom", o_paste.slug)
            tpl_paste["u_raw_text"] = paste.url("%s.txt", o_paste.slug)
            tpl_paste["snippet"] = o_paste.snippet
            tpl_paste["is_moderated"] = o_paste.is_moderated()
            tpl_paste["is_private"] = o_paste.is_private()
            tpl_paste["is_public"] = o_paste.is_public()
            tpl_paste["is_awaiting_approval"] = o_paste.is_waiting_for_approval()
            tpl_paste["is_code_viewable"] = o_paste.is_code_viewable()
            if o_paste.user:
                tpl_paste["u_user"] = paste.url("users/%s", o_paste.user.id)
            tpl_paste["user_name"] = o_paste.posted_by_user_name

            if o_paste.user:
                tpl_paste["u_gravatar"] = o_paste.user.get_gravatar(16)

            if o_paste.language and o_paste.language in smoid.languages.languages:
                tpl_paste["u_language_icon"] = smoid.languages.languages[o_paste.language]['u_icon']

            if o_paste.forks > 0:
                tpl_paste["forks"] = o_paste.forks

            if o_paste.posted_at != None:
                tpl_paste["posted_at"] = o_paste.posted_at.strftime(settings.DATETIME_FORMAT)
            else:
                tpl_paste["posted_at"] = ""

            if o_paste.characters:
                tpl_paste["size"] = paste.util.make_filesize_readable(o_paste.characters)
            tpl_paste["loc"] = o_paste.lines

            tpl_paste["language"] = {}
            tpl_paste["language"]["name"] = o_paste.get_language_name()
            tpl_paste["language"]["u_icon"] = o_paste.get_icon_url()
            tpl_paste["language"]["u"] = o_paste.get_language_url()

            tpl_pastes.append(tpl_paste)

        return tpl_pastes
