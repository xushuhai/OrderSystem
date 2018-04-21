DROP TABLE IF EXISTS `order_vehicle`;
CREATE TABLE `order_vehicle` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_order_number` varchar(24) NOT NULL COMMENT '订单号',
  `vehicle_type` varchar(11) DEFAULT NULL COMMENT '需求车型',
  `send_vehicle_type` int(11) DEFAULT NULL COMMENT '派车类别,1:一般车辆;2:挂车头与挂车厢;3:挂车头;4:挂车
厢',
  `plate` varchar(7) DEFAULT NULL COMMENT '车牌',
  `carriage_plate` varchar(7) DEFAULT NULL COMMENT '车厢车牌',
  `carriage_type` varchar(4) DEFAULT NULL COMMENT '车厢类型,GL:高栏;XS:厢式',
  `carriage_length_type` varchar(11) DEFAULT NULL COMMENT '车厢长度类型',
  `antipate_arrive_time` datetime DEFAULT NULL COMMENT '预计到车时间',
  `driver_name` varchar(45) DEFAULT NULL COMMENT '司机姓名',
  `driver_telephone` varchar(11) DEFAULT NULL COMMENT '司机手机号',
  `arrive_status` int(3) DEFAULT NULL COMMENT '到车状态,1:未到达;2:已到达;3:未知',
  `arrive_time` datetime DEFAULT NULL COMMENT '实际到车时间',
  `vehicle_if_exception` int(3) DEFAULT NULL COMMENT '车辆是否异常,1:正常;2:异常',
  `vehicle_exception_type` int(3) DEFAULT NULL COMMENT '车辆异常类型',
  `remark` varchar(1000) DEFAULT NULL COMMENT '车辆备注',
  `fk_operator_id` int(11) DEFAULT NULL COMMENT '操作者id',
  `flag` int(3) DEFAULT NULL COMMENT '数据标记,1:有效;2:历史',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `index_order_number` (`fk_order_number`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
