restful-distributed-lock-manager (RDLM)
=======================================

What is it ?
------------

``RDLM`` (Restful Distributed Lock Manager) is a lock manager over HTTP
built on `Tornado <http://www.tornadoweb.org/>`_.

Special features
----------------

-  RESTful interface
-  Timeout automatic management (to avoid stale locks)
-  Blocking wait for acquiring a lock (with customatizable timeout)
-  Very fast (in memory)
-  One unique single threaded process
-  Can deal with thousands of locks and simultaneous connections
-  Administrative password protected requests

Quickstart
----------

Installation
~~~~~~~~~~~~

::

    pip install rdlm

    Requirements: 
    - Python 2.6, 2.7, 3.2 or 3.3
    - Tornado >= 2.3

Starting the daemon
~~~~~~~~~~~~~~~~~~~

::

    rdlm-daemon.py --port=8888 --logging=debug

    (rdlm-daemon.py --help for the full list of options)

API
---

The complete HTTP API is described in `this specific document <https://github.com/thefab/restful-distributed-lock-manager/blob/0.4/API.md>`_.

If you prefer a pure python API, you can also have a look at : `this specific project <https://github.com/thefab/rdlm-py>`_.
