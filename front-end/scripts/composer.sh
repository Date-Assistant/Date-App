#!/bin/bash

# database-server

ssh -t it490admin@10.0.0.207 "sh /home/it490admin/Projects/Date-App/mariadb/scripts/start-up.sh"

# backend-server

ssh -t it490admin@10.0.0.108 "sh /home/it490admin/Projects/Date-App/back-end/scripts/start-up.sh"

# rabbitmq-server

ssh -t it490admin@10.0.0.218 "sh /home/it490admin/Projects/Date-App/rabbitmq/scripts/start-up.sh"
