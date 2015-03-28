#
# system related libraries
#

class system-update{
	exec{'yum-update':
		command => 'yum update -y',
		timeout => 0
	}
	$sysPackages = [
		"curl",
		"wget",
		"vim",
		"git",
		"openssl-devel",
		"nodejs",
		"nodejs-devel",
		"npm",
		"sqlite-devel",
		"sqlite",
		"postgresql",
		"postgresql-devel",
		"nginx"
	]
	package{$sysPackages:
		ensure => "latest",
		require => Exec['yum-update']
	}
}