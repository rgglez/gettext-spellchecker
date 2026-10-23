# Build, check and publish the gettext-spellchecker package.
#
# Two ways to publish:
#   - make release: tags vX.Y.Z and pushes the tag; the Publish GitHub workflow
#     uploads to PyPI with Trusted Publishing (no tokens needed).
#   - make publish-test / make publish: uploads from this machine with twine,
#     using the API tokens in ~/.pypirc or TWINE_USERNAME / TWINE_PASSWORD.
# Already published versions are skipped, bump the version to publish again.

PYTHON ?= python3
VERSION := $(shell sed -n 's/^__version__ = "\(.*\)"/\1/p' src/gettext_spellchecker/version.py)

.PHONY: help dev lint test build check publish-test publish release clean

help:
	@echo "make dev           install the package in editable mode and the dev tools"
	@echo "make lint          flake8"
	@echo "make test          pytest"
	@echo "make build         build sdist and wheel into dist/"
	@echo "make check         lint, test, build and twine check"
	@echo "make publish-test  upload dist/ to TestPyPI with twine"
	@echo "make publish       upload dist/ to PyPI with twine"
	@echo "make release       tag v$(VERSION) and push it, the Publish workflow uploads to PyPI"
	@echo "make clean         remove build artifacts"

dev:
	$(PYTHON) -m pip install -e . pytest flake8 build twine

lint:
	$(PYTHON) -m flake8 src tests

test:
	$(PYTHON) -m pytest

build: clean
	$(PYTHON) -m build --outdir dist

check: lint test build
	$(PYTHON) -m twine check --strict dist/*

publish-test: check
	$(PYTHON) -m twine upload --repository testpypi --skip-existing dist/*

publish: check
	@read -p "Upload dist/ to PyPI? Published versions can't be replaced [y/N] " answer && [ "$$answer" = y ]
	$(PYTHON) -m twine upload --skip-existing dist/*

release: check
	@git diff --quiet HEAD || { echo "Commit your changes first"; exit 1; }
	@read -p "Tag v$(VERSION) and push it to origin? [y/N] " answer && [ "$$answer" = y ]
	git tag -a v$(VERSION) -m "v$(VERSION)"
	git push origin v$(VERSION)

clean:
	rm -rf dist build src/*.egg-info
