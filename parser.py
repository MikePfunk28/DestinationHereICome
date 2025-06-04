def parse_command(command_input: str) -> tuple[str, str | None]:
    stripped_input = command_input.strip().lower()
    if not stripped_input:
        return ('error', 'No command entered.')

    words = stripped_input.split()
    action = words[0]
    target = None

    if len(words) > 1:
        if action == "talk" and words[1] == "to":
            action = "talk"
            if len(words) > 2: target = " ".join(words[2:])
            else: return ('error', "Talk to whom?")
        elif action == "upgrade" and words[1] == "hideout":
            action = "upgrade hideout"
        elif action == "accept" and len(words) > 1 and words[-1] == "quest":
            target = " ".join(words[1:-1])
            if not target: return ('error', "Accept which quest?")
        elif action == "complete" and len(words) > 1 and words[-1] == "quest":
            target = " ".join(words[1:-1])
            if not target: return ('error', "Complete which quest?")
        else:
            target = " ".join(words[1:])
    return (action, target)
