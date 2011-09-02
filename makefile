dROOT=.
dSRC=${dROOT}/src
dLIBS=${dSRC}/libs
dPYGMENTS=${dLIBS}/pygments
dRECAPTCHA=${dLIBS}/recaptcha
fSETTINGS=${dSRC}/settings.py
fSETTINGS_TEMPLATE=${dSRC}/settings_TEMPLATE.py

images-archive:
	tar czf p8ste_images.tar.gz src/static/images

check-install:check-settings
	python ${dSRC}/test_install.py

check-settings:
	@if [ ! -f "${fSETTINGS}" ] ; then echo "${fSETTINGS} cannot be found. Rename ${fSETTINGS_TEMPLATE} to ${fSETTINGS}" ; fi

deploy:
	python ${APPENGINE_PATH}/appcfg.py update ${dSRC}

install-python-dependencies:
	sh install_package.sh http://pypi.python.org/packages/source/P/Pygments/Pygments-1.4.tar.gz pygments ${dLIBS}
	sh install_package.sh http://pypi.python.org/packages/source/f/feedparser/feedparser-5.0.1.tar.gz feedparser ${dLIBS} feedparser.py
	sh install_package.sh http://pypi.python.org/packages/source/r/recaptcha-client/recaptcha-client-1.0.6.tar.gz recaptcha ${dLIBS}

pep8:
	find . -iname "*.py" -not -wholename "*pygments*" -not -wholename "*recaptcha*" -not -wholename "*feedparser*" -exec pep8 {} \;

run:
	python ${APPENGINE_PATH}/dev_appserver.py ${dSRC}

upload: deploy
