# Generic leaf-spine network topology for vagrant
#
#
#
#    NOTE: in order to use this Vagrantfile you will need:
#       -Vagrant(v1.8.6+) installed: http://www.vagrantup.com/downloads
#       -Virtualbox installed: https://www.virtualbox.org/wiki/Downloads

Vagrant.require_version ">= 2.0.1"

$script = <<SCRIPT
git clone https://github.com/IPvSean/ansible-networking-vagrant-demo
chown -R vagrant:vagrant ansible-networking-vagrant-demo
cp /home/vagrant/ansible-networking-vagrant-demo/training-course/ansible.cfg /home/vagrant/.ansible.cfg
cp /home/vagrant/ansible-networking-vagrant-demo/training-course/etchosts /etc/hosts
yum install python-pip tree -y
pip install git+https://github.com/ansible/ansible.git@devel
pip install netaddr
SCRIPT

Vagrant.configure("2") do |config|

  simid = 1
# FOR VYOS
  network_os = "samdoran/vyos"
  network_memory = 256

#FOR CUMULUS VX
  # network_os = "CumulusCommunity/cumulus-vx"
  # network_memory = 768

  config.vm.provider "virtualbox" do |v|
    v.gui=false
  end

  ##### DEFINE VM for ansible tower #####
  config.vm.define "ansible" do |device|
      device.vm.hostname = "ansible"
      device.vm.box = "ansible/tower"
      device.vm.network :forwarded_port, guest: 22, host: 6010
      device.vm.network "private_network", virtualbox__intnet: "1_mgmt", ip: "172.16.10.2"
      device.vm.provision "shell", inline: $script
  end

  ##### DEFINE VM for leaf01 #####
  config.vm.define "leaf01" do |device|
    device.vm.hostname = "leaf01"
    device.vm.box = "#{network_os}"
    device.vm.network "forwarded_port", guest: 22, host: 6001
    device.vm.provider "virtualbox" do |v|
      v.name = "#{simid}_leaf01"
      v.customize ["modifyvm", :id, '--audiocontroller', 'AC97', '--audio', 'Null']
      v.memory = network_memory
    end
    #   see note here: https://github.com/pradels/vagrant-libvirt#synced-folders
    device.vm.synced_folder ".", "/vagrant", disabled: true

    # NETWORK INTERFACES
      # eth1 mgmt network for ansible tower
      device.vm.network "private_network", ip: "172.16.10.11", virtualbox__intnet: "#{simid}_mgmt"
      # link for eth2 --> server01:eth1
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net2", auto_config: false
      # link for eth3 --> server02:eth1
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net12", auto_config: false
      # link for eth4 --> leaf02:eth4
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net10", auto_config: false
      # link for eth5 --> leaf02:eth5
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net1", auto_config: false
      # link for eth6 --> spine01:eth2
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net52", auto_config: false
      # link for eth7 --> spine02:eth2
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net23", auto_config: false

    device.vm.provider "virtualbox" do |vbox|
      vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc5', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc6', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc7', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc8', 'allow-all']
    end
end
 ##### DEFINE VM for leaf02 #####
 config.vm.define "leaf02" do |device|

	 device.vm.hostname = "leaf02"
	 device.vm.box = "#{network_os}"
    device.vm.network "forwarded_port", guest: 22, host: 6002
	 device.vm.provider "virtualbox" do |v|
		 v.name = "#{simid}_leaf02"
		 v.customize ["modifyvm", :id, '--audiocontroller', 'AC97', '--audio', 'Null']
		 v.memory = network_memory
	 end
	 #   see note here: https://github.com/pradels/vagrant-libvirt#synced-folders
	 device.vm.synced_folder ".", "/vagrant", disabled: true

	 # NETWORK INTERFACES
     # mgmt network for ansible tower
     device.vm.network "private_network", ip: "172.16.10.12", virtualbox__intnet: "#{simid}_mgmt"
		 # link for eth2 --> server01:eth2
		 device.vm.network "private_network", virtualbox__intnet: "#{simid}_net13", auto_config: false
		 # link for eth3 --> server02:eth2
		 device.vm.network "private_network", virtualbox__intnet: "#{simid}_net15", auto_config: false
		 # link for eth4 --> leaf01:eth4
		 device.vm.network "private_network", virtualbox__intnet: "#{simid}_net10", auto_config: false
		 # link for eth5 --> leaf01:eth5
		 device.vm.network "private_network", virtualbox__intnet: "#{simid}_net1", auto_config: false
		 # link for eth6 --> spine01:eth3
		 device.vm.network "private_network", virtualbox__intnet: "#{simid}_net25", auto_config: false
		 # link for eth7 --> spine02:eth3
		 device.vm.network "private_network", virtualbox__intnet: "#{simid}_net58", auto_config: false

	 device.vm.provider "virtualbox" do |vbox|
		 vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-all']
		 vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-all']
		 vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-all']
		 vbox.customize ['modifyvm', :id, '--nicpromisc5', 'allow-all']
		 vbox.customize ['modifyvm', :id, '--nicpromisc6', 'allow-all']
		 vbox.customize ['modifyvm', :id, '--nicpromisc7', 'allow-all']
	 end
end

  ##### DEFINE VM for spine01 #####
  config.vm.define "spine01" do |device|

    device.vm.hostname = "spine01"
    device.vm.box = "#{network_os}"
    device.vm.network "forwarded_port", guest: 22, host: 6003
    device.vm.provider "virtualbox" do |v|
      v.name = "#{simid}_spine01"
      v.customize ["modifyvm", :id, '--audiocontroller', 'AC97', '--audio', 'Null']
      v.memory = network_memory
    end
    #   see note here: https://github.com/pradels/vagrant-libvirt#synced-folders
    device.vm.synced_folder ".", "/vagrant", disabled: true

    # NETWORK INTERFACES
      # mgmt network for ansible tower
      device.vm.network "private_network", ip: "172.16.10.13", virtualbox__intnet: "#{simid}_mgmt"
      # link for spine01:eth2 --> leaf01:eth6
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net52", auto_config: false
      # link for spine01:eth3 --> leaf02:eth6
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net25", auto_config: false
      # link for spine01:eth4 --> spine02:eth4
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net45", auto_config: false
      # link for spine01:eth5 --> spine02:eth5
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net36", auto_config: false

    device.vm.provider "virtualbox" do |vbox|
      vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc5', 'allow-all']
    end
end

  ##### DEFINE VM for spine02 #####
  config.vm.define "spine02" do |device|

    device.vm.hostname = "spine02"
    device.vm.box = "#{network_os}"
    device.vm.network "forwarded_port", guest: 22, host: 6004
    device.vm.provider "virtualbox" do |v|
      v.name = "#{simid}_spine02"
      v.customize ["modifyvm", :id, '--audiocontroller', 'AC97', '--audio', 'Null']
      v.memory = network_memory
    end
    #   see note here: https://github.com/pradels/vagrant-libvirt#synced-folders
    device.vm.synced_folder ".", "/vagrant", disabled: true

    # NETWORK INTERFACES
      # mgmt network for ansible tower
      device.vm.network "private_network", ip: "172.16.10.14", virtualbox__intnet: "#{simid}_mgmt"
      # link for spine02:eth2 --> leaf01:eth6
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net23", auto_config: false
      # link for spine02:eth3 --> leaf02:eth6
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net58", auto_config: false
      # link for spine02:eth4 --> spine01:eth4
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net45", auto_config: false
      # link for spine02:eth5 --> spine01:eth5
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net36", auto_config: false

    device.vm.provider "virtualbox" do |vbox|
      vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc5', 'allow-all']
    end
end

  ##### DEFINE VM for server01 #####
  config.vm.define "server01" do |device|

    device.vm.hostname = "server01"
    device.vm.box = "centos/7"
    device.vm.provider "virtualbox" do |v|
      v.name = "#{simid}_server01"
      v.customize ["modifyvm", :id, '--audiocontroller', 'AC97', '--audio', 'Null']
      v.memory = 512
    end
    #   see note here: https://github.com/pradels/vagrant-libvirt#synced-folders
    device.vm.synced_folder ".", "/vagrant", disabled: true

    # NETWORK INTERFACES
      # server01:eth1 mgmt network for ansible tower
      device.vm.network "private_network", ip: "172.16.10.15", virtualbox__intnet: "#{simid}_mgmt"
      # link for server01:eth2 --> leaf01:eth2
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net2", auto_config: false
      # link for server01:eth3 --> leaf02:eth2
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net13", auto_config: false

    device.vm.provider "virtualbox" do |vbox|
      vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-all']
    end
end
  ##### DEFINE VM for server02 #####
  config.vm.define "server02" do |device|

    device.vm.hostname = "server02"
    device.vm.box = "centos/7"
    device.vm.provider "virtualbox" do |v|
      v.name = "#{simid}_server02"
      v.customize ["modifyvm", :id, '--audiocontroller', 'AC97', '--audio', 'Null']
      v.memory = 512
    end
    #   see note here: https://github.com/pradels/vagrant-libvirt#synced-folders
    device.vm.synced_folder ".", "/vagrant", disabled: true

    # NETWORK INTERFACES
      # server02:eth1 mgmt network for ansible tower
      device.vm.network "private_network", ip: "172.16.10.16", virtualbox__intnet: "#{simid}_mgmt"
      # link for server02:eth2 --> leaf01:eth3
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net12", auto_config: false
      # link for server02:eth3 --> leaf02:eth3
      device.vm.network "private_network", virtualbox__intnet: "#{simid}_net15", auto_config: false

    device.vm.provider "virtualbox" do |vbox|
      vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-all']
      vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-all']
    end
end

end
