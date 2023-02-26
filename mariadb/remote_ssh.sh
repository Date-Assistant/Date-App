#!/bin/bash

#rabbitmq
ssh -t tyrell@10.241.51.24 "sudo systemctl start rabbitmq-server && sudo systemctl status rabbitmq-server"


#front-end
ssh -t tyrell@10.241.228.14 "sudo systemctl start apache2 && sudo systemctl status apache2"


#

#backend
ssh -t tyrell@10.241.227.0 "sudo systemctl start apache2 && sudo systemctl status apache2"

