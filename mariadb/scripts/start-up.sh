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
	systemctl status mariadb
else
	echo "MariaDB is not running. Enabling now"
	sleep 5
	systemctl enable mariadb
	systemctl start mariadb
	systemctl status mariadb

fi
