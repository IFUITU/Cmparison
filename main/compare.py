import pandas as pd

from fuzzywuzzy import fuzz
from .packages.transliterate import to_cyrillic, to_latin
from .packages.helpers import toLowerAndReplaceNComma



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
        returns tuple (([]), ([])) with 0 and 1 indexes
    """
    first_title_row = ([first_df[col][0] for col in first_df.columns],) #to name columns in our first new file
    second_title_row = ([second_df[col][0] for col in second_df.columns],) #list inside tuple because we can append elements
    title_row = (first_title_row,) + (second_title_row,)

    return title_row


def getEqualsFromFile(first_df):
    pass


def make_comparison(data):
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
        pd.set_option('display.max_rows', None)
    except Exception as ex:
        print(ex)

    NEW_FILE_VALUES = ()
    NEW_FILE_VALUES += writeHeader(first_df, second_df)
    
    for first_row in first_df.iterrows(): #iter rows returns tuple(index, (columns[0, 1, 2, e.t.c]))
        print(first_row[1][first_med_col])

        if not pd.isnull(first_row[1][first_med_col]):
            cnt_same = 0
            continue_loop = False

            first_med = toLowerAndReplaceNComma(first_row[1][first_med_col])
            first_co = str(first_row[1][first_co_col]).lower()

            if "пор" in first_med:
                first_med = first_med.replace('пор', 'р-р')
        
            
        
            
            



