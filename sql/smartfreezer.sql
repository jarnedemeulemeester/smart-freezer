CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
CREATE USER 'flask'@'localhost' IDENTIFIED BY 'flask';
CREATE USER 'sensor'@'localhost' IDENTIFIED BY 'sensor';

CREATE DATABASE  IF NOT EXISTS `smartfreezer` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `smartfreezer`;

GRANT ALL PRIVILEGES ON smartfreezer.* to 'admin'@'localhost' WITH GRANT OPTION;
GRANT SELECT, INSERT, UPDATE, DELETE ON smartfreezer.* TO 'flask'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON smartfreezer.* TO 'sensor'@'localhost';
FLUSH PRIVILEGES;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: smartfreezer
-- ------------------------------------------------------
-- Server version	8.0.11

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
-- Table structure for table `icon`
--

DROP TABLE IF EXISTS `icon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `icon` (
  `idicon` int(11) NOT NULL AUTO_INCREMENT,
  `iconpath` varchar(100) NOT NULL,
  PRIMARY KEY (`idicon`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `icon`
--

LOCK TABLES `icon` WRITE;
/*!40000 ALTER TABLE `icon` DISABLE KEYS */;
INSERT INTO `icon` VALUES (1,'img/blank.png');
/*!40000 ALTER TABLE `icon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
  `idproduct` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `amount` int(11) NOT NULL,
  `creationdate` date NOT NULL,
  `expirationdate` date NOT NULL,
  `iconid` int(11) NOT NULL,
  `comments` varchar(200) DEFAULT NULL,
  `istemplate` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idproduct`,`iconid`),
  KEY `fk_product_icon_idx` (`iconid`),
  CONSTRAINT `fk_product_icon` FOREIGN KEY (`iconid`) REFERENCES `icon` (`idicon`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `settings` (
  `idsettings` int(11) NOT NULL AUTO_INCREMENT,
  `mintemp` int(11) NOT NULL DEFAULT '-30',
  `maxtemp` int(11) NOT NULL DEFAULT '-5',
  `temp` int(11) NOT NULL DEFAULT '-18',
  `pae` tinyint(4) NOT NULL DEFAULT '1',
  `pe` tinyint(4) NOT NULL DEFAULT '1',
  `shoppinglist` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`idsettings`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `settings`
--

LOCK TABLES `settings` WRITE;
/*!40000 ALTER TABLE `settings` DISABLE KEYS */;
INSERT INTO `settings` VALUES (1,-30,-5,-18,0,1,1);
/*!40000 ALTER TABLE `settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temperature`
--

DROP TABLE IF EXISTS `temperature`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temperature` (
  `idtemperature` int(11) NOT NULL AUTO_INCREMENT,
  `temp` float NOT NULL,
  PRIMARY KEY (`idtemperature`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temperature`
--

LOCK TABLES `temperature` WRITE;
/*!40000 ALTER TABLE `temperature` DISABLE KEYS */;
/*!40000 ALTER TABLE `temperature` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-17 21:45:27
