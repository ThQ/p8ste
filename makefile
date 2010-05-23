dLIBS=src/libs
dPYGMENTS=${dLIBS}/pygments
dRECAPTCHA=${dLIBS}/recaptcha
fSETTINGS=src/settings.py
fSETTINGS_TEMPLATE=src/settings_TEMPLATE.py
dROOT=.
dSRC=${dROOT}/src

check-install: check-pygments check-recaptcha check-settings

check-pygments:
	@if [ ! -d "${dPYGMENTS}" ] ; then \
		echo "Pygments does not seem to be installed. Download it from http://pygments.org/download/ and extract it to ${dPYGMENTS}." ; \
	fi

check-recaptcha:
	@if [ ! -d "${dRECAPTCHA}" ] ; then \
		echo "Recaptcha-client does not seem to be installed. Download it from http://pypi.python.org/pypi/recaptcha-client and extract it to ${dRECAPTCHA}." ; \
	fi

check-settings:
	@if [ ! -f "${fSETTINGS}" ] ; then echo "${fSETTINGS} cannot be found. Rename ${fSETTINGS_TEMPLATE} to ${fSETTINGS}" ; fi

deploy:
	python ${APPENGINE_PATH}/appcfg.py update ${dSRC}

pep8:
	find . -iname "*.py" -not -wholename "*pygments*" -not -wholename "*recaptcha*" -not -wholename "*feedparser*" -exec pep8 {} \;

run:
	python ${APPENGINE_PATH}/dev_appserver.py ${dSRC}

upload: deploy
