.PHONY: pypi-upload

pypi-upload:
	python setup.py sdist upload -r pypi
