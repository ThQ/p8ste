# What is it ?

   Paste-It is a python pastebin (where you paste code) for Google AppEngine. It
is licensed under GPLv3.

More infos:

* http://en.wikipedia.org/wiki/Pastebin
* http://python.org
* http://code.google.com/appengine/
* http://www.gnu.org/licenses/gpl-3.0.html



# Dependencies

* [Python][python]
* [Google AppEngine][gae]
* [Pygments][pygments]
* [recaptcha-client][recaptcha-client]



# Installation

* Download the latest source from
    `http://github.com/thomas-quemard/p8ste/tarball/master`
  and extract it to a local directory.

* Install [pygments][pygments] system wide or extract it to `/path/to/paste-it/`

* Install [recaptcha-client][recaptcha-client] system wide or extract it to `/path/to/paste-it/`

*  Run
   `cd /path/to/pate-it && make check-install`

* Don't forget to check `src/paste/__init__.py` and `src/paste/private.py`
  for configuration options.



# Run

    cd /path/to/google_appengine/
    python dev_appserver.py /path/to/paste-it/src



[gae]: http://code.google.com/appengine/
[pygments]: http://pygments.org
[python]: http://pythong.org
[recaptcha-client]: http://pypi.python.org/pypi/recaptcha-client
