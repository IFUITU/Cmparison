def mul_of_list(values):
    """
        returns multiple of digits in list
    """
    total = 1
    for val in values:
        if float(val) != 0:
            total *= float(val)
    return total


def toLowerReplaceNComma(text):
    """
        replaces № to _
        comma to dot
        if пор in text to р-р
    """
    text = text.lower().replace("№", '_').replace(",", '.')
    if 'пор' in text:
        text = text.replace('пор', "р-р")
    return text


def create_excel(values):
    print(values)




