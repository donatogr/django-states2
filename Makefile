DOCS_MAKE_CMD = html dirhtml latex latexpdf

.PHONY: $(DOCS_MAKE_CMD) docs clean test coverage release authors changelog

docs: $(DOCS_MAKE_CMD)

$(DOCS_MAKE_CMD):
	DJANGO_SETTINGS_MODULE=test_proj.settings $(MAKE) -C docs $@

clean: docs_clean
	$(MAKE) -C docs clean
	rm -rf dist django_states.egg-info
	find . -name '*pyc' -delete

test:
	tox

coverage:
	coverage run --source='.' test_proj/runtests.py
	coverage html --include="django_states*" --omit="*test*" --directory=.direnv/htmlcov
	coverage report --include="django_states*" --omit="*test*"

release: changelog
	@echo "Updating setup.py"
	@cp setup.py setup.py.bak
	@rm -f setup.py
	@sed 's/version=".*",/version="${VERSION}",/' setup.py.bak > setup.py
	@rm -f setup.py.bak
	@chmod +x setup.py
	@git add setup.py
	@echo "Updating django_states/__init__.py"
	@cp django_states/__init__.py django_states/__init__.py.bak
	@rm -f django_states/__init__.py
	@sed 's/__version__ = ".*"/__version__ = "${VERSION}"/' django_states/__init__.py.bak > django_states/__init__.py
	@rm -f django_states/__init__.py.bak
	@git add django_states/__init__.py
	@git commit -m "Bump version to v${VERSION}"
	@echo "Look through the CHANGELOG.rst file, clean it up and commit it:"
	@echo "  	git add CHANGELOG.rst && git commit --amend"
	@echo "When you're done, please run:"
	@echo "     git tag -a ${VERSION} -m \"django-states2 v${VERSION}\""

authors:
	@echo "Updating AUTHORS file"
	@rm -f AUTHORS && git log --all --format="%aN <%aE>" | sort -u > AUTHORS

changelog:
	@echo "Updating CHANGELOG.rst file"
	@rm -f CHANGELOG.new && touch CHANGELOG.new
	@echo "~~~~~~~~~" >> CHANGELOG.new
	@echo "CHANGELOG" >> CHANGELOG.new
	@echo "~~~~~~~~~" >> CHANGELOG.new
	@echo "v${VERSION} - $$(date +'%Y-%m-%d')" >> CHANGELOG.new
	@echo "v${VERSION} - $$(date +'%Y-%m-%d')" | sed "s/./=/g" >> CHANGELOG.new
	@git log $$(git describe --tags --abbrev=0)..HEAD --pretty=format:"- %s" >> CHANGELOG.new
	@echo "\n" >> CHANGELOG.new
	@tail -n +4  CHANGELOG.rst >> CHANGELOG.new
	@mv CHANGELOG.new CHANGELOG.rst
