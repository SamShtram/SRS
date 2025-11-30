def apply_capacity_penalty(shelters):
    penalties = {}

    for shelter in shelters:
        sid = shelter["id"]
        capacity = shelter["capacity"]

        penalty = 0
        if capacity > 80:
            penalty = 8
        elif capacity > 50:
            penalty = 4

        penalties[("B", sid)] = penalty
        penalties[("C", sid)] = penalty
        penalties[("A", sid)] = penalty

    return penalties
