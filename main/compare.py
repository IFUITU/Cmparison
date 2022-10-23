import pandas as pd

from fuzzywuzzy import fuzz
# from .packages.transliterate import to_cyrillic, to_latin
from .packages.helpers import toLowerReplaceNComma, mul_of_list
from .packages.datas import dict_container
from .regexes import digit_regex
from cyrtranslit import to_cyrillic, to_latin

TYPES = (
    "супп", "таб","р-р", "инф.", "саше",
    "капс", 'гел', "лосьон",
    "сироп", "масло", "сусп", 
    "спрей", "шампун", "пастилки",
    "шип", "лиоф", "капли", "душ", "крем",
    "паст", "маз", "инсулин",
    "рект", "гранулы", "инфузия", "жидкий",
    "увл", "sprey", 'аэр', 

    "supp", "tab","r-r", "inf.", "sashe",
    "kaps", 'gel', "los'on", 'losyon',
    'lasyon', "sirop", "maslo", "susp", "por", 
    "shampun", "pastilki",
    "ship", "liof", "kapli", "dush", "krem",
    "past", "maz", "insulin",
    "rekt", "granuly", "infuziya", "jidkiy",
    "uvl", 'aer.'
    )


class File:
    def __init__(self, med_col, co_col, file):
        self.med_col = med_col #medicine column
        self.co_col = co_col #cmpany column
        self.file = file

    @property
    def dataFrame(self):
        return pd.read_excel(self.file, header=None, usecols="A:Z")



def writeHeader(first_df, second_df):
    """
        #to write header for our result file
        returns dict {0:'first_header', 1:'secon_header'} with 0 and 1 keys
    """
    
    first_title_row = first_df[0] #to name columns in our first new file
    second_title_row = second_df[0] 
    title_row = {0:first_title_row, 1:second_title_row}
    # print(title_row)
    return title_row


def getEqualsFromFile(first_df):
    pass


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

def translateCO(first_co, second_val):
    """
        translates companies' values
    """
    if first_co.isascii() and second_val.isascii():
        pass
    elif not first_co.isascii() and not second_val.isascii():
        first_co = to_latin(first_co)
        second_val = to_latin(second_val)
    elif not first_co.isascii():
        first_co = to_latin(first_co)
    elif not second_val.isascii():
        second_val = to_latin(second_val)
    tuple_ = (first_co, second_val)
    return tuple_


def make_comparison(data):
    df3 = pd.DataFrame()
    first_med_col = int(data.cleaned_data['first_med_col'])
    first_co_col = int(data.cleaned_data['first_co_col'])
    first_file = data.cleaned_data['first_file']

    second_med_col = int(data.cleaned_data['second_med_col'])
    second_co_col = int(data.cleaned_data['second_co_col'])
    second_file = data.cleaned_data['second_file']

    first_df = None
    second_df = None

    try:
        first_df = pd.read_excel(first_file, header=None) #header=None -> not take first arguments as header
        second_df = pd.read_excel(second_file, header=None)

        first_df = first_df.to_dict("records")
        second_df = second_df.to_dict('records')
        pd.set_option('display.max_rows', None)

    except Exception as ex:
        print(ex)
    
    NEW_FILE_VALUES = []
    NEW_FILE_VALUES.append(writeHeader(first_df, second_df))
    
    for first_row in first_df: # df.iterrows() -> returns tuple(index, (columns[0, 1, 2, e.t.c]))
        
        if not pd.isnull(first_row[first_med_col]):
            cnt_same = 0
            continue_first_loop = False

            first_med = toLowerReplaceNComma(first_row[first_med_col])
            first_co = str(first_row[first_co_col]).lower()

    #         #if True:
    #             # for new_index, new_row in enumerate(NEW_FILE_VALUES):
    #             #     new_file_med = toLowerAndReplaceNComma(new_row[0][first_med_col]) #new_row[0] == tuple([first_file_vals] & [first_med_col] == columns of the med)
    #             #     new_file_co = new_row[0][first_co_col]
                    
    #             #     if "пор" in new_file_med: #replace poroshok to p-p
    #             #         new_file_med = new_file_med.replace('пор', 'р-р')

    #             #     translatedMED = translateMED(first_med, new_file_med)
    #             #     translatedCO = translateCO(first_co, new_file_co)

    #             #     first_med = translatedMED[0]
    #             #     first_co = translatedMED[1]
    #             #     new_file_med = translatedCO[0]
    #             #     new_file_co = translatedCO[1]

    #             #     if first_med == new_file_med and first_co == new_file_co:
    #             #         NEW_FILE_VALUES[new_index+1][0].append(first_row[1])
    #             #         continue_first_loop = True
    #             #         break
                        
    #             #     if first_med[0:6] == new_file_med[0:6]:
    #             #         if fuzz.ratio(first_co[0:6], new_file_co[0:6]) >= 50 or fuzz.ratio(first_co, new_file_co) >= 48:
    #             #             first_med_digits = digit_regex(first_med) #all digits from first_med 
    #             #             new_file_med_digits = digit_regex(new_file_med) #all digits from new_file_med

    #             #             calc_first_med = mul_of_list(first_med_digits) #multiple of the digits from first_medicine column
    #             #             calc_new_file_med = mul_of_list(new_file_med_digits)

    #             #             firstToNew_result = calc_first_med / calc_new_file_med # devided for the reason 1g == 1000mg

    #             #             if set(first_med_digits) == set(new_file_med_digits) or firstToNew_result == 1000 or firstToNew_result == 0.001 or firstToNew_result == 100 or firstToNew_result == 0.01:
    #             #                 # x = [type for type in TYPES if type in first_med and type in new_file_med]
    #             #                 for type_ in TYPES:
    #             #                     if type_ in first_med and type_ in new_file_med:
    #             #                         NEW_FILE_VALUES[new_index+1][0].append(first_row[1])
    #             #                         continue_first_loop = True
    #             #                         break
    #             #                     if continue_first_loop:
    #             #                         break

    #             # for second_row in second_df.iterrows():
    #             #     continue_second_loop = False
    #             #     if not pd.isnull(second_row[1][second_med_col]):
    #             #         second_med = toLowerAndReplaceNComma(second_row[1][second_med_col])
    #             #         second_co = second_row[1][second_co_col]

    #             #         if "пор" in second_med:
    #             #             second_med =  second_med.replace('пор', 'р-р')

                        



        

            for second_row in second_df:
                if not pd.isnull(second_row[second_med_col]):
                    second_med = toLowerReplaceNComma(second_row[second_med_col])
                    second_co = str(second_row[second_co_col]).lower()
                    
                    translatedMED = translateMED(first_med, second_med)
                    translatedCO = translateCO(first_co, second_co)

                    first_med = translatedMED[0]
                    first_co = translatedCO[0]
                    second_med = translatedMED[1]
                    second_co = translatedCO[1]

                    print(first_med, second_med)
                    if first_med == second_med and first_co == second_co:
                        print(first_row[first_med_col], second_row[second_med_col])
                        NEW_FILE_VALUES.append({0:first_row, 1:second_row})
    print(NEW_FILE_VALUES)
            # print(first_df.loc[first_row[1]])






