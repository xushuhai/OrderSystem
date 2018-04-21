DROP TABLE IF EXISTS `truck`;
CREATE TABLE `truck` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plate` varchar(7) NOT NULL COMMENT '车牌',
  `truck_no` varchar(45) DEFAULT NULL COMMENT '车辆编号',
  `type` int(11) DEFAULT NULL COMMENT '车厢类型,1:高栏:,2:厢式',
  `plate_type` int(11) DEFAULT NULL COMMENT '车牌类型,1:一般货车,2:挂车,3:车厢',
  `vehicle_type` varchar(45) DEFAULT NULL COMMENT '车辆属性，1:临时车,2:正式车',
  `container_length` varchar(10) DEFAULT NULL COMMENT '车厢长度',
  `container_wide` varchar(10) DEFAULT NULL COMMENT '车厢宽度',
  `container_high` varchar(10) DEFAULT NULL COMMENT '车厢高度',
  `container_volume` varchar(10) DEFAULT NULL COMMENT '车厢高度',
  `create_time` timestamp NULL DEFAULT NULL,
  `update_time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;