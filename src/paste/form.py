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

import datetime
import hashlib
import paste
import paste.model
import settings

def delete_token(ip_address, stoken):
    token = paste.model.Form()
    token.token = stoken
    token.created_by_ip = ip_address

    try:
        token.delete()
        result = True
    except:
        result = False

    return result

def has_valid_token(ip_address, token):
    tokens = paste.model.Form.all()
    tokens.filter("token =", token)
    tokens.filter("created_by_ip =", ip_address)
    tokens.filter("expired_at >", datetime.datetime.now())
    return tokens.get() != None

def put_form_token(ip_address, token=""):
    if token == "":
        token = make_token()

    ftoken = paste.model.Form()
    ftoken.token = token
    ftoken.created_at = datetime.datetime.now()
    ftoken.created_by_ip = ip_address
    ftoken.expired_at = datetime.datetime.now() + settings.PASTE_FORM_EXPIRATION_DELTA
    key = ftoken.put()
    if key != "":
        return token
    else:
        return ""

def make_token():
    hash = hashlib.sha256()
    hash.update(datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:BONOBO"))
    return hash.hexdigest()
