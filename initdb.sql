DROP DATABASE IF EXISTS Auth;
CREATE DATABASE Auth;

DROP TABLE IF EXISTS Auth.Login;
CREATE TABLE Auth.Login (
    user_id INT AUTO_INCREMENT,
    email VARCHAR(127) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
) ENGINE=INNODB;

INSERT INTO Auth.Login (email, password) VALUES ('cktam@ucalgary.ca', 'password');
INSERT INTO Auth.Login (email, password) VALUES ('scclo@ucalgary.ca', 'password');
INSERT INTO Auth.Login (email, password) VALUES ('dwyip@ucalgary.ca', 'password');
INSERT INTO Auth.Login (email, password) VALUES ('lhossack@ucalgary.ca', 'password');
