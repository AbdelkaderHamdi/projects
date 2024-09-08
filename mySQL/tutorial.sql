CREATE DATABASE IF NOT EXISTS kader;
DROP DATABASE IF EXISTS kader ;

% DataType 

Date   => YYYY-MM-DD 
Timestamp | DateTime  => YYYY-MM-DD HH:Mi:SS
Time   => HH:Mi:SS 
Year   => YYYY | YY

char   ==> for fixed number of charcters in feild  (Max charcter 255)
It is faster than Varchar 50% (use static memory)

char != Varchar

set ==> choose more than one from multiple choices 
enum ==> choose just one from multiple choices



USE DATABASE kader;
CREATE TABLE friends(
    id int(11); 
    name varchar(255); 
    email varchar(255)
);
DESCRIBE FROM kader; | SHOW COULUNMS FROM kader; | SHOW FIELDS FROM kader;

SHOW TABLE STATUS ;

ALTER TABLE friends CONVERT TO CHARACTER SET utf8;

RENAME TABLE t1 TO table1, t2 TO table2;
ALTER TABLE t1 RENAME table1; 

ALTER TABLE friends {ADD | MODIFY | DROP COLUMN} 

ALTER TABLE friends ADD user_name varchar(255) FIRST | AFTER name ;

#modify the position of a field 
ALTER TABLE friends CHANGE user_name user_name varchar(255) AFTER email;

ALTER TABLE friends CHANGE email email_msg varchar(255);






















