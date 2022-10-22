def mul_of_list(values):
    """
        returns multiple of digits in list
    """
    total = 1
    for val in values:
        if float(val) != 0:
            total *= float(val)
    return 


def toLowerReplaceNComma(text):
    """
        replaces № to _
        comma to dot
        if пор in text to р-р
    """
    if 'пор' in text:
        return text.replace('пор', "р-р")
    return text.lower().replace("№", '_').replace(",", '.')