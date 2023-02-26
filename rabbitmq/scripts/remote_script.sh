#!/bin/bash

#front-end
ssh -t lap@10.241.228.14 "sudo systemctl start apache2 && sudo systemctl status apache2"

#back-end
ssh -t lap@10.241.227.0 "sudo systemctl start apache2 && sudo systemctl status apache2"

#database
ssh -t lap@10.241.217.38 "sudo systemctl start mariadb && sudo systemctl status mariadb"
