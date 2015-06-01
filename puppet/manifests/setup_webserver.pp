#
# setup the webserver
#

class setup_webserver{
	$work_path = '/usr/local/bin/:/usr/local/:/usr/bin/:/bin/:/opt/python3.4/bin'
	exec{"python-env":
		command => '/opt/python3.4/bin/python3.4 -m venv /home/vagrant/pyEnv',
		cwd => '/home/vagrant',
		path => $work_path,
		user => vagrant
	}->
	exec{"install-setuptools":
		command => 'curl https://bootstrap.pypa.io/ez_setup.py -o - | /home/vagrant/pyEnv/bin/python',
		cwd => '/home/vagrant',
		path => $work_path,
		user => vagrant,
		timeout => 0
	}->
	exec{"install-pip":
		command => '/home/vagrant/pyEnv/bin/easy_install pip',
		cwd => '/home/vagrant',
		path => $work_path,
		user => vagrant,
		timeout => 0
	}->
	exec{"setup":
		command => '/home/vagrant/pyEnv/bin/python setup.py develop',
		cwd => '/vagrant/server',
		path => $work_path,
		user => vagrant,
		timeout => 0
	}->
	file{"/etc/docs_apt/docs.conf":
		ensure => "file",
		source => "file:///vagrant/server/conf/dev/docs.conf"
	}->
	exec{"init-database":
		command => '/home/vagrant/pyEnv/bin/python scripts/initdb.py --config=/etc/docs_apt/docs.conf',
		cwd => '/vagrant/server',
		path => $work_path,
		user => vagrant
	}->
	exec{"python-at-startup":
		command => 'echo ". /home/vagrant/pyEnv/bin/activate" >> /home/vagrant/.bashrc',
		cwd => '/home/vagrant',
		path => $work_path,
		user => vagrant
	}
}

include setup_webserver