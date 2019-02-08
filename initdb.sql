DROP DATABASE IF EXISTS Auth;
CREATE DATABASE Auth;

DROP TABLE IF EXISTS Auth.Login;
CREATE TABLE Auth.Login (
    user_id INT AUTO_INCREMENT,
    email VARCHAR(127) NOT NULL,
    password VARCHAR(255) NOT NULL,
    iot_id INT NOT NULL,
    PRIMARY KEY (user_id)
) ENGINE=INNODB;

INSERT INTO Auth.Login (email, password, iot_id) VALUES ('cktam@ucalgary.ca', 'password', 1);
INSERT INTO Auth.Login (email, password, iot_id) VALUES ('scclo@ucalgary.ca', 'password', 2);
INSERT INTO Auth.Login (email, password, iot_id) VALUES ('dwyip@ucalgary.ca', 'password', 3);
INSERT INTO Auth.Login (email, password, iot_id) VALUES ('lhossack@ucalgary.ca', 'password', 4);
