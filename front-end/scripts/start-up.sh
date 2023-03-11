STATUS="$(systemctl is-active apache2)"
if [ "${STATUS}" = "active" ]; then
    RESPONSE="true"
else 
    RESPONSE="false" 
fi
if [ "${RESPONSE}" = "true" ]; then
	echo "Checking front-end services"
	sleep 3
	echo "Apache2 is running... Wait for status"
	sleep 5
	echo "password" | su - it490admin
	systemctl status apache2
else
	echo "Apache2 is not running. Enabling now"
	sleep 5
    echo "password" | su - it490admin
    apt install -y apache2
	systemctl enable apache2
	systemctl start apache2
	systemctl status apache2

fi
