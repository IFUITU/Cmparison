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
    "увл", "sprey", 'аэр'

    )

EXTRA_TYPES = (
   "ультра", 'ultra',  "супер", "плюс", "мини", "д/детей", "детский", 
    "plus", "super", "baby", "беби", "комплект"
)

MEASURES = ("гр", "мг", "г", "мл", "МЕ","мкг", "ед", "%", "xxl", "M", "S", "2xl", "xl")


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
                _value_1 = str(i[med_col_1].value).lower()
                _com_1 = str(i[com_col_1].value).lower()
                for j in ws_2.iter_rows():          #to iter second col
                    if j[med_col_2].value != None:
                        _value_2 = str(j[med_col_2].value).lower()
                        _com_2 = str(j[com_col_2].value).lower()
                        if med_col_2 < len(j):

                                if _value_1.isascii() and _value_2.isascii(): #to check value is latin
                                    pass
                                elif _value_1.isascii():
                                    _value_1 = to_cyrillic(_value_1)
                                elif _value_2.isascii():
                                    _value_2 = to_cyrillic(_value_2)
                                
                                if _com_1.isascii() and _com_2.isascii():
                                    pass
                                elif not _com_1.isascii():
                                    _com_1 = to_latin(_com_1)
                                elif not _com_2.isascii():
                                    _com_2 = to_latin(_com_2)
                                
                                if  _value_1[0:7] == _value_2[0:7]:
                                    if fuzz.ratio(_com_1, _com_2) >= 65:
                                        for typ3 in TYPES:
                                            if typ3 in _value_1 and typ3 in _value_2:
                                                for measure in MEASURES:
                                                    if measure in _value_1 and measure in _value_2:
                                                        
                                                        for extra_type in EXTRA_TYPES:
                                                            if extra_type in _value_1 and extra_type in _value_2:
                                                                if set(digit_regex(_value_1)) == set(digit_regex(_value_2)):          
                                                                        NEW_FILE_VAlUES += ((i,j),)
                                                                        break
                                                        if not any(extra_type in _value_1 for extra_type in EXTRA_TYPES) and not any(extra_type in _value_2 for extra_type in EXTRA_TYPES):
                                                            if set(digit_regex(_value_1)) == set(digit_regex(_value_2)):          
                                                                NEW_FILE_VAlUES += ((i,j),)
                                                                break
                                                        break
                                                if not any(m3asure in _value_1 for m3asure in MEASURES) and not any(m3asure in _value_2 for m3asure in MEASURES):
                                                    for extra_type in EXTRA_TYPES:
                                                        if extra_type in _value_1 and extra_type in _value_2:
                                                            if set(digit_regex(_value_1)) == set(digit_regex(_value_2)):          
                                                                    NEW_FILE_VAlUES += ((i,j),)
                                                                    break
                                                    if not any(extra_type in _value_1 for extra_type in EXTRA_TYPES) and not any(extra_type in _value_2 for extra_type in EXTRA_TYPES):
                                                        if set(digit_regex(_value_1)) == set(digit_regex(_value_2)):          
                                                            NEW_FILE_VAlUES += ((i,j),)
                                                            break
                                                    break

                                        if not any(t1p3 in _value_1 for t1p3 in TYPES) and not any(t1p3 in _value_2 for t1p3 in TYPES):
                                            if fuzz.ratio(_value_1, _value_2) >= 80:
                                                for extra_type in EXTRA_TYPES:
                                                    if extra_type in _value_1 and extra_type in _value_2:
                                                        if set(digit_regex(_value_1)) == set(digit_regex(_value_2)):          
                                                            NEW_FILE_VAlUES += ((i,j),)
                                                            break
                                                if not any(extra_type in _value_1 for extra_type in EXTRA_TYPES) and not any(extra_type in _value_2 for extra_type in EXTRA_TYPES):
                                                    if set(digit_regex(_value_1)) == set(digit_regex(_value_2)):          
                                                        NEW_FILE_VAlUES += ((i,j),)


    wb.close()
    create_excel(NEW_FILE_VAlUES)

def create_excel(values):
    wb = Workbook()
    sheet = wb.active
    sheet.title = "RESULT"
    for index, data in enumerate(values):
        cnt_col = 1
        for zero_index in  range(len(data[0])):

            if data[0][zero_index].value != None:
                sheet.cell(row=index+1,  column=cnt_col).value=data[0][zero_index].value
                cnt_col += 1
        for first_index in range(len(data[1])):
            if data[1][first_index].value != None:
                sheet.cell(row=index+1, column=cnt_col).value=data[1][first_index].value
                cnt_col += 1

    
    wb.save(MEDIA_ROOT / "sample.xlsx")
    wb.close()