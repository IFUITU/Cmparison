def mul_of_list(values):
    """
        returns multiple of digits in list
    """
    total = 1
    for val in values:
        if float(val) != 0:
            total *= float(val)
    return 


def toLowerAndReplaceNComma(value):
    """
        replaces № to _
        comma to dot
    """
    return value.lower().replace("№", '_').replace(",", '.')
