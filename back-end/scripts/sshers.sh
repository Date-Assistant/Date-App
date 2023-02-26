#!/bin/bash

#rabbitmq
ssh -t brian@10.241.51.24 "sudo systemctl start rabbitmq-server && sudo systemctl status rabbitmq-server"
exit

#front-end
ssh -t brian@10.241.228.14 "sudo systemctl start apache2 && sudo systemctl status apache2"
exit

#

#database
ssh -t brian@10.241.217.38 "sudo systemctl start mariadb && sudo systemctl status mariadb"
exit