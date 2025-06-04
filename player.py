from factions import game_factions

class Player:
    def __init__(self, starting_location_key: str, name: str = "Player"):
        self.name = name
        self.inventory = []
        self.current_location = starting_location_key
        self.hp = 100
        self.max_hp = 100
        self.attack_power = 10
        self.defense = 5
        self.money = 50
        self.influence = 0
        self.hideout_level = 0
        self.faction_reputations = {f_id: fac.default_reputation for f_id, fac in game_factions.items()}
        self.active_tasks = {}
        self.chapter_one_completed = False

    def move(self, new_location_key: str):
        self.current_location = new_location_key

    def add_to_inventory(self, item_key: str, items_db_ref: dict):
        self.inventory.append(item_key)
        item_name = items_db_ref.get(item_key, {}).get('name', item_key.replace('_', ' ').capitalize())
        print(f"{item_name} added to inventory.")

    def remove_from_inventory(self, item_key: str, items_db_ref: dict) -> bool:
        if item_key in self.inventory:
            self.inventory.remove(item_key)
            item_name = items_db_ref.get(item_key, {}).get('name', item_key.replace('_', ' ').capitalize())
            print(f"{item_name} removed from inventory.")
            return True
        return False

    def get_inventory_display(self, items_db_ref: dict) -> str:
        if not self.inventory: return "Your inventory is empty."
        display_list = [items_db_ref.get(item_key, {}).get('name', item_key.replace('_', ' ').capitalize()) for item_key in self.inventory]
        return "You are carrying:\n" + "\n".join(f"- {item}" for item in display_list)

    def take_damage(self, amount: int, attacker):
        actual_damage = max(0, amount - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        attacker_name = attacker.name if hasattr(attacker, 'name') else "Something"
        print(f"You take {actual_damage} damage from {attacker_name}. HP: {self.hp}/{self.max_hp}")

    def is_alive(self) -> bool:
        return self.hp > 0

    def attack_target(self, target_npc):
        damage = max(0, self.attack_power - target_npc.defense)
        print(f"You attack {target_npc.name} for {damage} damage.")
        target_npc.take_damage(damage, self)
