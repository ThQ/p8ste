dPYGMENTS=src/pygments
dRECAPTCHA=src/recaptcha
fPASTE_PRIVATE=src/paste/private.py
fPASTE_PRIVATE_TEMPLATE=src/paste/private_TEMPLATE.py

check-install: check-pygments check-recaptcha check-paste-private

check-pygments:
	@if [ ! -d "${dPYGMENTS}" ] ; then echo "Pygments does not seem to be installed. Download it from http://pygments.org/download/ and extract it to ${dPYGMENTS}." ; fi

check-recaptcha:
	@if [ ! -d "${dRECAPTCHA}" ] ; then echo "Recaptcha does not seem to be installed. Download it from http://pypi.python.org/pypi/recaptcha-client and extract it to ${dRECAPTCHA}." ; fi

check-paste-private:
	@if [ ! -f "${fPASTE_PRIVATE}" ] ; then echo "${fPASTE_PRIVATE} cannot be found. Rename ${fPASTE_PRIVATE_TEMPLATE} to ${fPASTE_PRIVATE}" ; fi
