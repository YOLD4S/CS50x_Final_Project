CREATE TABLE IF NOT EXISTS `affinities` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`affinity_passive_id` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapons_w_affinities` (
	`id` int AUTO_INCREMENT NOT NULL,
	`main_weapon_id` int NOT NULL,
	`affinity_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`scaling` bigint NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `effects` (
	`id` int AUTO_INCREMENT NOT NULL,
	`desc` text NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapon_skills` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`aow_id` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapons` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`group_id` int NOT NULL,
	`weapon_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`desc` text NOT NULL,
	`weapon_passive_id` int NOT NULL,
	`hidden_effect_id` int NOT NULL,
	`default_skill_id` int NOT NULL,
	`weight` float NOT NULL,
	`req_str` smallint NOT NULL DEFAULT '0',
	`req_dex` smallint NOT NULL DEFAULT '0',
	`req_int` smallint NOT NULL DEFAULT '0',
	`req_fai` smallint NOT NULL DEFAULT '0',
	`req_arc` smallint NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `ashes_of_war` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`affinity_id` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapon_groups` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`ph_standard` boolean NOT NULL,
	`ph_strike` boolean NOT NULL,
	`ph_slash` boolean NOT NULL,
	`ph_pierce` boolean NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `affinities` ADD CONSTRAINT `affinities_fk2` FOREIGN KEY (`affinity_passive_id`) REFERENCES `effects`(`id`);
ALTER TABLE `weapons_w_affinities` ADD CONSTRAINT `weapons_w_affinities_fk1` FOREIGN KEY (`main_weapon_id`) REFERENCES `weapons`(`id`);

ALTER TABLE `weapons_w_affinities` ADD CONSTRAINT `weapons_w_affinities_fk2` FOREIGN KEY (`affinity_id`) REFERENCES `affinities`(`id`);

ALTER TABLE `weapon_skills` ADD CONSTRAINT `weapon_skills_fk2` FOREIGN KEY (`aow_id`) REFERENCES `ashes_of_war`(`id`);
ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk1` FOREIGN KEY (`group_id`) REFERENCES `weapon_groups`(`id`);

ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk5` FOREIGN KEY (`weapon_passive_id`) REFERENCES `effects`(`id`);

ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk6` FOREIGN KEY (`hidden_effect_id`) REFERENCES `effects`(`id`);

ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk7` FOREIGN KEY (`default_skill_id`) REFERENCES `weapon_skills`(`id`);
ALTER TABLE `ashes_of_war` ADD CONSTRAINT `ashes_of_war_fk2` FOREIGN KEY (`affinity_id`) REFERENCES `affinities`(`id`);
