DROP TABLE IF EXISTS `order_count`;
CREATE TABLE `order_count` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_date` date DEFAULT NULL COMMENT '日期',
  `order_amount` int(11) DEFAULT NULL COMMENT '总数',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `order_flow`;
CREATE TABLE `order_flow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_order_number` varchar(24) DEFAULT NULL COMMENT '订单号',
  `order_status` int(11) DEFAULT NULL COMMENT '订单状态',
  `status_time` datetime DEFAULT NULL COMMENT '状态时间',
  `fk_operator_id` int(11) DEFAULT NULL COMMENT '操作者id',
  `remark` varchar(1000) DEFAULT NULL COMMENT '备注',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_order_number` (`fk_order_number`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `order_operation_record`;
CREATE TABLE `order_operation_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_order_number` varchar(24) DEFAULT NULL COMMENT '订单号',
  `action` int(11) DEFAULT NULL COMMENT '操作类型',
  `op_time` datetime DEFAULT NULL COMMENT '操作时间',
  `fk_operator_id` int(11) DEFAULT NULL COMMENT '操作者id',
  `remark` varchar(1000) DEFAULT NULL COMMENT '备注',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_order_number` (`fk_order_number`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
