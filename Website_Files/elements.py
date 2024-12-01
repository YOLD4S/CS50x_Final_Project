from flask import url_for


class Item:
    def __init__(self, title, year=None):
        self.title = title
        self.year = year


class NPC:
    def __init__(self, name, hp, human, drops, image_path):
        self.name = name
        self.hp = hp
        self.human = human
        self.drops = drops
        self.image_path = image_path

