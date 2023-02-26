#!/bin/bash

#rabbitmq
ssh -t lap@10.241.51.24 "sudo systemctl start rabbitmq-server && sudo systemctl status rabbitmq-server"

#back-end
ssh -t lap@10.241.227.0 "sudo systemctl start apache2 && sudo systemctl status apache2"

#database
ssh -t lap@10.241.217.38 "sudo systemctl start mariadb && sudo systemctl status mariadb"

