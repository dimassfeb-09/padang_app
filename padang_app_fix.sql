-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: localhost    Database: padang_app
-- ------------------------------------------------------
-- Server version	8.0.35-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;
/*!50503 SET NAMES utf8mb4 */
;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */
;
/*!40103 SET TIME_ZONE='+00:00' */
;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */
;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */
;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */
;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */
;

--
-- Table structure for table `checkout`
--

CREATE DATABASE padang_app;

USE padang_app;

DROP TABLE IF EXISTS `checkout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE
    `checkout` (
        `id` int NOT NULL AUTO_INCREMENT,
        `product_id` int NOT NULL,
        `user_id` int NOT NULL,
        `quantity` int NOT NULL,
        PRIMARY KEY (`id`),
        KEY `product_id` (`product_id`),
        KEY `user_id` (`user_id`),
        CONSTRAINT `checkout_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
        CONSTRAINT `checkout_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    );
/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `checkout`
--

LOCK TABLES `checkout` WRITE;
/*!40000 ALTER TABLE `checkout` DISABLE KEYS */
;

INSERT INTO `checkout` VALUES (93, 1, 13, 1), (94, 2, 13, 1);
/*!40000 ALTER TABLE `checkout` ENABLE KEYS */
;

UNLOCK TABLES;

--
-- Table structure for table `order_item`
--

DROP TABLE IF EXISTS `order_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE
    `order_item` (
        `id` int NOT NULL AUTO_INCREMENT,
        `order_id` int NOT NULL,
        `product_id` int NOT NULL,
        `quantity` int NOT NULL,
        `subtotal` int NOT NULL,
        PRIMARY KEY (`id`),
        KEY `order_id` (`order_id`),
        KEY `product_id` (`product_id`),
        CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
        CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
    );
/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `order_item`
--

LOCK TABLES `order_item` WRITE;
/*!40000 ALTER TABLE `order_item` DISABLE KEYS */
;

INSERT INTO `order_item`
VALUES (27, 10, 1, 1, 35000), (28, 10, 2, 1, 25000), (29, 12, 2, 1, 25000), (30, 13, 2, 1, 25000), (31, 13, 3, 2, 30000), (32, 14, 2, 1, 25000), (33, 15, 2, 1, 25000), (34, 16, 2, 1, 25000), (35, 17, 2, 1, 25000), (36, 18, 2, 1, 25000), (37, 19, 2, 1, 25000), (38, 20, 3, 1, 15000), (39, 21, 3, 1, 15000), (40, 22, 1, 1, 35000), (41, 22, 2, 1, 25000), (42, 22, 3, 1, 15000), (43, 22, 4, 2, 60000), (44, 22, 5, 1, 28000), (45, 23, 6, 1, 30000), (46, 23, 5, 1, 28000), (47, 23, 2, 1, 25000), (48, 24, 2, 1, 25000), (49, 24, 1, 1, 35000), (50, 24, 3, 1, 15000), (51, 25, 6, 1, 30000), (52, 26, 1, 1, 35000), (53, 27, 1, 1, 35000), (54, 27, 2, 1, 25000), (55, 27, 3, 1, 15000), (56, 28, 2, 1, 25000), (57, 28, 4, 1, 30000), (58, 29, 1, 1, 35000), (59, 30, 6, 1, 30000), (60, 31, 4, 1, 30000), (61, 32, 4, 1, 30000), (62, 32, 5, 1, 28000), (63, 32, 3, 1, 15000), (64, 33, 2, 1, 25000), (65, 33, 6, 1, 30000), (66, 33, 1, 1, 35000), (67, 34, 6, 1, 30000), (68, 34, 3, 1, 15000), (69, 34, 2, 1, 25000), (70, 34, 1, 1, 35000), (71, 34, 4, 1, 30000), (72, 35, 5, 2, 56000), (73, 35, 3, 1, 15000), (74, 35, 4, 1, 30000), (75, 35, 2, 2, 50000), (76, 35, 1, 4, 140000), (77, 36, 1, 1, 35000), (78, 36, 2, 1, 25000), (79, 37, 1, 2, 70000), (80, 37, 5, 1, 28000), (81, 38, 6, 1, 30000), (82, 39, 1, 1, 35000), (83, 40, 4, 1, 30000), (84, 40, 5, 1, 28000);
/*!40000 ALTER TABLE `order_item` ENABLE KEYS */
;

UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE
    `orders` (
        `id` int NOT NULL AUTO_INCREMENT,
        `user_id` int NOT NULL,
        `order_date` datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        KEY `user_id` (`user_id`),
        CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
    );
/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */
;

INSERT INTO `orders`
VALUES (10, 8, '2024-01-05 20:20:31'), (11, 8, '2024-01-05 23:52:01'), (12, 8, '2024-01-05 23:52:08'), (13, 8, '2024-01-06 17:27:53'), (14, 9, '2024-01-06 21:00:24'), (15, 9, '2024-01-06 21:05:14'), (16, 9, '2024-01-06 21:05:48'), (17, 9, '2024-01-06 21:06:41'), (18, 9, '2024-01-06 21:07:06'), (19, 9, '2024-01-06 21:07:44'), (20, 9, '2024-01-06 21:07:57'), (21, 9, '2024-01-06 21:08:34'), (22, 9, '2024-01-06 21:17:27'), (23, 8, '2024-01-06 21:33:49'), (24, 8, '2024-01-06 21:43:57'), (25, 10, '2024-01-06 22:21:33'), (26, 10, '2024-01-06 22:22:41'), (27, 10, '2024-01-06 22:22:56'), (28, 8, '2024-01-06 22:25:02'), (29, 8, '2024-01-06 22:25:50'), (30, 8, '2024-01-06 22:27:27'), (31, 8, '2024-01-06 22:27:49'), (32, 8, '2024-01-06 22:28:48'), (33, 10, '2024-01-06 22:31:42'), (34, 10, '2024-01-06 22:31:53'), (35, 10, '2024-01-06 22:32:13'), (36, 8, '2024-01-07 00:17:35'), (37, 12, '2024-01-07 22:07:20'), (38, 8, '2024-01-07 22:08:19'), (39, 12, '2024-01-07 22:08:44'), (40, 12, '2024-01-07 22:09:02');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */
;

UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE
    `product` (
        `id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(30) NOT NULL,
        `price` int NOT NULL,
        `img` varchar(150) NOT NULL,
        PRIMARY KEY (`id`)
    );
/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */
;

INSERT INTO `product`
VALUES (
        1,
        'Rendang',
        35000,
        'https://asset.kompas.com/crops/AWXtnkYHOrbSxSggVuTs3EzQprM=/10x36:890x623/750x500/data/photo/2023/03/25/641e5ef63dea4.jpg'
    ), (
        2,
        'Sate Padang',
        25000,
        'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Sate_padang_Mak_Sharil_Yogyakarta.jpg/1200px-Sate_padang_Mak_Sharil_Yogyakarta.jpg'
    ), (
        3,
        'Nasi Padang',
        15000,
        'https://cdn.rri.co.id/berita/1/images/1689391542821-images_(22)/1689391542821-images_(22).jpeg'
    ), (
        4,
        'Gulai Kambing',
        30000,
        'https://www.dapurkobe.co.id/wp-content/uploads/gulai-kambing.jpg'
    ), (
        5,
        'Dendeng Balado',
        28000,
        'https://asset.kompas.com/crops/hn8rHYisgVkj5JSznC7YyW_JNpQ=/38x72:838x605/750x500/data/photo/2022/04/02/6247cfd4495ba.jpg'
    ), (
        6,
        'Ayam Pop',
        30000,
        'https://www.goodnewsfromindonesia.id/uploads/post/large-ayam-pop-olahan-ayam-goreng-pucat-khas-restoran-masakan-padang-sumatra-barat-sejarah-.jpg'
    );
/*!40000 ALTER TABLE `product` ENABLE KEYS */
;

UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */
;
/*!50503 SET character_set_client = utf8mb4 */
;

CREATE TABLE
    `users` (
        `id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(50) NOT NULL,
        `email` varchar(50) NOT NULL,
        `password` varchar(10) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `email` (`email`)
    );
/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */
;

INSERT INTO `users`
VALUES (
        8,
        'DIMAS FEBRIYANTO',
        'dimassfeb@gmail.com',
        'asdasd'
    ), (
        9,
        'DIMAS FEBRIYANTO',
        'asdasdasd@asdsd.com',
        'asdasd'
    ), (
        10,
        'tikuy',
        'asd@gmail.com',
        'asdasd'
    ), (
        11,
        'ucok',
        'ucok@gmail.com',
        'ucok'
    ), (
        12,
        'Dimas',
        'dimas@gmail.com',
        'asdasd'
    ), (
        13,
        'ale',
        'aldi@gmail.com',
        'ale123'
    ), (
        14,
        'ewing',
        'ewing@gmail.com',
        'ewing123'
    );
/*!40000 ALTER TABLE `users` ENABLE KEYS */
;

UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */
;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */
;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */
;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */
;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */
;

-- Dump completed on 2024-01-10  0:46:02
