clean:
	rm -f *.pyc
	cd tests && rm -f *.pyc
	cd rdlm && rm -f *.pyc
	cd tests && rm -Rf htmlcov 
	rm -f .coverage tests/.coverage
	rm -f tests/rdlm

link: 
	if ! test -L tests/rdlm; then ln -s ../rdlm tests/rdlm; fi

test: link
	cd tests && python -m tornado.test.runtests test_home test_lock

coverage: link
	cd tests && coverage run `which nosetests` && coverage html --include='*/restful-distributed-lock-manager/*' --omit='test_*'