def mul_of_list(values):
    total = 1
    for val in values:
        if float(val) != 0:
            total *= float(val)
    return total