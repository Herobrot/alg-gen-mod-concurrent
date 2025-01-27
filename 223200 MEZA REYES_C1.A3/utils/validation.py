def validate_inputs(params):
    validations = {
        "population_size": params["population_size"] > 0,
        "min_max_interval": params["min_interval_mutation_rate"] < params["max_interval_mutation_rate"],
        "crossover_rate": 0 <= params["crossover_rate"] <= 1,
        "mutation_rate": 0 <= params["mutation_rate"] <= 1,
    }
    
    invalid_fields = [field for field, is_valid in validations.items() if not is_valid]
    return len(invalid_fields) == 0, invalid_fields

def format_validation_error(invalid_fields):
    error_messages = {
        "min_interval_mutation_rate": "El intervalo mínimo de mutación debe ser menor que el máximo.",
        "crossover_rate": "La tasa de cruce debe estar entre 0 y 1.",
        "mutation_rate": "La tasa de mutación debe estar entre 0 y 1."
    }
    
    return "\n".join([error_messages[field] for field in invalid_fields])