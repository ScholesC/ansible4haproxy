ha:
	yum install -y epel-release 
	yum clean all
	yum install -y git ansible
	git pull
	ansible-playbook os_init.yml 
