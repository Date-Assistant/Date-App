STATUS="$(systemctl is-active mariadb)"
if [ "${STATUS}" = "active" ]; then
    RESPONSE="true"
else 
    RESPONSE="false"
    exit 1  
fi
if [ "${RESPONSE}" = "true" ]; then
    sudo systemctl status mariadb
else
    sudo systemctl enable mariadb
    sudo systemctl start mariadb