impala
======

`impala` is the Inventory of Music for Perusal, Acquisition, and Library
Administration. This is a Flask application which stores an inventory of
physical and digitized music along with a catalog of album metadata in
PostgreSQL.

The following applications currently work with impala, either directly or
indirectly.
- [smuggler](https://github.com/wuvt/smuggler) (an import service)
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
- Containerize
- uwsgi file
- Frontend build-out 
    - Holding detail page
    - HoldingGroup detail page
    - Search results should use our existing search API
    - Add auth
    - Support for reporting holdings/holding groups as bad
    - Support for adding non-digital holdings
    - Support for editing non-digital holdings
- Add a background deduplicator service

License
=======

    Copyright (C) 2017 Matt Hazinski and mutantmonkey

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
