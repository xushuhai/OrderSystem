DROP TABLE IF EXISTS `location_count`;
CREATE TABLE `location_count` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location_amount` int(11) DEFAULT NULL COMMENT '总数',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
