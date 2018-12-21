=============================
Flask Mega Tutorial Microblog
=============================
https://courses.miguelgrinberg.com/

Frameworks
==========

* `Flask-Login <https://flask-login.readthedocs.io/>`_, login management
* `Flask-Migrate <https://flask-migrate.readthedocs.io/en/latest/>`_, database management using Alembic
* `Flask-SQLAlchemy <http://flask-sqlalchemy.pocoo.org/>`_, database ORM
* `Flask-WTF <https://flask-wtf.readthedocs.io/>`_, a thin wrapper around `WTForms <https://wtforms.readthedocs.io/>`_
* `Flask-Mail <https://pythonhosted.org/Flask-Mail/>`_
* `PyJWT <https://pyjwt.readthedocs.io/en/latest/>`_, which uses `JSON Web Tokens <https://jwt.io/>`_
* `Flask-Bootstrap <https://pythonhosted.org/Flask-Bootstrap/>`_, which uses `Bootstrap <http://getbootstrap.com/>`_ for HTML
* `Flask-Moment <https://github.com/miguelgrinberg/Flask-Moment>`_, which makes it easy to incorporate `moment.js <http://momentjs.com>`_
* `Flask-Babel <https://pythonhosted.org/Flask-Babel/>`_ for internationalization


Initialize SQLite Database
==========================

.. code:: bash

    (flask-mega-tutorial-microblog) aimeeu@aimeeu-7520:~/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog$ flask db init
    Creating directory /home/aimeeu/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog/migrations ... done
    Creating directory /home/aimeeu/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog/migrations/versions ... done
    Generating /home/aimeeu/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog/migrations/alembic.ini ... done
    Generating /home/aimeeu/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog/migrations/README ... done
    Generating /home/aimeeu/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog/migrations/script.py.mako ... done
    Generating /home/aimeeu/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog/migrations/env.py ... done
    Please edit configuration/connection/logging settings in '/home/aimeeu/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog/migrations/alembic.ini' before proceeding.
    (flask-mega-tutorial-microblog) aimeeu@aimeeu-7520:~/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog$ flask db migrate -m "user and posts tables"
    INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.autogenerate.compare] Detected added table 'user'
    INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'
    INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'
    INFO  [alembic.autogenerate.compare] Detected added table 'post'
    INFO  [alembic.autogenerate.compare] Detected added index 'ix_post_timestamp' on '['timestamp']'
    Generating /home/aimeeu/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog/migrations/versions/28211911574d_user_and_posts_tables.py ... done
    (flask-mega-tutorial-microblog) aimeeu@aimeeu-7520:~/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog$ flask db upgrade
    INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> 28211911574d, user and posts tables
    (flask-mega-tutorial-microblog) aimeeu@aimeeu-7520:~/Dev/git/github.com/aimeeu/flask-mega-tutorial-microblog$
