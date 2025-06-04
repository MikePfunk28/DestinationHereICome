class NPC:
    def __init__(self, name: str, hp: int, attack_power: int, defense: int, description: str = ""):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.defense = defense
        self.description = description

    def take_damage(self, amount: int, attacker):
        actual_damage = max(0, amount - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        attacker_name = attacker.name if hasattr(attacker, 'name') else "Something"
        print(f"{self.name} takes {actual_damage} damage from {attacker_name}. HP: {self.hp}/{self.max_hp}")

    def is_alive(self) -> bool:
        return self.hp > 0

    def attack_target(self, target):
        damage = max(0, self.attack_power - target.defense)
        target_name = "you"
        if hasattr(target, 'name') and target.name != "Player":
             target_name = target.name
        print(f"{self.name} attacks {target_name} for {damage} damage.")
        target.take_damage(damage, self)

class Enemy(NPC):
    def __init__(self, name: str, hp: int, attack_power: int, defense: int, description: str = "", loot: list | None = None):
        super().__init__(name, hp, attack_power, defense, description)
        self.loot = loot or []

class Ally(NPC):
    def __init__(self, name: str, hp: int, attack_power: int, defense: int, description: str = "", dialogue: str = "Nothing to say"):
        super().__init__(name, hp, attack_power, defense, description)
        self.dialogue = dialogue
