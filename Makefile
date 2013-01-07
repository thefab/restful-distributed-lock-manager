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
	rm -f MANIFEST
	rm -Rf build
	rm -Rf dist
	rm -f *.rst
	rm -Rf rdlm.egg-info

sdist: clean
	python setup.py sdist

test:
	cd tests && python -m tornado.test.runtests test_home test_lock

rst:
	cat README.md |pandoc --from=markdown --to=rst >README.rst

upload: rst
	python setup.py sdist register upload

coverage:
	cd tests && coverage run `which nosetests` && coverage html --include='*/restful-distributed-lock-manager/*' --omit='test_*'

release: test coverage clean upload clean 
