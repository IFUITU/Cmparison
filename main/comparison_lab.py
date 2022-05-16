from openpyxl import Workbook, load_workbook
# from openpyxl.worksheet.dimensions import DimensionHolder, ColumnDimension
from .regexes  import digit_regex, regex_of_measure
from fuzzywuzzy import fuzz
from .packages.transliterate import to_cyrillic, to_latin
from config.settings import BASE_DIR, MEDIA_ROOT, MEDIA_URL


TYPES = (
    "супп", "таб","р-р", "инф.", "саше",
    "капс", 'гел', "лосьон",
    "сироп", "масло", "сусп", "пор", 
    "спрей", "шампун", "пастилки",
    "шип", "лиоф", "капли", "душ", "крем",
    "паст", "мазь", "инсулин",
    "рект", "гранулы", "инфузия", "жидкий",
    "увл", "sprey", "комплект", 'аэр',

    )

EXTRA_TYPES = (
   "ультра",  "супер", "плюс", "мини", "д/детей", "детский", 
    "plus", "super", "baby", "беби"
)

MEASURES = ("гр", "мг", "г", "мл", "МЕ","мкг", "ЕД", "%", "XXL", "M", "S", "2XL", "XL")


def make_comparison(data):
    med_col_1 = int(data.cleaned_data['med_name_col_1'])
    com_col_1 = int(data.cleaned_data['com_name_col_1'])
    file_1 = data.cleaned_data['file_1']

    med_col_2 = int(data.cleaned_data['med_name_col_2'])
    com_col_2 = int(data.cleaned_data['com_name_col_2'])
    file_2 = data.cleaned_data['file_2']

    wb = Workbook()
    first_wb = load_workbook(file_1)  #loading a workbook
    second_wb = load_workbook(file_2)

    ws_1 = first_wb.active
    ws_2 = second_wb.active
    
    NEW_FILE_VAlUES = () #ALL VALUES  COLS FOR WRITING DATA

    title_row = ()   #for name and title of cols
    for row in ws_1.iter_rows(min_row=ws_1.min_row,max_row=ws_1.min_row):
        if row != None:
            title_row += (row,)
    for row in ws_2.iter_rows(min_row=ws_2.min_row,max_row=ws_2.min_row):
        if row != None:
            title_row += (row,)
    NEW_FILE_VAlUES += (title_row,)
    
    #COMPARISON LABARATORY!
    for i in ws_1.iter_rows():
            if i[med_col_1].value != None: #medicine cell value
                for j in ws_2.iter_rows():          #to iter second col
                        if med_col_2 < len(j):
                            if j[med_col_2].value != None:
                                
                                _value_1 = str(i[med_col_1].value).lower()
                                _value_2 = str(j[med_col_2].value).lower()
                                
                                if _value_1.isascii() and _value_2.isascii(): #to check value is latin
                                    continue
                                elif _value_1.isascii():
                                    _value_1 = to_cyrillic(_value_1)
                                elif _value_2.isascii():
                                    _value_2 = to_cyrillic(_value_2)
                                    
                                
                                if  _value_1[0:6] == _value_2[0:6]:
                                    for typ3 in TYPES:
                                        if typ3 in _value_1 and typ3 in _value_2:
                                            
                                            for measure in MEASURES:
                                                if measure in _value_1 and measure in _value_2:
                                                    if regex_of_measure(measure, _value_1) != None and regex_of_measure(measure, _value_2) != None:
                                                        if digit_regex(regex_of_measure(measure, _value_1).group(0)).group(0) == digit_regex(regex_of_measure(measure, _value_2).group(0)).group(0):
                                                            if _value_1 != None and _value_2 != None:
                                                                if fuzz.ratio(to_latin(_value_1), to_latin(_value_2)) >= 60:
                                                                    # for ex_type in EXTRA_TYPES:
                                                                    #     if ex_type i[med_col_1].value.lower()
                                                                    # print(i[med_col_1].value, "<=>", j[med_col_2].value)
                                                                    NEW_FILE_VAlUES += ((i,j),)
                                                                    break
                                                            
                                                            # print(i[med_col_1].value,"<->", j[med_col_2].value, "__1__")
                                                            NEW_FILE_VAlUES += ((i,j),)
                                                            break
                                            break
                                        elif typ3 in _value_1 or typ3 in _value_2:
                                            print("ASdasd")
                                            continue
                                        else:
                                            for measure in MEASURES:
                                                print(_value_1, _value_2, "mes")
                                                if measure in _value_1 and measure in _value_2:
                                                    if regex_of_measure(measure, _value_1) != None and regex_of_measure(measure, _value_2) != None:
                                                        if digit_regex(regex_of_measure(measure, _value_1).group(0)).group(0) == digit_regex(regex_of_measure(measure, _value_2).group(0)).group(0):
                                                            if i[com_col_1].value != None and j[com_col_2].value != None:
                                                                if fuzz.ratio(to_latin(i[com_col_1].value.lower()), to_latin(j[com_col_2].value.lower())) >= 65:
                                                                    # print(i[com_col_1].value, "<*=*>", j[com_col_2].value, i[med_col_1].value, "<->", j[med_col_2].value)
                                                                    NEW_FILE_VAlUES += ((i,j),)
                                                                    break
                                                            
                                                            # print(i[com_col_1].value, "<*=*>", j[com_col_2].value, i[med_col_1].value, "<->", j[med_col_2].value)
                                                            NEW_FILE_VAlUES += ((i,j),)        
                                                            break
                                                elif measure in _value_1 and measure not in _value_2 or measure not in _value_1 and measure in _value_2:
                                                    continue
                                                else:
                                                    if fuzz.ratio(_value_1, _value_2) >= 85:
                                                        if i[com_col_1].value != None and j[com_col_2].value != None:
                                                            if fuzz.ratio(to_latin(i[com_col_1].value.lower()), to_latin(j[com_col_2].value.lower())) >= 65:
                                                                        # print(i[com_col_1].value, "<*=*>", j[com_col_2].value, i[med_col_1].value, "<->", j[med_col_2].value)
                                                                        NEW_FILE_VAlUES += ((i,j),)
                                                                        break
                                            break

    wb.close()
    create_excel(NEW_FILE_VAlUES)

def create_excel(values):
    wb = Workbook()
    sheet = wb.active
    sheet.title = "RESULT 5 star"
    for index, data in enumerate(values):
        cnt_col = 1
        for zero_index in  range(len(data[0])):
            sheet.cell(row=index+1,  column=cnt_col).value=data[0][zero_index].value
            cnt_col += 1
        for first_index in range(len(data[1])):
            sheet.cell(row=index+1, column=cnt_col).value=data[1][first_index].value
            cnt_col += 1

    
    wb.save(MEDIA_ROOT / "sample.xlsx")
    wb.close()