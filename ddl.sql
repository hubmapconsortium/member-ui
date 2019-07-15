CREATE TABLE `stage_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `globus_user_id` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `first_name` varchar(200) DEFAULT NULL,
  `last_name` varchar(200) DEFAULT NULL,
  `component` varchar(200) DEFAULT NULL,
  `other_component` varchar(200) DEFAULT NULL,
  `organization` varchar(200) DEFAULT NULL,
  `other_organization` varchar(200) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  `other_role` varchar(200) DEFAULT NULL,
  `working_group` varchar(500) DEFAULT NULL,
  `photo` varchar(500) DEFAULT NULL,
  `photo_url` varchar(500) DEFAULT NULL,
  `access_requests` varchar(500) DEFAULT NULL,
  `google_email` varchar(200) DEFAULT NULL,
  `github_username` varchar(200) DEFAULT NULL,
  `slack_username` varchar(200) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `website` varchar(500) DEFAULT NULL,
  `bio` longtext DEFAULT NULL,
  `orcid` varchar(100) DEFAULT NULL,
  `pm` tinyint(1) DEFAULT NULL,
  `pm_name` varchar(100) DEFAULT NULL,
  `pm_email` varchar(100) DEFAULT NULL,
  `created_at` timestamp,
  `deny` boolean DEFAULT NULL,
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