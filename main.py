import random
import ascii_art # Added import
from player import Player
from world import locations, items_db
from parser import parse_command
from npc import NPC, Enemy, Ally
from factions import game_factions

scrawny_thug_defeated_flag = False

def find_npc_in_room(room_npcs_list: list, target_name: str) -> NPC | None:
    if not target_name: return None
    for npc in room_npcs_list:
        if npc.name.lower() == target_name.lower().strip() and npc.is_alive():
            return npc
    return None

def print_location_details(player: Player):
    print("\nYou scan your surroundings...")
    loc_key = player.current_location
    if loc_key not in locations:
        print(f"Error: Unknown location {loc_key}"); return
    loc_data = locations[loc_key]
    print(f"\n--- {loc_data['name']}{f' (L{player.hideout_level})' if loc_data.get('is_hideout') else ''} ---")

    # Display ASCII art for the location
    if loc_key == 'player_hideout' and hasattr(ascii_art, 'player_hideout_art'):
        print(ascii_art.player_hideout_art)
    elif loc_key == 'shambles_square' and hasattr(ascii_art, 'shambles_square_art'):
        print(ascii_art.shambles_square_art)
    elif loc_key == 'old_sewer_tunnel' and hasattr(ascii_art, 'old_sewer_tunnel_art'):
        print(ascii_art.old_sewer_tunnel_art)

    print(loc_data.get(f'description_level_{player.hideout_level}', loc_data['description']) if loc_data.get('is_hideout') else loc_data['description'])
    if loc_data.get('items'):
        print("Items: " + ", ".join([items_db.get(i, {}).get('name', i) for i in loc_data['items']]))
    alive_npcs = [n for n in loc_data.get('npcs', []) if n.is_alive()]
    if alive_npcs:
        print("People:")
        for npc in alive_npcs: # Iterate through alive_npcs to print details
            if npc.name == "Wary Informant":
                if player.chapter_one_completed:
                    print(f"- {npc.name} ({npc.description}) - Points you towards the Scribe's Quarter.")
                elif player.active_tasks.get('sewer_package_quest') == 'completed':
                    print(f"- {npc.name} ({npc.description}) - Seems content with your work regarding the package.")
                elif player.active_tasks.get('sewer_package_quest') == 'accepted':
                    print(f"- {npc.name} ({npc.description}) - Expects you to find the package.")
                else:
                    print(f"- {npc.name} ({npc.description})") # Initial state or other
            else:
                print(f"- {npc.name} ({npc.description if hasattr(npc, 'description') else 'No description'})") # Generic NPC display
    if loc_data.get('exits'):
        print("Exits: " + ", ".join(loc_data['exits'].keys()))

def print_status(player: Player):
    print(f"\nStatus: HP {player.hp}/{player.max_hp}, ${player.money}, Inf {player.influence}, Hideout L{player.hideout_level}")
    # Faction reps, quests, chapter status can be added if needed for brevity here

def check_first_chapter_conclusion(player: Player):
    global scrawny_thug_defeated_flag
    thug_dead = True
    for npc_obj in locations.get('shambles_alley_deeper', {}).get('npcs', []):
        if npc_obj.name == "Scrawny Thug" and npc_obj.is_alive(): thug_dead = False; break

    if not player.chapter_one_completed and player.active_tasks.get('sewer_package_quest') == 'completed' and player.hideout_level >= 1 and thug_dead:
        player.chapter_one_completed = True
        print("\nCHAPTER 1 COMPLETE: You delivered package, upgraded hideout, defeated thug. Informant points to Scribe's Quarter scholar for Aethelgard info.")

def main_game_loop():
    global scrawny_thug_defeated_flag
    player = Player(starting_location_key='shambles_square')
    print("Welcome to Destination Here I Come. Find Aethelgard. Commands: go, look, inv, take, talk, attack, status, accept, complete, upgrade, quit.")
    print_status(player)
    print_location_details(player)

    while player.is_alive():
        try:
            cmd_in = input("\n> ").strip()
            if not cmd_in: continue
            action, target = parse_command(cmd_in)

            if action == 'error': print(target); continue

            room_data = locations[player.current_location]
            room_npcs = room_data.get('npcs', [])

            if action == 'quit': print("Bye."); break
            elif action == 'look': print_location_details(player)
            elif action == 'look at':
                if target:
                    # room_data is already defined in the loop as locations[player.current_location]
                    location_features = room_data.get('features')
                    if location_features:
                        # Normalize target for key lookup (e.g., lowercase)
                        normalized_target = target.lower()
                        feature_description = None
                        # Allow for synonyms or slightly different phrasings by checking if any part of the target is a key
                        for key in location_features.keys():
                            if key in normalized_target: # e.g. "wall" in "the crumbling wall"
                                feature_description = location_features[key]
                                break

                        if feature_description:
                            print(feature_description)
                        else:
                            print(f"You look closely at the {target}, but see nothing else of particular interest.")
                    else:
                        print(f"There are no special features to examine more closely here with 'look at'.")
                else:
                    # This case should ideally be caught by the parser returning ("error", "Look at what?")
                    # but as a fallback:
                    print("Look at what? You need to specify something.")
            elif action == 'inventory' or action == 'inv': print(player.get_inventory_display(items_db))
            elif action == 'status': print_status(player)
            elif action == 'go':
                if target and target in room_data.get('exits', {}):
                    player.move(room_data['exits'][target.lower()])
                    print_location_details(player)
                else:
                    if target: # Target was given but is not a valid exit
                        print(f"Alas, you cannot go '{target}' from here. That path is not open to you.")
                    else: # Should be caught by parser, but as a fallback
                        print("Go where? You need to specify a direction.")
            elif action == 'take':
                item_k = target.lower().replace(' ', '_') if target else None
                if item_k and item_k in room_data.get('items', []):
                    room_data['items'].remove(item_k)
                    player.add_to_inventory(item_k, items_db)
                else:
                    if target: # Target was given but item not found
                        print(f"You search around for a '{target}', but find nothing of the sort.")
                    else: # Should be caught by parser, but as a fallback
                        print("Take what, exactly? Best to be specific.")
            elif action == 'talk':
                npc_t = find_npc_in_room(room_npcs, target) if target else None
                if npc_t and isinstance(npc_t, Ally):
                    if npc_t.name == "Wary Informant":
                        if player.chapter_one_completed:
                            print(f"{npc_t.name}: \"The Scribe's Quarter is where you should look for that scholar I mentioned. Good luck.\"")
                        elif player.active_tasks.get('sewer_package_quest') == 'completed':
                            print(f"{npc_t.name}: \"Good work on that package. You're proving to be more than just another wanderer.\"")
                            check_first_chapter_conclusion(player) # Check if this dialogue fulfills other conditions
                        elif player.active_tasks.get('sewer_package_quest') == 'accepted':
                            print(f"{npc_t.name}: \"The package from the Old Sewer Tunnel. Have you got it yet?\"")
                        else:
                            print(f"{npc_t.name}: \"{npc_t.dialogue}\"") # Initial quest offer
                    else:
                        # For other Ally NPCs
                        print(f"{npc_t.name}: \"{npc_t.dialogue}\"")
                else: print(f"No '{target}' to talk to." if target else "Talk to whom?")
            elif action == 'attack':
                npc_a = find_npc_in_room(room_npcs, target) if target else None
                if npc_a and isinstance(npc_a, Enemy):
                    print(f"\n--- Combat Initiated: You vs {npc_a.name} ---")

                    # Display ASCII art for the enemy
                    if npc_a.name == "Diseased Rat" and hasattr(ascii_art, 'diseased_rat_art'):
                        print(ascii_art.diseased_rat_art)
                    elif npc_a.name == "Scrawny Thug" and hasattr(ascii_art, 'scrawny_thug_art'):
                        print(ascii_art.scrawny_thug_art)

                    combat_over = False
                    while player.is_alive() and npc_a.is_alive() and not combat_over:
                        combat_choice = input("Combat: [A]ttack or [R]un? ").strip().lower()
                        if combat_choice == 'a':
                            player.attack_target(npc_a)
                            if npc_a.is_alive():
                                npc_a.attack_target(player)
                        elif combat_choice == 'r':
                            if random.random() < 0.5: # 50% chance to escape
                                print("You successfully fled from combat!")
                                combat_over = True # Exit combat loop
                            else:
                                print("You failed to escape!")
                                npc_a.attack_target(player) # NPC gets an attack
                        else:
                            print("Invalid choice. Defaulting to attack.")
                            player.attack_target(npc_a)
                            if npc_a.is_alive():
                                npc_a.attack_target(player)

                        if not player.is_alive():
                            print(f"{npc_a.name} defeated you.")
                            combat_over = True
                        elif not npc_a.is_alive():
                            print(f"You defeated {npc_a.name}!")
                            if npc_a.name == "Scrawny Thug":
                                scrawny_thug_defeated_flag = True
                            if npc_a.loot:
                                print("Loot found:")
                                for item_l in npc_a.loot:
                                    if "_coins" in item_l:
                                        try:
                                            amt = int(item_l.split('_')[0])
                                            player.money += amt
                                            print(f"- Got {amt} coins.")
                                        except ValueError: # Should not happen with current items_db
                                            player.add_to_inventory(item_l, items_db)
                                    else:
                                        player.add_to_inventory(item_l, items_db)
                            if npc_a in room_npcs: # Ensure it's still there before removing
                                room_npcs.remove(npc_a)
                            check_first_chapter_conclusion(player)
                            combat_over = True

                    print("--- Combat Ended ---")
                    # Player death check after combat loop in case of failed run leading to death
                    if not player.is_alive() and not combat_over: # combat_over might be true if player fled then died somehow (not possible here)
                         print("You died.") # General death message if not handled above

                elif npc_a: print(f"Cannot attack {target}.") # Target is not an enemy
                else: print(f"No '{target}' to attack." if target else "Attack whom?")
            elif action == 'upgrade hideout':
                if player.current_location == 'player_hideout' and player.hideout_level == 0:
                    if player.money >= 100 and player.influence >= 5:
                        player.money -= 100; player.influence -= 5; player.hideout_level = 1
                        print("Hideout L1!"); check_first_chapter_conclusion(player)
                    else: print("Need $100, Inf 5.")
                else: print("Not in hideout or already upgraded.")
            elif action == 'accept' and target == 'package':
                if player.current_location == 'shambles_square' and 'sewer_package_quest' not in player.active_tasks:
                    player.active_tasks['sewer_package_quest'] = 'accepted'; player.money += 10
                    print("Package quest accepted. +$10.")
                else: print("Cannot accept now.")
            elif action == 'complete' and target == 'package':
                if player.active_tasks.get('sewer_package_quest') == 'accepted' and 'sealed_package' in player.inventory and player.current_location == 'shambles_square':
                    player.remove_from_inventory('sealed_package', items_db)
                    player.money += 50; player.influence += 5; player.faction_reputations['red_hands'] += 2
                    player.active_tasks['sewer_package_quest'] = 'completed'
                    print("Package quest complete!"); check_first_chapter_conclusion(player)
                else: print("Cannot complete now.")
            else: print("Unknown command.")
        except (EOFError, KeyboardInterrupt): print("\nBye."); break
    if not player.is_alive(): print("GAME OVER.")

if __name__ == "__main__":
    main_game_loop()
