def apply_hazard_penalties(crisis_type, edges):
    penalties = {}

    if crisis_type == "flood":
        for edge in edges:
            if (edge["from"], edge["to"]) == ("B", "C"):
                penalties[(edge["from"], edge["to"])] = 6
            else:
                penalties[(edge["from"], edge["to"])] = 0

    elif crisis_type == "wildfire":
        for edge in edges:
            if edge["to"] == "S2":
                penalties[(edge["from"], edge["to"])] = 8
            else:
                penalties[(edge["from"], edge["to"])] = 0

    elif crisis_type == "hurricane":
        for edge in edges:
            penalties[(edge["from"], edge["to"])] = 2

    else:
        for edge in edges:
            penalties[(edge["from"], edge["to"])] = 0

    return penalties
