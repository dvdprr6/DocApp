#
# install python3
#

class python3{
	exec{"download-python3":
		command => 'wget -q http://www.python.org/ftp/python/3.4.2/Python-3.4.2.tar.xz --no-check-certificate',
		cwd => '/home/vagrant/',
		creates => '/home/vagrant/Python-3.4.2.tar.xz',
		user => vagrant,
		timeout => 0,
		require => Class['system-update']
	}->
	exec{"untar-python":
		command => 'tar xJf Python-3.4.2.tar.xz',
		cwd => '/home/vagrant',
		creates => '/home/vagrant/Python-3.4.2',
		user => vagrant,
		require => Class['system-update']
	}->
	exec{"configure-python":
		command => 'sh configure --prefix=/opt.python3.4',
		cwd => '/home/vagrant/Python-3.4.2',
		user => vagrant,
		require => Class['system-update']
	}->
	exec{"install-python":
		command => 'make && make install',
		cwd => '/home/vagrant/Python-3.4.2',
		user => root,
		require => Class['system-update']
	}
}