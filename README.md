# MySQL Dump Split & Import
Python script for splitting a large mysql dump file into individual tables and importing the data in database.

## Introduction
Importing a huge MySQL database dump file is very troublesome and takes a lot of time. In this project, we split
the database dump into individual tables (split_sql_dump_file.py) and import the data using (import_dump.py)

We have added optimization tips in Import Data section below which will help you to cut down the data import time
significantly.

## Assumptions
- Pipe Viewer is installed. We use pv command during MySQL data import to display the import progress
- We have assumed that the database dump file is created using `mysqldump` and has below structure
```

-- MySQL dump XX.XX  Distrib XX.XX.XX, for Linux (x86_64)
--
-- Host: localhost    Database: cbseguid_askbot
-- ------------------------------------------------------
-- Server version       XX.XX.XX

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `table_name`
--

DROP TABLE IF EXISTS `table_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `table_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  ...
) ENGINE=InnoDB AUTO_INCREMENT=4079360 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `table_name`
--

LOCK TABLES `table_name` WRITE;
/*!40000 ALTER TABLE `table_name` DISABLE KEYS */;
INSERT INTO.......
/*!40000 ALTER TABLE `table_name` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on ...

```
- We extract environment variable setup from the dump file and append them at both start and end of each individual splitted file

## Splitting File

### Usage
Below command splits the `database_dump.sql` file into individual tables and places the data (INSERT INTO statements) in 
`data` directory and structure (CREATE TABLE statement) in `structure` directory inside below mentioned directory.

```
python split_sql_dump_file_py database_dump.sql output
```

## Importing Data

### Configuration to reduce the data import time
- Locate your my.cnf file and append below text at the end. Change the values based on your machine configuration.
```
innodb_buffer_pool_size = 4G
innodb_log_buffer_size = 256M
innodb_log_file_size = 1G
innodb_write_io_threads = 16
innodb_flush_log_at_trx_commit = 0
```
- In MacOSX the my.cnf file is located at `/usr/local/mysql/my.cnf`
- To find my.cnf location, use below command
```
mysql –-help | grep my.cnf
```
- Before starting the import process, run below command 
```
service mysql restart --innodb-doublewrite=0

In MacOSX,
sudo /usr/local/mysql/support-files/mysql.server stop 
sudo /usr/local/mysql/support-files/mysql.server start --innodb-doublewrite=0
```
- Once import is completed, restart MySQL server again
```
service mysql restart 

In MacOSX,
sudo /usr/local/mysql/support-files/mysql.server stop 
sudo /usr/local/mysql/support-files/mysql.server start 
```

### Usage
Make sure:
- my.cnf file is updated with optimization configuration
- mysql restarted with `--innodb-doublewrite=0`

```
python import_dump.py dump_directory

when using with above split command, 
python import_dump.py output/structure
python import_dump.py output/data
```

## References
- https://dba.stackexchange.com/questions/83125/mysql-any-way-to-import-a-huge-32-gb-sql-dump-faster
- https://github.com/kloddant/split_sql_dump_file
- https://github.com/kedarvj/mysqldumpsplitter