##Alembic Information
Generic single-database configuration

* Current version: `alembic -c /etc/docs_apt/docs.conf current`
* Autogen a revision: `alembic -c /etc/docs_apt/docs.conf revision --autogenerate -m "some message"`
* History: `alembic -c /etc/docs_apt/docs.conf history`

INIT:
`alembic -c /etc/docs_apt/docs.conf upgrade head` which will add an `alembic_version` table with the number

######THEN..

1. Update the models in the db module
2. Autogenerate the version upgrade (see above) and validate it
3. Update the database: `alembic -c /etc/docs_apt/docs.conf upgrade`

######First-time Deploy:
`alembic -c /etc/docs_apt/docs.conf upgrade head --sql > migrate.sql`