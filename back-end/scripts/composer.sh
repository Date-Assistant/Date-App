#!/bin/bash

# database-server

ssh -t it490admin@10.0.0.207 '''STATUS="$(systemctl is-active 
mariadb)"
if [ "${STATUS}" = "active" ]; then
RESPONSE="true"
else
RESPONSE="false"
if [ "${RESPONSE}" = "true" ]; then
systemctl status mariadb
else
systemctl enable mariadb
systemctl start mariadb
exit 1
'''


#sudo systemctl enable apache2
#sudo systemctl start apache2
#sudo systemctl status apache2
