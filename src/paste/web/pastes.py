import paste
import paste.model
import paste.util
import paste.web
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
            if o_paste.title != None:
                tpl_paste["title"] = o_paste.title
            else:
                tpl_paste["title"] = o_paste.slug
            tpl_paste["slug"] = o_paste.slug)
            tpl_paste["u"] = paste.url("%s", o_paste.slug)
            tpl_paste["snippet"] = o_paste.snippet
            tpl_paste["is_moderated"] = o_paste.is_moderated

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
                tpl_paste["posted_at"] = o_paste.posted_at.strftime(paste.config["datetime.format"])
            else:
                tpl_paste["posted_at"] = ""

            if o_paste.characters:
                tpl_paste["size"] = paste.util.make_filesize_readable(o_paste.characters)
            tpl_paste["lines"] = o_paste.lines
            if o_paste.language:
                tpl_paste["language"] = o_paste.language
            else:
                tpl_paste["language"] = ""

            tpl_pastes.append(tpl_paste)

        return tpl_pastes
