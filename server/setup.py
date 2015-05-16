from setuptools import setup, find_packages

version = '0.0.1'

install_requires = [
	'SQLAlchemy==0.9.4',
	'alembic==0.7.1',
	'psycopg2==2.5.4',
	'tornado==4.0.2',
	'colour-runner'
]

setup(
	name='Doctor-Appointment-App',
	version=version,
	description=('Application for doctors to manager their appointments with patients'),
	author='David Parr',
	author_email='dvdprr6@gmail.com',
	packages=find_packages(),
	install_requires=install_requires,
	entry_points={
		'console_scripts':['docsaptwebapp = doctor.webserver:main']
	}
)