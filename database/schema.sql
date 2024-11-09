CREATE TABLE IF NOT EXISTS `affinities` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`affinity_passive_id` int,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapons_w_affinities` (
	`id` int AUTO_INCREMENT NOT NULL,
	`main_weapon_id` int NOT NULL,
	`affinity_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`scaling` varchar(255),
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
	`aow_id` int,
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

CREATE TABLE IF NOT EXISTS `regions` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `locations` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
	`region` int NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `npcs` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`encounter_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`hp` int NOT NULL,
	`human` bool NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `armors` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`set_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`equip_slot` varchar(255) NOT NULL,
	`desc` text NOT NULL,
	`weight` float NOT NULL,
	`can_alter` bool NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `npc_encounters` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
	`hp` int NOT NULL,
	`runes` int NOT NULL,
	`location_id` int NOT NULL,
	`only_night` bool NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `npc_gear` (
	`id` int NOT NULL UNIQUE,
	`right_weapon_id` int,
	`right_weapon_skill_id` int,
	`left_weapon_id` int,
	`left_weapon_skill_id` int,
	`armor_head_id` int,
	`armor_body_id` int,
	`armor_arms_id` int,
	`armor_legs_id` int,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `armor_sets` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
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


ALTER TABLE `locations` ADD CONSTRAINT `locations_fk2` FOREIGN KEY (`region`) REFERENCES `regions`(`id`);
ALTER TABLE `npcs` ADD CONSTRAINT `npcs_fk1` FOREIGN KEY (`encounter_id`) REFERENCES `npc_encounters`(`id`);
ALTER TABLE `armors` ADD CONSTRAINT `armors_fk1` FOREIGN KEY (`set_id`) REFERENCES `armor_sets`(`id`);
ALTER TABLE `npc_encounters` ADD CONSTRAINT `npc_encounters_fk4` FOREIGN KEY (`location_id`) REFERENCES `locations`(`id`);
ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk0` FOREIGN KEY (`id`) REFERENCES `npcs`(`id`);

ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk1` FOREIGN KEY (`right_weapon_id`) REFERENCES `weapons_w_affinities`(`id`);

ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk2` FOREIGN KEY (`right_weapon_skill_id`) REFERENCES `weapon_skills`(`id`);

ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk3` FOREIGN KEY (`left_weapon_id`) REFERENCES `weapons_w_affinities`(`id`);

ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk4` FOREIGN KEY (`left_weapon_skill_id`) REFERENCES `weapon_skills`(`id`);

ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk5` FOREIGN KEY (`armor_head_id`) REFERENCES `armors`(`id`);

ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk6` FOREIGN KEY (`armor_body_id`) REFERENCES `armors`(`id`);

ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk7` FOREIGN KEY (`armor_arms_id`) REFERENCES `armors`(`id`);

ALTER TABLE `npc_gear` ADD CONSTRAINT `npc_gear_fk8` FOREIGN KEY (`armor_legs_id`) REFERENCES `armors`(`id`);
