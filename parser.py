def parse_command(command_input: str) -> tuple[str, str | None]:
    stripped_input = command_input.strip().lower()
    if not stripped_input:
        return ('error', 'No command entered.')

    words = stripped_input.split()
    action = words[0]
    target = None

    if action == "look" and len(words) > 1 and words[1] == "at":
        action = "look at"
        if len(words) > 2:
            target = " ".join(words[2:])
        else:
            return ('error', "Look at what?")
    elif len(words) > 1: # Original logic for other commands
        if action == "talk" and words[1] == "to":
            action = "talk"
            if len(words) > 2: target = " ".join(words[2:])
            else: return ('error', "Talk to whom?")
        elif action == "upgrade" and words[1] == "hideout":
            action = "upgrade hideout" # This is a specific command
        # Ensure quest commands are checked before generic target assignment
        elif action == "accept" and words[-1] == "quest": # Check words len > 1 has already been done by elif len(words) > 1
            target = " ".join(words[1:-1])
            if not target: return ('error', "Accept which quest?")
        elif action == "complete" and words[-1] == "quest": # Check words len > 1
            target = " ".join(words[1:-1])
            if not target: return ('error', "Complete which quest?")
        # If it's not 'look at' (already handled), and not any other special compound command, then the rest is the target.
        # We must ensure that 'look' by itself does not get a target here.
        elif action != "look":
             target = " ".join(words[1:])
        # If action is 'look' at this point, target correctly remains None.

    return (action, target)
