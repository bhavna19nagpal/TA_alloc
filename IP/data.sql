-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ta_allocationv3
-- ------------------------------------------------------
-- Server version	5.5.35-0ubuntu0.12.04.2

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add user social auth',7,'add_usersocialauth'),(20,'Can change user social auth',7,'change_usersocialauth'),(21,'Can delete user social auth',7,'delete_usersocialauth'),(22,'Can add nonce',8,'add_nonce'),(23,'Can change nonce',8,'change_nonce'),(24,'Can delete nonce',8,'delete_nonce'),(25,'Can add association',9,'add_association'),(26,'Can change association',9,'change_association'),(27,'Can delete association',9,'delete_association'),(28,'Can add code',10,'add_code'),(29,'Can change code',10,'change_code'),(30,'Can delete code',10,'delete_code'),(31,'Can add document',11,'add_document'),(32,'Can change document',11,'change_document'),(33,'Can delete document',11,'delete_document'),(34,'Can add role_list',12,'add_role_list'),(35,'Can change role_list',12,'change_role_list'),(36,'Can delete role_list',12,'delete_role_list'),(37,'Can add policy',13,'add_policy'),(38,'Can change policy',13,'change_policy'),(39,'Can delete policy',13,'delete_policy'),(40,'Can add course',14,'add_course'),(41,'Can change course',14,'change_course'),(42,'Can delete course',14,'delete_course'),(43,'Can add student_allocated',15,'add_student_allocated'),(44,'Can change student_allocated',15,'change_student_allocated'),(45,'Can delete student_allocated',15,'delete_student_allocated'),(46,'Can add course_allocated',16,'add_course_allocated'),(47,'Can change course_allocated',16,'change_course_allocated'),(48,'Can delete course_allocated',16,'delete_course_allocated'),(49,'Can add student_course_scores',17,'add_student_course_scores'),(50,'Can change student_course_scores',17,'change_student_course_scores'),(51,'Can delete student_course_scores',17,'delete_student_course_scores'),(52,'Can add prereq_univ_set',18,'add_prereq_univ_set'),(53,'Can change prereq_univ_set',18,'change_prereq_univ_set'),(54,'Can delete prereq_univ_set',18,'delete_prereq_univ_set'),(55,'Can add prereq_mapping',19,'add_prereq_mapping'),(56,'Can change prereq_mapping',19,'change_prereq_mapping'),(57,'Can delete prereq_mapping',19,'delete_prereq_mapping'),(58,'Can add skill_kind',20,'add_skill_kind'),(59,'Can change skill_kind',20,'change_skill_kind'),(60,'Can delete skill_kind',20,'delete_skill_kind'),(61,'Can add skill_univ_set',21,'add_skill_univ_set'),(62,'Can change skill_univ_set',21,'change_skill_univ_set'),(63,'Can delete skill_univ_set',21,'delete_skill_univ_set'),(64,'Can add skill_mapping',22,'add_skill_mapping'),(65,'Can change skill_mapping',22,'change_skill_mapping'),(66,'Can delete skill_mapping',22,'delete_skill_mapping'),(67,'Can add student_general',23,'add_student_general'),(68,'Can change student_general',23,'change_student_general'),(69,'Can delete student_general',23,'delete_student_general'),(70,'Can add student_application',24,'add_student_application'),(71,'Can change student_application',24,'change_student_application'),(72,'Can delete student_application',24,'delete_student_application'),(73,'Can add student_prereq_grade',25,'add_student_prereq_grade'),(74,'Can change student_prereq_grade',25,'change_student_prereq_grade'),(75,'Can delete student_prereq_grade',25,'delete_student_prereq_grade'),(76,'Can add student_skill_level',26,'add_student_skill_level'),(77,'Can change student_skill_level',26,'change_student_skill_level'),(78,'Can delete student_skill_level',26,'delete_student_skill_level'),(79,'Can add complaints_request',27,'add_complaints_request'),(80,'Can change complaints_request',27,'change_complaints_request'),(81,'Can delete complaints_request',27,'delete_complaints_request');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$L4oOutyCAmGW$POlErBkTA6BfaVPYfu/E08Lagr/ffSY/qZG1E/4V5Hg=','2015-01-18 10:07:26',1,'admin','','','gagan11046@iiitd.ac.in',1,1,'2015-01-18 10:07:26'),(2,'!7FEEPzqiVPszLDGL8Dei9SPhlQy4DxnAkH0kXWyR','2015-02-18 15:00:01',0,'Gagan11046','Gagan','Khanijau','Gagan11046@iiitd.ac.in',0,1,'2015-01-18 10:08:40'),(3,'!MrmYLDsT4V16TfsaoHmnjfNNALPoR4SAGEy9ETtc','2015-02-18 20:02:55',0,'gagankhanijau','Gagan','Khanijau','gagankhanijau@gmail.com',0,1,'2015-01-18 10:17:41'),(4,'!1oZjLleQtBG5LiO0fEgrpm2uPnxlSfPqVRZqmX7R','2015-02-17 07:19:46',0,'Sourabh11112','Sourabh','Singh','Sourabh11112@iiitd.ac.in',0,1,'2015-02-10 23:22:41'),(5,'!Eitmj1nh1tiuORIcp4Nwsm9BMqynGe9aCJ5InUTi','2015-02-18 05:49:09',0,'gkhanijau','khanijau','gagan','gkhanijau@gmail.com',0,1,'2015-02-17 07:58:28');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'user social auth','default','usersocialauth'),(8,'nonce','default','nonce'),(9,'association','default','association'),(10,'code','default','code'),(11,'document','ta_alloc','document'),(12,'role_list','ta_alloc','role_list'),(13,'policy','ta_alloc','policy'),(14,'course','ta_alloc','course'),(15,'student_allocated','ta_alloc','student_allocated'),(16,'course_allocated','ta_alloc','course_allocated'),(17,'student_course_scores','ta_alloc','student_course_scores'),(18,'prereq_univ_set','ta_alloc','prereq_univ_set'),(19,'prereq_mapping','ta_alloc','prereq_mapping'),(20,'skill_kind','ta_alloc','skill_kind'),(21,'skill_univ_set','ta_alloc','skill_univ_set'),(22,'skill_mapping','ta_alloc','skill_mapping'),(23,'student_general','ta_alloc','student_general'),(24,'student_application','ta_alloc','student_application'),(25,'student_prereq_grade','ta_alloc','student_prereq_grade'),(26,'student_skill_level','ta_alloc','student_skill_level'),(27,'complaints_request','ta_alloc','complaints_request');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1huud09hyl6c9z28wyoqo58pjg57xxmn','ODZhNDY1MDFkN2IyYmMwNjgwZGY4MjM0NDk5ZGEzZTIwOTY0MTY4NTp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoiaGR2d2Z4d0lwRGJ3djk0OU1Wd05IT3hZMFVlSXZVeUwiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjJ9','2015-02-01 10:19:55'),('3qgy26a0vu9vwhn10wtm2cfkvxi7jwuu','ZWYzNzIyY2IyZTM5N2U5MWNhNzNlMjhiYzViNDVjYzc2MjFhZDVkNjp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoidWtCbG0wWDgyM1pJT2VvZWdJdjcwQnZwYWJBUDZ4TEIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjN9','2015-03-04 20:02:55'),('b39buj51xral8k7k2o18az5lp3eo3ibu','Yjc2OTQ0ZTIxYzQyNDlhMzQwZDAwNmFjMTgwMDg2MTlhMjM3ODJiYTp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoiNldTd3NrZDdwVjM2T2lEa1JoWFFXWmNZZTRrRVd1WUIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjN9','2015-03-04 15:01:16'),('gh3s9vedkbj4p9k1scly0pghot7i224g','ZWQwODU4ZjRjMmUwYzdjNzk5ZjcwZTI1MjI3YTlhZjA5MDFjZDk1ZDp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoieWJWc2V4S2pzZmxHQ0hWSHFzVWJZTlJ0bDM0TUQ5eVgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjN9','2015-03-03 19:44:12'),('jwodwsc4ca98wxc221c2cauturjqacjf','MzExMzgyZDMzNTIwZGJlNmYzMTkyMTBhYzU2NjJhMGI3OGFlMjA1Mzp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoiWXk0MlhBQnhyODh3eE53czBWaFI0TkFPYzE4MllUODciLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjR9','2015-03-03 07:19:47'),('mui7d0045hb3xa6w0zkub8h2klsawzax','ZDY3Mjk2YTVjYzlkODNmNjY2NWM5NGRkZWY4ODQzY2NlM2M2OTBiMzp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoicDlJM21EY0prc09PdmVCTDlCRVk2WHBxNmFheFdwUGQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjN9','2015-03-04 16:14:53'),('nmt9mhfri30zct8yytc8t0rbmnlw961m','YmQ4YjRjNjZkMzBjNDA3NDVmOTNlMjMzYTNkZTRiNWYwMmIxZDA5MDp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoiTlNnR0kxd2thNXpCZzVVY2d6UXhOclJQZ3BxUUV0d0YiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjN9','2015-02-01 10:17:42'),('oj2uerxhtvvushppevmf9zyaubab3yw5','MjA0YTJhNjgwOTBjOTI3YjAxNTAyODNhMGY4NmIzN2UzNTUwY2JiMTp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoiZ0dkS3g1SHVuZ05kQWJGU0lucG03eXhsc1BMUWl2a3QiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjN9','2015-03-04 15:40:01'),('ryvslya3idvn21tgzw6xu2xn50bvpm8x','Y2VmMjkyNjUzN2RmZDdjMzZhMzNkZjY4NjQ5OTRhYmVhZDBkNzYzZTp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoiU1NiUjJxMTZXM0x6a2NxY2JzNElnYmE5MTVFYXZCNEoiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjV9','2015-03-04 05:49:09'),('t8i60ldmttg457fgahrcsey5xqb7tyam','M2E3ZWI1YTliY2FlNzkwNDMxZWI1NDEyMTNiMzk0ZjVhODNhZjMwZDp7Imdvb2dsZS1vYXV0aDJfc3RhdGUiOiIzYmpFZU9TSHl1eXRVdmhwNVZXR2NDWXhJdU5XTW9VUyJ9','2015-03-04 09:07:40'),('z5m4crodae494uajo9gnydda2f20rdbr','NTI1OTdkOTNiMDU2MzNmZTliZWJkMzU1NzJkZmFiNjRjZWNkZDRiZjp7InNvY2lhbF9hdXRoX2xhc3RfbG9naW5fYmFja2VuZCI6Imdvb2dsZS1vYXV0aDIiLCJnb29nbGUtb2F1dGgyX3N0YXRlIjoiZ002RWVTNTY0WWJEQ3ZmVXpQUU10Q29YcE5Bb3VjMWQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzb2NpYWwuYmFja2VuZHMuZ29vZ2xlLkdvb2dsZU9BdXRoMiIsIl9hdXRoX3VzZXJfaWQiOjN9','2015-02-24 16:12:34');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_association`
--

DROP TABLE IF EXISTS `social_auth_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(32) NOT NULL,
  `handle` varchar(32) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_association`
--

LOCK TABLES `social_auth_association` WRITE;
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_code`
--

DROP TABLE IF EXISTS `social_auth_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(75) NOT NULL,
  `code` varchar(32) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`,`code`),
  KEY `social_auth_code_09bb5fb3` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_code`
--

LOCK TABLES `social_auth_code` WRITE;
/*!40000 ALTER TABLE `social_auth_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_nonce`
--

DROP TABLE IF EXISTS `social_auth_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(32) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(65) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_nonce`
--

LOCK TABLES `social_auth_nonce` WRITE;
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_usersocialauth`
--

DROP TABLE IF EXISTS `social_auth_usersocialauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_usersocialauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(64) NOT NULL,
  `extra_data` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `provider` (`provider`,`uid`),
  KEY `social_auth_usersocialauth_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_e6cbdf29` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_usersocialauth`
--

LOCK TABLES `social_auth_usersocialauth` WRITE;
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
INSERT INTO `social_auth_usersocialauth` VALUES (1,2,'google-oauth2','Gagan11046@iiitd.ac.in','{\"token_type\": \"Bearer\", \"access_token\": \"ya29.HgH5pTSwWos3VveLzh-eLyrFTAdtaXqOueZeBKZn8OYWLSVx9XswJLpnNZpsFUFW8rY3mjJ-Uvl1tQ\", \"expires\": 3600}'),(2,3,'google-oauth2','gagankhanijau@gmail.com','{\"token_type\": \"Bearer\", \"access_token\": \"ya29.HgHrEfC98dU7rwNi8Q4u3ks6q_MRU8bDMVOOyKTSP6FZsBA-OU3bcm6zQdkdVl1CMGjplzUEdEK_DA\", \"expires\": 3600}'),(3,4,'google-oauth2','Sourabh11112@iiitd.ac.in','{\"token_type\": \"Bearer\", \"access_token\": \"ya29.HQHkxz2ItulHc13ZNT0XI1KzB2Dk0b3uIylLXZ8Q2Q4RfBLSeWo8EzU1\", \"expires\": 3576}'),(4,5,'google-oauth2','gkhanijau@gmail.com','{\"token_type\": \"Bearer\", \"access_token\": \"ya29.HgHxyt7wYu80QrSj3foibKXWS20l1Anf5LZP4o3vtJR_Ch8CFzi-Kc8e9VddS9yb08RLhOvlShh8ZQ\", \"expires\": 3599}');
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_complaints_request`
--

DROP TABLE IF EXISTS `ta_alloc_complaints_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_complaints_request` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `uid_id` int(11) NOT NULL,
  `req` varchar(502) NOT NULL,
  PRIMARY KEY (`aid`),
  KEY `ta_alloc_complaints_request_82ae9392` (`uid_id`),
  CONSTRAINT `uid_id_refs_aid_91cfe113` FOREIGN KEY (`uid_id`) REFERENCES `ta_alloc_role_list` (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_complaints_request`
--

LOCK TABLES `ta_alloc_complaints_request` WRITE;
/*!40000 ALTER TABLE `ta_alloc_complaints_request` DISABLE KEYS */;
INSERT INTO `ta_alloc_complaints_request` VALUES (6,1,'Testing request1'),(7,5,'Testing Request 2'),(9,1,'Testing Request 4'),(10,5,'Testing again');
/*!40000 ALTER TABLE `ta_alloc_complaints_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_course`
--

DROP TABLE IF EXISTS `ta_alloc_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_course` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `cid` varchar(100) NOT NULL,
  `cname` varchar(500) NOT NULL,
  `cdesc` longtext NOT NULL,
  `sem` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `prof_id1_id` int(11) NOT NULL,
  `prof_id2_id` int(11) DEFAULT NULL,
  `reg_no` int(11) NOT NULL,
  `course_type_id` int(11) NOT NULL,
  `tutors_min` int(11) NOT NULL,
  `tutors_max` int(11) NOT NULL,
  `s_ta_min` int(11) NOT NULL,
  `s_ta_max` int(11) NOT NULL,
  `j_ta_min` int(11) NOT NULL,
  `j_ta_max` int(11) NOT NULL,
  `btech_ta_min` int(11) NOT NULL,
  `btech_ta_max` int(11) NOT NULL,
  `select_max` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `cid` (`cid`),
  UNIQUE KEY `cid_2` (`cid`,`sem`,`year`),
  KEY `ta_alloc_course_7e9d44f4` (`prof_id1_id`),
  KEY `ta_alloc_course_fcd7cbd5` (`prof_id2_id`),
  KEY `ta_alloc_course_0ce887d1` (`course_type_id`),
  CONSTRAINT `course_type_id_refs_course_type_65e08858` FOREIGN KEY (`course_type_id`) REFERENCES `ta_alloc_policy` (`course_type`),
  CONSTRAINT `prof_id1_id_refs_aid_052b528c` FOREIGN KEY (`prof_id1_id`) REFERENCES `ta_alloc_role_list` (`aid`),
  CONSTRAINT `prof_id2_id_refs_aid_052b528c` FOREIGN KEY (`prof_id2_id`) REFERENCES `ta_alloc_role_list` (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_course`
--

LOCK TABLES `ta_alloc_course` WRITE;
/*!40000 ALTER TABLE `ta_alloc_course` DISABLE KEYS */;
INSERT INTO `ta_alloc_course` VALUES (3,'CSEtest','Testing of Database','asdasdasda',2,2014,1,NULL,100,1,2,4,4,6,5,7,10,10,0,1);
/*!40000 ALTER TABLE `ta_alloc_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_course_allocated`
--

DROP TABLE IF EXISTS `ta_alloc_course_allocated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_course_allocated` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id_id` int(11) NOT NULL,
  `avg_score` decimal(5,2) NOT NULL,
  `median_rank` decimal(5,2) NOT NULL,
  `ta_required` int(11) NOT NULL,
  `ta_allocated` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ta_alloc_course_allocated_064a9e9c` (`course_id_id`),
  CONSTRAINT `course_id_id_refs_aid_1403aaf9` FOREIGN KEY (`course_id_id`) REFERENCES `ta_alloc_course` (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_course_allocated`
--

LOCK TABLES `ta_alloc_course_allocated` WRITE;
/*!40000 ALTER TABLE `ta_alloc_course_allocated` DISABLE KEYS */;
/*!40000 ALTER TABLE `ta_alloc_course_allocated` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_document`
--

DROP TABLE IF EXISTS `ta_alloc_document`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_document` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `docfile` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_document`
--

LOCK TABLES `ta_alloc_document` WRITE;
/*!40000 ALTER TABLE `ta_alloc_document` DISABLE KEYS */;
INSERT INTO `ta_alloc_document` VALUES (1,'documents/2015/01/18/00/PreRequisites.xls'),(2,'documents/2015/01/18/02/SkillKinds.xls'),(3,'documents/2015/01/18/02/Skills.xls'),(4,'documents/2015/01/18/03/Courses.xls'),(5,'documents/2015/01/18/06/Courses.xls'),(6,'documents/2015/01/18/06/Policy.xls'),(7,'documents/2015/01/18/07/Courses.xls');
/*!40000 ALTER TABLE `ta_alloc_document` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_policy`
--

DROP TABLE IF EXISTS `ta_alloc_policy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_policy` (
  `course_type` int(11) NOT NULL,
  `ratio_tutors_min` int(11) NOT NULL,
  `ratio_s_ta_min` int(11) NOT NULL,
  `ratio_j_ta_min` int(11) NOT NULL,
  `ratio_btech_ta_min` int(11) NOT NULL,
  `ratio_select_max` int(11) NOT NULL,
  PRIMARY KEY (`course_type`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_policy`
--

LOCK TABLES `ta_alloc_policy` WRITE;
/*!40000 ALTER TABLE `ta_alloc_policy` DISABLE KEYS */;
INSERT INTO `ta_alloc_policy` VALUES (1,40,25,20,10,1),(2,10,10,10,10,1),(3,10,10,10,10,1),(4,10,10,10,10,1);
/*!40000 ALTER TABLE `ta_alloc_policy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_prereq_mapping`
--

DROP TABLE IF EXISTS `ta_alloc_prereq_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_prereq_mapping` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `prereq_id` int(11) NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `cid_id` (`cid_id`,`prereq_id`),
  KEY `ta_alloc_prereq_mapping_fdd506be` (`cid_id`),
  KEY `ta_alloc_prereq_mapping_be2ec252` (`prereq_id`),
  CONSTRAINT `cid_id_refs_aid_e18dc4ff` FOREIGN KEY (`cid_id`) REFERENCES `ta_alloc_course` (`aid`),
  CONSTRAINT `prereq_id_refs_aid_bfa1dbd9` FOREIGN KEY (`prereq_id`) REFERENCES `ta_alloc_prereq_univ_set` (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_prereq_mapping`
--

LOCK TABLES `ta_alloc_prereq_mapping` WRITE;
/*!40000 ALTER TABLE `ta_alloc_prereq_mapping` DISABLE KEYS */;
INSERT INTO `ta_alloc_prereq_mapping` VALUES (1,3,1,1),(3,3,2,1);
/*!40000 ALTER TABLE `ta_alloc_prereq_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_prereq_univ_set`
--

DROP TABLE IF EXISTS `ta_alloc_prereq_univ_set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_prereq_univ_set` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` varchar(20) NOT NULL,
  `cname` varchar(50) NOT NULL,
  `year` int(11) NOT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_prereq_univ_set`
--

LOCK TABLES `ta_alloc_prereq_univ_set` WRITE;
/*!40000 ALTER TABLE `ta_alloc_prereq_univ_set` DISABLE KEYS */;
INSERT INTO `ta_alloc_prereq_univ_set` VALUES (1,'1.0','Introduction to Programming',1),(2,'2.0','Digital Circuits',1),(3,'3.0','System Management',1),(4,'4.0','Linear Algebra',1),(5,'5.0','Data Structures and Algorithms',1),(6,'6.0','Electronic circuits-Intro to Engineering Design',1),(7,'7.0','Computer Organisation',1),(8,'8.0','Probability and statistics',1),(9,'9.0','Advanced Programming',2),(10,'10.0','Theory of Computation',2),(11,'11.0','Principles of Communication Systems',2),(12,'12.0','Discrete Maths',2),(13,'13.0','Operating Systems',2),(14,'14.0','Embedded Logic Design',2),(15,'15.0','Linear Circuits',2),(16,'16.0','Signals & Systems',2),(17,'17.0','Math III (Complex Variables-Vector Calculus)',2),(18,'18.0','Fields and Waves',2),(19,'19.0','Integrated Electronics',2),(20,'20.0','Principles of Communication Systems',2),(21,'21.0','Molecular biology and biochemistry',2),(22,'22.0','Computer Networks',2),(23,'23.0','Introduction to DBMS',2),(24,'24.0','Analysis and Design of Algorithms',2),(25,'25.0','Transducers and Signal Conditioning',2),(26,'26.0','Algebra',2),(27,'27.0','Software Engg',3),(28,'28.0','Systems Biology',3),(29,'29.0','Pattern Recognition',3),(30,'30.0','Randomized Algorithms (RA)',3),(31,'31.0','Animation and Graphics',3),(32,'32.0','Semiconductors and Optics',3),(33,'33.0','Computational Genomics',3),(34,'34.0','Secure Coding',3),(35,'35.0','Multimedia Security',3),(36,'36.0','Optimal Control Systems',3),(37,'37.0','Applied Econometric Analysis',3),(38,'38.0','System on Chip Design and Test',3),(39,'39.0','Advanced Signal Processing',3),(40,'40.0','Advanced Embedded Logic Design',3),(41,'41.0','Wavelet Transform and Applications',3),(42,'42.0','Antennas Theory and Design',3),(43,'43.0','Wireless and Cellular System',3),(44,'44.0','Advanced Topics in Mobile Computing',3),(45,'45.0','Algorithms in Spatial Databases',3),(46,'46.0','Multiagent Systems',3),(47,'47.0','Ad Hoc Wireless Networks',3),(48,'48.0','Digital and Cyber Forensics',3),(49,'49.0','Program Optimization',3),(50,'50.0','Computer Vision',3),(51,'51.0','Competitive Programming',3),(52,'52.0','Designing Human-Centred Systems',3),(53,'53.0','Molecular biology and biochemistry',3),(54,'54.0','Algorithms in computational biology',3),(55,'55.0','Logic Programming and Learning (PL)',3),(56,'56.0','Statistical Computation',3),(57,'57.0','Algorithms for discrete optimizations',3),(58,'58.0','Image Analysis',3),(59,'59.0','Machine Learning',3),(60,'60.0','Foundations of Computer Security',3),(61,'61.0','Compilers (NEW)',3),(62,'62.0','Privacy and Security in Online Social Networks',3),(63,'63.0','Data Mining (DM)\"',3),(64,'64.0','Privacy in Location-based Services (PLBS)',3),(65,'65.0','Computer Architecture (CompArch)',3),(66,'66.0','Logic for Computer Science',3),(67,'67.0','Mobile Computing (MC)',3),(68,'68.0','Cellular Data Network',3),(69,'69.0','Applied Cryptography (AC)',3),(70,'70.0','Graduate Algorithms',3),(71,'71.0','PvsNP',3),(72,'72.0','Theory of Modern Cryptography',3),(73,'73.0','Probability and Random Processes',3),(74,'74.0','Digital Hardware Design(DHD)',3),(75,'75.0','Introduction to VLSI Design (IVD)',3),(76,'76.0','Analog Circuit Design',3),(77,'77.0','Operating Systems',3),(78,'78.0','Collabortive Filtering',3),(79,'79.0','Introduction to Economic Analysis',3),(80,'80.0','Economics of Information & IT',3),(81,'81.0','Entrepreneurship',3),(82,'82.0','Robotics',3),(83,'83.0','Physics-1',3),(84,'84.0','Digital and Cyber Forensics',3),(85,'85.0','Elementary Number Theory',3),(86,'86.0','Theory of Modern Cryptography',3),(87,'87.0','Information Retrieval',3),(88,'88.0','Advanced topics in Mobile Computing',3),(89,'89.0','Ad Hoc Wireless Networks',3),(90,'90.0','Biometrics',3),(91,'91.0','Verification of Reactive Systems',3),(92,'92.0','Entrepreneurship as Career II',3),(93,'93.0','Technical Communication',3),(94,'94.0','Embedded Systems',3),(95,'95.0','Topics in Crypt-analysis',3),(96,'96.0','Intelligent Systems 1',3),(97,'97.0','Introduction to Computational',3),(98,'98.0','Neuroscience',3),(99,'99.0','Applied Econometric Analysis',3),(100,'100.0','System on Chip Design and Test',3),(101,'101.0','Advanced FPGA Design',3),(102,'102.0','Advanced Signal Processing',3),(103,'103.0','RF Circuit Design',3),(104,'104.0','Semiconductors and Optics',3),(105,'105.0','Transducers & Signal Conditioning',3),(106,'106.0','Multiagent systems',3),(107,'107.0','Multimedia',3),(108,'108.0','Designing Human-Centered Systems (HCI)',3),(109,'109.0','Network Protocol Security',3),(110,'110.0','Theory of Computation',3),(111,'111.0','Database System Implementation',3);
/*!40000 ALTER TABLE `ta_alloc_prereq_univ_set` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_role_list`
--

DROP TABLE IF EXISTS `ta_alloc_role_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_role_list` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `loginid` varchar(50) NOT NULL,
  `role` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `program` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `loginid` (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_role_list`
--

LOCK TABLES `ta_alloc_role_list` WRITE;
/*!40000 ALTER TABLE `ta_alloc_role_list` DISABLE KEYS */;
INSERT INTO `ta_alloc_role_list` VALUES (1,'gagankhanijau@gmail.com',9,1,0),(2,'gagan11046@iiitd.ac.in',0,1,0),(3,'prakhar11074@iiitd.ac.in',9,1,-1),(4,'gkhanijau@gmail.com',0,1,4),(5,'sourabh11112@iiitd.ac.in',0,1,0),(6,'g@gmail.com',1,1,-1);
/*!40000 ALTER TABLE `ta_alloc_role_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_skill_kind`
--

DROP TABLE IF EXISTS `ta_alloc_skill_kind`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_skill_kind` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `kname` varchar(50) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `kname` (`kname`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_skill_kind`
--

LOCK TABLES `ta_alloc_skill_kind` WRITE;
/*!40000 ALTER TABLE `ta_alloc_skill_kind` DISABLE KEYS */;
INSERT INTO `ta_alloc_skill_kind` VALUES (1,'ECE'),(3,'Miscelleneous'),(4,'Programming'),(2,'System Skills'),(5,'Theory');
/*!40000 ALTER TABLE `ta_alloc_skill_kind` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_skill_mapping`
--

DROP TABLE IF EXISTS `ta_alloc_skill_mapping`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_skill_mapping` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `cid_id` int(11) NOT NULL,
  `skill_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `cid_id` (`cid_id`,`skill_id`),
  KEY `ta_alloc_skill_mapping_fdd506be` (`cid_id`),
  KEY `ta_alloc_skill_mapping_85a9a3f0` (`skill_id`),
  CONSTRAINT `cid_id_refs_aid_279729a5` FOREIGN KEY (`cid_id`) REFERENCES `ta_alloc_course` (`aid`),
  CONSTRAINT `skill_id_refs_aid_b04ab921` FOREIGN KEY (`skill_id`) REFERENCES `ta_alloc_skill_univ_set` (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_skill_mapping`
--

LOCK TABLES `ta_alloc_skill_mapping` WRITE;
/*!40000 ALTER TABLE `ta_alloc_skill_mapping` DISABLE KEYS */;
INSERT INTO `ta_alloc_skill_mapping` VALUES (1,3,13,5);
/*!40000 ALTER TABLE `ta_alloc_skill_mapping` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_skill_univ_set`
--

DROP TABLE IF EXISTS `ta_alloc_skill_univ_set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_skill_univ_set` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `sname` varchar(50) NOT NULL,
  `kind_id` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `sname` (`sname`),
  KEY `ta_alloc_skill_univ_set_21ec032f` (`kind_id`),
  CONSTRAINT `kind_id_refs_aid_0d63f377` FOREIGN KEY (`kind_id`) REFERENCES `ta_alloc_skill_kind` (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_skill_univ_set`
--

LOCK TABLES `ta_alloc_skill_univ_set` WRITE;
/*!40000 ALTER TABLE `ta_alloc_skill_univ_set` DISABLE KEYS */;
INSERT INTO `ta_alloc_skill_univ_set` VALUES (1,'HDL Coding',1),(2,'Robotics',1),(3,'EDA tools',1),(4,'Circuit Theory',1),(5,'Analog Circuits',1),(6,'Hardware lab',1),(7,'Radio frequency',1),(8,'Microcontrollers',1),(9,'FPGA',1),(10,'Computer architecture',1),(11,'Verilog',1),(12,'Hardware Design',1),(13,'TTL & CMOS chips',1),(14,'Linear Systems in ECE',1),(15,'Basic Linux',2),(16,'Networking',2),(17,'Shell Scripting',2),(18,'kernel programming',2),(19,'Socket programming',2),(20,'Web development',3),(21,'Databases',3),(22,'Mobile development',3),(23,'software testing',3),(24,'Courseware tools (moodle)',3),(25,'software engineering',3),(26,'C',4),(27,'C++',4),(28,'Java',4),(29,'Python',4),(30,'Android',4),(31,'IOS',4),(32,'PHP',4),(33,'Matlab',4),(34,'C#.net',4),(35,'Linear algebra',5),(36,'Data Structure and Algorithms',5),(37,'Discrete mathematics',5),(38,'Linear Systems',5),(39,'Probability',5),(40,'Analysis and Design of Algorithms',5),(41,'Geometry',5);
/*!40000 ALTER TABLE `ta_alloc_skill_univ_set` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_student_allocated`
--

DROP TABLE IF EXISTS `ta_alloc_student_allocated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_student_allocated` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id_id` int(11) NOT NULL,
  `course_id_id` int(11) NOT NULL,
  `rank` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `course_id_id` (`course_id_id`,`student_id_id`),
  KEY `ta_alloc_student_allocated_001718d2` (`student_id_id`),
  KEY `ta_alloc_student_allocated_064a9e9c` (`course_id_id`),
  CONSTRAINT `course_id_id_refs_aid_31132809` FOREIGN KEY (`course_id_id`) REFERENCES `ta_alloc_course` (`aid`),
  CONSTRAINT `student_id_id_refs_aid_757ace63` FOREIGN KEY (`student_id_id`) REFERENCES `ta_alloc_role_list` (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_student_allocated`
--

LOCK TABLES `ta_alloc_student_allocated` WRITE;
/*!40000 ALTER TABLE `ta_alloc_student_allocated` DISABLE KEYS */;
INSERT INTO `ta_alloc_student_allocated` VALUES (1,2,3,0.00);
/*!40000 ALTER TABLE `ta_alloc_student_allocated` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_student_application`
--

DROP TABLE IF EXISTS `ta_alloc_student_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_student_application` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `uid_id` varchar(50) NOT NULL,
  `cid_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `pref` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `uid_id` (`uid_id`,`cid_id`),
  KEY `ta_alloc_student_application_82ae9392` (`uid_id`),
  KEY `ta_alloc_student_application_fdd506be` (`cid_id`),
  CONSTRAINT `cid_id_refs_aid_ee30cc91` FOREIGN KEY (`cid_id`) REFERENCES `ta_alloc_course` (`aid`),
  CONSTRAINT `uid_id_refs_loginid_id_f91c3b68` FOREIGN KEY (`uid_id`) REFERENCES `ta_alloc_student_general` (`loginid_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_student_application`
--

LOCK TABLES `ta_alloc_student_application` WRITE;
/*!40000 ALTER TABLE `ta_alloc_student_application` DISABLE KEYS */;
INSERT INTO `ta_alloc_student_application` VALUES (1,'gagan11046@iiitd.ac.in',3,10,1,1),(2,'sourabh11112@iiitd.ac.in',3,10,0,1),(3,'gkhanijau@gmail.com',3,10,0,1);
/*!40000 ALTER TABLE `ta_alloc_student_application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_student_course_scores`
--

DROP TABLE IF EXISTS `ta_alloc_student_course_scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_student_course_scores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id_id` int(11) NOT NULL,
  `course_id_id` int(11) NOT NULL,
  `score` decimal(5,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ta_alloc_student_course_scores_001718d2` (`student_id_id`),
  KEY `ta_alloc_student_course_scores_064a9e9c` (`course_id_id`),
  CONSTRAINT `course_id_id_refs_aid_4efbd7cc` FOREIGN KEY (`course_id_id`) REFERENCES `ta_alloc_course` (`aid`),
  CONSTRAINT `student_id_id_refs_aid_6102890d` FOREIGN KEY (`student_id_id`) REFERENCES `ta_alloc_role_list` (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_student_course_scores`
--

LOCK TABLES `ta_alloc_student_course_scores` WRITE;
/*!40000 ALTER TABLE `ta_alloc_student_course_scores` DISABLE KEYS */;
/*!40000 ALTER TABLE `ta_alloc_student_course_scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_student_general`
--

DROP TABLE IF EXISTS `ta_alloc_student_general`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_student_general` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `loginid_id` varchar(50) NOT NULL,
  `roll_no` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `program` int(11) NOT NULL,
  `other_courses` longtext NOT NULL,
  `other_skills` longtext NOT NULL,
  `status` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `loginid_id` (`loginid_id`),
  CONSTRAINT `loginid_id_refs_loginid_4eb32dab` FOREIGN KEY (`loginid_id`) REFERENCES `ta_alloc_role_list` (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_student_general`
--

LOCK TABLES `ta_alloc_student_general` WRITE;
/*!40000 ALTER TABLE `ta_alloc_student_general` DISABLE KEYS */;
INSERT INTO `ta_alloc_student_general` VALUES (1,'gagan11046@iiitd.ac.in','2011046','Gagan',0,'','',1),(3,'sourabh11112@iiitd.ac.in','2011112','Sourabh',0,'','',0),(4,'gkhanijau@gmail.com','20101','Khanijau Gagan',4,'','',0);
/*!40000 ALTER TABLE `ta_alloc_student_general` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_student_prereq_grade`
--

DROP TABLE IF EXISTS `ta_alloc_student_prereq_grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_student_prereq_grade` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `uid_id` varchar(50) NOT NULL,
  `pid_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `uid_id` (`uid_id`,`pid_id`),
  KEY `ta_alloc_student_prereq_grade_82ae9392` (`uid_id`),
  KEY `ta_alloc_student_prereq_grade_664e8aab` (`pid_id`),
  CONSTRAINT `pid_id_refs_aid_a3d9430f` FOREIGN KEY (`pid_id`) REFERENCES `ta_alloc_prereq_univ_set` (`aid`),
  CONSTRAINT `uid_id_refs_loginid_854622b9` FOREIGN KEY (`uid_id`) REFERENCES `ta_alloc_role_list` (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_student_prereq_grade`
--

LOCK TABLES `ta_alloc_student_prereq_grade` WRITE;
/*!40000 ALTER TABLE `ta_alloc_student_prereq_grade` DISABLE KEYS */;
INSERT INTO `ta_alloc_student_prereq_grade` VALUES (1,'gagan11046@iiitd.ac.in',1,10),(2,'gagan11046@iiitd.ac.in',2,4),(3,'sourabh11112@iiitd.ac.in',1,8),(4,'sourabh11112@iiitd.ac.in',2,8),(5,'gkhanijau@gmail.com',1,9),(6,'gkhanijau@gmail.com',2,9);
/*!40000 ALTER TABLE `ta_alloc_student_prereq_grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ta_alloc_student_skill_level`
--

DROP TABLE IF EXISTS `ta_alloc_student_skill_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ta_alloc_student_skill_level` (
  `aid` int(11) NOT NULL AUTO_INCREMENT,
  `uid_id` varchar(50) NOT NULL,
  `sid_id` int(11) NOT NULL,
  `value` int(11) NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `uid_id` (`uid_id`,`sid_id`),
  KEY `ta_alloc_student_skill_level_82ae9392` (`uid_id`),
  KEY `ta_alloc_student_skill_level_9563f214` (`sid_id`),
  CONSTRAINT `sid_id_refs_aid_1146eab9` FOREIGN KEY (`sid_id`) REFERENCES `ta_alloc_skill_univ_set` (`aid`),
  CONSTRAINT `uid_id_refs_loginid_705e7a3b` FOREIGN KEY (`uid_id`) REFERENCES `ta_alloc_role_list` (`loginid`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ta_alloc_student_skill_level`
--

LOCK TABLES `ta_alloc_student_skill_level` WRITE;
/*!40000 ALTER TABLE `ta_alloc_student_skill_level` DISABLE KEYS */;
INSERT INTO `ta_alloc_student_skill_level` VALUES (1,'gagan11046@iiitd.ac.in',13,9),(2,'sourabh11112@iiitd.ac.in',1,5),(3,'sourabh11112@iiitd.ac.in',2,5),(4,'sourabh11112@iiitd.ac.in',3,7),(5,'sourabh11112@iiitd.ac.in',4,5),(6,'sourabh11112@iiitd.ac.in',5,5),(7,'sourabh11112@iiitd.ac.in',6,5),(8,'sourabh11112@iiitd.ac.in',7,5),(9,'sourabh11112@iiitd.ac.in',8,7),(10,'sourabh11112@iiitd.ac.in',9,5),(11,'sourabh11112@iiitd.ac.in',10,5),(12,'sourabh11112@iiitd.ac.in',11,5),(13,'sourabh11112@iiitd.ac.in',12,5),(14,'sourabh11112@iiitd.ac.in',13,0),(15,'sourabh11112@iiitd.ac.in',14,5),(16,'sourabh11112@iiitd.ac.in',15,5),(17,'sourabh11112@iiitd.ac.in',16,5),(18,'sourabh11112@iiitd.ac.in',17,7),(19,'sourabh11112@iiitd.ac.in',18,5),(20,'sourabh11112@iiitd.ac.in',19,5),(21,'sourabh11112@iiitd.ac.in',20,5),(22,'sourabh11112@iiitd.ac.in',21,5),(23,'sourabh11112@iiitd.ac.in',22,5),(24,'sourabh11112@iiitd.ac.in',23,5),(25,'sourabh11112@iiitd.ac.in',24,5),(26,'sourabh11112@iiitd.ac.in',25,5),(27,'sourabh11112@iiitd.ac.in',26,5),(28,'sourabh11112@iiitd.ac.in',27,5),(29,'sourabh11112@iiitd.ac.in',28,5),(30,'sourabh11112@iiitd.ac.in',29,5),(31,'sourabh11112@iiitd.ac.in',30,5),(32,'sourabh11112@iiitd.ac.in',31,5),(33,'sourabh11112@iiitd.ac.in',32,5),(34,'sourabh11112@iiitd.ac.in',33,5),(35,'sourabh11112@iiitd.ac.in',34,5),(36,'sourabh11112@iiitd.ac.in',35,5),(37,'sourabh11112@iiitd.ac.in',36,5),(38,'sourabh11112@iiitd.ac.in',37,5),(39,'sourabh11112@iiitd.ac.in',38,5),(40,'sourabh11112@iiitd.ac.in',39,5),(41,'sourabh11112@iiitd.ac.in',40,5),(42,'sourabh11112@iiitd.ac.in',41,5),(43,'gkhanijau@gmail.com',13,9);
/*!40000 ALTER TABLE `ta_alloc_student_skill_level` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-02-19  2:07:04
