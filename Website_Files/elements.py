from flask import url_for


class Item:
    def __init__(self, title, year=None):
        self.title = title
        self.year = year


class NPC:
    def __init__(self, name, hp, human, location_id, only_night):
        self.name = name
        self.hp = hp
        self.human = human
        self.location_id = location_id
        self.only_night = only_night

