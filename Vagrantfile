# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  
  config.vm.box = "oel65-64"
  config.vm.hostname = "docs-apt-dev"
  config.vm.network :forwarded_port, guest: 8888, host: 8888
  config.vm.synced_folder "./", "/vagrant"
  config.ssh.forward_agent = true

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  #
  # allow for vpn connections
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
  end

  #
  # system init
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.manifest_file = "dev.pp"
    puppet.module_path = "puppet/modules"
  end

  #
  # database setup
  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet/manifests"
    puppet.manifest_file = "database.pp"
    puppet.module_path = "puppet/modules"
  end
end
