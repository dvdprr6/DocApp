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
    }->
    exec{"unlink-localtime":
        command => 'unlink /etc/localtime',
        cwd => '/home/vagrant',
        user => root
    }->
    file{"/etc/localtime":
        ensure => 'link',
        target => '/usr/share/zoneinfo/Canada/Eastern',
        owner => root
    }

}

include doc-apt-webapp
include python3
include system-update