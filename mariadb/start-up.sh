STATUS="$(systemctl is-active mariadb)"
if [ "${STATUS}" = "active" ]; then
    RESPONSE="true"
else 
    RESPONSE="false" 
fi
if [ "${RESPONSE}" = "true" ]; then
	echo "MariaDB is running... Wait for status"
	sleep 5
	sudo systemctl status mariadb
else
	echo "MariaDB is not running. Enabling now"
	sleep 5
	sudo systemctl enable mariadb
	sudo systemctl start mariadb
	sudo systemctl status mariadb

fi
