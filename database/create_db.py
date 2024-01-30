import mysql.connector as mc

# Connect to the MySQL database
with  mc.connect(host="localhost",user='root',passwd="KOKOWaWa1Ak9",database='twitter') as db:
    cursor = db.cursor()
    cursor.execute(
        """CREATE TABLE users (
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(255),
email VARCHAR(255),
followers INT,
following INT
)"""
)
    
    cursor.execute(
        """CREATE TABLE tweets (
id INT AUTO_INCREMENT PRIMARY KEY,
date DATETIME,
topic ENUM('food', 'sports', 'education','games','home','cooking'),
text VARCHAR(400),
mentions INT,
creator INT,
likes INT,
shares INT,
FOREIGN KEY (creator) REFERENCES users(id),
FOREIGN KEY (mentions) REFERENCES users(id)
)
""")

print("DB was created successfully")