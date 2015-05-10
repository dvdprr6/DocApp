#
# Setup the dev environment
#

Exec { path => ["/bin/", "/sbin/", "/usr/bin", "/usr/sbin/" ] }

class doc-apt-webapp{
	file{"/etc/rc.d/init.d/docsaptwebapp":
		ensure => 'link',
		target => '/vagrant/server/conf/docsaptwebapp',
		owner => root,
		mode => '755',
	}->
	file{"/etc/docs_apt/":
		ensure => 'directory'
	}

}

include doc-apt-webapp
include python3
include system-update