#!/bin/bash

# database-server

ssh -t it490admin@10.0.0.207 "sh Projects/Date-App/mariadb/start-up.sh"


#sudo systemctl enable apache2
#sudo systemctl start apache2
#sudo systemctl status apache2
