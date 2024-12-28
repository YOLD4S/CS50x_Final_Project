from flask import url_for


class Item:
    def __init__(self, title, year=None):
        self.title = title
        self.year = year


class NPC:
    def __init__(self, id, encounter_id, name, hp, human, gear_id, dropped_item_id, image_url):
        self.id = id
        self.encounter_id = encounter_id
        self.name = name
        self.hp = hp
        self.human = human
        self.gear_id = gear_id
        self.dropped_item_id = dropped_item_id
        self.image_url = image_url

class Talisman:
    def __init__(self, id, info, description, weight, price, image_url):
        self.id = id
        self.info = info
        self.description = description
        self.weight = weight
        self.price = price
        self.image_url = image_url


class Bolster:
    def __init__(self, id, info, description, max_held, max_storage, price, image_url):
        self.id = id
        self.info = info
        self.description = description
        self.max_held = max_held
        self.max_storage = max_storage
        self.price = price
        self.image_url = image_url


class Key_Item:
    def __init__(self, id, info, description, type_id, image_url):
        self.id = id
        self.info = info
        self.description = description
        self.type_id = type_id
        self.image_url = image_url


class Magic:
    def __init__(self, id, type_id, info, description, fp_cost, fp_cost_continuous, stamina_cost, slots_used, req_int, req_fai, req_arc, image_url):
        self.id = id
        self.type_id = type_id
        self.info = info
        self.description = description
        self.fp_cost = fp_cost
        self.fp_cost_continuous = fp_cost_continuous
        self.stamina_cost = stamina_cost
        self.slots_used = slots_used
        self.req_int = req_int
        self.req_fai = req_fai
        self.req_arc = req_arc
        self.image_url = image_url


class Spirit_Ashe:
    def __init__(self, id, info, description, fp_cost, hp_cost, hp, image_url):
        self.id = id
        self.info = info
        self.description = description
        self.fp_cost = fp_cost
        self.hp_cost = hp_cost
        self.hp = hp
        self.image_url = image_url


class Weapon_With_Affinity:
    def __init__(self, id, main_weapon_id, affinity_id, str_scaling, dex_scaling, int_scaling, fai_scaling, arc_scaling):
        self.id = id
        self.main_weapon_id = main_weapon_id
        self.affinity_id = affinity_id
        self.str_scaling = str_scaling
        self.dex_scaling = dex_scaling
        self.int_scaling = int_scaling
        self.fai_scaling = fai_scaling
        self.arc_scaling = arc_scaling
