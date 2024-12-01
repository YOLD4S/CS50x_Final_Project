from elements import Item, NPC


class ItemDatabase:
    def __init__(self):
        self.items = {}
        self._last_item_key = 0

    def add_item(self, item):
        self._last_item_key += 1
        self.items[self._last_item_key] = item
        return self._last_item_key

    def delete_item(self, item_key):
        if item_key in self.items:
            del self.items[item_key]

    def get_item(self, item_key):
        item = self.items.get(item_key)
        if item is None:
            return None
        item_ = Item(item.title, year=item.year)
        return item_

    def get_items(self):
        items = []
        for item_key, item in self.items.items():
            item_ = Item(item.title, year=item.year)
            items.append((item_key, item_))
        return items

class NPCDatabase:
    def __init__(self):
        self.npcs = {}
        self._last_npc_key = 0

    def add_npc(self, npc):
        self._last_npc_key += 1
        self.npcs[self._last_npc_key] = npc
        return self._last_npc_key

    def delete_npc(self, npc_key):
        if npc_key in self.npcs:
            del self.npcs[npc_key]

    def get_npc(self, npc_key):
        npc = self.npcs.get(npc_key)
        if npc is None:
            return None
        npc_ = NPC(name=npc.name, hp=npc.hp, human=npc.human, drops=npc.drops, image_path=npc.image_path)
        return npc_

    def get_npcs(self):
        npcs = []
        for npc_key, npc in self.npcs.items():
            npc_ = NPC(name=npc.name, hp=npc.hp, human=npc.human, drops=npc.drops, image_path=npc.image_path)
            npcs.append((npc_key, npc_))
        return npcs