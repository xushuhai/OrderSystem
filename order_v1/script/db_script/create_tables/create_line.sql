
DROP TABLE IF EXISTS `line`;
CREATE TABLE `line` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `line_code` VARCHAR(17) NOT NULL COMMENT '线路编号',
  `line_name` VARCHAR(256) DEFAULT NULL COMMENT '线路名称',
  `line_status` INT DEFAULT NULL COMMENT '线路状态 1 启用，2 禁用',
  `line_type` INT DEFAULT NULL COMMENT '线路属性 1 临时，2 正式',
  `line_kilometre` INT DEFAULT NULL COMMENT '线路运行公里数 单位千米',
  `line_runtime` INT DEFAULT NULL COMMENT '运行时长 单位小时',
  `fk_operator_id` INT DEFAULT NULL COMMENT '操作人id',
  `create_time` datetime DEFAULT NULL COMMENT '创单时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `line_location`;
CREATE TABLE `line_location` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_line_code` VARCHAR(17) NOT NULL COMMENT '线路编号',
  `location_code` VARCHAR(6) DEFAULT NULL COMMENT '径停点编码',
  `sequence` INT DEFAULT NULL COMMENT '径停点顺序',
  `location_status` INT DEFAULT NULL COMMENT '径停点状态 1 启用，2 禁用',
  `fk_operator_id` INT DEFAULT NULL COMMENT '操作人id',
  `create_time` datetime DEFAULT NULL COMMENT '创单时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

