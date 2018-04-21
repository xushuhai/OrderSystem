DROP TABLE IF EXISTS `location`;
CREATE TABLE `location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location_name` VARCHAR(256) NOT NULL COMMENT '网点名称',
  `location_code` VARCHAR(6) DEFAULT NULL COMMENT '网点编码',
  `detailed_address` VARCHAR(256) DEFAULT NULL COMMENT '详细地址',
  `lot` int(11) DEFAULT NULL COMMENT '经度',
  `lat` int(11) DEFAULT NULL COMMENT '纬度',
  `province` VARCHAR(256) DEFAULT NULL COMMENT '省份',
  `city` VARCHAR(256) DEFAULT NULL COMMENT '市区',
  `create_time` datetime DEFAULT NULL COMMENT '创单时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `location_contacts`;
CREATE TABLE `location_contacts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_location_code` VARCHAR(6) DEFAULT NULL COMMENT '网点编码',
  `contacts_name` VARCHAR(256) DEFAULT NULL COMMENT '联系人名称',
  `contacts_telephone` VARCHAR(11) DEFAULT NULL COMMENT '联系人手机号码',
  `create_time` datetime DEFAULT NULL COMMENT '创单时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;