#!/bin/bash

# frontend-server

ssh -t it490admin@10.0.0.156 "sh /home/it490admin/Projects/Date-App/front-end/scripts/start-up.sh"

# backend-server

ssh -t it490admin@10.0.0.108 "sh /home/it490admin/Projects/Date-App/back-end/scripts/start-up.sh"

# database-server

ssh -t it490admin@10.0.0.207 "sh /home/it490admin/Projects/Date-App/mariadb/scripts/start-up.sh"