def calculate_risk(similarity, clause_type):
    base_risk = (1 - similarity) * 10

    multiplier = {
        "liability": 2.5,
        "termination": 2.0,
        "payment": 1.8,
        "confidentiality": 2.2
    }.get(clause_type, 1.0)

    return round(base_risk * multiplier, 2)
