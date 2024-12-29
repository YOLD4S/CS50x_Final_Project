CREATE TABLE IF NOT EXISTS `affinities` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`affinity_passive_id` int NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapons_w_affinities` (
	`id` int NOT NULL,
	`main_weapon_id` int NOT NULL,
	`affinity_id` int NULL,
	`str_scaling` smallint NOT NULL DEFAULT '0',
	`dex_scaling` smallint NOT NULL DEFAULT '0',
	`int_scaling` smallint NOT NULL DEFAULT '0',
	`fai_scaling` smallint NOT NULL DEFAULT '0',
	`arc_scaling` smallint NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `effects` (
	`id` int AUTO_INCREMENT NOT NULL,
	`description` text NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapon_skills` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapons` (
	`id` int AUTO_INCREMENT NOT NULL,
	`group_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`description` text,
	`weapon_passive_id` int NULL,
	`hidden_effect_id` int NULL,
	`default_skill_id` int NULL,
	`weight` float NOT NULL,
	`req_str` smallint NOT NULL DEFAULT '0',
	`req_dex` smallint NOT NULL DEFAULT '0',
	`req_int` smallint NOT NULL DEFAULT '0',
	`req_fai` smallint NOT NULL DEFAULT '0',
	`req_arc` smallint NOT NULL DEFAULT '0',
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `ashes_of_war` (
	`id` int NOT NULL,
	`affinity_id` int NOT NULL,
	`skill_id` int NOT NULL,
	`description` text,
	`fp_cost` int NOT NULL DEFAULT '0',
	`fp_cost_light` int,
	`fp_cost_heavy` int,
	`image_url` varchar(255),
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
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `locations` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`region_id` int NOT NULL,
	`description` text,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `npcs` (
	`id` int AUTO_INCREMENT NOT NULL,
	`encounter_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`hp` int NOT NULL,
	`human` bool NOT NULL,
	`gear_id` int NULL,
	`dropped_item_id` int NULL,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `armors` (
	`id` int NOT NULL,
	`set_id` int NOT NULL,
	`equip_slot_id` int NOT NULL,
	`description` text,
	`weight` float NOT NULL,
	`price` int,
	`can_alter` bool NOT NULL,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `npc_encounters` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`hp` int NOT NULL,
	`runes` int NOT NULL,
	`location_id` int NULL,
	`only_night` bool NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `gear` (
	`id` int AUTO_INCREMENT NOT NULL,
	`right_weapon_id` int NULL,
	`right_weapon_skill_id` int NULL,
	`left_weapon_id` int NULL,
	`left_weapon_skill_id` int NULL,
	`armor_head_id` int NULL,
	`armor_body_id` int NULL,
	`armor_arms_id` int NULL,
	`armor_legs_id` int NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `armor_sets` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `talismans` (
	`id` int NOT NULL,
	`info` text,
	`description` text,
	`weight` float NOT NULL,
	`price` int,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `magic` (
	`id` int NOT NULL,
	`type_id` int NOT NULL,
	`info` text,
	`description` text,
	`fp_cost` int NOT NULL,
	`fp_cost_continuous` int,
	`stamina_cost` int NOT NULL,
	`slots_used` int NOT NULL DEFAULT '1',
	`req_int` int NOT NULL DEFAULT '0',
	`req_fai` int NOT NULL DEFAULT '0',
	`req_arc` int NOT NULL DEFAULT '0',
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `spirit_ashes` (
	`id` int NOT NULL,
	`info` text,
	`description` text,
	`fp_cost` int,
	`hp_cost` int,
	`hp` int NOT NULL,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `items` (
	`id` int AUTO_INCREMENT NOT NULL,
	`type_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `bolsters` (
	`id` int NOT NULL,
	`info` text,
	`description` text,
	`max_held` int NOT NULL,
	`max_storage` int NOT NULL,
	`price` int,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `key_items` (
	`id` int NOT NULL,
	`info` text,
	`description` text,
	`type_id` int NOT NULL,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `users` (
	`id` int AUTO_INCREMENT NOT NULL,
	`username` varchar(255) NOT NULL UNIQUE,
	`name` varchar(255),
	`email` varchar(255),
	`password` varchar(255) NOT NULL,
	`steam_url` varchar(255),
	`profile_picture` varchar(255),
    `admin` bool NOT NULL,
	`created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	`last_login` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `characters` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`creator_id` int NOT NULL,
	`gear_id` int NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `item_types` (
	`id` int AUTO_INCREMENT NOT NULL,
	`item_type` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `magic_types` (
	`id` int AUTO_INCREMENT NOT NULL,
	`magic_type` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `key_item_types` (
	`id` int AUTO_INCREMENT NOT NULL,
	`key_item_type` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `armor_equip_slots` (
	`id` int AUTO_INCREMENT NOT NULL,
	`equip_slot` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);
