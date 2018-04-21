DROP TABLE IF EXISTS `waybill`;
CREATE TABLE `waybill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `waybill_number` varchar(15) DEFAULT NULL COMMENT '运单号',
  `waybill_type` int(11) DEFAULT NULL COMMENT '运单类型 1:正常,2:异常,3:废止',
  `waybill_status` int(11) DEFAULT NULL COMMENT '运单状态 200:待装车,300:运输中,500:已完成',
  `is_onway` int(2) DEFAULT NULL COMMENT '是否在途 1:在途 2:到达',
  `line_no` varchar(100) DEFAULT NULL COMMENT '线路编号',
  `fk_to_location_code` varchar(6) NOT NULL COMMENT '出发地编码',
  `fk_at_location_code` varchar(6) NOT NULL COMMENT '到达地编码',
  `plate` varchar(8) DEFAULT NULL COMMENT '车牌',
  `start_time` varchar(16) DEFAULT NULL COMMENT '车辆出发时间',
  `end_time` varchar(16) DEFAULT NULL COMMENT '车辆到达时间',
  `driver_name` VARCHAR(256) DEFAULT NULL COMMENT '司机姓名',
  `driver_telephone` VARCHAR(11) DEFAULT NULL COMMENT '司机号码',
  `remarks` text DEFAULT NULL COMMENT '备注',
  `fk_operator_id` int(11) DEFAULT NULL COMMENT '操作人id',
  `create_date` date DEFAULT NULL COMMENT '运单创建时间',
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;



