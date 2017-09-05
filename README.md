# djdashboard
Dashboard of apps (currently 1) to re-familiarize myself with Django.

Commutity **WORK IN PROGRESS -- VERY EARLY STAGES**
---------
Idea: Application for connecting college commuters together - it can be hard to make friends at first if you're a commuter!

Setup
-----
Install MySQL onto your local machine: https://www.mysql.com/downloads/

As the root user, create a database user 'djdashboard_admin'
 $ mysql -u root -p
 Enter password: 
 mysql> CREATE USER 'djdashboard_admin'@'localhost IDENTIFIED BY 'password';
 mysql> GRANT ALL PRIVILEGES ON *.* TO 'djdashboard_admin'@'localhost';
 mysql> FLUSH PRIVILEGES;
 mysql> exit;

Switch from root to djdashboard_admin, and create a database named 'CommutityDB':
 $ mysql -u djdashboard_admin -p
 Enter password: 
 mysql> CREATE DATABASE CommutityDB;
 mysql> exit;

Install Python 3.5+: https://www.python.org/

Install Python packages utilized in this project:
 $ pip install mysqlclient
 $ pip install pycrypto

Run the server:
 /.../djdashboard/
 $ python manage.py runserver

Navigate to localhost:8000/commutity/
