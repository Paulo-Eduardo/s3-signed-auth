install:
	easy_install pip
	pip install --upgrade -r requirements.txt

dev-env: install
	pip install --upgrade -r dev-requirements.txt
