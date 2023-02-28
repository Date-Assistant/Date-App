#!/bin/bash
STATUS="$(systemctl is-active rabbitmq-server)"
if [ "${STATUS}" = "active" ]; then
    RESPONSE="true"
else 
    RESPONSE="false" 
fi
if [ "${RESPONSE}" = "true" ]; then
	echo "Arabbitmq-server is running... Wait for status"
	sleep 5
	systemctl status rabbitmq-server
else
	echo "rabbitmq-server is not running. Enabling now"
	sleep 5
	systemctl enable rabbitmq-server
	systemctl start rabbitmq-server
	systemctl status rabbitmq-server

fi

