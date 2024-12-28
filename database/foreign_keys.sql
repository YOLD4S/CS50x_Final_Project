ALTER TABLE `affinities` ADD CONSTRAINT `affinities_fk2` FOREIGN KEY (`affinity_passive_id`) REFERENCES `effects`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `weapons_w_affinities` ADD CONSTRAINT `weapons_w_affinities_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `weapons_w_affinities` ADD CONSTRAINT `weapons_w_affinities_fk1` FOREIGN KEY (`main_weapon_id`) REFERENCES `weapons`(`id`) ON DELETE CASCADE ON UPDATE CASCADE; -- careful on this, implement the weapon adding/deleting methods according to this
ALTER TABLE `weapons_w_affinities` ADD CONSTRAINT `weapons_w_affinities_fk2` FOREIGN KEY (`affinity_id`) REFERENCES `affinities`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk1` FOREIGN KEY (`group_id`) REFERENCES `weapon_groups`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk4` FOREIGN KEY (`weapon_passive_id`) REFERENCES `effects`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk5` FOREIGN KEY (`hidden_effect_id`) REFERENCES `effects`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `weapons` ADD CONSTRAINT `weapons_fk6` FOREIGN KEY (`default_skill_id`) REFERENCES `weapon_skills`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `ashes_of_war` ADD CONSTRAINT `ashes_of_war_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `ashes_of_war` ADD CONSTRAINT `ashes_of_war_fk1` FOREIGN KEY (`affinity_id`) REFERENCES `affinities`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE; -- it should prevent deleting the skill if an ash of war is refering to it, first delete the aow then affinity
ALTER TABLE `ashes_of_war` ADD CONSTRAINT `ashes_of_war_fk2` FOREIGN KEY (`skill_id`) REFERENCES `weapon_skills`(`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `locations` ADD CONSTRAINT `locations_fk2` FOREIGN KEY (`region_id`) REFERENCES `regions`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `npcs` ADD CONSTRAINT `npcs_fk1` FOREIGN KEY (`encounter_id`) REFERENCES `npc_encounters`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `npcs` ADD CONSTRAINT `npcs_fk5` FOREIGN KEY (`gear_id`) REFERENCES `gear`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `npcs` ADD CONSTRAINT `npcs_fk6` FOREIGN KEY (`dropped_item_id`) REFERENCES `items`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `armors` ADD CONSTRAINT `armors_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `armors` ADD CONSTRAINT `armors_fk1` FOREIGN KEY (`set_id`) REFERENCES `armor_sets`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `armors` ADD CONSTRAINT `armors_fk2` FOREIGN KEY (`equip_slot_id`) REFERENCES `armor_equip_slots`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `npc_encounters` ADD CONSTRAINT `npc_encounters_fk4` FOREIGN KEY (`location_id`) REFERENCES `locations`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `gear` ADD CONSTRAINT `gear_fk1` FOREIGN KEY (`right_weapon_id`) REFERENCES `weapons_w_affinities`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `gear` ADD CONSTRAINT `gear_fk2` FOREIGN KEY (`right_weapon_skill_id`) REFERENCES `weapon_skills`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `gear` ADD CONSTRAINT `gear_fk3` FOREIGN KEY (`left_weapon_id`) REFERENCES `weapons_w_affinities`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `gear` ADD CONSTRAINT `gear_fk4` FOREIGN KEY (`left_weapon_skill_id`) REFERENCES `weapon_skills`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `gear` ADD CONSTRAINT `gear_fk5` FOREIGN KEY (`armor_head_id`) REFERENCES `armors`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `gear` ADD CONSTRAINT `gear_fk6` FOREIGN KEY (`armor_body_id`) REFERENCES `armors`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `gear` ADD CONSTRAINT `gear_fk7` FOREIGN KEY (`armor_arms_id`) REFERENCES `armors`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
ALTER TABLE `gear` ADD CONSTRAINT `gear_fk8` FOREIGN KEY (`armor_legs_id`) REFERENCES `armors`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE `talismans` ADD CONSTRAINT `talismans_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `magic` ADD CONSTRAINT `magic_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `magic` ADD CONSTRAINT `magic_fk1` FOREIGN KEY (`type_id`) REFERENCES `magic_types`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `spirit_ashes` ADD CONSTRAINT `spirit_ashes_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `items` ADD CONSTRAINT `items_fk1` FOREIGN KEY (`type_id`) REFERENCES `item_types`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `bolsters` ADD CONSTRAINT `bolsters_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE `key_items` ADD CONSTRAINT `key_items_fk0` FOREIGN KEY (`id`) REFERENCES `items`(`id`) ON DELETE CASCADE ON UPDATE CASCADE; 
ALTER TABLE `key_items` ADD CONSTRAINT `key_items_fk3` FOREIGN KEY (`type_id`) REFERENCES `key_item_types`(`id`) ON DELETE CASCADE ON UPDATE CASCADE; -- when an item is removed in its own category, 

ALTER TABLE `characters` ADD CONSTRAINT `characters_fk2` FOREIGN KEY (`creator_id`) REFERENCES `users`(`id`) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE `characters` ADD CONSTRAINT `characters_fk3` FOREIGN KEY (`gear_id`) REFERENCES `gear`(`id`) ON DELETE SET NULL ON UPDATE CASCADE;
