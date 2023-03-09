#!/bin/bash
STATUS="$(systemctl is-active rabbitmq-server)"
if [ "${STATUS}" = "active" ]; then
    RESPONSE="true"
else 
    RESPONSE="false" 
fi
if [ "${RESPONSE}" = "true" ]; then
	echo "Checking rabbitmq-server services"
	sleep 3
	echo "Rabbitmq-server is running... Wait for status"
	sleep 5
	echo "password" | sudo systemctl status rabbitmq-server
else
	echo "rabbitmq-server is not running. Enabling now"
	sleep 5
	echo "password" | sudo systemctl enable rabbitmq-server
	echo "password" | sudo systemctl start rabbitmq-server
	echo "password" | sudo systemctl status rabbitmq-server

fi

