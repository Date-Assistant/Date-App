#!/bin/bash

# database-server

ssh -t it490admin@10.0.0.207 "sh /home/it490admin/Projects/Date-App/mariadb/scripts/start-up.sh"

# frontend-server

ssh -t it490admin@10.0.0.156 "sh /home/it490admin/Projects/Date-App/front-end/scripts/start-up.sh"

# rabbitmq-server

ssh -t it490admin@10.0.0.218 "sh /home/it490admin/Projects/Date-App/rabbitmq/scripts/start-up.sh"
