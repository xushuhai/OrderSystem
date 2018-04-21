USE `order_system`;
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) DEFAULT NULL comment '姓名',
  `username` varchar(24) NOT NULL comment '用户名',
  `password` varchar(256) NOT NULL comment '密码',
  `mobile` varchar(11) DEFAULT NULL comment '手机号码',
  `role_type` int(11) DEFAULT NULL comment '用户权限',
  `fk_location_code` VARCHAR(6) DEFAULT NULL  comment '所在转运网点编号',
  `create_time` datetime DEFAULT NULL comment '创建时间',
  `update_time` datetime DEFAULT NULL comment '修改时间',
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `verifying_code`;
CREATE TABLE `verifying_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `telephone` varchar(11) DEFAULT NULL comment '手机号码',
  `verifying_code` varchar(6) DEFAULT NULL comment '验证码',
  `create_time` datetime DEFAULT NULL comment '创建时间',
  `update_time` datetime DEFAULT NULL comment '修改时间',
  PRIMARY KEY (`id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;

