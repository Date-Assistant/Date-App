STATUS="$(systemctl is-active mariadb)"
if [ "${STATUS}" = "active" ]; then
    RESPONSE="true"
else 
    RESPONSE="false" 
fi
if [ "${RESPONSE}" = "true" ]; then
	echo "Checking database services"
	sleep 3
	echo "MariaDB is running... Wait for status"
	sleep 5
	echo "password" | sudo systemctl status mariadb
else
	echo "MariaDB is not running. Enabling now"
	sleep 5
	echo "password" | sudo systemctl enable mariadb
	echo "password" | sudo systemctl start mariadb
	echo "password" | sudo systemctl status mariadb

fi
