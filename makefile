dLIBS=src/libs
dPYGMENTS=${dLIBS}/pygments
dRECAPTCHA=${dLIBS}/recaptcha
fSETTINGS=src/settings.py
fSETTINGS_TEMPLATE=src/settings_TEMPLATE.py
dROOT=.
dSRC=${dROOT}/src

check-install:check-settings
	python ${dSRC}/test_install.py

check-settings:
	@if [ ! -f "${fSETTINGS}" ] ; then echo "${fSETTINGS} cannot be found. Rename ${fSETTINGS_TEMPLATE} to ${fSETTINGS}" ; fi

deploy:
	python ${APPENGINE_PATH}/appcfg.py update ${dSRC}

pep8:
	find . -iname "*.py" -not -wholename "*pygments*" -not -wholename "*recaptcha*" -not -wholename "*feedparser*" -exec pep8 {} \;

run:
	python ${APPENGINE_PATH}/dev_appserver.py ${dSRC}

upload: deploy
