# this is an edit
# sudo apt update
# sudo apt install mariadb-server
# sudo systemctl start mariadb.service
# sudo mysql_secure_installation
# sudo mariadb
# GRANT ALL ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;


import mysql.connector as mariadb
mariadb_connection = mariadb.connect(host='it490database.canztlnjai3e.us-east-1.rds.amazonaws.com', user='admin', password='password', port='3306',database='IT490')
cursor = mariadb_connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, fname VARCHAR(100), lname VARCHAR(100), email VARCHAR(250), password VARCHAR(100), phone VARCHAR(25), address VARCHAR(250), zipcode VARCHAR(100), received_emails VARCHAR(100));")
mariadb_connection.commit()
mariadb_connection.close()
