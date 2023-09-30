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
  `arrival time` datetime NOT NULL DEFAULT current_timestamp(),
  `exit_time` datetime NOT NULL DEFAULT current_timestamp(),
  `arrival_km` double DEFAULT NULL,
  `exit_km` double DEFAULT NULL,
  `destiny` varchar(200) DEFAULT NULL,
  `observation` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `access_register_ibfk_1` (`driver_id`),
  KEY `access_register_ibfk_2` (`vehicle_id`),
  CONSTRAINT `access_register_ibfk_1` FOREIGN KEY (`driver_id`) REFERENCES `driver` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `access_register_ibfk_2` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicles` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `access_register_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `access_register` */

LOCK TABLES `access_register` WRITE;

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

insert  into `access_type`(`id`,`name`) values (1,'regular'),(2,'invitado');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `driver` */

LOCK TABLES `driver` WRITE;

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

insert  into `driver_type`(`id`,`name`) values (1,'estudiante'),(2,'docente'),(3,'administrativo'),(4,'militar'),(5,'particular');

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

insert  into `rol`(`rol_id`,`rol_name`) values (1,'super'),(2,'administrador'),(3,'usuario');

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

insert  into `status_type`(`id`,`name`) values (1,'INGRESO'),(2,'SALIDA');

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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `user` */

LOCK TABLES `user` WRITE;

insert  into `user`(`id`,`dni`,`name`,`surname`,`username`,`password`,`fk_user_status_id`) values (1,'0000000000','Super','Admin','G4r1t4_2xx3','$2b$12$Cureq7STeHlTGDC.DuWHD.Jj1EBHC28x1j4Thsj2cWS6coU6TMKri',3),(2,'0000000001','Admin','System','ECu4d0r_2xx3','$2b$12$RJVEdhLO4CdmRgFZEOwntOS3vqdFBFyvQ2QGdOWJjmELSJrexncly',1),(3,'0000000002','Guardia','Seguridad','S3cUrity_Eye','$2b$12$QoTA/UpJPrkWr/PsP0ETn.Wd39iyN0wFL7kZDvUFKCml6YhDgIJ7y',1);

UNLOCK TABLES;

/*Table structure for table `user_rol` */

DROP TABLE IF EXISTS `user_rol`;

CREATE TABLE `user_rol` (
  `user_rol_id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_rol_id` int(11) NOT NULL,
  `fk_user_id` int(11) NOT NULL,
  `editor` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_rol_id`),
  KEY `fk_rol_id` (`fk_rol_id`),
  KEY `fk_user_id` (`fk_user_id`),
  CONSTRAINT `user_rol_ibfk_1` FOREIGN KEY (`fk_rol_id`) REFERENCES `rol` (`rol_id`) ON UPDATE CASCADE,
  CONSTRAINT `user_rol_ibfk_2` FOREIGN KEY (`fk_user_id`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

/*Data for the table `user_rol` */

LOCK TABLES `user_rol` WRITE;

insert  into `user_rol`(`user_rol_id`,`fk_rol_id`,`fk_user_id`,`editor`) values (1,1,1,1),(2,2,2,1),(3,3,3,0);

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

insert  into `user_status`(`user_status_id`,`status_name`) values (1,'habilitado'),(2,'deshabilitado'),(3,'permanente');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*Data for the table `vehicles` */

LOCK TABLES `vehicles` WRITE;

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

insert  into `vehicles_type`(`id`,`name`) values (1,'militar'),(2,'particular'),(3,'administrativo'),(4,'estudiante');

UNLOCK TABLES;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
