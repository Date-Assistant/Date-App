# this is an edit
# sudo apt update
# sudo apt install mariadb-server
# sudo systemctl start mariadb.service
# sudo mysql_secure_installation
# sudo mariadb
# GRANT ALL ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;


import mysql.connector as mariadb
mariadb_connection = mariadb.connect(host='it490database.canztlnjai3e.us-east-1.rds.amazonaws.com', user='admin', password='password', port='3306')
cursor = mariadb_connection.cursor()
cursor.execute("GRANT ALL ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;")
cursor.execute("GRANT ALL ON *.* TO 'admin'@10.0.0.207 IDENTIFIED BY 'password' WITH GRANT OPTION;")
cursor.execute("GRANT ALL ON *.* TO 'it490admin'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;")
cursor.execute("GRANT ALL ON *.* TO 'it490admin'@10.0.0.207 IDENTIFIED BY 'password' WITH GRANT OPTION;")
cursor.execute("GRANT ALL ON *.* TO 'lap'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;")
cursor.execute("GRANT ALL ON *.* TO 'lap'@10.0.0.207 IDENTIFIED BY 'password' WITH GRANT OPTION;")
cursor.execute("GRANT ALL ON *.* TO 'brian'@'localhost' IDENTIFIED BY 'password' WITH GRANT OPTION;")
cursor.execute("GRANT ALL ON *.* TO 'brian'@10.0.0.207 IDENTIFIED BY 'password' WITH GRANT OPTION;")
cursor.execute("FLUSH PRIVILEGES;")
cursor.execute("CREATE DATABASE IF NOT EXISTS IT490;")
cursor.execute("CREATE DATABASE IF NOT EXISTS IT490BACKUP;")
mariadb_connection.commit()
mariadb_connection.close()
