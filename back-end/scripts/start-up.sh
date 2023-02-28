STATUS="$(systemctl is-active apache2)"
if [ "${STATUS}" = "active" ]; then
    RESPONSE="true"
else 
    RESPONSE="false" 
fi
if [ "${RESPONSE}" = "true" ]; then
	echo "Checking backend services"
	sleep 3
	echo "Apache2 is running... Wait for status"
	sleep 5
	systemctl status apache2
else
	echo "Apache2 is not running. Enabling now"
	sleep 5
	systemctl enable apache2
	systemctl start apache2
	systemctl status apache2

fi
