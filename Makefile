default: all

all:
	python setup.py build

install: all
	python setup.py install

clean:
	rm -f *.pyc
	cd tests && rm -f *.pyc
	cd rdlm && rm -f *.pyc
	cd tests && rm -Rf htmlcov 
	rm -f .coverage tests/.coverage
	rm -f tests/rdlm
	rm -f rdlm/rdlm
	rm -f MANIFEST
	rm -Rf build
	rm -Rf dist
	rm -f *.rst

sdist: clean
	python setup.py sdist --no-defaults

link: 
	if ! test -L tests/rdlm; then ln -s ../rdlm tests/rdlm; fi

test: link
	cd tests && python -m tornado.test.runtests test_home test_lock

rst:
	cat README.md |pandoc --from=markdown --to=rst >README.rst

coverage: link
	cd tests && coverage run `which nosetests` && coverage html --include='*/restful-distributed-lock-manager/*' --omit='test_*'
