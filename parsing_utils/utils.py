
def float_converter(value):
    if isinstance(value, str):
        value = value.replace(",", ".")
    value = float(value)
    return value


