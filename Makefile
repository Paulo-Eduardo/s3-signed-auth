install:
	easy_install pip
	pip install --upgrade -r requirements.txt

dev-env: install
	pip install --upgrade -r dev-requirements.txt

pep8:
	py.test --pep8 -rs --clearcache -m pep8 s3signedauth tests

test: pep8
	py.test -rxs --clearcache tests
