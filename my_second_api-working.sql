-- MariaDB dump 10.19  Distrib 10.6.5-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: my_second_api
-- ------------------------------------------------------
-- Server version	10.6.5-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employee` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `hired_at` date NOT NULL,
  `hourly_wage` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `employee_check` CHECK (`hourly_wage` > 0)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'employee_1','2012-01-05',15.00),(2,'employee_2','2010-03-04',16.00),(3,'employee_3','2016-09-09',16.50),(4,'employee_4','2020-10-10',17.00),(5,'employee_5','2021-05-30',14.99);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `item` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) NOT NULL,
  `quantity` tinyint(3) unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `item_un` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES (1,'item1','description1',0,'2022-02-05 16:09:42'),(2,'item 2','description 2',5,'2022-02-04 16:09:42'),(3,'item 3','description 3',1,'2022-02-04 16:09:42'),(4,'item 4','description 4',1,'2022-02-02 16:09:42'),(5,'item 5','description 5',1,'2022-02-03 16:09:42'),(6,'item 6','description 6',1,'2022-02-01 16:09:42'),(7,'item 7','description 7',1,'2022-02-05 13:09:42'),(8,'item 8','description 8',1,'2022-02-01 10:09:42'),(9,'item 9','description 9',1,'2022-02-02 09:09:42'),(10,'item 0','description 0',1,'2022-02-04 16:39:42'),(11,'newItem','same old description',1,'2022-02-05 17:14:17'),(13,'newItem2','same old description',1,'2022-02-05 17:21:28'),(14,'newItem23','same old description',1,'2022-02-05 17:24:01'),(16,'newItem233','same old description',1,'2022-02-05 17:27:06'),(17,'','same old description',1,'2022-02-05 17:27:42'),(21,'item_postman','description',2,'2022-02-07 17:26:23'),(27,'item_postman2','postnman_description',56,'2022-02-07 18:03:49'),(28,'item_postman3','postnman_description',1,'2022-02-07 18:11:15'),(31,'item_postman4','postnman_description',1,'2022-02-07 18:12:05'),(32,'item_postman5','postnman_description',1,'2022-02-07 18:15:47');
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'my_second_api'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-07 20:26:01
