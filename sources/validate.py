

def float_range(min=0, max=100):
    def validate(value):
        try:
            float_value = float(value)
        except ValueError:
            raise ValueError("Invalid literal for float(): {0}".format(value))
        if min <= float_value <= max:
            return float_value
        raise ValueError(f"Value must be in range [{min}, {max}]")

    return validate
