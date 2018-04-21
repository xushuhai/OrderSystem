DROP TABLE IF EXISTS `cargo_order`;
CREATE TABLE `cargo_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(24) NOT NULL COMMENT '订单号',
  `origin` varchar(6) DEFAULT NULL COMMENT '始发地编码',
  `origin_field` varchar(2) DEFAULT NULL COMMENT '始发地场地编码',
  `destination` varchar(6) DEFAULT NULL COMMENT '目的地编码',
  `destination_field` varchar(2) DEFAULT NULL COMMENT '目的地场地编码',
  `order_status` int(11) DEFAULT NULL COMMENT '订单状态',
  `order_type` varchar(12) DEFAULT NULL COMMENT '订单类型,vehicle:整车;breakweight:零担',
  `cargo_name` varchar(128) DEFAULT NULL COMMENT '货物名称',
  `cargo_volume` varchar(11) DEFAULT NULL COMMENT '货物体积',
  `cargo_weight` varchar(8) DEFAULT NULL COMMENT '货物重量',
  `specified_arrival_time` datetime DEFAULT NULL COMMENT '要求到货时间',
  `consignor_name` varchar(24) DEFAULT NULL COMMENT '发货人姓名',
  `consignor_telephone` varchar(11) DEFAULT NULL COMMENT '发货人手机',
  `consignee_name` varchar(24) DEFAULT NULL COMMENT '收货人姓名',
  `consignee_telephone` varchar(11) DEFAULT NULL COMMENT '收货人手机',
  `fk_operator_id` int(11) DEFAULT NULL COMMENT '操作者id',
  `create_date` date DEFAULT NULL COMMENT '创单日期',
  `create_time` datetime DEFAULT NULL COMMENT '创单时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

