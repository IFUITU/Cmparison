import pandas as pd
from django.shortcuts import redirect
from config.settings import MEDIA_ROOT
from fuzzywuzzy import fuzz

from .packages.helpers import *
from .packages.datas import dict_container
from .regexes import digit_regex


TYPES = (
    "супп", "таб","р-р", "инф.", "саше",
    "капс", 'гел', "лосьон",
    "сироп", "масло", "сусп", 
    "спрей", "шампун", "пастилки",
    "шип", "лиоф", "капли", "душ", "крем",
    "паст", "маз", "инсулин",
    "рект", "гранулы", "инфузия", "жидкий",
    "увл", "sprey", 'аэр', "космет"

    "supp", "tab","r-r", "inf.", "sashe",
    "kaps", 'gel', "los'on", 'losyon',
    'lasyon', "sirop", "maslo", "susp", "por", 
    "shampun", "pastilki",
    "ship", "liof", "kapli", "dush", "krem",
    "past", "maz", "insulin",
    "rekt", "granuly", "infuziya", "jidkiy",
    "uvl", 'aer.', 'kosmet'
    )


def make_comparison(data, request): 
    
    first_med_col = int(data.cleaned_data['first_med_col'])
    first_co_col = int(data.cleaned_data['first_co_col'])
    first_file = data.cleaned_data['first_file']

    second_med_col = int(data.cleaned_data['second_med_col'])
    second_co_col = int(data.cleaned_data['second_co_col'])
    second_file = data.cleaned_data['second_file']

    first_df = None
    second_df = None
    df = None

    try:
        first_df = pd.read_excel(first_file, header=None) #header=None -> not take first arguments as header
        second_df = pd.read_excel(second_file, header=None)
        first_df = first_df.dropna(how="all")
        second_df = second_df.dropna(how="all")
        first_df.sort_values(by=[first_med_col])
        second_df.sort_values(by=[second_med_col])
        df = pd.DataFrame()
        
        first_df = first_df.to_dict("records")
        second_df = second_df.to_dict('records')

        pd.set_option('display.max_rows', None)

    except Exception as ex:
        print(ex)
    
    rewrited_header = writeHeader(first_df, second_df)
    left_side = rewrited_header[0] # write first file title
    right_side = rewrited_header[1] #write second file title

    cnt_l_side = 0 #l = left
    cnt_r_side = 0 #r = right
    
    for findex, first_row in enumerate(first_df): # returns > {0:'name', 1:"name 2"}
        
        # if not pd.isnull(first_row[first_med_col]):
        cnt_fst_same = 0
        cnt_sec_same = 0

        first_med = toLowerReplaceNComma(first_row[first_med_col])
        first_co = str(first_row[first_co_col]).lower()
        print(findex)
    
        if cnt_r_side > cnt_l_side:
            cnt_l_side = cnt_r_side
        else:
            cnt_r_side = cnt_l_side
        
        df.loc[cnt_l_side, left_side.values()] = first_row.values() #this line added to add first comparer into left_side
        df.loc[cnt_l_side, '<<>>'] = ""
        cnt_l_side += 1
        
        for new_index, new_row in enumerate(first_df[:]):
            
            if findex != new_index:
                continue_first_loop = False
                    
                if not pd.isnull(new_row[first_med_col]):
                    
                    new_file_med = toLowerReplaceNComma(new_row[first_med_col]) #new_row -> {0:({}, {}, {}),  1:({}, {}, {})}
                    new_file_co = new_row[first_co_col].lower() #left_side[first_co_col] -> first_company_name
                    if first_med == new_file_med and first_co == new_file_co:
                        df.loc[cnt_l_side, left_side.values()] = new_row.values() #left_side values is columns names!
                        # first_df[new_index][first_med_col] = None  #insted of pop or remove we can use None attribute 
                        first_df.remove(new_row)
                        #adding to coloring rows                            
                        if findex % 2 == 0:
                            df.loc[cnt_l_side, 'cnt_index_for_style'] = 1
                        else:
                            df.loc[cnt_l_side, 'cnt_index_for_style'] = 0
                        continue_first_loop = True
                        cnt_l_side += 1
                        cnt_fst_same += 1
                        continue

                    translatedMED = translateMED(first_med, new_file_med)
                    translatedCO = translateCO(first_co, new_file_co)

                    first_med = translatedMED[0]
                    first_co = translatedCO[0]
                    new_file_med = translatedMED[1]
                    new_file_co = translatedCO[1]

                    if first_med[0:6] == new_file_med[0:6]:

                        if fuzz.token_sort_ratio(first_co[0:6], new_file_co[0:6]) >= 50 or fuzz.token_sort_ratio(first_co, new_file_co) >= 48:
                            first_med_digits = digit_regex(first_med) #all digits from first_med 
                            new_file_med_digits = digit_regex(new_file_med) #all digits from new_file_med

                            calc_first_med = mul_of_list(first_med_digits) #multiple of the digits from first_medicine column
                            calc_new_file_med = mul_of_list(new_file_med_digits)

                            firstToNew_result = calc_first_med / calc_new_file_med # devided for the reason 1g == 1000mg
                            
                            if set(first_med_digits) == set(new_file_med_digits) or firstToNew_result == 1000 or firstToNew_result == 0.001 or firstToNew_result == 100 or firstToNew_result == 0.01:
                                # x = [type for type in TYPES if type in first_med and type in new_file_med]
                                for type_ in TYPES:
                                    if type_ in first_med and type_ in new_file_med:

                                        df.loc[cnt_l_side, left_side.values()] = new_row.values()
                                        # first_df[new_index][first_med_col] = None
                                        first_df.remove(new_row)
                                        #adding to coloring rows                            
                                        if findex % 2 == 0:
                                            df.loc[cnt_l_side, 'cnt_index_for_style'] = 1
                                        else:
                                            df.loc[cnt_l_side, 'cnt_index_for_style'] = 0
                                        continue_first_loop = True
                                        cnt_l_side += 1
                                        cnt_fst_same += 1
                                        break

                                if continue_first_loop: #to ignore code under this selection!
                                    continue

                                type_in_first_med = any(t1p3 in first_med for t1p3 in TYPES)
                                type_in_new_med = any(t1p3 in new_file_med for t1p3 in TYPES)
                                if (not type_in_first_med and not type_in_new_med) or (not type_in_first_med and type_in_new_med) or (type_in_first_med and not type_in_new_med):
                                    
                                    df.loc[cnt_l_side, left_side.values()] = new_row.values()
                                    # first_df[new_index][first_med_col] = None
                                    first_df.remove(new_row)
                                    #adding to coloring rows                            
                                    if findex % 2 == 0:
                                        df.loc[cnt_l_side, 'cnt_index_for_style'] = 1
                                    else:
                                        df.loc[cnt_l_side, 'cnt_index_for_style'] = 0
                                    continue_first_loop = True
                                    cnt_l_side += 1
                                    cnt_fst_same += 1

        for second_row in second_df:
            continue_second_loop = False

            if not pd.isnull(second_row[second_med_col]):
                second_med = toLowerReplaceNComma(second_row[second_med_col])
                second_co = str(second_row[second_co_col]).lower()

                if first_med == second_med and first_co == second_co:
                    df.loc[cnt_r_side, right_side.values()] = second_row.values()

                    #adding to coloring rows
                    if findex % 2 == 0:
                        df.loc[cnt_r_side, 'cnt_index_for_style'] = 1
                    else:
                        df.loc[cnt_r_side, 'cnt_index_for_style'] = 0

                    cnt_sec_same += 1
                    cnt_r_side += 1
                    continue
                
                translatedMED = translateMED(first_med, second_med)
                translatedCO = translateCO(first_co, second_co)
                
                first_med = translatedMED[0]
                first_co = translatedCO[0]
                second_med = translatedMED[1]
                second_co = translatedCO[1]
                
                
                if first_med[0:6] == second_med[0:6]:
                    
                    if fuzz.token_sort_ratio(first_co[0:6], second_co[0:6]) >= 50 or fuzz.token_sort_ratio(first_co, second_co) >= 48:
                        
                        calc_fmed = mul_of_list(digit_regex(first_med))
                        calc_smed = mul_of_list(digit_regex(second_med))
                        result = calc_fmed / calc_smed
                        if set(digit_regex(first_med)) == set(digit_regex(second_med)) or result == 1000 or result == 0.001 or result == 100 or result == 0.01:
                            # x = [[first_row, second_row] for type_ in TYPES if type_ in first_med and type_ in second_med]
                            for type_ in TYPES:
                                if type_ in first_med and type_ in second_med:
                                    df.loc[cnt_r_side, right_side.values()] = second_row.values()
                                    #adding to coloring rows
                                    if findex % 2 == 0:
                                        df.loc[cnt_r_side, 'cnt_index_for_style'] = 1
                                    else:
                                        df.loc[cnt_r_side, 'cnt_index_for_style'] = 0
                                      
                                    cnt_sec_same += 1 
                                    cnt_r_side += 1
                                    continue_second_loop = True
                                    break

                            if continue_second_loop:
                                continue

                            type_in_fmed = any(t1p3 in first_med for t1p3 in TYPES)
                            type_in_smed = any(t1p3 in second_med for t1p3 in TYPES)
                            if (not type_in_fmed and not type_in_smed) or (not type_in_fmed and type_in_smed) or (type_in_fmed and not type_in_smed):    

                                df.loc[cnt_r_side, right_side.values()] = second_row.values()
                                #adding to coloring rows

                                if findex % 2 == 0:
                                    df.loc[cnt_r_side, 'cnt_index_for_style'] = 1
                                else:
                                    df.loc[cnt_r_side, 'cnt_index_for_style'] = 0
                                cnt_sec_same += 1
                                cnt_r_side += 1


        if cnt_sec_same == 0 and findex != 0:

            df.loc[cnt_r_side, right_side.values()] = 'Yoq'

            #adding to coloring rows                            
            if findex % 2 == 0:
                df.loc[cnt_r_side, 'cnt_index_for_style'] = 1
            else:
                df.loc[cnt_r_side, 'cnt_index_for_style'] = 0
            cnt_l_side += 1
            cnt_r_side = cnt_l_side
    
    df = df.style.apply(change_colour, axis=None)
    df.to_excel(MEDIA_ROOT / 'sample_{}.xlsx'.format(request.user))

    # return redirect(to="main:done")




