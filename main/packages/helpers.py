def mul_of_list(values):
    total = 1
    for val in values:
        if val != 0:
            total *= float(val)
    return total