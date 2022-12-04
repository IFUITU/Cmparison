from main.packages.cyrlat.translitirate import to_latin, to_cyrillic

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


def translateMED(first_val, second_val):
    """
        to translate medicine's values
    """
    if first_val.isascii() and second_val.isascii() or not first_val.isascii() and not second_val.isascii(): #to check value is latin
        pass
    elif first_val.isascii():
        first_val = to_cyrillic(first_val)
    elif second_val.isascii():
        second_val = to_cyrillic(second_val)
    tuple_ = (first_val, second_val)
    return tuple_

def translateCO(first_co, second_co):
    """
        translates companies' values
    """
    if first_co.isascii() and second_co.isascii():
        pass
    elif not first_co.isascii() and not second_co.isascii():
        first_co = to_latin(first_co)
        second_co = to_latin(second_co)
    elif not first_co.isascii():
        first_co = to_latin(first_co)
    elif not second_co.isascii():
        second_co = to_latin(second_co)
    tuple_ = (first_co, second_co)
    return tuple_



def change_colour(val):
    df = val.copy()
    is_mos = df['cnt_index_for_style'] == 1
    # is_none = df == 'None'
    df.loc[is_mos,:] = 'background-color: #8897bf;'
    df.loc[~is_mos,:] = 'color: green'
    # df.loc[is_none,:] = 'background-color: red;'
    return df

def writeHeader(first_df, second_df):
    """
        #to write header
        returns dict {0:'first_header', 1:'secon_header'} with 0 and 1 keys
    """
    first_title_row = {k:'[1]' + str(v) for (k, v) in first_df[0].items()}
    second_title_row = {k:'[2]' + str(v) for (k, v) in second_df[0].items()}
    # first_title_row = first_df[0]
    # second_title_row = second_df[0]
    first_df.pop(0)
    second_df.pop(0)
    title_row = {0:first_title_row, 1:second_title_row}
    # print(title_row)
    return title_row


def create_excel(data):
    pass







