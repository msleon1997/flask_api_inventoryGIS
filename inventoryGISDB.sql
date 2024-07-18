/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE TABLE IF NOT EXISTS `mapa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `geometry` geometry NOT NULL,
  PRIMARY KEY (`id`),
  SPATIAL KEY `geometry` (`geometry`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS `ordenes_compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `codigo_compra` varchar(5) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `cantidad` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `impuesto` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `observaciones` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_creacion` date NOT NULL,
  `estado` int NOT NULL,
  `users_id` int NOT NULL,
  `proveedores_id` int NOT NULL,
  `producto_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_ordenes_compra_users1_idx` (`users_id`),
  KEY `fk_ordenes_compra_tproveedores1_idx` (`proveedores_id`) USING BTREE,
  KEY `fk_ordenes_compra_tproducto1_idx` (`producto_id`) USING BTREE,
  CONSTRAINT `fk_ordenes_compra_tproducto1` FOREIGN KEY (`producto_id`) REFERENCES `tproducto` (`id`),
  CONSTRAINT `fk_ordenes_compra_tproveedores1` FOREIGN KEY (`proveedores_id`) REFERENCES `tproveedores` (`id`),
  CONSTRAINT `fk_ordenes_compra_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `ordenes_compra` (`id`, `codigo_compra`, `cantidad`, `precio`, `impuesto`, `descuento`, `total`, `observaciones`, `fecha_creacion`, `estado`, `users_id`, `proveedores_id`, `producto_id`) VALUES
	(2, 'C002', 20, 2.50, 15.00, 0.00, 57.50, 'nada', '2024-07-14', 2, 39, 1, 6),
	(9, 'p005', 10, 150.00, 15.00, 0.00, 1725.00, 'nada', '2024-07-16', 1, 39, 1, 4),
	(10, 'C006', 5, 5.00, 15.00, 0.00, 28.75, 'nuevo stock', '2024-07-17', 3, 39, 3, 4),
	(11, 'C006', 100, 1200.00, 15.00, 0.00, 138000.00, 'nuevo stock', '2024-07-18', 3, 39, 1, 1),
	(12, 'C006', 60, 1.50, 15.00, 0.00, 103.50, 'nuevo stock ', '2024-07-18', 3, 39, 3, 10),
	(14, 'C006', 20, 1.50, 15.00, 0.00, 34.50, 'nuevo stock', '2024-07-18', 3, 39, 1, 10);

CREATE TABLE IF NOT EXISTS `system_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `meta_field` text COLLATE utf8mb4_general_ci NOT NULL,
  `meta_value` text COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `system_info` (`id`, `meta_field`, `meta_value`) VALUES
	(1, 'name', 'Sistema de Inventario InventoryGIS'),
	(6, 'short_name', 'SIG'),
	(11, 'logo', 'uploads/logo-1647660173.png'),
	(13, 'user_avatar', 'uploads/user_avatar.jpg'),
	(14, 'cover', 'uploads/fondo-login.jpg');

CREATE TABLE IF NOT EXISTS `tcliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `CLI_Identificacion` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `CLI_TipoIdentificacion` varchar(1) COLLATE utf8mb4_general_ci NOT NULL,
  `CLI_NombresCompletos` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `CLI_Direccion` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `CLI_Telefono` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `CLI_Correo` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `CLI_FechaNacimiento` date NOT NULL,
  `CLI_FechaCreacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `users_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_TCliente_users` (`users_id`),
  CONSTRAINT `FK_TCliente_users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tcliente` (`id`, `CLI_Identificacion`, `CLI_TipoIdentificacion`, `CLI_NombresCompletos`, `CLI_Direccion`, `CLI_Telefono`, `CLI_Correo`, `CLI_FechaNacimiento`, `CLI_FechaCreacion`, `users_id`) VALUES
	(9, '0107356511', 'C', 'Marlon Santiago Leon Beltran ', 'av. de los laureles', '0984158557', 'marlonsantiagoleonbeltran@gmail.com', '1997-07-04', '2024-07-18 01:28:37', 39),
	(11, '0100750058', 'C', 'Juan Diego Ambrosi Morales', 'av. de los laureles', '0984158557', 'marlonslb@outlook.com', '1997-07-04', '2024-07-13 19:14:39', 39),
	(12, '0178946131', 'C', 'Diana Elizabeth Mendez Perez', 'av. de los laureles', '0984158557', 'marlonslb@outlook.com', '2024-07-02', '2024-07-13 22:06:44', 39);

CREATE TABLE IF NOT EXISTS `tdevoluciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `DEV_codigo_devolucion` varchar(10) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `DEV_unidad` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `DEV_cantidad_devuelta` int NOT NULL,
  `DEV_producto_costo` decimal(10,2) NOT NULL,
  `DEV_total_devolucion` decimal(10,2) NOT NULL,
  `DEV_fecha_devolucion` datetime DEFAULT CURRENT_TIMESTAMP,
  `DEV_razon_devolucion` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `DEV_estado_devolucion` int DEFAULT NULL,
  `DEV_notas` text COLLATE utf8mb4_general_ci,
  `proveedor_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `users_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_DevolucionesProveedor_Proveedor` (`proveedor_id`),
  KEY `FK_DevolucionesProveedor_Producto` (`producto_id`),
  KEY `FK_DevolucionesProveedor_Users` (`users_id`),
  CONSTRAINT `FK_DevolucionesProveedor_Producto` FOREIGN KEY (`producto_id`) REFERENCES `tproducto` (`id`),
  CONSTRAINT `FK_DevolucionesProveedor_Proveedor` FOREIGN KEY (`proveedor_id`) REFERENCES `tproveedores` (`id`),
  CONSTRAINT `FK_DevolucionesProveedor_Users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tdevoluciones` (`id`, `DEV_codigo_devolucion`, `DEV_unidad`, `DEV_cantidad_devuelta`, `DEV_producto_costo`, `DEV_total_devolucion`, `DEV_fecha_devolucion`, `DEV_razon_devolucion`, `DEV_estado_devolucion`, `DEV_notas`, `proveedor_id`, `producto_id`, `users_id`) VALUES
	(14, 'dev001', 'kilos', 2, 2.50, 5.00, '2024-07-14 16:29:10', 'expiradas', 2, 'ninguna', 1, 6, 39),
	(15, 'dev002', 'kilos', 5, 250.00, 1250.00, '2024-07-06 20:08:43', 'dasdsadaf', 3, 'dsfdfsdfs', 1, 4, 39),
	(16, 'dev003', 'kilos', 2, 500.00, 1000.00, '2024-07-18 00:47:45', 'falla técnica', 2, '', 3, 1, 39);

CREATE TABLE IF NOT EXISTS `texistencias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `EXIS_Descripcion_product` varchar(500) NOT NULL,
  `EXIS_Existencias_cant` int NOT NULL,
  `EXIS_Fecha` date NOT NULL,
  `EXIS_Categoria_product` varchar(55) NOT NULL,
  `producto_id` int NOT NULL,
  `proveedor_id` int NOT NULL,
  `users_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idExistencias_UNIQUE` (`id`),
  KEY `fk_Existencias_users1_idx` (`users_id`),
  KEY `fk_Existencias_tproducto1_idx` (`producto_id`) USING BTREE,
  KEY `fk_Existencias_tproveedores1_idx` (`proveedor_id`) USING BTREE,
  CONSTRAINT `fk_Existencias_tproducto1` FOREIGN KEY (`producto_id`) REFERENCES `tproducto` (`id`),
  CONSTRAINT `fk_Existencias_tproveedores1` FOREIGN KEY (`proveedor_id`) REFERENCES `tproveedores` (`id`),
  CONSTRAINT `fk_Existencias_users1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `texistencias` (`id`, `EXIS_Descripcion_product`, `EXIS_Existencias_cant`, `EXIS_Fecha`, `EXIS_Categoria_product`, `producto_id`, `proveedor_id`, `users_id`) VALUES
	(1, 'galletas de sal', 20, '2024-07-08', 'productos consumibles', 6, 1, 35);

CREATE TABLE IF NOT EXISTS `tproducto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `PRO_Nombre` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `PRO_Descripcion` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `PRO_Precio` decimal(18,2) NOT NULL,
  `PRO_ExcentoIva` int NOT NULL DEFAULT '0',
  `PRO_FechaCreacion` datetime NOT NULL,
  `PRO_Cantidad` int NOT NULL,
  `PRO_Total` decimal(18,2) NOT NULL,
  `PRO_Estado` int NOT NULL,
  `users_id` int NOT NULL,
  `proveedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_TProducto_Users` (`users_id`),
  KEY `fk_tproducto_tproveedores1_idx` (`proveedor_id`) USING BTREE,
  CONSTRAINT `fk_tproducto_tproveedores1` FOREIGN KEY (`proveedor_id`) REFERENCES `tproveedores` (`id`),
  CONSTRAINT `FK_TProducto_Users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tproducto` (`id`, `PRO_Nombre`, `PRO_Descripcion`, `PRO_Precio`, `PRO_ExcentoIva`, `PRO_FechaCreacion`, `PRO_Cantidad`, `PRO_Total`, `PRO_Estado`, `users_id`, `proveedor_id`) VALUES
	(1, 'Computadoras', 'intel, amd', 500.00, 15, '2024-07-11 21:34:09', 99, 0.00, 1, 39, 1),
	(4, 'Procesadores', 'intel, ryzen', 250.00, 15, '2024-07-05 16:41:24', 50, 35.60, 2, 39, 1),
	(6, 'galletas', 'salticas', 2.50, 15, '2024-07-07 20:43:10', 5, 34.50, 2, 39, 1),
	(10, 'papas', 'funda de papas fritas', 0.80, 15, '2024-07-18 09:38:24', 105, 92.00, 2, 39, 1);

CREATE TABLE IF NOT EXISTS `tproveedores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `PROV_Identificacion` varchar(13) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `PROV_nombre_empresa` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `PROV_direccion` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `PROV_persona` varchar(45) COLLATE utf8mb4_general_ci NOT NULL,
  `PROV_email` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `PROV_telefono` varchar(20) COLLATE utf8mb4_general_ci NOT NULL,
  `PROV_pagina_web` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `PROV_fecha_registro` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `notas` text COLLATE utf8mb4_general_ci,
  `estado_proveedor` int NOT NULL DEFAULT '0',
  `PM_Ciudad` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `PM_Provincia` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `PM_Longitud` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `PM_Latitud` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `users_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Proveedores_Users` (`users_id`),
  CONSTRAINT `FK_Proveedores_Users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tproveedores` (`id`, `PROV_Identificacion`, `PROV_nombre_empresa`, `PROV_direccion`, `PROV_persona`, `PROV_email`, `PROV_telefono`, `PROV_pagina_web`, `PROV_fecha_registro`, `notas`, `estado_proveedor`, `PM_Ciudad`, `PM_Provincia`, `PM_Longitud`, `PM_Latitud`, `users_id`) VALUES
	(1, '0107356511', 'UCACUE', 'CENTRO', 'SCRUM MASTER', 'email@gmail.com', '0986493497', 'catolica@est.ucacue.edu.ec', '2024-07-17 15:44:58', 'este es un ejemplo', 2, 'Azogues', 'Cañar', '-78.8442', '-2.7416', 39),
	(3, '1164654646', 'SUSUN', 'av. mexico', 'Guillermo del Toro', 'guille@gmail.com', '0984513132', '', '2024-07-15 21:10:10', 'cambio de ubicacion', 2, 'Quito', 'Pichincha', '-78.4678', '-0.1807', 39),
	(4, '0188613513', 'centrosur', 'Luis cordero y juan jaramillo', 'Ismael Jimenez', 'isma@centrosur.ec', '0984513132', '', '2024-07-17 23:27:48', 'nuevo proveedor', 2, 'Cuenca', 'Azuay', '-79.00453', '-2.90055', 39),
	(5, '0144567891', 'Armadon ', 'Luis cordero y juan jaramillo', 'Jose luis', 'guille@gmail.com', '0984513132', '', '2024-07-18 00:21:14', '', 2, 'Puyo', 'Pastaza', '-77.89169419425103', '-1.4718000824125514', 39),
	(6, '0146664131', 'Cocacola', 'Jose de orozco y juan montalvo', 'Diego Fernz', 'diego@gmail.com', '0984513132', '', '2024-07-17 22:56:42', '', 1, 'Riobamba', 'Chimborazo', '-78.6546', '-1.6636', 39),
	(7, '0166557535', 'Laragon', 'camilo monte negro', 'Ismael Jimenez', 'lara@gmail.com', '0883800', '', '2024-07-17 23:20:39', '', 2, 'Guaranda', 'Bolívar', '-78.99873756277721', '-1.5960812585736526', 39);

CREATE TABLE IF NOT EXISTS `tventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `VENT_codigo_venta` varchar(10) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `cliente_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `VENT_cantidad` int NOT NULL,
  `VENT_producto_costo` decimal(10,2) NOT NULL,
  `VENT_total` decimal(10,2) NOT NULL,
  `VENT_fecha_venta` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `VENT_estado_venta` int DEFAULT NULL,
  `VENT_notas` text COLLATE utf8mb4_general_ci,
  `users_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Ventas_Producto` (`producto_id`),
  KEY `FK_Ventas_Cliente` (`cliente_id`),
  KEY `FK_Ventas_Users` (`users_id`),
  CONSTRAINT `FK_Ventas_Cliente` FOREIGN KEY (`cliente_id`) REFERENCES `tcliente` (`id`),
  CONSTRAINT `FK_Ventas_Producto` FOREIGN KEY (`producto_id`) REFERENCES `tproducto` (`id`),
  CONSTRAINT `FK_Ventas_Users` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `tventas` (`id`, `VENT_codigo_venta`, `cliente_id`, `producto_id`, `VENT_cantidad`, `VENT_producto_costo`, `VENT_total`, `VENT_fecha_venta`, `VENT_estado_venta`, `VENT_notas`, `users_id`) VALUES
	(1, 'v001', 11, 1, 5, 500.00, 2875.00, '2024-07-14 16:30:55', 1, 'venta de 5 pc completas', 39),
	(4, 'v002', 9, 4, 2, 250.00, 575.00, '2024-07-14 12:33:10', 3, 'nada', 39),
	(5, 'f003', 9, 4, 5, 250.00, 1437.50, '2024-07-16 00:20:52', 3, 'venta concretada', 39),
	(6, 'v003', 9, 6, 5, 2.50, 14.38, '2024-07-18 01:16:20', 3, '', 39),
	(7, 'v004', 9, 1, 1, 500.00, 575.00, '2024-07-18 09:13:07', 3, 'venta concretada', 39),
	(8, 'v005', 9, 10, 5, 0.80, 4.60, '2024-07-18 10:24:07', 3, 'venta concretada', 39),
	(9, 'v006', 9, 6, 5, 2.50, 14.38, '2024-07-18 10:37:35', 3, 'venta concretada', 39),
	(10, 'v007', 11, 6, 2, 2.50, 5.75, '2024-07-18 10:48:31', 3, 'venta concretada', 39);

CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cedula` varchar(10) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `firstname` varchar(250) COLLATE utf8mb4_general_ci NOT NULL,
  `middlename` text COLLATE utf8mb4_general_ci,
  `lastname` varchar(250) COLLATE utf8mb4_general_ci NOT NULL,
  `username` text COLLATE utf8mb4_general_ci,
  `password` text COLLATE utf8mb4_general_ci NOT NULL,
  `avatar` text COLLATE utf8mb4_general_ci,
  `last_login` datetime DEFAULT NULL,
  `type` tinyint(1) NOT NULL DEFAULT '0',
  `status` int NOT NULL DEFAULT '1' COMMENT '0=not verified, 1 = verified',
  `date_added` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `users` (`id`, `cedula`, `firstname`, `middlename`, `lastname`, `username`, `password`, `avatar`, `last_login`, `type`, `status`, `date_added`, `date_updated`) VALUES
	(35, '0100750058', 'Natalia', NULL, 'Alvarado', NULL, '$2y$10$dw7st9etlxCzTnvkqFgpuuZATvQsrQM8WsXLwlRwPA0Ab972.5rYi', NULL, NULL, 1, 1, '2024-06-24 23:48:15', NULL),
	(39, '0107356511', 'Marlon', NULL, 'leon', NULL, '$2y$10$9F9t4ra5REZ7CeeM6c.qPuEdXigqPRo0LZRlQgocvX4JYZ2nUCyMi', NULL, NULL, 1, 1, '2024-06-26 22:38:26', NULL),
	(40, '0106758477', 'Mateo', NULL, 'Bravo', NULL, '$2y$10$oB5GFaQZ1nOq29hfrQVB/uiln63KjIJvmo01u3mrXbW2zebdr.s9G', NULL, NULL, 1, 1, '2024-07-02 00:49:07', NULL),
	(41, '0150492700', 'Natali', NULL, 'Balverde', NULL, '$2y$10$S5Z0gEuF307JYXLwKrB.QO2K5KTnt3OIk9efUdyhA86JMpJ5RFO/K', NULL, NULL, 1, 1, '2024-07-04 00:39:36', NULL);

SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tgr_actualizarstock` AFTER INSERT ON `ordenes_compra` FOR EACH ROW BEGIN
    
        UPDATE tproducto
        SET PRO_Cantidad = PRO_Cantidad + NEW.cantidad
        WHERE id = NEW.producto_id;
  
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tgr_actualizarventa` AFTER INSERT ON `tventas` FOR EACH ROW BEGIN
    
        UPDATE tproducto
        SET PRO_Cantidad = PRO_Cantidad - NEW.VENT_cantidad
        WHERE id = NEW.producto_id;
   
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tgr_createaumentarstock` AFTER INSERT ON `ordenes_compra` FOR EACH ROW BEGIN
    
        UPDATE tproducto
        SET PRO_Cantidad = PRO_Cantidad + NEW.cantidad
        WHERE id = NEW.producto_id;
  
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `tgr_createventa` AFTER UPDATE ON `tventas` FOR EACH ROW BEGIN
    
        UPDATE tproducto
        SET PRO_Cantidad = PRO_Cantidad - NEW.VENT_cantidad
        WHERE id = NEW.producto_id;
   
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
