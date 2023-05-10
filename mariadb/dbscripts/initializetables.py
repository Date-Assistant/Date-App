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
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(100),
    lname VARCHAR(100),
    email VARCHAR(250),
    password VARCHAR(100),
    phone VARCHAR(25),
    address VARCHAR(250),
    zipcode VARCHAR(100),
    received_emails VARCHAR(100),
    discount VARCHAR(200),
    membership VARCHAR(250)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS businesses (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    bname VARCHAR(100),
    oname VARCHAR(100),
    email VARCHAR(250),
    password VARCHAR(100),
    phone VARCHAR(25),
    address VARCHAR(250),
    zipcode VARCHAR(100),
    received_emails VARCHAR(100),
    discount VARCHAR(200),
    membership VARCHAR(250)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS userpayment (
    user_id INT NOT NULL PRIMARY KEY,
    cardholder_name VARCHAR(100),
    card_number VARCHAR(100),
    expiration_date VARCHAR(7),
    cvc VARCHAR(4),
    saveCardInfo VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS businesspayment (
    business_id INT NOT NULL PRIMARY KEY,
    cardholder_name VARCHAR(100),
    card_number VARCHAR(100),
    expiration_date VARCHAR(7),
    cvc VARCHAR(4),
    saveCardInfo VARCHAR(100),
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    user_id INT NOT NULL,
    place_id VARCHAR(50) NOT NULL,
    PRIMARY KEY (user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

mariadb_connection.commit()
mariadb_connection.close()
