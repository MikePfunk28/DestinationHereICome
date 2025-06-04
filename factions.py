class Faction:
    def __init__(self, id_name: str, display_name: str, description: str, default_reputation: int = 0):
        self.id_name = id_name
        self.display_name = display_name
        self.description = description
        self.default_reputation = default_reputation

game_factions = {
    'city_watch': Faction(
        id_name='city_watch',
        display_name="City Watch",
        description="Veridia law enforcement",
        default_reputation=-5
    ),
    'red_hands': Faction(
        id_name='red_hands',
        display_name="The Red Hands",
        description="Shambles street gang",
        default_reputation=-10
    ),
    'merchant_guild': Faction(
        id_name='merchant_guild',
        display_name="Merchant Guild",
        description="Controls city trade",
        default_reputation=0
    )
}
