/* Create the database */
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
/* Create the user */
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
/* Grant all privileges */
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
/* Grant select privilege */
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
