#
# Database setup
#

class psql_db{
	class{'postgresql::globals':
		manage_package_repo => true,
		encoding => 'UTF8',
		version => '8.4'
	} ->
	class{'postgresql::server':
		listen_addresses => '*',
		postgres_password => 'bot'
	}
	postgresql::server::db{'data':
		user => 'vagrant',
		password => postgresql_password('vagrant', 'bot'),
		encoding => 'UTF8'
	}
}

include psql_db