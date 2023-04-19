-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: ht_database
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `account_id` int NOT NULL,
  `contact_id` int DEFAULT NULL,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `user_type` varchar(45) DEFAULT NULL,
  `currency_type` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`account_id`),
  KEY `contact_id_idx` (`contact_id`),
  CONSTRAINT `contact_id` FOREIGN KEY (`contact_id`) REFERENCES `contacts` (`contact_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (25000,20000,'lightless','70ccd9007338d6d81dd3b6271621b9cf9a97ea00','Admin','Pounds'),(25001,20001,'lightless','67a258218f68f6b5f7142593cf4b1f7d87622dd8','Standard','Euros'),(25002,20002,'johnsmith2','058010c2776afdf1d7afec578d1330616cf92567','Standard','Pounds'),(25003,20003,'jsmith3','058010c2776afdf1d7afec578d1330616cf92567','Standard','Pounds'),(25004,20004,'User1','039aa1b8d4260122f0eff3fb1b82e1a2a055816e','Standard','Pounds'),(25005,20005,'user2','039aa1b8d4260122f0eff3fb1b82e1a2a055816e','Standard','Pounds');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `booking_id` int NOT NULL,
  `payment_id` int DEFAULT NULL,
  `seat_type` varchar(8) DEFAULT NULL,
  `passengers` int DEFAULT NULL,
  `departure_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `commute_type` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `payment_id_idx` (`payment_id`),
  CONSTRAINT `payment_id` FOREIGN KEY (`payment_id`) REFERENCES `booking_payment` (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (47204,12387,'Economy',1,'2023-04-20','2023-04-20','Oneway Trip'),(47205,12388,'Economy',1,'2023-04-20','2023-04-20','Oneway Trip'),(47206,12389,'Economy',1,'2023-07-17','2023-07-17','Oneway Trip'),(47207,12390,'Economy',1,'2023-07-14','2023-07-14','Oneway Trip'),(47208,12391,'Economy',1,'2023-04-20','2023-04-20','Oneway Trip'),(47209,12392,'Economy',1,'2023-04-20','2023-04-20','Oneway Trip'),(47210,12393,'Economy',1,'2023-07-13','2023-07-13','Oneway Trip');
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking_payment`
--

DROP TABLE IF EXISTS `booking_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking_payment` (
  `payment_id` int NOT NULL,
  `account_id` int DEFAULT NULL,
  `price` decimal(7,2) DEFAULT NULL,
  `discount_percentage` varchar(15) DEFAULT NULL,
  `payment_method` varchar(15) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `purchase_status` varchar(45) DEFAULT NULL,
  `journey_id` int DEFAULT NULL,
  `cancellation_date` date DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `account_id_idx` (`account_id`),
  KEY `journey_id_idx` (`journey_id`),
  CONSTRAINT `account_id` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`),
  CONSTRAINT `journey_id` FOREIGN KEY (`journey_id`) REFERENCES `journey` (`journey_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking_payment`
--

LOCK TABLES `booking_payment` WRITE;
/*!40000 ALTER TABLE `booking_payment` DISABLE KEYS */;
INSERT INTO `booking_payment` VALUES (12387,25000,80.00,'0','PayPal','2023-04-19','Cancelled',2,NULL),(12388,25000,80.00,'0','PayPal','2023-04-19','Cancelled',2,NULL),(12389,25000,64.00,'0.2','PayPal','2023-04-19','Cancelled',2,NULL),(12390,25000,64.00,'0.2','PayPal','2023-04-19','Cancelled',2,NULL),(12391,25000,80.00,'0','PayPal','2023-04-19','Cancelled',2,NULL),(12392,25000,75.00,'0','PayPal','2023-04-19','Cancelled',1,'2023-04-19'),(12393,25000,60.00,'0.2','PayPal','2023-04-19','Cancelled',1,'2023-04-19');
/*!40000 ALTER TABLE `booking_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contacts` (
  `contact_id` int NOT NULL,
  `customer_id` int DEFAULT NULL,
  `telephone` varchar(20) DEFAULT NULL,
  `email_address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`contact_id`),
  KEY `customer_id_idx` (`customer_id`),
  CONSTRAINT `customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
INSERT INTO `contacts` VALUES (20000,10000,'7763470820','lightlessgaming@gmail.com'),(20001,10001,'7763470820','reeceturner35@gmail.com'),(20002,10002,'09999999999','johnsmith2@gmail.com'),(20003,10003,'9999999999','johnsmith3@gmail.com'),(20004,10004,'0999999999','user1@user1.com'),(20005,10005,'083838383','user2@x.com');
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL,
  `first_name` varchar(45) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  PRIMARY KEY (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (10000,'Reece','Turner','2000-08-03'),(10001,'Reece','Turner','2000-08-03'),(10002,'John','Smith','1999-08-03'),(10003,'John','Smith3','1998-08-02'),(10004,'UserFirst','UserLast','1999-08-03'),(10005,'lana','kane','1999-04-03');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `journey`
--

DROP TABLE IF EXISTS `journey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journey` (
  `journey_id` int NOT NULL,
  `departure_location` varchar(45) DEFAULT NULL,
  `departure_time` time DEFAULT NULL,
  `return_location` varchar(45) DEFAULT NULL,
  `return_time` time DEFAULT NULL,
  PRIMARY KEY (`journey_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journey`
--

LOCK TABLES `journey` WRITE;
/*!40000 ALTER TABLE `journey` DISABLE KEYS */;
INSERT INTO `journey` VALUES (1,'Newcastle','16:45:00','Bristol','18:00:00'),(2,'Bristol','08:00:00','Newcastle','09:15:00'),(3,'Cardiff','06:00:00','Edinburgh','07:30:00'),(4,'Bristol','11:30:00','Manchester','12:30:00'),(5,'Manchester','12:20:00','Bristol','13:20:00'),(6,'Bristol','07:40:00','London','08:20:00'),(7,'London','11:00:00','Manchester','12:20:00'),(8,'Manchester','12:20:00','Glasgow','13:30:00'),(9,'Bristol','07:40:00','Glasgow','08:45:00'),(10,'Glasgow','14:30:00','Newcastle','15:45:00'),(11,'Newcastle','16:15:00','Manchester','17:05:00'),(12,'Manchester','18:25:00','Bristol','19:30:00'),(13,'Bristol','06:20:00','Manchester','07:20:00'),(14,'Portsmouth','12:00:00','Dundee','14:00:00'),(15,'Dundee','10:00:00','Portsmouth','12:00:00'),(16,'Edinburgh','18:30:00','Cardiff','20:00:00'),(17,'Southampton','12:00:00','Manchester','13:30:00'),(18,'Manchester','19:00:00','Southampton','20:30:00'),(19,'Birmingham','16:00:00','Newcastle','17:30:00'),(20,'Newcastle','06:00:00','Birmingham','07:30:00'),(21,'Aberdeen','07:00:00','Portsmouth','09:00:00');
/*!40000 ALTER TABLE `journey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `locations` (
  `location_id` int NOT NULL,
  `location` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` VALUES (1,'Newcastle'),(2,'Bristol'),(3,'Cardiff'),(4,'London'),(5,'Glasgow'),(6,'Portsmouth'),(7,'Dundee'),(8,'Edinburgh'),(9,'Southampton'),(10,'Manchester'),(11,'Birmingham'),(12,'Aberdeen');
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-19  6:30:25
