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


def change_colour(val):
    df = val.copy()
    is_mos = df['cnt_index_for_style'] == 1
    # is_none = df == 'None'
    df.loc[is_mos,:] = 'background-color: #8897bf;'
    df.loc[~is_mos,:] = 'color: green'
    # df.loc[is_none,:] = 'background-color: red;'
    return df

def create_excel(values):
    pass







