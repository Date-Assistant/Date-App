# this is an edit
# sudo apt update
# sudo apt install mariadb-server
# sudo systemctl start mariadb.service
# sudo mysql_secure_installation
# sudo mariadb
# GRANT ALL ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;


import mysql.connector as mariadb
mariadb_connection = mariadb.connect(host='localhost', user='root', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (fname VARCHAR(100), lname VARCHAR(100), email VARCHAR(100), password VARCHAR(60), phone VARCHAR(25), address VARCHAR(250), zipcode INT(7), received_emails BOOLEAN NOT NULL default 0);")
mariadb_connection.commit()