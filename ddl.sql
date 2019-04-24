CREATE TABLE `stage_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `globus_user_id` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `first_name` varchar(200) DEFAULT NULL,
  `last_name` varchar(200) DEFAULT NULL,
  `component` varchar(200) DEFAULT NULL,
  `other_component` varchar(200) DEFAULT NULL,
  `organization` varchar(200) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `group` varchar(500) DEFAULT NULL,
  `photo` varchar(500) DEFAULT NULL,
  `photo_url` varchar(500) DEFAULT NULL,
  `access_requests` varchar(500) DEFAULT NULL,
  `alt_email` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `website` varchar(500) DEFAULT NULL,
  `biosketch` varchar(200) DEFAULT NULL,
  `expertise` varchar(500) DEFAULT NULL,
  `orcid` varchar(100) DEFAULT NULL,
  `github` varchar(200) DEFAULT NULL,
  `slack` varchar(200) DEFAULT NULL,
  `stack` varchar(200) DEFAULT NULL,
  `assistant` tinyint(1) DEFAULT NULL,
  `assistant_email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `globus_user_id` (`globus_user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

CREATE TABLE `user_connection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `connection_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;