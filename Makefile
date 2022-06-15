ha:
	yum install -y epel-release 
	yum clean all
	yum install -y git ansible
	ansible-playbook os_init.yml 
