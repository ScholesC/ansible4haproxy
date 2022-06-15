#!/bin/bash
#
yum install -y git wget
git clone https://github.com/ScholesC/ansible4haproxy.git
cd ansible4haproxy && make
