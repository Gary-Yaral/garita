/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.5.5-10.4.24-MariaDB : Database - guard_booth
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`guard_booth` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `guard_booth`;

/*Table structure for table `access_register` */

DROP TABLE IF EXISTS `access_register`;

CREATE TABLE `access_register` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `driver_id` int(11) NOT NULL,
  `vehicle_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `kms` varchar(50) DEFAULT NULL,
  `destiny` varchar(200) DEFAULT NULL,
  `observation` varchar(200) DEFAULT NULL,
  `register_type_id` int(11) NOT NULL,
  `current_time` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `register_type_id` (`register_type_id`),
  KEY `access_register_ibfk_1` (`driver_id`),
  KEY `access_register_ibfk_2` (`vehicle_id`),
  KEY `access_register_ibfk_3` (`user_id`),
  CONSTRAINT `access_register_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `driver` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `access_register_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `access_register_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `access_register_ibfk_4` FOREIGN KEY (`register_type_id`) REFERENCES `register_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4;

/*Data for the table `access_register` */

LOCK TABLES `access_register` WRITE;

insert  into `access_register`(`id`,`driver_id`,`vehicle_id`,`user_id`,`kms`,`destiny`,`observation`,`register_type_id`,`current_time`) values (9,14,1,10,'3466','Francia','Ninguna',1,'2023-12-14 15:47:30'),(20,13,1,10,'436','vbcbc','fgjgj',2,'2023-12-14 17:14:17'),(21,13,1,10,'436','vbcbc','ghgg',1,'2023-12-14 17:18:57'),(22,14,1,10,'36','fhfh','hfhhf',2,'2023-12-14 17:45:58'),(23,14,1,10,'636','gf','fgfdgf',1,'2023-12-14 17:46:22'),(25,14,1,10,'566','dsgsd','dsgg',1,'2023-12-14 17:50:51'),(27,14,1,10,'54645','Galapagos','mundo',1,'2023-12-14 18:07:04'),(28,14,1,10,'546','56','gsssdg',2,'2023-12-14 18:17:17'),(29,14,1,10,'45','cxcc','xzxv',1,'2023-12-14 18:18:15'),(30,14,1,10,'4','ddg','dgsdgs',2,'2023-12-14 18:19:19'),(31,14,1,10,'4545','edgdsg','dgsg',1,'2023-12-14 18:19:36'),(32,14,1,10,'656','ssaf','safsf',2,'2023-12-14 18:20:45'),(33,14,1,10,'56546','ff','fdhh',1,'2023-12-14 18:21:54'),(34,14,1,10,'52','ffdsfd','fdsfs',2,'2023-12-14 18:22:42'),(35,14,1,10,'234','vds','dsvsdv',1,'2023-12-14 18:23:59'),(36,14,1,10,'6346','gsg','dsgdsg',2,'2023-12-14 18:28:24'),(37,14,1,10,'345','xvzz','zxvzvz',1,'2023-12-14 18:31:56'),(38,14,1,10,'435','dfdf','sdfsdf',2,'2023-12-14 18:32:35'),(39,14,1,10,'454','fdsf','dsfsdf',1,'2023-12-14 18:32:49'),(40,13,1,10,'333','Mexico','Hello',2,'2023-12-16 11:33:31'),(41,14,1,10,'54645','fhdf','Mi destino',1,'2023-12-16 12:31:48'),(42,4,1,10,'1244','Florida','Ninguna',2,'2023-12-16 16:36:51'),(43,2,2,10,'','','',2,'2023-12-16 16:40:05');

UNLOCK TABLES;

/*Table structure for table `access_type` */

DROP TABLE IF EXISTS `access_type`;

CREATE TABLE `access_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `access_type` */

LOCK TABLES `access_type` WRITE;

insert  into `access_type`(`id`,`name`) values (1,'Regular'),(2,'Invitado');

UNLOCK TABLES;

/*Table structure for table `driver` */

DROP TABLE IF EXISTS `driver`;

CREATE TABLE `driver` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dni` varchar(12) NOT NULL,
  `name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `drive_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `drive_type_id` (`drive_type_id`),
  CONSTRAINT `driver_ibfk_1` FOREIGN KEY (`drive_type_id`) REFERENCES `driver_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;

/*Data for the table `driver` */

LOCK TABLES `driver` WRITE;

insert  into `driver`(`id`,`dni`,`name`,`surname`,`drive_type_id`) values (2,'1243545462','Adrian Flores','Barba',2),(4,'1335454664','Flavia Maria','Contreras',1),(5,'1457686861','Marcos','Andrade',4),(6,'1465757753','Diana','Arboleda',5),(7,'1233578754','Gustavo Mario','Mora Litardo',4),(8,'1247658659','Hugo','Torres',4),(10,'1567645443','Julio','Nagua',4),(13,'1345464653','Oliver Andrés','Atom Mirana',2),(14,'1358684742','Amalia Mirai','Gonzales Plata',1),(17,'1555254596','Olivia Maria','Gonzales',4);

UNLOCK TABLES;

/*Table structure for table `driver_type` */

DROP TABLE IF EXISTS `driver_type`;

CREATE TABLE `driver_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

/*Data for the table `driver_type` */

LOCK TABLES `driver_type` WRITE;

insert  into `driver_type`(`id`,`name`) values (1,'Estudiante'),(2,'Docente'),(3,'Administrativo'),(4,'Militar'),(5,'Particular');

UNLOCK TABLES;

/*Table structure for table `register_type` */

DROP TABLE IF EXISTS `register_type`;

CREATE TABLE `register_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `register_type` */

LOCK TABLES `register_type` WRITE;

insert  into `register_type`(`id`,`name`) values (1,'Entrada'),(2,'Salida');

UNLOCK TABLES;

/*Table structure for table `rol` */

DROP TABLE IF EXISTS `rol`;

CREATE TABLE `rol` (
  `rol_id` int(11) NOT NULL AUTO_INCREMENT,
  `rol_name` varchar(100) NOT NULL,
  PRIMARY KEY (`rol_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `rol` */

LOCK TABLES `rol` WRITE;

insert  into `rol`(`rol_id`,`rol_name`) values (1,'administrador'),(2,'usuario');

UNLOCK TABLES;

/*Table structure for table `status_type` */

DROP TABLE IF EXISTS `status_type`;

CREATE TABLE `status_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

/*Data for the table `status_type` */

LOCK TABLES `status_type` WRITE;

insert  into `status_type`(`id`,`name`) values (1,'Dentro'),(2,'Fuera');

UNLOCK TABLES;

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dni` varchar(12) NOT NULL,
  `name` varchar(100) NOT NULL,
  `surname` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `fk_user_status_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_status_id` (`fk_user_status_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`fk_user_status_id`) REFERENCES `user_status` (`user_status_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;

/*Data for the table `user` */

LOCK TABLES `user` WRITE;

insert  into `user`(`id`,`dni`,`name`,`surname`,`username`,`password`,`fk_user_status_id`) values (10,'1345464653','Usuario','Administrador','Miusuario_2023','$2b$12$yFm8Mse8rsZl9OijXnYG8uzZAvY.B0MsLe7wIPYLdxjIRA9EevFgi',1),(12,'1345465651','Flavia Agustina','Contreras','S3cUrity_Eye','$2b$12$AOPC6mzfnQJgPKzY7OoHJek1rRXqdzGnkGYp85ecpksbaGHj87nQK',2),(15,'1345464323','Diana Maria','Gutierrez Miranda','FDm_2023','$2b$12$vu8fl5AvxmJV0NhL5lFuWuuVHoa4B960g5/LqRlacLTmPa8Jr2q12',2);

UNLOCK TABLES;

/*Table structure for table `user_rol` */

DROP TABLE IF EXISTS `user_rol`;

CREATE TABLE `user_rol` (
  `user_rol_id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_rol_id` int(11) NOT NULL,
  `fk_user_id` int(11) NOT NULL,
  `editor` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_rol_id`),
  KEY `user_rol_ibfk_1` (`fk_rol_id`),
  KEY `user_rol_ibfk_2` (`fk_user_id`),
  CONSTRAINT `user_rol_ibfk_1` FOREIGN KEY (`fk_rol_id`) REFERENCES `rol` (`rol_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_rol_ibfk_2` FOREIGN KEY (`fk_user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;

/*Data for the table `user_rol` */

LOCK TABLES `user_rol` WRITE;

insert  into `user_rol`(`user_rol_id`,`fk_rol_id`,`fk_user_id`,`editor`) values (9,1,10,0),(11,1,12,0),(14,2,15,0);

UNLOCK TABLES;

/*Table structure for table `user_status` */

DROP TABLE IF EXISTS `user_status`;

CREATE TABLE `user_status` (
  `user_status_id` int(11) NOT NULL AUTO_INCREMENT,
  `status_name` varchar(100) NOT NULL,
  PRIMARY KEY (`user_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `user_status` */

LOCK TABLES `user_status` WRITE;

insert  into `user_status`(`user_status_id`,`status_name`) values (1,'Habilitado'),(2,'Deshabilitado');

UNLOCK TABLES;

/*Table structure for table `vehicles` */

DROP TABLE IF EXISTS `vehicles`;

CREATE TABLE `vehicles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plate_number` varchar(12) NOT NULL,
  `access_type_id` int(11) NOT NULL,
  `status_type_id` int(11) NOT NULL,
  `vehicle_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `access_type_id` (`access_type_id`),
  KEY `status_type_id` (`status_type_id`),
  KEY `vehicle_type_id` (`vehicle_type_id`),
  CONSTRAINT `vehicles_ibfk_1` FOREIGN KEY (`access_type_id`) REFERENCES `access_type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `vehicles_ibfk_2` FOREIGN KEY (`status_type_id`) REFERENCES `status_type` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `vehicles_ibfk_3` FOREIGN KEY (`vehicle_type_id`) REFERENCES `vehicles_type` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

/*Data for the table `vehicles` */

LOCK TABLES `vehicles` WRITE;

insert  into `vehicles`(`id`,`plate_number`,`access_type_id`,`status_type_id`,`vehicle_type_id`) values (1,'RAA-101',1,2,1),(2,'DDE-234',1,2,2),(3,'GHT-2354',1,1,1),(8,'GHT-2353',1,1,2),(9,'TGG-4663',1,1,2);

UNLOCK TABLES;

/*Table structure for table `vehicles_type` */

DROP TABLE IF EXISTS `vehicles_type`;

CREATE TABLE `vehicles_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

/*Data for the table `vehicles_type` */

LOCK TABLES `vehicles_type` WRITE;

insert  into `vehicles_type`(`id`,`name`) values (1,'Militar'),(2,'Particular'),(3,'Administrativo'),(4,'Estudiante');

UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
