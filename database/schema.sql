CREATE TABLE IF NOT EXISTS `affinities` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(255) NOT NULL,
	`affinity_passive_id` int,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapons_w_affinities` (
	`id` int AUTO_INCREMENT NOT NULL,
	`main_weapon_id` int NOT NULL,
	`affinity_id` int,
	`str_scaling` int,
	`dex_scaling` int NOT NULL DEFAULT '0',
	`int_scaling` int NOT NULL DEFAULT '0',
	`fai_scaling` int NOT NULL DEFAULT '0',
	`arc_scaling` int NOT NULL DEFAULT '0',
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
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `weapons` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`group_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`desc` text,
	`weapon_passive_id` int,
	`hidden_effect_id` int,
	`default_skill_id` int,
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
	`id` int AUTO_INCREMENT NOT NULL,
	`affinity_id` int NOT NULL,
	`skill_id` int NOT NULL,
	`desc` text NOT NULL,
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
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `locations` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
	`region_id` int NOT NULL,
	`desc` text,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `npcs` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`encounter_id` int NOT NULL,
	`name` varchar(255) NOT NULL,
	`hp` int NOT NULL,
	`human` bool NOT NULL,
	`gear_id` int,
	`dropped_item_id` int,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `armors` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`set_id` int NOT NULL,
	`equip_slot_id` int NOT NULL,
	`desc` text,
	`weight` float NOT NULL,
	`price` int NOT NULL,
	`can_alter` bool NOT NULL,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `npc_encounters` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
	`hp` int NOT NULL,
	`runes` int NOT NULL,
	`location_id` int,
	`only_night` bool NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `gear` (
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

CREATE TABLE IF NOT EXISTS `talismans` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`info` text NOT NULL,
	`desc` text NOT NULL,
	`weight` float NOT NULL,
	`price` int NOT NULL,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `magic` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`type_id` int NOT NULL,
	`info` text NOT NULL,
	`desc` text NOT NULL,
	`fp_cost` int NOT NULL,
	`fp_cost_continuous` int,
	`stamina_cost` int NOT NULL,
	`slots_used` int NOT NULL DEFAULT '0',
	`req_int` int NOT NULL DEFAULT '0',
	`req_fai` int NOT NULL DEFAULT '0',
	`req_arc` int NOT NULL DEFAULT '0',
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `spirit_ashes` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`info` text NOT NULL,
	`desc` text NOT NULL,
	`fp_cost` int NOT NULL,
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
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`info` text NOT NULL,
	`desc` text NOT NULL,
	`max_held` int NOT NULL,
	`max_storage` int NOT NULL,
	`price` int,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `key_items` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`info` text NOT NULL,
	`desc` text NOT NULL,
	`type_id` int NOT NULL,
	`image_url` varchar(255),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `users` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`username` varchar(255) NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
	`email` varchar(255),
	`password` varchar(255) NOT NULL,
	`steam_url` varchar(255),
	`profile_picture` varchar(255),
	`created_at` timestamp NOT NULL,
	`last_login` timestamp NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `characters` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(255) NOT NULL,
	`creator_id` int NOT NULL,
	`gear_id` int,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `item_types` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`item_type` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `magic_types` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`magic_type` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `key_item_types` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`key_item_type` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `armor_equip_slots` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`equip_slot` varchar(255) NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `affinities` ADD CONSTRAINT `affinities_fk2` FOREIGN KEY (`affinity_passive_id`) REFERENCES `effects`(`id`);
ALTER TABLE `weapons_w_affinities` ADD CONSTRAINT `weapons_w_affinities_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`);

ALTER TABLE `weapons_w_affinities` ADD CONSTRAINT `weapons_w_affinities_fk1` FOREIGN KEY (`main_weapon_id`) REFERENCES `weapons`(`id`);

ALTER TABLE `weapons_w_affinities` ADD CONSTRAINT `weapons_w_affinities_fk2` FOREIGN KEY (`affinity_id`) REFERENCES `affinities`(`id`);


ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk1` FOREIGN KEY (`group_id`) REFERENCES `weapon_groups`(`id`);

ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk4` FOREIGN KEY (`weapon_passive_id`) REFERENCES `effects`(`id`);

ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk5` FOREIGN KEY (`hidden_effect_id`) REFERENCES `effects`(`id`);


ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk6` FOREIGN KEY (`default_skill_id`) REFERENCES `weapon_skills`(`id`);

ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk7` FOREIGN KEY (`default_skill_id`) REFERENCES `weapon_skills`(`id`);


ALTER TABLE `ashes_of_war` ADD CONSTRAINT `ashes_of_war_fk1` FOREIGN KEY (`id`) REFERENCES `items`(`id`);

ALTER TABLE `ashes_of_war` ADD CONSTRAINT `ashes_of_war_fk2` FOREIGN KEY (`affinity_id`) REFERENCES `affinities`(`id`);

ALTER TABLE `ashes_of_war` ADD CONSTRAINT `ashes_of_war_fk3` FOREIGN KEY (`skill_id`) REFERENCES `weapon_skills`(`id`);


ALTER TABLE `locations` ADD CONSTRAINT `locations_fk2` FOREIGN KEY (`region_id`) REFERENCES `regions`(`id`);
ALTER TABLE `npcs` ADD CONSTRAINT `npcs_fk1` FOREIGN KEY (`encounter_id`) REFERENCES `npc_encounters`(`id`);

ALTER TABLE `npcs` ADD CONSTRAINT `npcs_fk5` FOREIGN KEY (`gear_id`) REFERENCES `gear`(`id`);

ALTER TABLE `npcs` ADD CONSTRAINT `npcs_fk6` FOREIGN KEY (`dropped_item_id`) REFERENCES `items`(`id`);
ALTER TABLE `armors` ADD CONSTRAINT `armors_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`);

ALTER TABLE `armors` ADD CONSTRAINT `armors_fk1` FOREIGN KEY (`set_id`) REFERENCES `armor_sets`(`id`);

ALTER TABLE `armors` ADD CONSTRAINT `armors_fk2` FOREIGN KEY (`equip_slot_id`) REFERENCES `armor_equip_slots`(`id`);
ALTER TABLE `npc_encounters` ADD CONSTRAINT `npc_encounters_fk4` FOREIGN KEY (`location_id`) REFERENCES `locations`(`id`);
ALTER TABLE `gear` ADD CONSTRAINT `gear_fk1` FOREIGN KEY (`right_weapon_id`) REFERENCES `weapons_w_affinities`(`id`);

ALTER TABLE `gear` ADD CONSTRAINT `gear_fk2` FOREIGN KEY (`right_weapon_skill_id`) REFERENCES `weapon_skills`(`id`);

ALTER TABLE `gear` ADD CONSTRAINT `gear_fk3` FOREIGN KEY (`left_weapon_id`) REFERENCES `weapons_w_affinities`(`id`);

ALTER TABLE `gear` ADD CONSTRAINT `gear_fk4` FOREIGN KEY (`left_weapon_skill_id`) REFERENCES `weapon_skills`(`id`);

ALTER TABLE `gear` ADD CONSTRAINT `gear_fk5` FOREIGN KEY (`armor_head_id`) REFERENCES `armors`(`id`);

ALTER TABLE `gear` ADD CONSTRAINT `gear_fk6` FOREIGN KEY (`armor_body_id`) REFERENCES `armors`(`id`);

ALTER TABLE `gear` ADD CONSTRAINT `gear_fk7` FOREIGN KEY (`armor_arms_id`) REFERENCES `armors`(`id`);

ALTER TABLE `gear` ADD CONSTRAINT `gear_fk8` FOREIGN KEY (`armor_legs_id`) REFERENCES `armors`(`id`);

ALTER TABLE `talismans` ADD CONSTRAINT `talismans_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`);
ALTER TABLE `magic` ADD CONSTRAINT `magic_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`);

ALTER TABLE `magic` ADD CONSTRAINT `magic_fk1` FOREIGN KEY (`type_id`) REFERENCES `magic_types`(`id`);
ALTER TABLE `spirit_ashes` ADD CONSTRAINT `spirit_ashes_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`);
ALTER TABLE `items` ADD CONSTRAINT `items_fk1` FOREIGN KEY (`type_id`) REFERENCES `item_types`(`id`);
ALTER TABLE `bolsters` ADD CONSTRAINT `bolsters_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`);
ALTER TABLE `key_items` ADD CONSTRAINT `key_items_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`); 

ALTER TABLE `key_items` ADD CONSTRAINT `key_items_fk3` FOREIGN KEY (`type_id`) REFERENCES `key_item_types`(`id`);

ALTER TABLE `characters` ADD CONSTRAINT `characters_fk2` FOREIGN KEY (`creator_id`) REFERENCES `users`(`id`);

ALTER TABLE `characters` ADD CONSTRAINT `characters_fk3` FOREIGN KEY (`gear_id`) REFERENCES `gear`(`id`);



