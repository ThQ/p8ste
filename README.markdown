# What is it ?

   **Paste-It** is a [python](http://python.org) [pastebin](http://en.wikipedia.org/wiki/Pastebin) (where you paste code) for [Google AppEngine](http://code.google.com/appengine/). It
is licensed under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.html).



# Dependencies

* [Pygments][pygments]
* [recaptcha-client][recaptcha-client]
* [FeedParser][feedparser]



# Installation

* Download the latest source from
    `http://github.com/thomas-quemard/p8ste/tarball/master`
  and extract it to a local directory.

* Run `make install-python-dependencies` or extract python dependencies to `/path/to/p8ste/src/`

*  Run
   `cd /path/to/paste-it && make check-install`


Note : The repository does not contain images, if you want them, download the following archive :
https://github.com/downloads/thomas-quemard/p8ste/p8ste_images.tar.gz



# Run

    cd /path/to/google_appengine/
    python dev_appserver.py /path/to/p8ste/src



[gae]: http://code.google.com/appengine/
[pygments]: http://pygments.org
[python]: http://pythong.org
[recaptcha-client]: http://pypi.python.org/pypi/recaptcha-client
[feedparser]:http://www.feedparser.org/
