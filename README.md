impala
======

`impala` is the Inventory of Music for Perusal, Acquisition, and Library
Administration. This is a Flask application which stores an inventory of
physical and digitized music along with a catalog of album metadata in
PostgreSQL.

The following applications currently work with impala, either directly or
indirectly.
- smuggler (an import service)
- [moss](https://github.com/wuvt/moss) (an object store for entire albums)


Components so far
=================

- Versioned api ('/api') with PUT/POST for each model. Verson 1 is currently
  stable.
- Authentication with two roles (user and librarian)
- Catalog models


Running a dev server
====================

``
pip install -r requirements.txt
export FLASK_APP=impala
export FLASK_DEBUG=1
flask run
``

If you change the schema:
``
flask db migrate
flask db upgrade
``

TODO (in order)
===============
- Frontend build-out 
    - Holding detail page
    - HoldingGroup detail page
    - Search results should use our existing search API
    - Add auth
    - Support for reporting holdings/holding groups as bad
    - Support for adding non-digital holdings
    - Support for editing non-digital holdings
- uwsgi file
- Containerize
