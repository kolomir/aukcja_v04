-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: auction_db2
-- ------------------------------------------------------
-- Server version	5.5.5-10.11.5-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auctions`
--

DROP TABLE IF EXISTS `auctions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auctions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `item_name` varchar(255) NOT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `start_price` decimal(10,2) NOT NULL,
  `current_price` decimal(10,2) NOT NULL,
  `auction_step` decimal(10,2) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `status` enum('active','closed') DEFAULT 'active',
  `description` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auctions`
--

LOCK TABLES `auctions` WRITE;
/*!40000 ALTER TABLE `auctions` DISABLE KEYS */;
INSERT INTO `auctions` VALUES (1,'komputer 1','img/img1',500.00,850.00,50.00,'2024-12-09 18:00:00','2024-12-09 22:00:00','closed','Procesor: i5; RAM 32 GB'),(2,'Komp 2','img/img2',600.00,750.00,50.00,'2024-12-09 18:00:00','2024-12-16 18:00:00','active','Procesor: i7; RAM 8 GB'),(3,'komp3','img/img3',400.00,650.00,50.00,'2024-12-09 18:00:00','2024-12-15 18:00:00','active','Procesor: i5; RAM 16 GB');
/*!40000 ALTER TABLE `auctions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bids`
--

DROP TABLE IF EXISTS `bids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bids` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `auction_id` int(11) NOT NULL,
  `bidder_name` varchar(255) NOT NULL,
  `bid_time` datetime NOT NULL,
  `bid_amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auction_id` (`auction_id`),
  CONSTRAINT `bids_ibfk_1` FOREIGN KEY (`auction_id`) REFERENCES `auctions` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bids`
--

LOCK TABLES `bids` WRITE;
/*!40000 ALTER TABLE `bids` DISABLE KEYS */;
INSERT INTO `bids` VALUES (1,1,'Jakis','2024-12-09 18:26:06',550.00),(2,2,'aaad','2024-12-09 18:26:13',650.00),(3,1,'sdfsdf','2024-12-09 21:14:50',600.00),(4,3,'aaaa','2024-12-09 21:43:30',450.00),(5,3,'sssss','2024-12-09 21:43:34',500.00),(6,3,'ddddddd','2024-12-09 21:43:38',550.00),(7,1,'aaaa','2024-12-09 21:56:49',650.00),(8,1,'ssss','2024-12-09 21:56:52',700.00),(9,1,'wwww','2024-12-09 21:56:54',750.00),(10,1,'eeee','2024-12-09 21:56:57',800.00),(11,1,'xxxx','2024-12-09 21:57:02',850.00),(12,3,'dfg','2024-12-09 23:36:13',600.00),(13,2,'retert','2024-12-09 23:36:17',700.00),(14,3,'dfgdfg','2024-12-09 23:36:27',650.00),(15,2,'rrrrrrrrrrrrrrrrr','2024-12-09 23:36:31',750.00);
/*!40000 ALTER TABLE `bids` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'auction_db2'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-09 23:37:32
