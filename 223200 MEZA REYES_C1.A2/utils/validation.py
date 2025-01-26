def validate_inputs(params):
    validations = [
        params["delta"] > 0,
        params["min_val"] < params["max_val"],
        params["iteration"] > 0,
        params["pop_max"] > params["pop_min"],
        0 <= params["crossover_rate"] <= 1,
        0 <= params["mutation_rate"] <= 1,
        0 <= params["bit_mutation_rate"] <= 1,
    ]

    return all(validations)
